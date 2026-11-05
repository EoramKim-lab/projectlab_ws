// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from drone_interfaces:msg/Halfplanes.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "drone_interfaces/msg/detail/halfplanes__rosidl_typesupport_introspection_c.h"
#include "drone_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "drone_interfaces/msg/detail/halfplanes__functions.h"
#include "drone_interfaces/msg/detail/halfplanes__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"
// Member `a`
// Member `b`
// Member `sector_ids`
// Member `nearest_range`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  drone_interfaces__msg__Halfplanes__init(message_memory);
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_fini_function(void * message_memory)
{
  drone_interfaces__msg__Halfplanes__fini(message_memory);
}

size_t drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__size_function__Halfplanes__a(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__a(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__a(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__fetch_function__Halfplanes__a(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__a(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__assign_function__Halfplanes__a(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__a(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__resize_function__Halfplanes__a(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__size_function__Halfplanes__b(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__b(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__b(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__fetch_function__Halfplanes__b(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__b(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__assign_function__Halfplanes__b(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__b(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__resize_function__Halfplanes__b(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__size_function__Halfplanes__sector_ids(
  const void * untyped_member)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__sector_ids(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__int32__Sequence * member =
    (const rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__sector_ids(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__fetch_function__Halfplanes__sector_ids(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const int32_t * item =
    ((const int32_t *)
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__sector_ids(untyped_member, index));
  int32_t * value =
    (int32_t *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__assign_function__Halfplanes__sector_ids(
  void * untyped_member, size_t index, const void * untyped_value)
{
  int32_t * item =
    ((int32_t *)
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__sector_ids(untyped_member, index));
  const int32_t * value =
    (const int32_t *)(untyped_value);
  *item = *value;
}

bool drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__resize_function__Halfplanes__sector_ids(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__int32__Sequence * member =
    (rosidl_runtime_c__int32__Sequence *)(untyped_member);
  rosidl_runtime_c__int32__Sequence__fini(member);
  return rosidl_runtime_c__int32__Sequence__init(member, size);
}

size_t drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__size_function__Halfplanes__nearest_range(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__nearest_range(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__nearest_range(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__fetch_function__Halfplanes__nearest_range(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__nearest_range(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__assign_function__Halfplanes__nearest_range(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__nearest_range(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__resize_function__Halfplanes__nearest_range(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_member_array[8] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__Halfplanes, header),  // bytes offset in struct
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
    offsetof(drone_interfaces__msg__Halfplanes, valid),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reason",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__Halfplanes, reason),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "origin_feasible",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__Halfplanes, origin_feasible),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "a",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__Halfplanes, a),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__size_function__Halfplanes__a,  // size() function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__a,  // get_const(index) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__a,  // get(index) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__fetch_function__Halfplanes__a,  // fetch(index, &value) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__assign_function__Halfplanes__a,  // assign(index, value) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__resize_function__Halfplanes__a  // resize(index) function pointer
  },
  {
    "b",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__Halfplanes, b),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__size_function__Halfplanes__b,  // size() function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__b,  // get_const(index) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__b,  // get(index) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__fetch_function__Halfplanes__b,  // fetch(index, &value) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__assign_function__Halfplanes__b,  // assign(index, value) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__resize_function__Halfplanes__b  // resize(index) function pointer
  },
  {
    "sector_ids",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__Halfplanes, sector_ids),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__size_function__Halfplanes__sector_ids,  // size() function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__sector_ids,  // get_const(index) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__sector_ids,  // get(index) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__fetch_function__Halfplanes__sector_ids,  // fetch(index, &value) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__assign_function__Halfplanes__sector_ids,  // assign(index, value) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__resize_function__Halfplanes__sector_ids  // resize(index) function pointer
  },
  {
    "nearest_range",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_interfaces__msg__Halfplanes, nearest_range),  // bytes offset in struct
    NULL,  // default value
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__size_function__Halfplanes__nearest_range,  // size() function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_const_function__Halfplanes__nearest_range,  // get_const(index) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__get_function__Halfplanes__nearest_range,  // get(index) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__fetch_function__Halfplanes__nearest_range,  // fetch(index, &value) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__assign_function__Halfplanes__nearest_range,  // assign(index, value) function pointer
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__resize_function__Halfplanes__nearest_range  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_members = {
  "drone_interfaces__msg",  // message namespace
  "Halfplanes",  // message name
  8,  // number of fields
  sizeof(drone_interfaces__msg__Halfplanes),
  drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_member_array,  // message members
  drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_init_function,  // function to initialize message memory (memory has to be allocated)
  drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_type_support_handle = {
  0,
  &drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_drone_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_interfaces, msg, Halfplanes)() {
  drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_type_support_handle.typesupport_identifier) {
    drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &drone_interfaces__msg__Halfplanes__rosidl_typesupport_introspection_c__Halfplanes_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
