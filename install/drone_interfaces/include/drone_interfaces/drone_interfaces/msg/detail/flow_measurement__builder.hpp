// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from drone_interfaces:msg/FlowMeasurement.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__BUILDER_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "drone_interfaces/msg/detail/flow_measurement__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace drone_interfaces
{

namespace msg
{

namespace builder
{

class Init_FlowMeasurement_valid
{
public:
  explicit Init_FlowMeasurement_valid(::drone_interfaces::msg::FlowMeasurement & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::msg::FlowMeasurement valid(::drone_interfaces::msg::FlowMeasurement::_valid_type arg)
  {
    msg_.valid = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::msg::FlowMeasurement msg_;
};

class Init_FlowMeasurement_quality
{
public:
  explicit Init_FlowMeasurement_quality(::drone_interfaces::msg::FlowMeasurement & msg)
  : msg_(msg)
  {}
  Init_FlowMeasurement_valid quality(::drone_interfaces::msg::FlowMeasurement::_quality_type arg)
  {
    msg_.quality = std::move(arg);
    return Init_FlowMeasurement_valid(msg_);
  }

private:
  ::drone_interfaces::msg::FlowMeasurement msg_;
};

class Init_FlowMeasurement_distance_m
{
public:
  explicit Init_FlowMeasurement_distance_m(::drone_interfaces::msg::FlowMeasurement & msg)
  : msg_(msg)
  {}
  Init_FlowMeasurement_quality distance_m(::drone_interfaces::msg::FlowMeasurement::_distance_m_type arg)
  {
    msg_.distance_m = std::move(arg);
    return Init_FlowMeasurement_quality(msg_);
  }

private:
  ::drone_interfaces::msg::FlowMeasurement msg_;
};

class Init_FlowMeasurement_integration_dt
{
public:
  explicit Init_FlowMeasurement_integration_dt(::drone_interfaces::msg::FlowMeasurement & msg)
  : msg_(msg)
  {}
  Init_FlowMeasurement_distance_m integration_dt(::drone_interfaces::msg::FlowMeasurement::_integration_dt_type arg)
  {
    msg_.integration_dt = std::move(arg);
    return Init_FlowMeasurement_distance_m(msg_);
  }

private:
  ::drone_interfaces::msg::FlowMeasurement msg_;
};

class Init_FlowMeasurement_delta_angle
{
public:
  explicit Init_FlowMeasurement_delta_angle(::drone_interfaces::msg::FlowMeasurement & msg)
  : msg_(msg)
  {}
  Init_FlowMeasurement_integration_dt delta_angle(::drone_interfaces::msg::FlowMeasurement::_delta_angle_type arg)
  {
    msg_.delta_angle = std::move(arg);
    return Init_FlowMeasurement_integration_dt(msg_);
  }

private:
  ::drone_interfaces::msg::FlowMeasurement msg_;
};

class Init_FlowMeasurement_pixel_flow
{
public:
  explicit Init_FlowMeasurement_pixel_flow(::drone_interfaces::msg::FlowMeasurement & msg)
  : msg_(msg)
  {}
  Init_FlowMeasurement_delta_angle pixel_flow(::drone_interfaces::msg::FlowMeasurement::_pixel_flow_type arg)
  {
    msg_.pixel_flow = std::move(arg);
    return Init_FlowMeasurement_delta_angle(msg_);
  }

private:
  ::drone_interfaces::msg::FlowMeasurement msg_;
};

class Init_FlowMeasurement_px4_timestamp_sample
{
public:
  explicit Init_FlowMeasurement_px4_timestamp_sample(::drone_interfaces::msg::FlowMeasurement & msg)
  : msg_(msg)
  {}
  Init_FlowMeasurement_pixel_flow px4_timestamp_sample(::drone_interfaces::msg::FlowMeasurement::_px4_timestamp_sample_type arg)
  {
    msg_.px4_timestamp_sample = std::move(arg);
    return Init_FlowMeasurement_pixel_flow(msg_);
  }

private:
  ::drone_interfaces::msg::FlowMeasurement msg_;
};

class Init_FlowMeasurement_header
{
public:
  Init_FlowMeasurement_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FlowMeasurement_px4_timestamp_sample header(::drone_interfaces::msg::FlowMeasurement::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_FlowMeasurement_px4_timestamp_sample(msg_);
  }

private:
  ::drone_interfaces::msg::FlowMeasurement msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::msg::FlowMeasurement>()
{
  return drone_interfaces::msg::builder::Init_FlowMeasurement_header();
}

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__BUILDER_HPP_
