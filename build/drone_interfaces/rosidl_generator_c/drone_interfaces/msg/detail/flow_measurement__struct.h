// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from drone_interfaces:msg/FlowMeasurement.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__STRUCT_H_
#define DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__STRUCT_H_

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

/// Struct defined in msg/FlowMeasurement in the package drone_interfaces.
/**
  * PX4 optical flow and gyro integrals expressed about body FRD axes.
  * Downward range is a positive distance, not a NED z position.
 */
typedef struct drone_interfaces__msg__FlowMeasurement
{
  std_msgs__msg__Header header;
  uint64_t px4_timestamp_sample;
  double pixel_flow[2];
  double delta_angle[3];
  double integration_dt;
  double distance_m;
  uint8_t quality;
  bool valid;
} drone_interfaces__msg__FlowMeasurement;

// Struct for a sequence of drone_interfaces__msg__FlowMeasurement.
typedef struct drone_interfaces__msg__FlowMeasurement__Sequence
{
  drone_interfaces__msg__FlowMeasurement * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__msg__FlowMeasurement__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__STRUCT_H_
