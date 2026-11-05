// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from drone_interfaces:msg/NavigationState.idl
// generated code does not contain a copyright notice
#include "drone_interfaces/msg/detail/navigation_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `child_frame_id`
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `twist`
#include "geometry_msgs/msg/detail/twist__functions.h"
// Member `acceleration`
#include "geometry_msgs/msg/detail/vector3__functions.h"

bool
drone_interfaces__msg__NavigationState__init(drone_interfaces__msg__NavigationState * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    drone_interfaces__msg__NavigationState__fini(msg);
    return false;
  }
  // child_frame_id
  if (!rosidl_runtime_c__String__init(&msg->child_frame_id)) {
    drone_interfaces__msg__NavigationState__fini(msg);
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    drone_interfaces__msg__NavigationState__fini(msg);
    return false;
  }
  // twist
  if (!geometry_msgs__msg__Twist__init(&msg->twist)) {
    drone_interfaces__msg__NavigationState__fini(msg);
    return false;
  }
  // acceleration
  if (!geometry_msgs__msg__Vector3__init(&msg->acceleration)) {
    drone_interfaces__msg__NavigationState__fini(msg);
    return false;
  }
  // valid
  // reason
  if (!rosidl_runtime_c__String__init(&msg->reason)) {
    drone_interfaces__msg__NavigationState__fini(msg);
    return false;
  }
  // local_position_age
  // gps_age
  // estimator_flags_age
  // attitude_age
  // imu_age
  // gps_eph
  // gps_epv
  // gps_fix_type
  // gps_satellites_used
  // gnss_aided
  // ekf_gnss_fusion
  // eph
  // epv
  return true;
}

void
drone_interfaces__msg__NavigationState__fini(drone_interfaces__msg__NavigationState * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // child_frame_id
  rosidl_runtime_c__String__fini(&msg->child_frame_id);
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // twist
  geometry_msgs__msg__Twist__fini(&msg->twist);
  // acceleration
  geometry_msgs__msg__Vector3__fini(&msg->acceleration);
  // valid
  // reason
  rosidl_runtime_c__String__fini(&msg->reason);
  // local_position_age
  // gps_age
  // estimator_flags_age
  // attitude_age
  // imu_age
  // gps_eph
  // gps_epv
  // gps_fix_type
  // gps_satellites_used
  // gnss_aided
  // ekf_gnss_fusion
  // eph
  // epv
}

bool
drone_interfaces__msg__NavigationState__are_equal(const drone_interfaces__msg__NavigationState * lhs, const drone_interfaces__msg__NavigationState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // child_frame_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->child_frame_id), &(rhs->child_frame_id)))
  {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // twist
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->twist), &(rhs->twist)))
  {
    return false;
  }
  // acceleration
  if (!geometry_msgs__msg__Vector3__are_equal(
      &(lhs->acceleration), &(rhs->acceleration)))
  {
    return false;
  }
  // valid
  if (lhs->valid != rhs->valid) {
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reason), &(rhs->reason)))
  {
    return false;
  }
  // local_position_age
  if (lhs->local_position_age != rhs->local_position_age) {
    return false;
  }
  // gps_age
  if (lhs->gps_age != rhs->gps_age) {
    return false;
  }
  // estimator_flags_age
  if (lhs->estimator_flags_age != rhs->estimator_flags_age) {
    return false;
  }
  // attitude_age
  if (lhs->attitude_age != rhs->attitude_age) {
    return false;
  }
  // imu_age
  if (lhs->imu_age != rhs->imu_age) {
    return false;
  }
  // gps_eph
  if (lhs->gps_eph != rhs->gps_eph) {
    return false;
  }
  // gps_epv
  if (lhs->gps_epv != rhs->gps_epv) {
    return false;
  }
  // gps_fix_type
  if (lhs->gps_fix_type != rhs->gps_fix_type) {
    return false;
  }
  // gps_satellites_used
  if (lhs->gps_satellites_used != rhs->gps_satellites_used) {
    return false;
  }
  // gnss_aided
  if (lhs->gnss_aided != rhs->gnss_aided) {
    return false;
  }
  // ekf_gnss_fusion
  if (lhs->ekf_gnss_fusion != rhs->ekf_gnss_fusion) {
    return false;
  }
  // eph
  if (lhs->eph != rhs->eph) {
    return false;
  }
  // epv
  if (lhs->epv != rhs->epv) {
    return false;
  }
  return true;
}

