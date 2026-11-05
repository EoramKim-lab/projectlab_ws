# PX4 optical flow and gyro integrals expressed about body FRD axes.
# Downward range is a positive distance, not a NED z position.
std_msgs/Header header
uint64 px4_timestamp_sample
float64[2] pixel_flow
float64[3] delta_angle
float64 integration_dt
float64 distance_m
uint8 quality
bool valid
