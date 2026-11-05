// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from drone_interfaces:msg/FlowMeasurement.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "drone_interfaces/msg/detail/flow_measurement__rosidl_typesupport_introspection_c.h"
#include "drone_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "drone_interfaces/msg/detail/flow_measurement__functions.h"
#include "drone_interfaces/msg/detail/flow_measurement__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  drone_interfaces__msg__FlowMeasurement__init(message_memory);
}

void drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_fini_function(void * message_memory)
{
  drone_interfaces__msg__FlowMeasurement__fini(message_memory);
}

size_t drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__size_function__FlowMeasurement__pixel_flow(
  const void * untyped_member)
{
  (void)untyped_member;
  return 2;
}

const void * drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_const_function__FlowMeasurement__pixel_flow(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_function__FlowMeasurement__pixel_flow(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__fetch_function__FlowMeasurement__pixel_flow(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_const_function__FlowMeasurement__pixel_flow(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__assign_function__FlowMeasurement__pixel_flow(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_function__FlowMeasurement__pixel_flow(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__size_function__FlowMeasurement__delta_angle(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_const_function__FlowMeasurement__delta_angle(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_function__FlowMeasurement__delta_angle(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__fetch_function__FlowMeasurement__delta_angle(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_const_function__FlowMeasurement__delta_angle(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__assign_function__FlowMeasurement__delta_angle(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_function__FlowMeasurement__delta_angle(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_member_array[8] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__FlowMeasurement, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "px4_timestamp_sample",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__FlowMeasurement, px4_timestamp_sample),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pixel_flow",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    2,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__FlowMeasurement, pixel_flow),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__size_function__FlowMeasurement__pixel_flow,  // size() function pointer
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_const_function__FlowMeasurement__pixel_flow,  // get_const(index) function pointer
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_function__FlowMeasurement__pixel_flow,  // get(index) function pointer
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__fetch_function__FlowMeasurement__pixel_flow,  // fetch(index, &value) function pointer
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__assign_function__FlowMeasurement__pixel_flow,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "delta_angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__FlowMeasurement, delta_angle),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__size_function__FlowMeasurement__delta_angle,  // size() function pointer
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_const_function__FlowMeasurement__delta_angle,  // get_const(index) function pointer
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__get_function__FlowMeasurement__delta_angle,  // get(index) function pointer
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__fetch_function__FlowMeasurement__delta_angle,  // fetch(index, &value) function pointer
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__assign_function__FlowMeasurement__delta_angle,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "integration_dt",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__FlowMeasurement, integration_dt),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "distance_m",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__FlowMeasurement, distance_m),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "quality",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__FlowMeasurement, quality),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "valid",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__FlowMeasurement, valid),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_members = {
  "drone_interfaces__msg",  // message namespace
  "FlowMeasurement",  // message name
  8,  // number of fields
  sizeof(drone_interfaces__msg__FlowMeasurement),
  drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_member_array,  // message members
  drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_init_function,  // function to initialize message memory (memory has to be allocated)
  drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_type_support_handle = {
  0,
  &drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_drone_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, msg, FlowMeasurement)() {
  drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_type_support_handle.typesupport_identifier) {
    drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &drone_interfaces__msg__FlowMeasurement__rosidl_typesupport_introspection_c__FlowMeasurement_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
