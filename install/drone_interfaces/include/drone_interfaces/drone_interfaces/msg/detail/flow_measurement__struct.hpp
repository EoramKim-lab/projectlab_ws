// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from drone_interfaces:msg/FlowMeasurement.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__STRUCT_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__drone_interfaces__msg__FlowMeasurement __attribute__((deprecated))
#else
# define DEPRECATED__drone_interfaces__msg__FlowMeasurement __declspec(deprecated)
#endif

namespace drone_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct FlowMeasurement_
{
  using Type = FlowMeasurement_<ContainerAllocator>;

  explicit FlowMeasurement_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->px4_timestamp_sample = 0ull;
      std::fill<typename std::array<double, 2>::iterator, double>(this->pixel_flow.begin(), this->pixel_flow.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->delta_angle.begin(), this->delta_angle.end(), 0.0);
      this->integration_dt = 0.0;
      this->distance_m = 0.0;
      this->quality = 0;
      this->valid = false;
    }
  }

  explicit FlowMeasurement_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    pixel_flow(_alloc),
    delta_angle(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->px4_timestamp_sample = 0ull;
      std::fill<typename std::array<double, 2>::iterator, double>(this->pixel_flow.begin(), this->pixel_flow.end(), 0.0);
      std::fill<typename std::array<double, 3>::iterator, double>(this->delta_angle.begin(), this->delta_angle.end(), 0.0);
      this->integration_dt = 0.0;
      this->distance_m = 0.0;
      this->quality = 0;
      this->valid = false;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _px4_timestamp_sample_type =
    uint64_t;
  _px4_timestamp_sample_type px4_timestamp_sample;
  using _pixel_flow_type =
    std::array<double, 2>;
  _pixel_flow_type pixel_flow;
  using _delta_angle_type =
    std::array<double, 3>;
  _delta_angle_type delta_angle;
  using _integration_dt_type =
    double;
  _integration_dt_type integration_dt;
  using _distance_m_type =
    double;
  _distance_m_type distance_m;
  using _quality_type =
    uint8_t;
  _quality_type quality;
  using _valid_type =
    bool;
  _valid_type valid;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__px4_timestamp_sample(
    const uint64_t & _arg)
  {
    this->px4_timestamp_sample = _arg;
    return *this;
  }
  Type & set__pixel_flow(
    const std::array<double, 2> & _arg)
  {
    this->pixel_flow = _arg;
    return *this;
  }
  Type & set__delta_angle(
    const std::array<double, 3> & _arg)
  {
    this->delta_angle = _arg;
    return *this;
  }
  Type & set__integration_dt(
    const double & _arg)
  {
    this->integration_dt = _arg;
    return *this;
  }
  Type & set__distance_m(
    const double & _arg)
  {
    this->distance_m = _arg;
    return *this;
  }
  Type & set__quality(
    const uint8_t & _arg)
  {
    this->quality = _arg;
    return *this;
  }
  Type & set__valid(
    const bool & _arg)
  {
    this->valid = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    drone_interfaces::msg::FlowMeasurement_<ContainerAllocator> *;
  using ConstRawPtr =
    const drone_interfaces::msg::FlowMeasurement_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<drone_interfaces::msg::FlowMeasurement_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<drone_interfaces::msg::FlowMeasurement_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      drone_interfaces::msg::FlowMeasurement_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<drone_interfaces::msg::FlowMeasurement_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      drone_interfaces::msg::FlowMeasurement_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<drone_interfaces::msg::FlowMeasurement_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<drone_interfaces::msg::FlowMeasurement_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<drone_interfaces::msg::FlowMeasurement_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__drone_interfaces__msg__FlowMeasurement
    std::shared_ptr<drone_interfaces::msg::FlowMeasurement_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__drone_interfaces__msg__FlowMeasurement
    std::shared_ptr<drone_interfaces::msg::FlowMeasurement_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FlowMeasurement_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->px4_timestamp_sample != other.px4_timestamp_sample) {
      return false;
    }
    if (this->pixel_flow != other.pixel_flow) {
      return false;
    }
    if (this->delta_angle != other.delta_angle) {
      return false;
    }
    if (this->integration_dt != other.integration_dt) {
      return false;
    }
    if (this->distance_m != other.distance_m) {
      return false;
    }
    if (this->quality != other.quality) {
      return false;
    }
    if (this->valid != other.valid) {
      return false;
    }
    return true;
  }
  bool operator!=(const FlowMeasurement_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FlowMeasurement_

// alias to use template instance with default allocator
using FlowMeasurement =
  drone_interfaces::msg::FlowMeasurement_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__STRUCT_HPP_
