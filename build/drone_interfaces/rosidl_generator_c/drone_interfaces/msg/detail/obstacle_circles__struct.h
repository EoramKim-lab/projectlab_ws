// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from drone_interfaces:msg/ObstacleCircles.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__STRUCT_H_
#define DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__STRUCT_H_

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
// Member 'xy'
// Member 'radius'
// Member 'safe_radius'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/ObstacleCircles in the package drone_interfaces.
/**
  * Generated circles in map NED, before capacity and solver checks.
  * Only published for valid scans aligned with navigation; silence is not free space.
 */
typedef struct drone_interfaces__msg__ObstacleCircles
{
  std_msgs__msg__Header header;
  /// Interleaved center x/y (m); array index is not a persistent tracking ID.
  rosidl_runtime_c__double__Sequence xy;
  rosidl_runtime_c__double__Sequence radius;
  /// Observed radius + drone radius + safety margin (m).
  rosidl_runtime_c__double__Sequence safe_radius;
  bool over_capacity;
} drone_interfaces__msg__ObstacleCircles;

// Struct for a sequence of drone_interfaces__msg__ObstacleCircles.
typedef struct drone_interfaces__msg__ObstacleCircles__Sequence
{
  drone_interfaces__msg__ObstacleCircles * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_interfaces__msg__ObstacleCircles__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__STRUCT_H_
