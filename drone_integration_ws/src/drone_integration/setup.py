from glob import glob
from setuptools import setup, find_packages

setup(
    name='drone_integration',
    version='0.2.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/drone_integration']),
        ('share/drone_integration', ['package.xml', 'LICENSE']),
        ('share/drone_integration/config', glob('config/*.yaml')),
        ('share/drone_integration/launch', glob('launch/*.py')),
    ],
    install_requires=['setuptools', 'numpy', 'casadi>=3.6,<4', 'matplotlib', 'Pillow'],
    zip_safe=True,
    maintainer='Eoram Kim',
    maintainer_email='eoram@example.com',
    description='PX4 v1.16 ROS 2 GPS/EKF navigation, LiDAR collision avoidance and MPC integration',
    license='MIT',
    entry_points={
        'console_scripts': [
            'gz_reference_node = drone_integration.gz_reference_node:main',
            'flight_report = drone_integration.flight_report:main',
            'px4_imu_receiver_node = drone_integration.sensor.px4_imu_receiver_node:main',
            'optical_flow_receiver_node = drone_integration.sensor.optical_flow_receiver_node:main',
            'lidar_receiver_node = drone_integration.sensor.lidar_receiver_node:main',
            'gz_scan_time_adapter_node = drone_integration.sensor.gz_scan_time_adapter_node:main',
            'gps_navigation_node = drone_integration.navigation.gps_navigation_node:main',
            'collision_constraints_node = drone_integration.control.collision_constraints_node:main',
            'data_logger_node = drone_integration.data_logger_node:main',
            'mpc_node = drone_integration.control.mpc_node:main',
            'px4_command_node = drone_integration.control.px4_command_node:main',
        ]
    },
)
