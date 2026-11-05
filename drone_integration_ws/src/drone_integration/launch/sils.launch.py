"""Bring up the ROS 2 half of PX4 v1.16 + Gazebo Harmonic SILS."""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


DEFAULT_GZ_SCAN_TOPIC = (
    '/world/default/model/x500_lidar_2d_0/link/link/'
    'sensor/lidar_2d_v2/scan'
)


def _nodes(context, *args, **kwargs):
    scan_topic = LaunchConfiguration('gz_scan_topic').perform(context)
    config = os.path.join(get_package_share_directory('drone_integration'),
                          'config', 'sils.yaml')

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='gz_scan_bridge',
        arguments=[f'{scan_topic}@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'],
        remappings=[(scan_topic, '/scan_gz')],
        output='screen')

    node_specs = [
        ('drone_integration', 'gz_reference_node'),
        ('drone_integration', 'px4_imu_receiver_node'),
        ('drone_integration', 'gps_navigation_node'),
        ('drone_integration', 'gz_scan_time_adapter_node'),
        ('drone_integration', 'lidar_receiver_node'),
        ('drone_integration', 'collision_constraints_node'),
        ('drone_integration', 'mpc_node'),
        ('drone_integration', 'px4_command_node'),
        ('drone_integration', 'data_logger_node'),
    ]
    world_sdf = LaunchConfiguration('world_sdf').perform(context)
    nodes = [Node(package=package, executable=executable,
                  name=executable, parameters=[config] + ([{'report_world_sdf': world_sdf}]
                     if executable == 'data_logger_node' else []), output='screen')
             for package, executable in node_specs]
    return [bridge, *nodes]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('world_sdf', default_value='',
                              description='Configured Gazebo SDF to snapshot in flight reports'),
        DeclareLaunchArgument(
            'gz_scan_topic', default_value=DEFAULT_GZ_SCAN_TOPIC,
            description='Gazebo Transport LaserScan topic from x500_lidar_2d'),
        OpaqueFunction(function=_nodes),
    ])
