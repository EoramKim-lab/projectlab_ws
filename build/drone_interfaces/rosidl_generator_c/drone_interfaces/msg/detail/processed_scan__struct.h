// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from drone_interfaces:msg/ProcessedScan.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__PROCESSED_SCAN__STRUCT_H_
#define DRONE_INTERFACES__MSG__DETAIL__PROCESSED_SCAN__STRUCT_H_

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
// Member 'reason'
#include "rosidl_runtime_c/string.h"
// Member 'xy'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/ProcessedScan in the package drone_interfaces.
typedef struct drone_interfaces__msg__ProcessedScan
{
  std_msgs__msg__Header header;
  bool valid;
  rosidl_runtime_c__String reason;
  uint32_t raw_count;
  /// Interleaved body FRD xy, meters. Origin = body reference point at scan time.
  rosidl_runtime_c__double__Sequence xy;
} drone_interfaces__msg__ProcessedScan;

// Struct for a sequence of drone_interfaces__msg__ProcessedScan.
typedef struct drone_interfaces__msg__ProcessedScan__Sequence
{
  drone_interfaces__msg__ProcessedScan * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__msg__ProcessedScan__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRONE_INTERFACES__MSG__DETAIL__PROCESSED_SCAN__STRUCT_H_
