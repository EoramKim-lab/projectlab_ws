// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from drone_interfaces:msg/Halfplanes.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__STRUCT_H_
#define DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__STRUCT_H_

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
// Member 'a'
// Member 'b'
// Member 'sector_ids'
// Member 'nearest_range'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/Halfplanes in the package drone_interfaces.
typedef struct drone_interfaces__msg__Halfplanes
{
  std_msgs__msg__Header header;
  bool valid;
  rosidl_runtime_c__String reason;
  bool origin_feasible;
  /// A has shape (len(b),2), row-major. A * p_body_frd_at_scan <= b.
  rosidl_runtime_c__double__Sequence a;
  rosidl_runtime_c__double__Sequence b;
  rosidl_runtime_c__int32__Sequence sector_ids;
  rosidl_runtime_c__double__Sequence nearest_range;
} drone_interfaces__msg__Halfplanes;

// Struct for a sequence of drone_interfaces__msg__Halfplanes.
typedef struct drone_interfaces__msg__Halfplanes__Sequence
{
  drone_interfaces__msg__Halfplanes * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__msg__Halfplanes__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__STRUCT_H_
