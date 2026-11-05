"""Restamp Gazebo LaserScan arrivals to the PX4/ROS wall-clock epoch for SILS."""
from copy import deepcopy
from sensor_msgs.msg import LaserScan
from ..common import Base, SENSOR_QOS, run


class GzScanTimeAdapterNode(Base):
    def __init__(self):
        super().__init__('gz_scan_time_adapter_node')
        self.input_topic = self.param('input_topic', '/scan_gz')
        self.output_topic = self.param('output_topic', '/scan')
        self.frame = self.param('scan_frame', 'lidar_c1_link')
        self.start_monitor('gazebo_scan')
        self.pub = self.create_publisher(LaserScan, self.output_topic, 10)
        self.create_subscription(LaserScan, self.input_topic, self.scan, SENSOR_QOS)

    def scan(self, msg):
        out = deepcopy(msg)
        # Gazebo's sensor stamp is simulation time. PX4 uXRCE-DDS timestamps in
        # this workspace are synchronized to the host ROS clock, so stamp the
        # bridged scan at receipt to keep the scan/state skew check meaningful.
        out.header.stamp = self.get_clock().now().to_msg()
        out.header.frame_id = self.frame
        self.pub.publish(out)
        self.observe('gazebo_scan', f'beams={len(out.ranges)} frame={out.header.frame_id}')


def main(args=None):
    run(GzScanTimeAdapterNode, args)
