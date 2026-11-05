// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from drone_interfaces:msg/FlowMeasurement.idl
// generated code does not contain a copyright notice
#include "drone_interfaces/msg/detail/flow_measurement__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
drone_interfaces__msg__FlowMeasurement__init(drone_interfaces__msg__FlowMeasurement * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    drone_interfaces__msg__FlowMeasurement__fini(msg);
    return false;
  }
  // px4_timestamp_sample
  // pixel_flow
  // delta_angle
  // integration_dt
  // distance_m
  // quality
  // valid
  return true;
}

void
drone_interfaces__msg__FlowMeasurement__fini(drone_interfaces__msg__FlowMeasurement * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // px4_timestamp_sample
  // pixel_flow
  // delta_angle
  // integration_dt
  // distance_m
  // quality
  // valid
}

bool
drone_interfaces__msg__FlowMeasurement__are_equal(const drone_interfaces__msg__FlowMeasurement * lhs, const drone_interfaces__msg__FlowMeasurement * rhs)
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
  // px4_timestamp_sample
  if (lhs->px4_timestamp_sample != rhs->px4_timestamp_sample) {
    return false;
  }
  // pixel_flow
  for (size_t i = 0; i < 2; ++i) {
    if (lhs->pixel_flow[i] != rhs->pixel_flow[i]) {
      return false;
    }
  }
  // delta_angle
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->delta_angle[i] != rhs->delta_angle[i]) {
      return false;
    }
  }
  // integration_dt
  if (lhs->integration_dt != rhs->integration_dt) {
    return false;
  }
  // distance_m
  if (lhs->distance_m != rhs->distance_m) {
    return false;
  }
  // quality
  if (lhs->quality != rhs->quality) {
    return false;
  }
  // valid
  if (lhs->valid != rhs->valid) {
    return false;
  }
  return true;
}

bool
drone_interfaces__msg__FlowMeasurement__copy(
  const drone_interfaces__msg__FlowMeasurement * input,
  drone_interfaces__msg__FlowMeasurement * output)
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
  // px4_timestamp_sample
  output->px4_timestamp_sample = input->px4_timestamp_sample;
  // pixel_flow
  for (size_t i = 0; i < 2; ++i) {
    output->pixel_flow[i] = input->pixel_flow[i];
  }
  // delta_angle
  for (size_t i = 0; i < 3; ++i) {
    output->delta_angle[i] = input->delta_angle[i];
  }
  // integration_dt
  output->integration_dt = input->integration_dt;
  // distance_m
  output->distance_m = input->distance_m;
  // quality
  output->quality = input->quality;
  // valid
  output->valid = input->valid;
  return true;
}

drone_interfaces__msg__FlowMeasurement *
drone_interfaces__msg__FlowMeasurement__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__FlowMeasurement * msg = (drone_interfaces__msg__FlowMeasurement *)allocator.allocate(sizeof(drone_interfaces__msg__FlowMeasurement), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_interfaces__msg__FlowMeasurement));
  bool success = drone_interfaces__msg__FlowMeasurement__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_interfaces__msg__FlowMeasurement__destroy(drone_interfaces__msg__FlowMeasurement * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_interfaces__msg__FlowMeasurement__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_interfaces__msg__FlowMeasurement__Sequence__init(drone_interfaces__msg__FlowMeasurement__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__FlowMeasurement * data = NULL;

  if (size) {
    data = (drone_interfaces__msg__FlowMeasurement *)allocator.zero_allocate(size, sizeof(drone_interfaces__msg__FlowMeasurement), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_interfaces__msg__FlowMeasurement__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_interfaces__msg__FlowMeasurement__fini(&data[i - 1]);
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
drone_interfaces__msg__FlowMeasurement__Sequence__fini(drone_interfaces__msg__FlowMeasurement__Sequence * array)
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
      drone_interfaces__msg__FlowMeasurement__fini(&array->data[i]);
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

drone_interfaces__msg__FlowMeasurement__Sequence *
drone_interfaces__msg__FlowMeasurement__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_interfaces__msg__FlowMeasurement__Sequence * array = (drone_interfaces__msg__FlowMeasurement__Sequence *)allocator.allocate(sizeof(drone_interfaces__msg__FlowMeasurement__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_interfaces__msg__FlowMeasurement__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_interfaces__msg__FlowMeasurement__Sequence__destroy(drone_interfaces__msg__FlowMeasurement__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_interfaces__msg__FlowMeasurement__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_interfaces__msg__FlowMeasurement__Sequence__are_equal(const drone_interfaces__msg__FlowMeasurement__Sequence * lhs, const drone_interfaces__msg__FlowMeasurement__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_interfaces__msg__FlowMeasurement__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_interfaces__msg__FlowMeasurement__Sequence__copy(
  const drone_interfaces__msg__FlowMeasurement__Sequence * input,
  drone_interfaces__msg__FlowMeasurement__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(drone_interfaces__msg__FlowMeasurement);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_interfaces__msg__FlowMeasurement * data =
      (drone_interfaces__msg__FlowMeasurement *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_interfaces__msg__FlowMeasurement__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_interfaces__msg__FlowMeasurement__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_interfaces__msg__FlowMeasurement__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
