// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from drone_interfaces:msg/NavigationState.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__STRUCT_H_
#define DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'child_frame_id'
// Member 'reason'
#include "rosidl_runtime_c/string.h"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'twist'
#include "geometry_msgs/msg/detail/twist__struct.h"
// Member 'acceleration'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in msg/NavigationState in the package drone_interfaces.
typedef struct drone_interfaces__msg__NavigationState
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String child_frame_id;
  /// pose: map NED, quaternion xyzw (FRD body -> NED world).
  /// twist linear: map NED; angular: body FRD.
  geometry_msgs__msg__Pose pose;
  geometry_msgs__msg__Twist twist;
  /// PX4 EKF2 acceleration estimate in map NED.
  geometry_msgs__msg__Vector3 acceleration;
  bool valid;
  rosidl_runtime_c__String reason;
  /// Freshness of source measurements, seconds.
  double local_position_age;
  double gps_age;
  double estimator_flags_age;
  double attitude_age;
  double imu_age;
  /// Raw PX4 SensorGps quality indicators.
  double gps_eph;
  double gps_epv;
  uint8_t gps_fix_type;
  uint8_t gps_satellites_used;
  /// True only when the raw GNSS fix is healthy and EKF2 has a global, non-dead-reckoning reference.
  bool gnss_aided;
  /// PX4 EKF2 EstimatorStatusFlags.cs_gnss_pos (GNSS position fusion intended).
  bool ekf_gnss_fusion;
  /// PX4 EKF2 local position accuracy estimates.
  double eph;
  double epv;
} drone_interfaces__msg__NavigationState;

// Struct for a sequence of drone_interfaces__msg__NavigationState.
typedef struct drone_interfaces__msg__NavigationState__Sequence
{
  drone_interfaces__msg__NavigationState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__msg__NavigationState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__STRUCT_H_
