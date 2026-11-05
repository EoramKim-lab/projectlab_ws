// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from drone_interfaces:msg/ObstacleCircles.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__STRUCT_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__STRUCT_HPP_

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
# define DEPRECATED__drone_interfaces__msg__ObstacleCircles __attribute__((deprecated))
#else
# define DEPRECATED__drone_interfaces__msg__ObstacleCircles __declspec(deprecated)
#endif

namespace drone_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObstacleCircles_
{
  using Type = ObstacleCircles_<ContainerAllocator>;

  explicit ObstacleCircles_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->over_capacity = false;
    }
  }

  explicit ObstacleCircles_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->over_capacity = false;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _xy_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _xy_type xy;
  using _radius_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _radius_type radius;
  using _safe_radius_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _safe_radius_type safe_radius;
  using _over_capacity_type =
    bool;
  _over_capacity_type over_capacity;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__xy(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->xy = _arg;
    return *this;
  }
  Type & set__radius(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->radius = _arg;
    return *this;
  }
  Type & set__safe_radius(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->safe_radius = _arg;
    return *this;
  }
  Type & set__over_capacity(
    const bool & _arg)
  {
    this->over_capacity = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    drone_interfaces::msg::ObstacleCircles_<ContainerAllocator> *;
  using ConstRawPtr =
    const drone_interfaces::msg::ObstacleCircles_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<drone_interfaces::msg::ObstacleCircles_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<drone_interfaces::msg::ObstacleCircles_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      drone_interfaces::msg::ObstacleCircles_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<drone_interfaces::msg::ObstacleCircles_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      drone_interfaces::msg::ObstacleCircles_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<drone_interfaces::msg::ObstacleCircles_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<drone_interfaces::msg::ObstacleCircles_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<drone_interfaces::msg::ObstacleCircles_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__drone_interfaces__msg__ObstacleCircles
    std::shared_ptr<drone_interfaces::msg::ObstacleCircles_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__drone_interfaces__msg__ObstacleCircles
    std::shared_ptr<drone_interfaces::msg::ObstacleCircles_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObstacleCircles_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->xy != other.xy) {
      return false;
    }
    if (this->radius != other.radius) {
      return false;
    }
    if (this->safe_radius != other.safe_radius) {
      return false;
    }
    if (this->over_capacity != other.over_capacity) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObstacleCircles_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObstacleCircles_

// alias to use template instance with default allocator
using ObstacleCircles =
  drone_interfaces::msg::ObstacleCircles_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__STRUCT_HPP_
