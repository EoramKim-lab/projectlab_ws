"""Local NED dead reckoning from PX4 attitude, IMU, flow and range."""
import math
import numpy as np
from geometry_msgs.msg import QuaternionStamped
from sensor_msgs.msg import Imu, Range
from std_msgs.msg import Empty
from drone_interfaces.msg import FlowMeasurement, NavigationState
from ..common import Base, run, seconds
from ..math_utils import rotation, vector, qvalues, assign, assign_q
from .estimator import Estimator


class DeadReckoningNode(Base):
    def __init__(self):
        Base.__init__(self, 'dead_reckoning_node')
        self.frame = self.param('map_frame', 'map_ned')
        self.body = self.param('body_frame', 'base_link_frd')
        self.timeout = self.param('sensor_timeout', 0.25)
        self.max_skew = self.param('max_attitude_skew', 0.08)
        self.strict_sensor_checks = self.param('strict_sensor_checks', False)
        self.offset = np.asarray(self.param('range_offset_frd', [0., 0., 0.]))
        self.height_gain = self.param('height_velocity_gain', 0.5)
        rate = self.param('publish_rate', 20.0)
        if (not all(math.isfinite(x) and x > 0 for x in (self.timeout, self.max_skew, rate))
                or self.offset.shape != (3,) or not np.isfinite(self.offset).all()
                or not 0 <= self.height_gain <= 1):
            raise ValueError('invalid dead reckoning parameters')
        self.ground_z = 0.
        self.core = Estimator(flow_velocity_gain=self.param('flow_velocity_gain', 0.8),
                              max_prediction_dt=.1 if self.strict_sensor_checks else None)
        self.stamps = {}
        self.last_range = None
        self.previous_height = None
        self.flow_good = False
        self.pub = self.create_publisher(NavigationState, 'navigation/state', 10)
        self.start_monitor('navigation')
        self.create_subscription(Empty, 'sensors/px4_reset', self.receive_px4_reset, 10)
        for typ, topic, cb in (
                (QuaternionStamped, 'sensors/attitude', self.attitude),
                (Imu, 'sensors/imu', self.imu),
                (Range, 'sensors/range', self.distance),
                (FlowMeasurement, 'sensors/flow', self.flow)):
            self.create_subscription(typ, topic, cb, 10)
        self.create_timer(1. / rate, self.publish)
        self.get_logger().info('Dead reckoning: horizontal origin at startup; z is negative range-aided height above ground; PX4 NED axes')
        if not self.strict_sensor_checks:
            self.get_logger().warning('Relaxed sensor checks: ignoring input frame labels, sample age and attitude skew; integrating the full positive IMU dt. Actual axes must still be NED/FRD.')

    def accept(self, key, msg, frame):
        if self.strict_sensor_checks:
            if msg.header.frame_id != frame or not self.fresh(msg.header.stamp, self.timeout):
                return False
        t = seconds(msg.header.stamp)
        if not math.isfinite(t) or t <= 0 or not self.increasing(key, t):
            return False
        self.stamps[key] = msg.header.stamp
        return True

    def aligned(self, msg):
        stamp = self.stamps.get('attitude')
        return not self.strict_sensor_checks or (
            stamp is not None and abs(seconds(stamp)-seconds(msg.header.stamp)) <= self.max_skew)

    def range_matches_flow(self, msg):
        if self.strict_sensor_checks:
            return (self.last_range is not None
                    and self.fresh(self.last_range.header.stamp, self.timeout)
                    and abs(seconds(msg.header.stamp)-seconds(self.last_range.header.stamp)) <= self.max_skew)
        return self.last_range is not None

    def on_px4_reset(self):
        self.core = Estimator(flow_velocity_gain=self.core.kf,
                              max_prediction_dt=self.core.max_prediction_dt)
        self.stamps.clear()
        self._source_stamps = {}
        self.last_range = self.previous_height = None
        self.flow_good = False
        self.get_logger().warning('PX4 reset: dead reckoning origin cleared; waiting for fresh sensors')

    def distance(self, msg):
        if (not math.isfinite(msg.range) or not msg.min_range <= msg.range <= msg.max_range
                or not self.aligned(msg) or rotation(self.core.q)[2, 2] < .96
                or not self.accept('range', msg, self.body)):
            return
        self.last_range = msg
        self.core.range_height(msg.range, self.ground_z, self.offset)
        t, z = seconds(msg.header.stamp), float(self.core.p[2])
        if self.previous_height is not None:
            old_t, old_z = self.previous_height
            dt = t - old_t
            if dt >= .001 and (not self.strict_sensor_checks or dt <= self.timeout):
                k = self.height_gain
                self.core.v[2] = (1-k)*self.core.v[2] + k*(z-old_z)/dt
        self.previous_height = (t, z)
        self.core.initialize_height()


    def report(self, out):
        p, v, q = out.pose.position, out.twist.linear, out.pose.orientation
        yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))
        self.observe('navigation', f'valid={out.valid} reason={out.reason} '
                     f'p_NED=({p.x:.3f},{p.y:.3f},{p.z:.3f})m '
                     f'v_NED=({v.x:.3f},{v.y:.3f},{v.z:.3f})m/s yaw={yaw:.3f}rad '
                     f'ages[imu,att,range,flow]=[{out.imu_age:.2f},'
                     f'{out.attitude_age:.2f},{out.range_age:.2f},{out.flow_age:.2f}]s')

    def attitude(self,msg):
        q = qvalues(msg.quaternion)
        try:
            rotation(q)
        except ValueError:
            return
        if self.accept('attitude',msg,self.frame):
            self.core.q = np.array(q)/np.linalg.norm(q)

    def imu(self,msg):
        a,w = vector(msg.linear_acceleration),vector(msg.angular_velocity)
        if np.isfinite(a).all() and np.isfinite(w).all() and self.aligned(msg) and self.accept('imu',msg,self.body):
            self.core.predict(seconds(msg.header.stamp),a,w)

    def flow(self,msg):
        # Duplicate/out-of-order/wrong-frame packets must not invalidate the
        # last accepted observation. A new bad observation still invalidates it.
        if not self.accept('flow',msg,self.body):
            return
        self.flow_good = False
        if not msg.valid or not self.aligned(msg):
            return
        distance = msg.distance_m
        if not math.isfinite(distance) or distance <= 0:
            if not self.range_matches_flow(msg):
                return
            distance = self.last_range.range
        try:
            self.flow_good = self.core.flow(msg.pixel_flow,msg.delta_angle,msg.integration_dt,distance)
        except ValueError:
            pass

    def publish(self):
        out = NavigationState()
        out.header.stamp = self.get_clock().now().to_msg()
        out.header.frame_id,out.child_frame_id = self.frame,self.body
        missing = []
        for key in ['imu','attitude','range','flow']:
            stamp = self.stamps.get(key)
            age = self.age(stamp) if stamp is not None else 1e9
            setattr(out,key+'_age',float(age))
            if not (-.05 <= age <= self.timeout):
                missing.append(key)
        if not self.flow_good:
            missing.append('flow_invalid')
        if not self.core.initialized:
            missing.append('uninitialized')
        if self.core.prediction_gap:
            missing.append('imu_prediction_gap')
        if rotation(self.core.q)[2,2] < math.cos(math.radians(15.)):
            missing.append('tilt_exceeds_planar_model')
        if not np.isfinite(np.r_[self.core.p,self.core.v,self.core.a]).all():
            missing.append('nonfinite_state')
        out.valid = not missing
        out.reason = 'ok' if out.valid else ','.join(missing)
        assign(out.pose.position,self.core.p)
        assign_q(out.pose.orientation,self.core.q)
        assign(out.twist.linear,self.core.v)
        assign(out.twist.angular,self.core.w)
        assign(out.acceleration,self.core.a)
        self.report(out)
        self.pub.publish(out)


def main(args=None):
    run(DeadReckoningNode, args)