bool
drone_interfaces__msg__NavigationState__copy(
  const drone_interfaces__msg__NavigationState * input,
  drone_interfaces__msg__NavigationState * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // child_frame_id
  if (!rosidl_runtime_c__String__copy(
      &(input->child_frame_id), &(output->child_frame_id)))
  {
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // twist
  if (!geometry_msgs__msg__Twist__copy(
      &(input->twist), &(output->twist)))
  {
    return false;
  }
  // acceleration
  if (!geometry_msgs__msg__Vector3__copy(
      &(input->acceleration), &(output->acceleration)))
  {
    return false;
  }
  // valid
  output->valid = input->valid;
  // reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reason), &(output->reason)))
  {
    return false;
  }
  // local_position_age
  output->local_position_age = input->local_position_age;
  // gps_age
  output->gps_age = input->gps_age;
  // estimator_flags_age
  output->estimator_flags_age = input->estimator_flags_age;
  // attitude_age
  output->attitude_age = input->attitude_age;
  // imu_age
  output->imu_age = input->imu_age;
  // gps_eph
  output->gps_eph = input->gps_eph;
  // gps_epv
  output->gps_epv = input->gps_epv;
  // gps_fix_type
  output->gps_fix_type = input->gps_fix_type;
  // gps_satellites_used
  output->gps_satellites_used = input->gps_satellites_used;
  // gnss_aided
  output->gnss_aided = input->gnss_aided;
  // ekf_gnss_fusion
  output->ekf_gnss_fusion = input->ekf_gnss_fusion;
  // eph
  output->eph = input->eph;
  // epv
  output->epv = input->epv;
  return true;
}

drone_interfaces__msg__NavigationState *
drone_interfaces__msg__NavigationState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__NavigationState * msg = (drone_interfaces__msg__NavigationState *)allocator.allocate(sizeof(drone_interfaces__msg__NavigationState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__msg__NavigationState));
  bool success = drone_interfaces__msg__NavigationState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__msg__NavigationState__destroy(drone_interfaces__msg__NavigationState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__msg__NavigationState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__msg__NavigationState__Sequence__init(drone_interfaces__msg__NavigationState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__NavigationState * data = NULL;

  if (size) {
    data = (drone_interfaces__msg__NavigationState *)allocator.zero_allocate(size, sizeof(drone_interfaces__msg__NavigationState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__msg__NavigationState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__msg__NavigationState__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_interfaces__msg__NavigationState__Sequence__fini(drone_interfaces__msg__NavigationState__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_interfaces__msg__NavigationState__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_interfaces__msg__NavigationState__Sequence *
drone_interfaces__msg__NavigationState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__NavigationState__Sequence * array = (drone_interfaces__msg__NavigationState__Sequence *)allocator.allocate(sizeof(drone_interfaces__msg__NavigationState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__msg__NavigationState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__msg__NavigationState__Sequence__destroy(drone_interfaces__msg__NavigationState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__msg__NavigationState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__msg__NavigationState__Sequence__are_equal(const drone_interfaces__msg__NavigationState__Sequence * lhs, const drone_interfaces__msg__NavigationState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__msg__NavigationState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__msg__NavigationState__Sequence__copy(
  const drone_interfaces__msg__NavigationState__Sequence * input,
  drone_interfaces__msg__NavigationState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__msg__NavigationState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__msg__NavigationState * data =
      (drone_interfaces__msg__NavigationState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__msg__NavigationState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__msg__NavigationState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__msg__NavigationState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
