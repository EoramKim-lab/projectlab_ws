// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from drone_interfaces:msg/ProcessedScan.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__PROCESSED_SCAN__BUILDER_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__PROCESSED_SCAN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "drone_interfaces/msg/detail/processed_scan__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace drone_interfaces
{

namespace msg
{

namespace builder
{

class Init_ProcessedScan_xy
{
public:
  explicit Init_ProcessedScan_xy(::drone_interfaces::msg::ProcessedScan & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::msg::ProcessedScan xy(::drone_interfaces::msg::ProcessedScan::_xy_type arg)
  {
    msg_.xy = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::msg::ProcessedScan msg_;
};

class Init_ProcessedScan_raw_count
{
public:
  explicit Init_ProcessedScan_raw_count(::drone_interfaces::msg::ProcessedScan & msg)
  : msg_(msg)
  {}
  Init_ProcessedScan_xy raw_count(::drone_interfaces::msg::ProcessedScan::_raw_count_type arg)
  {
    msg_.raw_count = std::move(arg);
    return Init_ProcessedScan_xy(msg_);
  }

private:
  ::drone_interfaces::msg::ProcessedScan msg_;
};

class Init_ProcessedScan_reason
{
public:
  explicit Init_ProcessedScan_reason(::drone_interfaces::msg::ProcessedScan & msg)
  : msg_(msg)
  {}
  Init_ProcessedScan_raw_count reason(::drone_interfaces::msg::ProcessedScan::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_ProcessedScan_raw_count(msg_);
  }

private:
  ::drone_interfaces::msg::ProcessedScan msg_;
};

class Init_ProcessedScan_valid
{
public:
  explicit Init_ProcessedScan_valid(::drone_interfaces::msg::ProcessedScan & msg)
  : msg_(msg)
  {}
  Init_ProcessedScan_reason valid(::drone_interfaces::msg::ProcessedScan::_valid_type arg)
  {
    msg_.valid = std::move(arg);
    return Init_ProcessedScan_reason(msg_);
  }

private:
  ::drone_interfaces::msg::ProcessedScan msg_;
};

class Init_ProcessedScan_header
{
public:
  Init_ProcessedScan_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ProcessedScan_valid header(::drone_interfaces::msg::ProcessedScan::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ProcessedScan_valid(msg_);
  }

private:
  ::drone_interfaces::msg::ProcessedScan msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::msg::ProcessedScan>()
{
  return drone_interfaces::msg::builder::Init_ProcessedScan_header();
}

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__MSG__DETAIL__PROCESSED_SCAN__BUILDER_HPP_
