// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from drone_interfaces:msg/NavigationState.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__STRUCT_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__STRUCT_HPP_

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
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"
// Member 'twist'
#include "geometry_msgs/msg/detail/twist__struct.hpp"
// Member 'acceleration'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__drone_interfaces__msg__NavigationState __attribute__((deprecated))
#else
# define DEPRECATED__drone_interfaces__msg__NavigationState __declspec(deprecated)
#endif

namespace drone_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct NavigationState_
{
  using Type = NavigationState_<ContainerAllocator>;

  explicit NavigationState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    pose(_init),
    twist(_init),
    acceleration(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->child_frame_id = "";
      this->valid = false;
      this->reason = "";
      this->local_position_age = 0.0;
      this->gps_age = 0.0;
      this->estimator_flags_age = 0.0;
      this->attitude_age = 0.0;
      this->imu_age = 0.0;
      this->gps_eph = 0.0;
      this->gps_epv = 0.0;
      this->gps_fix_type = 0;
      this->gps_satellites_used = 0;
      this->gnss_aided = false;
      this->ekf_gnss_fusion = false;
      this->eph = 0.0;
      this->epv = 0.0;
    }
  }

  explicit NavigationState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    child_frame_id(_alloc),
    pose(_alloc, _init),
    twist(_alloc, _init),
    acceleration(_alloc, _init),
    reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->child_frame_id = "";
      this->valid = false;
      this->reason = "";
      this->local_position_age = 0.0;
      this->gps_age = 0.0;
      this->estimator_flags_age = 0.0;
      this->attitude_age = 0.0;
      this->imu_age = 0.0;
      this->gps_eph = 0.0;
      this->gps_epv = 0.0;
      this->gps_fix_type = 0;
      this->gps_satellites_used = 0;
      this->gnss_aided = false;
      this->ekf_gnss_fusion = false;
      this->eph = 0.0;
      this->epv = 0.0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _child_frame_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _child_frame_id_type child_frame_id;
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _twist_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _twist_type twist;
  using _acceleration_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _acceleration_type acceleration;
  using _valid_type =
    bool;
  _valid_type valid;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;
  using _local_position_age_type =
    double;
  _local_position_age_type local_position_age;
  using _gps_age_type =
    double;
  _gps_age_type gps_age;
  using _estimator_flags_age_type =
    double;
  _estimator_flags_age_type estimator_flags_age;
  using _attitude_age_type =
    double;
  _attitude_age_type attitude_age;
  using _imu_age_type =
    double;
  _imu_age_type imu_age;
  using _gps_eph_type =
    double;
  _gps_eph_type gps_eph;
  using _gps_epv_type =
    double;
  _gps_epv_type gps_epv;
  using _gps_fix_type_type =
    uint8_t;
  _gps_fix_type_type gps_fix_type;
  using _gps_satellites_used_type =
    uint8_t;
  _gps_satellites_used_type gps_satellites_used;
  using _gnss_aided_type =
    bool;
  _gnss_aided_type gnss_aided;
  using _ekf_gnss_fusion_type =
    bool;
  _ekf_gnss_fusion_type ekf_gnss_fusion;
  using _eph_type =
    double;
  _eph_type eph;
  using _epv_type =
    double;
  _epv_type epv;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__child_frame_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->child_frame_id = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__twist(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->twist = _arg;
    return *this;
  }
  Type & set__acceleration(
    const geometry_msgs::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->acceleration = _arg;
    return *this;
  }
  Type & set__valid(
    const bool & _arg)
  {
    this->valid = _arg;
    return *this;
  }
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }
  Type & set__local_position_age(
    const double & _arg)
  {
    this->local_position_age = _arg;
    return *this;
  }
  Type & set__gps_age(
    const double & _arg)
  {
    this->gps_age = _arg;
    return *this;
  }
  Type & set__estimator_flags_age(
    const double & _arg)
  {
    this->estimator_flags_age = _arg;
    return *this;
  }
  Type & set__attitude_age(
    const double & _arg)
  {
    this->attitude_age = _arg;
    return *this;
  }
  Type & set__imu_age(
    const double & _arg)
  {
    this->imu_age = _arg;
    return *this;
  }
  Type & set__gps_eph(
    const double & _arg)
  {
    this->gps_eph = _arg;
    return *this;
  }
  Type & set__gps_epv(
    const double & _arg)
  {
    this->gps_epv = _arg;
    return *this;
  }
  Type & set__gps_fix_type(
    const uint8_t & _arg)
  {
    this->gps_fix_type = _arg;
    return *this;
  }
  Type & set__gps_satellites_used(
    const uint8_t & _arg)
  {
    this->gps_satellites_used = _arg;
    return *this;
  }
  Type & set__gnss_aided(
    const bool & _arg)
  {
    this->gnss_aided = _arg;
    return *this;
  }
  Type & set__ekf_gnss_fusion(
    const bool & _arg)
  {
    this->ekf_gnss_fusion = _arg;
    return *this;
  }
  Type & set__eph(
    const double & _arg)
  {
    this->eph = _arg;
    return *this;
  }
  Type & set__epv(
    const double & _arg)
  {
    this->epv = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    drone_interfaces::msg::NavigationState_<ContainerAllocator> *;
  using ConstRawPtr =
    const drone_interfaces::msg::NavigationState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<drone_interfaces::msg::NavigationState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<drone_interfaces::msg::NavigationState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      drone_interfaces::msg::NavigationState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<drone_interfaces::msg::NavigationState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      drone_interfaces::msg::NavigationState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<drone_interfaces::msg::NavigationState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<drone_interfaces::msg::NavigationState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<drone_interfaces::msg::NavigationState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__drone_interfaces__msg__NavigationState
    std::shared_ptr<drone_interfaces::msg::NavigationState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__drone_interfaces__msg__NavigationState
    std::shared_ptr<drone_interfaces::msg::NavigationState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const NavigationState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->child_frame_id != other.child_frame_id) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    if (this->twist != other.twist) {
      return false;
    }
    if (this->acceleration != other.acceleration) {
      return false;
    }
    if (this->valid != other.valid) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    if (this->local_position_age != other.local_position_age) {
      return false;
    }
    if (this->gps_age != other.gps_age) {
      return false;
    }
    if (this->estimator_flags_age != other.estimator_flags_age) {
      return false;
    }
    if (this->attitude_age != other.attitude_age) {
      return false;
    }
    if (this->imu_age != other.imu_age) {
      return false;
    }
    if (this->gps_eph != other.gps_eph) {
      return false;
    }
    if (this->gps_epv != other.gps_epv) {
      return false;
    }
    if (this->gps_fix_type != other.gps_fix_type) {
      return false;
    }
    if (this->gps_satellites_used != other.gps_satellites_used) {
      return false;
    }
    if (this->gnss_aided != other.gnss_aided) {
      return false;
    }
    if (this->ekf_gnss_fusion != other.ekf_gnss_fusion) {
      return false;
    }
    if (this->eph != other.eph) {
      return false;
    }
    if (this->epv != other.epv) {
      return false;
    }
    return true;
  }
  bool operator!=(const NavigationState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct NavigationState_

// alias to use template instance with default allocator
using NavigationState =
  drone_interfaces::msg::NavigationState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__STRUCT_HPP_
