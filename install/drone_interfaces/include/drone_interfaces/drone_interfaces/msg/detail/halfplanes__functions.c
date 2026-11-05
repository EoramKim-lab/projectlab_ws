// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from drone_interfaces:msg/Halfplanes.idl
// generated code does not contain a copyright notice
#include "drone_interfaces/msg/detail/halfplanes__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"
// Member `a`
// Member `b`
// Member `sector_ids`
// Member `nearest_range`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
drone_interfaces__msg__Halfplanes__init(drone_interfaces__msg__Halfplanes * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    drone_interfaces__msg__Halfplanes__fini(msg);
    return false;
  }
  // valid
  // reason
  if (!rosidl_runtime_c__String__init(&msg->reason)) {
    drone_interfaces__msg__Halfplanes__fini(msg);
    return false;
  }
  // origin_feasible
  // a
  if (!rosidl_runtime_c__double__Sequence__init(&msg->a, 0)) {
    drone_interfaces__msg__Halfplanes__fini(msg);
    return false;
  }
  // b
  if (!rosidl_runtime_c__double__Sequence__init(&msg->b, 0)) {
    drone_interfaces__msg__Halfplanes__fini(msg);
    return false;
  }
  // sector_ids
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->sector_ids, 0)) {
    drone_interfaces__msg__Halfplanes__fini(msg);
    return false;
  }
  // nearest_range
  if (!rosidl_runtime_c__double__Sequence__init(&msg->nearest_range, 0)) {
    drone_interfaces__msg__Halfplanes__fini(msg);
    return false;
  }
  return true;
}

void
drone_interfaces__msg__Halfplanes__fini(drone_interfaces__msg__Halfplanes * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // valid
  // reason
  rosidl_runtime_c__String__fini(&msg->reason);
  // origin_feasible
  // a
  rosidl_runtime_c__double__Sequence__fini(&msg->a);
  // b
  rosidl_runtime_c__double__Sequence__fini(&msg->b);
  // sector_ids
  rosidl_runtime_c__int32__Sequence__fini(&msg->sector_ids);
  // nearest_range
  rosidl_runtime_c__double__Sequence__fini(&msg->nearest_range);
}

bool
drone_interfaces__msg__Halfplanes__are_equal(const drone_interfaces__msg__Halfplanes * lhs, const drone_interfaces__msg__Halfplanes * rhs)
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
  // origin_feasible
  if (lhs->origin_feasible != rhs->origin_feasible) {
    return false;
  }
  // a
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->a), &(rhs->a)))
  {
    return false;
  }
  // b
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->b), &(rhs->b)))
  {
    return false;
  }
  // sector_ids
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->sector_ids), &(rhs->sector_ids)))
  {
    return false;
  }
  // nearest_range
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->nearest_range), &(rhs->nearest_range)))
  {
    return false;
  }
  return true;
}

bool
drone_interfaces__msg__Halfplanes__copy(
  const drone_interfaces__msg__Halfplanes * input,
  drone_interfaces__msg__Halfplanes * output)
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
  // valid
  output->valid = input->valid;
  // reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reason), &(output->reason)))
  {
    return false;
  }
  // origin_feasible
  output->origin_feasible = input->origin_feasible;
  // a
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->a), &(output->a)))
  {
    return false;
  }
  // b
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->b), &(output->b)))
  {
    return false;
  }
  // sector_ids
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->sector_ids), &(output->sector_ids)))
  {
    return false;
  }
  // nearest_range
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->nearest_range), &(output->nearest_range)))
  {
    return false;
  }
  return true;
}

drone_interfaces__msg__Halfplanes *
drone_interfaces__msg__Halfplanes__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__Halfplanes * msg = (drone_interfaces__msg__Halfplanes *)allocator.allocate(sizeof(drone_interfaces__msg__Halfplanes), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__msg__Halfplanes));
  bool success = drone_interfaces__msg__Halfplanes__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__msg__Halfplanes__destroy(drone_interfaces__msg__Halfplanes * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__msg__Halfplanes__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__msg__Halfplanes__Sequence__init(drone_interfaces__msg__Halfplanes__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__Halfplanes * data = NULL;

  if (size) {
    data = (drone_interfaces__msg__Halfplanes *)allocator.zero_allocate(size, sizeof(drone_interfaces__msg__Halfplanes), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__msg__Halfplanes__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__msg__Halfplanes__fini(&data[i - 1]);
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
drone_interfaces__msg__Halfplanes__Sequence__fini(drone_interfaces__msg__Halfplanes__Sequence * array)
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
      drone_interfaces__msg__Halfplanes__fini(&array->data[i]);
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

drone_interfaces__msg__Halfplanes__Sequence *
drone_interfaces__msg__Halfplanes__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__Halfplanes__Sequence * array = (drone_interfaces__msg__Halfplanes__Sequence *)allocator.allocate(sizeof(drone_interfaces__msg__Halfplanes__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__msg__Halfplanes__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__msg__Halfplanes__Sequence__destroy(drone_interfaces__msg__Halfplanes__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__msg__Halfplanes__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__msg__Halfplanes__Sequence__are_equal(const drone_interfaces__msg__Halfplanes__Sequence * lhs, const drone_interfaces__msg__Halfplanes__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__msg__Halfplanes__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__msg__Halfplanes__Sequence__copy(
  const drone_interfaces__msg__Halfplanes__Sequence * input,
  drone_interfaces__msg__Halfplanes__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__msg__Halfplanes);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__msg__Halfplanes * data =
      (drone_interfaces__msg__Halfplanes *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__msg__Halfplanes__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__msg__Halfplanes__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__msg__Halfplanes__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
