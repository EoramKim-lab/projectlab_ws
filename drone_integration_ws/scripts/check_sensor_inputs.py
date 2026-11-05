#!/usr/bin/env python3
"""Read-only ROS sensor diagnosis. Does not enable control or publish messages."""
import argparse
from collections import Counter
import importlib
import os
import socket
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=10.)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error('--seconds must be positive')
    # Do not mistake a sandbox transport restriction for absent hardware.
    try:
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.close()
    except OSError as exc:
        print(f'Cannot inspect live DDS: UDP socket unavailable: {exc}')
        print('Run this script in a host terminal with ROS and this workspace sourced.')
        return 2
    import rclpy
    from rclpy.qos import qos_profile_sensor_data
    from rosidl_runtime_py.utilities import get_message
    from ament_index_python.packages import get_package_prefix
    rclpy.init()
    node = rclpy.create_node('sensor_input_diagnostic')
    topics = {
        '/fmu/out/sensor_combined': 'px4_msgs/msg/SensorCombined',
        '/fmu/out/vehicle_attitude': 'px4_msgs/msg/VehicleAttitude',
        '/fmu/out/vehicle_optical_flow': 'px4_msgs/msg/VehicleOpticalFlow',
        '/fmu/out/sensor_optical_flow': 'px4_msgs/msg/SensorOpticalFlow',
        '/fmu/out/distance_sensor': 'px4_msgs/msg/DistanceSensor',
        '/fmu/out/vehicle_local_position': 'px4_msgs/msg/VehicleLocalPosition',
        '/fmu/out/vehicle_status_v1': 'px4_msgs/msg/VehicleStatus',
        '/scan': 'sensor_msgs/msg/LaserScan',
        '/lidar/processed': 'drone_interfaces/msg/ProcessedScan',
        '/sensors/imu': 'sensor_msgs/msg/Imu',
        '/sensors/attitude': 'geometry_msgs/msg/QuaternionStamped',
        '/sensors/flow': 'drone_interfaces/msg/FlowMeasurement',
        '/sensors/range': 'sensor_msgs/msg/Range',
        '/navigation/state': 'drone_interfaces/msg/NavigationState',
        '/collision/halfplanes': 'drone_interfaces/msg/Halfplanes',
        '/control/velocity_cmd': 'geometry_msgs/msg/TwistStamped',
        '/sensors/px4_reset': 'std_msgs/msg/Empty',
    }
    counts, latest = Counter(), {}
    def receive(topic, msg):
        counts[topic] += 1
        latest[topic] = msg
    try:
        print('px4_msgs prefix:', get_package_prefix('px4_msgs'))
        print('SensorCombined Python:', importlib.import_module('px4_msgs.msg._sensor_combined').__file__)
        print('ROS_DOMAIN_ID:', os.environ.get('ROS_DOMAIN_ID', '0'))
        for topic, typ in topics.items():
            node.create_subscription(get_message(typ), topic,
                                     lambda msg, topic=topic: receive(topic, msg), qos_profile_sensor_data)
        started = time.monotonic()
        while time.monotonic() - started < args.seconds:
            rclpy.spin_once(node, timeout_sec=.1)
        elapsed = time.monotonic() - started
        for topic in topics:
            pubs = node.get_publishers_info_by_topic(topic)
            print(f'{topic}: publishers={len(pubs)} rx={counts[topic]} rate={counts[topic]/elapsed:.1f}Hz')
            msg = latest.get(topic)
            if msg is not None:
                for key in ('timestamp', 'timestamp_sample', 'accelerometer_clipping', 'gyro_clipping',
                            'gyro_rad', 'accelerometer_m_s2', 'quality', 'distance_m',
                            'current_distance', 'orientation', 'signal_quality', 'valid', 'reason',
                            'accelerometer_timestamp_relative', 'integration_timespan_us',
                            'delta_angle', 'v_xy_valid', 'v_z_valid', 'nav_state', 'arming_state',
                            'origin_feasible'):
                    if hasattr(msg, key):
                        print(f'  {key}={getattr(msg,key)}')
            if not pubs:
                print('  No discovered publisher: check PX4 DDS exports, driver and ROS domain.')
            elif not counts[topic]:
                print('  Publisher discovered but no samples: check source activity, DDS/QoS and message compatibility.')
    finally:
        node.destroy_node()
        rclpy.shutdown()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
