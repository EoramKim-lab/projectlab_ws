# Measurement time and execution rates

PX4 adapters preserve the timestamps synchronized by uXRCE-DDS. They do not
estimate an offset from packet arrival and do not substitute ROS now().
Reference: https://docs.px4.io/v1.14/en/middleware/uxrce_dds

- IMU stamp: SensorCombined.timestamp + accelerometer_timestamp_relative.
  Acceleration drives translation; gyro values retain their original sample
  and can differ by the relative offset (sensor_msgs/Imu has only one header).
- Attitude and flow stamp: timestamp_sample.
- Range stamp: timestamp (no separate sample timestamp in this message).
- LiDAR and mocap retain their input headers; accuracy depends on the driver.
- Reject nonpositive, >50 ms future, or older than px4_sample_timeout (250 ms)
  timestamps at the PX4 adapter, including in relaxed dead-reckoning mode.
- Monitor LIVE/STALE uses monotonic receipt time; navigation freshness and
  integration use measurement time. No fallback to receipt-based integration.

Navigation, dead reckoning, MPC execution and PX4 command output default to
20 Hz. Cartesian MPC uses a first prediction interval of 1/publish_rate
(0.05 s), followed by 19 intervals of dt=0.15 s (2.9 s total). This ensures
the first commanded velocity increment respects the acceleration limit at
the actual output rate. The state includes measured horizontal velocity;
prediction acceleration is expressed in map NED, independently of body yaw.
Sensor adapters and collision processing remain event-driven; watchdog and
monitor timers keep their independent diagnostic periods. Equal timer periods
are not phase synchronization. No sensor samples are fabricated or repeated to
match a control period.

Validation before operation: inspect raw PX4 timestamp/sample age against ROS
clock and /fmu/out/timesync_status; confirm no adapter time warnings. Measure
sensor arrival rates and gaps; confirm MPC solve time stays below 50 ms under
load. Restart nodes after building. This change does not implement historical
attitude interpolation or delayed-measurement replay. Bridge synchronization
can hide a PX4 reboot from timestamp rollback detection; existing explicit
reset handling remains in place.
