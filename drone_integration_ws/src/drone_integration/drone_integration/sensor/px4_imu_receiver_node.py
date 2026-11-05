"""Pixhawk calibrated specific force / rate and PX4 EKF attitude, preserved in FRD/NED."""
import numpy as np
from sensor_msgs.msg import Imu
from geometry_msgs.msg import QuaternionStamped
from px4_msgs.msg import SensorCombined, VehicleAttitude
from ..common import Base, SENSOR_QOS, run
from ..math_utils import px4_attitude, assign, assign_q

class Px4ImuReceiverNode(Base):
    def __init__(self):
        super().__init__('px4_imu_receiver_node')
        self.body = self.param('body_frame','base_link_frd')
        self.frame = self.param('map_frame','map_ned')
        self.watch_px4_clock()
        self.start_monitor('imu', 'attitude')
        self.imu_pub = self.create_publisher(Imu,'sensors/imu',10)
        self.att_pub = self.create_publisher(QuaternionStamped,'sensors/attitude',10)
        self.create_subscription(SensorCombined,'/fmu/out/sensor_combined',self.imu,SENSOR_QOS)
        self.create_subscription(VehicleAttitude,'/fmu/out/vehicle_attitude',self.attitude,SENSOR_QOS)

    def imu(self,msg):
        mask = SensorCombined.CLIPPING_X | SensorCombined.CLIPPING_Y | SensorCombined.CLIPPING_Z
        if (int(msg.accelerometer_clipping) | int(msg.gyro_clipping)) & ~mask:
            self.observe('imu', f'REJECTED invalid clipping bitmask accel={msg.accelerometer_clipping} '
                         f'gyro={msg.gyro_clipping}; expected 0..{mask}; check firmware/CDR/message definitions')
            return
        if (msg.accelerometer_timestamp_relative == SensorCombined.RELATIVE_TIMESTAMP_INVALID
                or msg.accelerometer_clipping or msg.gyro_clipping):
            self.observe('imu', f'REJECTED accel_relative_timestamp={msg.accelerometer_timestamp_relative} '
                         f'accel_clipping={msg.accelerometer_clipping} gyro_clipping={msg.gyro_clipping}')
            return
        a,w = np.asarray(msg.accelerometer_m_s2),np.asarray(msg.gyro_rad)
        if not np.isfinite(a).all() or not np.isfinite(w).all() or not self.px4_increasing('imu',msg.timestamp):
            return
        # Translation is driven by acceleration; SensorCombined gyro has a
        # separate sample time, offset by accelerometer_timestamp_relative.
        stamp = self.px4_sample_stamp(int(msg.timestamp) + int(msg.accelerometer_timestamp_relative))
        if stamp is None:
            return
        out = Imu()
        out.header.stamp = stamp
        out.header.frame_id = self.body
        out.orientation_covariance[0] = -1.0  # attitude is published separately
        assign(out.linear_acceleration,a)
        assign(out.angular_velocity,w)
        self.observe('imu', f'a_FRD={np.round(a, 3).tolist()}m/s2 gyro_FRD={np.round(w, 3).tolist()}rad/s')
        self.imu_pub.publish(out)

    def attitude(self,msg):
        try:
            q = px4_attitude(msg.q)
        except ValueError:
            self.observe('attitude', 'REJECTED invalid quaternion')
            return
        if not self.px4_increasing('attitude',msg.timestamp_sample):
            return
        stamp = self.px4_sample_stamp(msg.timestamp_sample)
        if stamp is None:
            return
        out = QuaternionStamped()
        out.header.stamp = stamp
        out.header.frame_id = self.frame
        assign_q(out.quaternion,q)
        self.observe('attitude', f'q_NED_xyzw={np.round(q, 4).tolist()}')
        self.att_pub.publish(out)

def main(args=None): run(Px4ImuReceiverNode,args)
