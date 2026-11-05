// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from drone_interfaces:msg/NavigationState.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__BUILDER_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "drone_interfaces/msg/detail/navigation_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace drone_interfaces
{

namespace msg
{

namespace builder
{

class Init_NavigationState_epv
{
public:
  explicit Init_NavigationState_epv(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::msg::NavigationState epv(::drone_interfaces::msg::NavigationState::_epv_type arg)
  {
    msg_.epv = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_eph
{
public:
  explicit Init_NavigationState_eph(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_epv eph(::drone_interfaces::msg::NavigationState::_eph_type arg)
  {
    msg_.eph = std::move(arg);
    return Init_NavigationState_epv(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_ekf_gnss_fusion
{
public:
  explicit Init_NavigationState_ekf_gnss_fusion(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_eph ekf_gnss_fusion(::drone_interfaces::msg::NavigationState::_ekf_gnss_fusion_type arg)
  {
    msg_.ekf_gnss_fusion = std::move(arg);
    return Init_NavigationState_eph(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_gnss_aided
{
public:
  explicit Init_NavigationState_gnss_aided(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_ekf_gnss_fusion gnss_aided(::drone_interfaces::msg::NavigationState::_gnss_aided_type arg)
  {
    msg_.gnss_aided = std::move(arg);
    return Init_NavigationState_ekf_gnss_fusion(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_gps_satellites_used
{
public:
  explicit Init_NavigationState_gps_satellites_used(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_gnss_aided gps_satellites_used(::drone_interfaces::msg::NavigationState::_gps_satellites_used_type arg)
  {
    msg_.gps_satellites_used = std::move(arg);
    return Init_NavigationState_gnss_aided(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_gps_fix_type
{
public:
  explicit Init_NavigationState_gps_fix_type(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_gps_satellites_used gps_fix_type(::drone_interfaces::msg::NavigationState::_gps_fix_type_type arg)
  {
    msg_.gps_fix_type = std::move(arg);
    return Init_NavigationState_gps_satellites_used(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_gps_epv
{
public:
  explicit Init_NavigationState_gps_epv(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_gps_fix_type gps_epv(::drone_interfaces::msg::NavigationState::_gps_epv_type arg)
  {
    msg_.gps_epv = std::move(arg);
    return Init_NavigationState_gps_fix_type(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_gps_eph
{
public:
  explicit Init_NavigationState_gps_eph(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_gps_epv gps_eph(::drone_interfaces::msg::NavigationState::_gps_eph_type arg)
  {
    msg_.gps_eph = std::move(arg);
    return Init_NavigationState_gps_epv(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_imu_age
{
public:
  explicit Init_NavigationState_imu_age(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_gps_eph imu_age(::drone_interfaces::msg::NavigationState::_imu_age_type arg)
  {
    msg_.imu_age = std::move(arg);
    return Init_NavigationState_gps_eph(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_attitude_age
{
public:
  explicit Init_NavigationState_attitude_age(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_imu_age attitude_age(::drone_interfaces::msg::NavigationState::_attitude_age_type arg)
  {
    msg_.attitude_age = std::move(arg);
    return Init_NavigationState_imu_age(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_estimator_flags_age
{
public:
  explicit Init_NavigationState_estimator_flags_age(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_attitude_age estimator_flags_age(::drone_interfaces::msg::NavigationState::_estimator_flags_age_type arg)
  {
    msg_.estimator_flags_age = std::move(arg);
    return Init_NavigationState_attitude_age(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_gps_age
{
public:
  explicit Init_NavigationState_gps_age(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_estimator_flags_age gps_age(::drone_interfaces::msg::NavigationState::_gps_age_type arg)
  {
    msg_.gps_age = std::move(arg);
    return Init_NavigationState_estimator_flags_age(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_local_position_age
{
public:
  explicit Init_NavigationState_local_position_age(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_gps_age local_position_age(::drone_interfaces::msg::NavigationState::_local_position_age_type arg)
  {
    msg_.local_position_age = std::move(arg);
    return Init_NavigationState_gps_age(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_reason
{
public:
  explicit Init_NavigationState_reason(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_local_position_age reason(::drone_interfaces::msg::NavigationState::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_NavigationState_local_position_age(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_valid
{
public:
  explicit Init_NavigationState_valid(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_reason valid(::drone_interfaces::msg::NavigationState::_valid_type arg)
  {
    msg_.valid = std::move(arg);
    return Init_NavigationState_reason(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_acceleration
{
public:
  explicit Init_NavigationState_acceleration(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_valid acceleration(::drone_interfaces::msg::NavigationState::_acceleration_type arg)
  {
    msg_.acceleration = std::move(arg);
    return Init_NavigationState_valid(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_twist
{
public:
  explicit Init_NavigationState_twist(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_acceleration twist(::drone_interfaces::msg::NavigationState::_twist_type arg)
  {
    msg_.twist = std::move(arg);
    return Init_NavigationState_acceleration(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_pose
{
public:
  explicit Init_NavigationState_pose(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_twist pose(::drone_interfaces::msg::NavigationState::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_NavigationState_twist(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_child_frame_id
{
public:
  explicit Init_NavigationState_child_frame_id(::drone_interfaces::msg::NavigationState & msg)
  : msg_(msg)
  {}
  Init_NavigationState_pose child_frame_id(::drone_interfaces::msg::NavigationState::_child_frame_id_type arg)
  {
    msg_.child_frame_id = std::move(arg);
    return Init_NavigationState_pose(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

class Init_NavigationState_header
{
public:
  Init_NavigationState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_NavigationState_child_frame_id header(::drone_interfaces::msg::NavigationState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_NavigationState_child_frame_id(msg_);
  }

private:
  ::drone_interfaces::msg::NavigationState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::msg::NavigationState>()
{
  return drone_interfaces::msg::builder::Init_NavigationState_header();
}

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__BUILDER_HPP_
