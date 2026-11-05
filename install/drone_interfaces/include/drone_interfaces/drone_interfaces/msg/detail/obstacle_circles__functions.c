// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from drone_interfaces:msg/ObstacleCircles.idl
// generated code does not contain a copyright notice
#include "drone_interfaces/msg/detail/obstacle_circles__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `xy`
// Member `radius`
// Member `safe_radius`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
drone_interfaces__msg__ObstacleCircles__init(drone_interfaces__msg__ObstacleCircles * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    drone_interfaces__msg__ObstacleCircles__fini(msg);
    return false;
  }
  // xy
  if (!rosidl_runtime_c__double__Sequence__init(&msg->xy, 0)) {
    drone_interfaces__msg__ObstacleCircles__fini(msg);
    return false;
  }
  // radius
  if (!rosidl_runtime_c__double__Sequence__init(&msg->radius, 0)) {
    drone_interfaces__msg__ObstacleCircles__fini(msg);
    return false;
  }
  // safe_radius
  if (!rosidl_runtime_c__double__Sequence__init(&msg->safe_radius, 0)) {
    drone_interfaces__msg__ObstacleCircles__fini(msg);
    return false;
  }
  // over_capacity
  return true;
}

void
drone_interfaces__msg__ObstacleCircles__fini(drone_interfaces__msg__ObstacleCircles * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // xy
  rosidl_runtime_c__double__Sequence__fini(&msg->xy);
  // radius
  rosidl_runtime_c__double__Sequence__fini(&msg->radius);
  // safe_radius
  rosidl_runtime_c__double__Sequence__fini(&msg->safe_radius);
  // over_capacity
}

bool
drone_interfaces__msg__ObstacleCircles__are_equal(const drone_interfaces__msg__ObstacleCircles * lhs, const drone_interfaces__msg__ObstacleCircles * rhs)
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
  // xy
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->xy), &(rhs->xy)))
  {
    return false;
  }
  // radius
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->radius), &(rhs->radius)))
  {
    return false;
  }
  // safe_radius
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->safe_radius), &(rhs->safe_radius)))
  {
    return false;
  }
  // over_capacity
  if (lhs->over_capacity != rhs->over_capacity) {
    return false;
  }
  return true;
}

bool
drone_interfaces__msg__ObstacleCircles__copy(
  const drone_interfaces__msg__ObstacleCircles * input,
  drone_interfaces__msg__ObstacleCircles * output)
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
  // xy
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->xy), &(output->xy)))
  {
    return false;
  }
  // radius
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->radius), &(output->radius)))
  {
    return false;
  }
  // safe_radius
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->safe_radius), &(output->safe_radius)))
  {
    return false;
  }
  // over_capacity
  output->over_capacity = input->over_capacity;
  return true;
}

drone_interfaces__msg__ObstacleCircles *
drone_interfaces__msg__ObstacleCircles__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__ObstacleCircles * msg = (drone_interfaces__msg__ObstacleCircles *)allocator.allocate(sizeof(drone_interfaces__msg__ObstacleCircles), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__msg__ObstacleCircles));
  bool success = drone_interfaces__msg__ObstacleCircles__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__msg__ObstacleCircles__destroy(drone_interfaces__msg__ObstacleCircles * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__msg__ObstacleCircles__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__msg__ObstacleCircles__Sequence__init(drone_interfaces__msg__ObstacleCircles__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__ObstacleCircles * data = NULL;

  if (size) {
    data = (drone_interfaces__msg__ObstacleCircles *)allocator.zero_allocate(size, sizeof(drone_interfaces__msg__ObstacleCircles), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__msg__ObstacleCircles__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__msg__ObstacleCircles__fini(&data[i - 1]);
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
drone_interfaces__msg__ObstacleCircles__Sequence__fini(drone_interfaces__msg__ObstacleCircles__Sequence * array)
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
      drone_interfaces__msg__ObstacleCircles__fini(&array->data[i]);
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

drone_interfaces__msg__ObstacleCircles__Sequence *
drone_interfaces__msg__ObstacleCircles__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__ObstacleCircles__Sequence * array = (drone_interfaces__msg__ObstacleCircles__Sequence *)allocator.allocate(sizeof(drone_interfaces__msg__ObstacleCircles__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__msg__ObstacleCircles__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__msg__ObstacleCircles__Sequence__destroy(drone_interfaces__msg__ObstacleCircles__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__msg__ObstacleCircles__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__msg__ObstacleCircles__Sequence__are_equal(const drone_interfaces__msg__ObstacleCircles__Sequence * lhs, const drone_interfaces__msg__ObstacleCircles__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__msg__ObstacleCircles__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__msg__ObstacleCircles__Sequence__copy(
  const drone_interfaces__msg__ObstacleCircles__Sequence * input,
  drone_interfaces__msg__ObstacleCircles__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__msg__ObstacleCircles);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__msg__ObstacleCircles * data =
      (drone_interfaces__msg__ObstacleCircles *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__msg__ObstacleCircles__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__msg__ObstacleCircles__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__msg__ObstacleCircles__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
