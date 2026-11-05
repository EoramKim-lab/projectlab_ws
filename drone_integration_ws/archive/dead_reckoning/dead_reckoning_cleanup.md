# Dead-reckoning-only application

Removed the generic NavigationNode and mocap adapter, their console scripts,
configuration sections, logger subscriptions, and mocap4r2_msgs dependency.
NavigationState no longer contains mocap_age; rebuild external consumers.
DeadReckoningNode now directly derives from Base and owns its four sensor
callbacks, validity reporting and reset behavior. Estimator has no absolute
position or mocap velocity correction; first range initializes the horizontal
origin once. A later range update cannot clear a latched IMU prediction gap.

Removed dummy-navigation tests and command special cases. Sensor checks remain
in check_experiment_ros.py; dead-reckoning tests cover origin initialization,
flow integration, range correction, stale/invalid data and reset. Fixed MPC
reference defaults now use the local ENU origin and a six-meter x goal.

Unused third-party mocap packages have COLCON_IGNORE; their source and historical
results remain available. Previous instructions are archived under validation.
No vehicle commands or live controller changes were issued during this refactor.

Validation completed: 34 offline unit tests and 36 ROS message/callback tests
passed. drone_interfaces, drone_integration and the previously missing px4_msgs
installation built successfully. ROS callback tests emitted sandbox socket
warnings; they do not establish live DDS delivery or hardware timing.
