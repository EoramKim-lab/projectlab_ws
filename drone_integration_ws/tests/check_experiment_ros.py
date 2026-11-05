"""ROS message/callback checks, run separately after sourcing ROS and workspace.
Does not arm, enable Offboard or publish PX4 setpoints.
"""
import math
import time
import unittest
import numpy as np
import rclpy
from sensor_msgs.msg import LaserScan
from px4_msgs.msg import SensorCombined, VehicleAttitude, VehicleOpticalFlow, SensorOpticalFlow, DistanceSensor
from drone_integration.sensor.lidar_receiver_node import LidarReceiverNode
from drone_integration.sensor.optical_flow_receiver_node import OpticalFlowReceiverNode
from drone_integration.sensor.px4_imu_receiver_node import Px4ImuReceiverNode
from drone_integration.control.px4_command_node import Px4CommandNode
from drone_integration.control.mpc_node import MpcNode
from drone_interfaces.msg import ProcessedScan


class Capture:
    def __init__(self): self.messages = []
    def publish(self, msg): self.messages.append(msg)


class ExperimentTests(unittest.TestCase):
    def setUp(self): self.nodes = []
    def tearDown(self):
        for node in self.nodes: node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

    def make(self, cls):
        node = cls(); self.nodes.append(node); return node



    def test_sensor_values_and_monitor(self):
        rclpy.init()
        lidar = self.make(LidarReceiverNode)
        lidar.pub = Capture()
        scan = LaserScan()
        scan.header.stamp = lidar.get_clock().now().to_msg()
        scan.angle_increment = .01
        scan.range_min,scan.range_max = .1,8.
        scan.ranges = [2.] * 100
        lidar.scan(scan)
        self.assertTrue(lidar.pub.messages[-1].valid)
        self.assertIn('nearest_body=2.000m', lidar._monitor_values['lidar'][1])
        lidar.print_monitor()
        imu = self.make(Px4ImuReceiverNode)
        imu.imu_pub,imu.att_pub = Capture(),Capture()
        sample = SensorCombined()
        sample.timestamp = imu.get_clock().now().nanoseconds//1000
        sample.accelerometer_m_s2 = [0.,0.,-9.81]
        sample.gyro_rad = [0.,.1,0.]
        imu.imu(sample)
        attitude = VehicleAttitude()
        attitude.timestamp_sample = sample.timestamp
        attitude.q = [1.,0.,0.,0.]
        imu.attitude(attitude)
        self.assertAlmostEqual(imu.imu_pub.messages[-1].linear_acceleration.z,-9.81,places=4)
        self.assertEqual(len(imu.att_pub.messages),1)
        imu.print_monitor()
        sample.timestamp += 1
        sample.gyro_clipping = 176
        imu.imu(sample)
        self.assertEqual(len(imu.imu_pub.messages), 1)
        self.assertIn('invalid clipping bitmask', imu._monitor_values['imu'][1])
        sample.gyro_clipping = 1
        imu.imu(sample)
        self.assertEqual(len(imu.imu_pub.messages), 1)
        self.assertIn('gyro_clipping=1', imu._monitor_values['imu'][1])
        optical = self.make(OpticalFlowReceiverNode)
        optical.flow_pub,optical.range_pub = Capture(),Capture()
        topics = {sub.topic_name: sub.msg_type for sub in optical.subscriptions}
        self.assertIs(topics['/fmu/out/sensor_optical_flow'], SensorOpticalFlow)
        self.assertNotIn('/fmu/out/vehicle_optical_flow', topics)
        raw = SensorOpticalFlow()
        raw.timestamp_sample = optical.get_clock().now().nanoseconds//1000
        raw.quality = 200
        raw.pixel_flow = [.01, .02]
        optical.raw_flow(raw)
        self.assertEqual(len(optical.flow_pub.messages), 1)
        self.assertFalse(optical.flow_pub.messages[-1].valid)
        self.assertIn('RAW_SENSOR_AXES', optical._monitor_values['raw_flow'][1])
        flow = VehicleOpticalFlow()
        flow.timestamp_sample,flow.integration_timespan_us,flow.quality = raw.timestamp_sample+1,20000,200
        flow.pixel_flow,flow.delta_angle = [.01,.02],[0.,0.,0.]
        flow.distance_m = 1.5
        distance = DistanceSensor()
        distance.timestamp = raw.timestamp_sample
        distance.orientation = DistanceSensor.ROTATION_DOWNWARD_FACING
        distance.signal_quality = 100
        distance.min_distance,distance.max_distance,distance.current_distance = .1,8.,1.5
        optical.distance(distance)
        optical.flow(flow)
        self.assertTrue(optical.flow_pub.messages[-1].valid)
        self.assertAlmostEqual(optical.range_pub.messages[-1].range,1.5)
        optical.print_monitor()
        # Verify WAITING and STALE without spinning or flooding logs.
        imu._monitor_values['attitude'] = None
        _,detail = imu._monitor_values['imu']
        imu._monitor_values['imu'] = (time.monotonic()-1.,detail)
        imu.print_monitor()



if __name__ == '__main__': unittest.main()
