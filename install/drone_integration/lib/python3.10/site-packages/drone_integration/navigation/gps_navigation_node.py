"""Publish NavigationState from PX4 EKF2 local position, attitude, IMU and GNSS."""
import math
import numpy as np
from geometry_msgs.msg import QuaternionStamped
from sensor_msgs.msg import Imu
from std_msgs.msg import Empty
from px4_msgs.msg import EstimatorStatusFlags, SensorGps, VehicleLocalPosition
from drone_interfaces.msg import NavigationState
from ..common import Base, SENSOR_QOS, run, seconds
from ..math_utils import qvalues, vector, rotation, assign, assign_q
from .gps_state import gps_quality_reasons, local_position_reasons, gnss_aided


class GpsNavigationNode(Base):
    def __init__(self):
        super().__init__('gps_navigation_node')
        self.frame = self.param('map_frame', 'map_ned')
        self.body = self.param('body_frame', 'base_link_frd')
        self.timeout = float(self.param('sensor_timeout', 0.25))
        self.estimator_flags_timeout = float(self.param('estimator_flags_timeout', 2.0))
        self.max_attitude_skew = float(self.param('max_attitude_skew', 0.08))
        self.max_imu_skew = float(self.param('max_imu_skew', 0.15))
        self.min_satellites = int(self.param('min_satellites', 6))
        self.max_gps_eph = float(self.param('max_gps_eph', 5.0))
        self.max_gps_epv = float(self.param('max_gps_epv', 8.0))
        self.require_gnss = bool(self.param('require_gnss_aiding', True))
        rate = float(self.param('publish_rate', 20.0))
        if (not all(math.isfinite(v) and v > 0 for v in
                    (self.timeout, self.estimator_flags_timeout, self.max_attitude_skew, self.max_imu_skew,
                     self.max_gps_eph, self.max_gps_epv, rate))
                or self.min_satellites < 1):
            raise ValueError('invalid GPS navigation parameters')

        self.watch_px4_clock()
        self.start_monitor('gps', 'local_position', 'attitude', 'imu', 'navigation')
        self.local = self.gps = self.estimator_flags = self.attitude = self.imu = None
        self.local_stamp = self.gps_stamp = self.estimator_flags_stamp = None
        self.attitude_stamp = self.imu_stamp = None
        self.reset_signature = None
        self.last_ekf_gnss_state = None
        self.reset_pub = self.create_publisher(Empty, 'navigation/reset', 10)
        self.pub = self.create_publisher(NavigationState, 'navigation/state', 10)

        self.create_subscription(VehicleLocalPosition,
                                 '/fmu/out/vehicle_local_position',
                                 self.local_position, SENSOR_QOS)
        self.create_subscription(SensorGps,
                                 '/fmu/out/vehicle_gps_position',
                                 self.gps_position, SENSOR_QOS)
        self.create_subscription(EstimatorStatusFlags,
                                 '/fmu/out/estimator_status_flags',
                                 self.estimator_status, SENSOR_QOS)
        self.create_subscription(QuaternionStamped,
                                 'sensors/attitude', self.on_attitude, 10)
        self.create_subscription(Imu, 'sensors/imu', self.on_imu, 10)
        self.create_timer(1.0 / rate, self.publish)
        self.get_logger().info(
            'GPS navigation: PX4 EKF2 VehicleLocalPosition (NED) + raw GNSS health gate; '
            'position is not integrated in this ROS node')

    def on_px4_reset(self):
        self.local = self.gps = self.estimator_flags = self.attitude = self.imu = None
        self.local_stamp = self.gps_stamp = self.estimator_flags_stamp = None
        self.attitude_stamp = self.imu_stamp = None
        self.reset_signature = None
        self.last_ekf_gnss_state = None
        self.get_logger().warning('PX4 clock reset: clearing GPS navigation inputs')

    def local_position(self, msg):
        if not self.px4_increasing('local_position', int(msg.timestamp)):
            return
        stamp = self.px4_sample_stamp(int(msg.timestamp))
        if stamp is None:
            return

        signature = (int(msg.xy_reset_counter), int(msg.z_reset_counter),
                     int(msg.vxy_reset_counter), int(msg.vz_reset_counter),
                     int(msg.heading_reset_counter))
        if self.reset_signature is None:
            self.reset_signature = signature
        elif signature != self.reset_signature:
            previous = self.reset_signature
            self.reset_signature = signature
            self.reset_pub.publish(Empty())
            self.get_logger().warning(
                f'PX4 EKF reset counters changed {previous} -> {signature}; '
                'MPC reference/history and Offboard stream are reset')

        self.local, self.local_stamp = msg, stamp
        self.observe('local_position',
                     f'NED=({msg.x:.2f},{msg.y:.2f},{msg.z:.2f})m '
                     f'v=({msg.vx:.2f},{msg.vy:.2f},{msg.vz:.2f})m/s '
                     f'xy_valid={msg.xy_valid} xy_global={msg.xy_global} '
                     f'dead_reckoning={msg.dead_reckoning}')

    def gps_position(self, msg):
        if not self.px4_increasing('gps', int(msg.timestamp)):
            return
        stamp = self.px4_sample_stamp(int(msg.timestamp_sample or msg.timestamp))
        if stamp is None:
            return
        self.gps, self.gps_stamp = msg, stamp
        self.observe('gps',
                     f'fix={msg.fix_type} satellites={msg.satellites_used} '
                     f'eph={msg.eph:.2f}m epv={msg.epv:.2f}m')

    def estimator_status(self, msg):
        if not self.px4_increasing('estimator_flags', int(msg.timestamp)):
            return
        stamp = self.px4_sample_stamp(int(msg.timestamp))
        if stamp is None:
            return
        self.estimator_flags, self.estimator_flags_stamp = msg, stamp
        active = bool(msg.cs_gnss_pos)
        if active != self.last_ekf_gnss_state:
            self.last_ekf_gnss_state = active
            self.get_logger().info(
                f'PX4 EKF GNSS position fusion intended: {active} '
                f'(cs_opt_flow={msg.cs_opt_flow}, '
                f'cs_inertial_dead_reckoning={msg.cs_inertial_dead_reckoning})')

    def on_attitude(self, msg):
        if msg.header.frame_id != self.frame:
            return
        try:
            q = qvalues(msg.quaternion)
            rotation(q)
        except (ValueError, TypeError):
            return
        t = seconds(msg.header.stamp)
        if not math.isfinite(t) or t <= 0 or not self.increasing('attitude', t):
            return
        self.attitude, self.attitude_stamp = msg, msg.header.stamp
        self.observe('attitude', f'q_NED_xyzw={np.round(q, 4).tolist()}')

    def on_imu(self, msg):
        if msg.header.frame_id != self.body:
            return
        a, w = vector(msg.linear_acceleration), vector(msg.angular_velocity)
        if not np.isfinite(a).all() or not np.isfinite(w).all():
            return
        t = seconds(msg.header.stamp)
        if not math.isfinite(t) or t <= 0 or not self.increasing('imu', t):
            return
        self.imu, self.imu_stamp = msg, msg.header.stamp
        self.observe('imu', f'gyro_FRD={np.round(w, 3).tolist()}rad/s')

    def publish(self):
        out = NavigationState()
        now = self.get_clock().now().to_msg()
        out.header.stamp = self.local_stamp if self.local_stamp is not None else now
        out.header.frame_id = self.frame
        out.child_frame_id = self.body

        missing = []
        local = self.local
        gps = self.gps
        if self.local_stamp is None or not self.fresh(self.local_stamp, self.timeout):
            missing.append('local_position_missing_or_stale')
        if self.gps_stamp is None or not self.fresh(self.gps_stamp, self.timeout):
            missing.append('gps_missing_or_stale')
        if self.require_gnss and (self.estimator_flags_stamp is None or
                                  not self.fresh(self.estimator_flags_stamp, self.estimator_flags_timeout)):
            missing.append('estimator_flags_missing_or_stale')
        if self.attitude is None or self.attitude_stamp is None or not self.fresh(self.attitude_stamp, self.timeout):
            missing.append('attitude_missing_or_stale')
        if self.imu is None or self.imu_stamp is None or not self.fresh(self.imu_stamp, self.timeout):
            missing.append('imu_missing_or_stale')

        if self.local_stamp is not None and self.attitude_stamp is not None:
            skew = abs(seconds(self.local_stamp) - seconds(self.attitude_stamp))
            if skew > self.max_attitude_skew:
                missing.append('attitude_local_position_skew')
        if self.local_stamp is not None and self.imu_stamp is not None:
            skew = abs(seconds(self.local_stamp) - seconds(self.imu_stamp))
            if skew > self.max_imu_skew:
                missing.append('imu_local_position_skew')

        gps_reasons = gps_quality_reasons(
            gps, self.min_satellites, self.max_gps_eph, self.max_gps_epv)
        gps_fresh = self.gps_stamp is not None and self.fresh(self.gps_stamp, self.timeout)
        local_fresh = self.local_stamp is not None and self.fresh(self.local_stamp, self.timeout)
        estimator_flags_fresh = (self.estimator_flags_stamp is not None and
                                 self.fresh(self.estimator_flags_stamp, self.estimator_flags_timeout))
        if not gps_fresh:
            gps_reasons.append('gps_stale')
        local_reasons = local_position_reasons(local, self.require_gnss)
        if self.require_gnss:
            missing.extend(gps_reasons)
            if not estimator_flags_fresh:
                missing.append('estimator_flags_stale')
            elif not self.estimator_flags.cs_gnss_pos:
                missing.append('ekf_gnss_fusion_inactive')
        missing.extend(local_reasons)

        if local is not None:
            values = np.asarray([local.x, local.y, local.z,
                                 local.vx, local.vy, local.vz,
                                 local.ax, local.ay, local.az], dtype=float)
            if np.isfinite(values).all():
                assign(out.pose.position, values[:3])
                assign(out.twist.linear, values[3:6])
                assign(out.acceleration, values[6:9])
            out.eph = float(local.eph)
            out.epv = float(local.epv)
        if self.attitude is not None:
            try:
                q = qvalues(self.attitude.quaternion)
                rotation(q)
                assign_q(out.pose.orientation, q)
            except (ValueError, TypeError):
                missing.append('attitude_invalid')
        if self.imu is not None:
            assign(out.twist.angular, vector(self.imu.angular_velocity))

        if gps is not None:
            out.gps_fix_type = int(gps.fix_type)
            out.gps_satellites_used = int(gps.satellites_used)
            out.gps_eph = float(gps.eph)
            out.gps_epv = float(gps.epv)
        out.local_position_age = float(self.age(self.local_stamp)) if self.local_stamp is not None else float('inf')
        out.gps_age = float(self.age(self.gps_stamp)) if self.gps_stamp is not None else float('inf')
        out.estimator_flags_age = (float(self.age(self.estimator_flags_stamp))
                                   if self.estimator_flags_stamp is not None else float('inf'))
        out.attitude_age = float(self.age(self.attitude_stamp)) if self.attitude_stamp is not None else float('inf')
        out.imu_age = float(self.age(self.imu_stamp)) if self.imu_stamp is not None else float('inf')
        out.ekf_gnss_fusion = bool(self.estimator_flags is not None and
                                   self.estimator_flags.cs_gnss_pos and estimator_flags_fresh)
        out.gnss_aided = bool(local_fresh and gps_fresh and
                              gnss_aided(local, gps, gps_reasons, self.estimator_flags) and
                              estimator_flags_fresh)
        if self.require_gnss and not out.gnss_aided and not any(
                reason.startswith('gps_') or reason.startswith('gnss_') for reason in missing):
            missing.append('gnss_aiding_not_confirmed')

        out.valid = not missing
        out.reason = 'ok' if out.valid else ','.join(dict.fromkeys(missing))
        self.observe('navigation',
                     f'valid={out.valid} reason={out.reason} '
                     f'p_NED=({out.pose.position.x:.2f},{out.pose.position.y:.2f},{out.pose.position.z:.2f})m '
                     f'v_NED=({out.twist.linear.x:.2f},{out.twist.linear.y:.2f},{out.twist.linear.z:.2f})m/s '
                     f'GNSS={out.gnss_aided} EKF_GNSS={out.ekf_gnss_fusion} '
                     f'GPS_fix={out.gps_fix_type} sats={out.gps_satellites_used}')
        self.pub.publish(out)


def main(args=None):
    run(GpsNavigationNode, args)
