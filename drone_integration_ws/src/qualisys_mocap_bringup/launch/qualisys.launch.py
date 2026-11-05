"""Receive raw QTM topics without starting the drone control stack."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, RegisterEventHandler
from launch.events import matches_action
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from launch_ros.parameter_descriptions import ParameterValue
from lifecycle_msgs.msg import Transition


def generate_launch_description():
    default_config = os.path.join(
        get_package_share_directory('qualisys_mocap_bringup'),
        'config', 'qualisys.yaml')
    driver = LifecycleNode(
        package='qualisys_driver', executable='qualisys_driver_main',
        name='qualisys_driver_node', namespace='', output='screen',
        parameters=[LaunchConfiguration('config'), {
            'use_sim_time': False,
            'host_name': ParameterValue(LaunchConfiguration('host_name'), value_type=str),
            'port': ParameterValue(LaunchConfiguration('port'), value_type=int),
        }],
        remappings=[('rigid_bodies', '/mocap/rigid_bodies'),
                    ('/markers', '/mocap/markers')],
    )
    activate = RegisterEventHandler(OnStateTransition(
        target_lifecycle_node=driver, start_state='configuring', goal_state='inactive',
        entities=[EmitEvent(event=ChangeState(
            lifecycle_node_matcher=matches_action(driver),
            transition_id=Transition.TRANSITION_ACTIVATE))],
    ))
    return LaunchDescription([
        DeclareLaunchArgument('host_name', default_value='192.168.0.34',
                              description='IPv4 address of the QTM PC'),
        DeclareLaunchArgument('port', default_value='22222'),
        DeclareLaunchArgument('config', default_value=default_config),
        activate,
        driver,
        EmitEvent(event=ChangeState(
            lifecycle_node_matcher=matches_action(driver),
            transition_id=Transition.TRANSITION_CONFIGURE)),
    ])
