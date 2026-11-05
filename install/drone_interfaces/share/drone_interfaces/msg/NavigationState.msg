std_msgs/Header header
string child_frame_id
# pose: map NED, quaternion xyzw (FRD body -> NED world).
# twist linear: map NED; angular: body FRD.
geometry_msgs/Pose pose
geometry_msgs/Twist twist
# PX4 EKF2 acceleration estimate in map NED.
geometry_msgs/Vector3 acceleration
bool valid
string reason
# Freshness of source measurements, seconds.
float64 local_position_age
float64 gps_age
float64 estimator_flags_age
float64 attitude_age
float64 imu_age
# Raw PX4 SensorGps quality indicators.
float64 gps_eph
float64 gps_epv
uint8 gps_fix_type
uint8 gps_satellites_used
# True only when the raw GNSS fix is healthy and EKF2 has a global, non-dead-reckoning reference.
bool gnss_aided
# PX4 EKF2 EstimatorStatusFlags.cs_gnss_pos (GNSS position fusion intended).
bool ekf_gnss_fusion
# PX4 EKF2 local position accuracy estimates.
float64 eph
float64 epv
