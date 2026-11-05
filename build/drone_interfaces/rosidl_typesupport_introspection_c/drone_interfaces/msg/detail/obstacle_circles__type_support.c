// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from drone_interfaces:msg/ObstacleCircles.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "drone_interfaces/msg/detail/obstacle_circles__rosidl_typesupport_introspection_c.h"
#include "drone_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "drone_interfaces/msg/detail/obstacle_circles__functions.h"
#include "drone_interfaces/msg/detail/obstacle_circles__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `xy`
// Member `radius`
// Member `safe_radius`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  drone_interfaces__msg__ObstacleCircles__init(message_memory);
}

void drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_fini_function(void * message_memory)
{
  drone_interfaces__msg__ObstacleCircles__fini(message_memory);
}

size_t drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__size_function__ObstacleCircles__xy(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__xy(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__xy(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__fetch_function__ObstacleCircles__xy(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__xy(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__assign_function__ObstacleCircles__xy(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__xy(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__resize_function__ObstacleCircles__xy(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__size_function__ObstacleCircles__radius(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__radius(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__radius(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__fetch_function__ObstacleCircles__radius(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__radius(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__assign_function__ObstacleCircles__radius(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__radius(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__resize_function__ObstacleCircles__radius(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__size_function__ObstacleCircles__safe_radius(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__safe_radius(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__safe_radius(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__fetch_function__ObstacleCircles__safe_radius(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__safe_radius(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__assign_function__ObstacleCircles__safe_radius(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__safe_radius(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__resize_function__ObstacleCircles__safe_radius(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_member_array[5] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__ObstacleCircles, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "xy",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__ObstacleCircles, xy),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__size_function__ObstacleCircles__xy,  // size() function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__xy,  // get_const(index) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__xy,  // get(index) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__fetch_function__ObstacleCircles__xy,  // fetch(index, &value) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__assign_function__ObstacleCircles__xy,  // assign(index, value) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__resize_function__ObstacleCircles__xy  // resize(index) function pointer
  },
  {
    "radius",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__ObstacleCircles, radius),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__size_function__ObstacleCircles__radius,  // size() function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__radius,  // get_const(index) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__radius,  // get(index) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__fetch_function__ObstacleCircles__radius,  // fetch(index, &value) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__assign_function__ObstacleCircles__radius,  // assign(index, value) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__resize_function__ObstacleCircles__radius  // resize(index) function pointer
  },
  {
    "safe_radius",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__ObstacleCircles, safe_radius),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__size_function__ObstacleCircles__safe_radius,  // size() function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_const_function__ObstacleCircles__safe_radius,  // get_const(index) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__get_function__ObstacleCircles__safe_radius,  // get(index) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__fetch_function__ObstacleCircles__safe_radius,  // fetch(index, &value) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__assign_function__ObstacleCircles__safe_radius,  // assign(index, value) function pointer
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__resize_function__ObstacleCircles__safe_radius  // resize(index) function pointer
  },
  {
    "over_capacity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__ObstacleCircles, over_capacity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_members = {
  "drone_interfaces__msg",  // message namespace
  "ObstacleCircles",  // message name
  5,  // number of fields
  sizeof(drone_interfaces__msg__ObstacleCircles),
  drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_member_array,  // message members
  drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_init_function,  // function to initialize message memory (memory has to be allocated)
  drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_type_support_handle = {
  0,
  &drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_drone_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, msg, ObstacleCircles)() {
  drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_type_support_handle.typesupport_identifier) {
    drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &drone_interfaces__msg__ObstacleCircles__rosidl_typesupport_introspection_c__ObstacleCircles_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
