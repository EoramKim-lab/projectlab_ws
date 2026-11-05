// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from drone_interfaces:msg/Halfplanes.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__BUILDER_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "drone_interfaces/msg/detail/halfplanes__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace drone_interfaces
{

namespace msg
{

namespace builder
{

class Init_Halfplanes_nearest_range
{
public:
  explicit Init_Halfplanes_nearest_range(::drone_interfaces::msg::Halfplanes & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::msg::Halfplanes nearest_range(::drone_interfaces::msg::Halfplanes::_nearest_range_type arg)
  {
    msg_.nearest_range = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::msg::Halfplanes msg_;
};

class Init_Halfplanes_sector_ids
{
public:
  explicit Init_Halfplanes_sector_ids(::drone_interfaces::msg::Halfplanes & msg)
  : msg_(msg)
  {}
  Init_Halfplanes_nearest_range sector_ids(::drone_interfaces::msg::Halfplanes::_sector_ids_type arg)
  {
    msg_.sector_ids = std::move(arg);
    return Init_Halfplanes_nearest_range(msg_);
  }

private:
  ::drone_interfaces::msg::Halfplanes msg_;
};

class Init_Halfplanes_b
{
public:
  explicit Init_Halfplanes_b(::drone_interfaces::msg::Halfplanes & msg)
  : msg_(msg)
  {}
  Init_Halfplanes_sector_ids b(::drone_interfaces::msg::Halfplanes::_b_type arg)
  {
    msg_.b = std::move(arg);
    return Init_Halfplanes_sector_ids(msg_);
  }

private:
  ::drone_interfaces::msg::Halfplanes msg_;
};

class Init_Halfplanes_a
{
public:
  explicit Init_Halfplanes_a(::drone_interfaces::msg::Halfplanes & msg)
  : msg_(msg)
  {}
  Init_Halfplanes_b a(::drone_interfaces::msg::Halfplanes::_a_type arg)
  {
    msg_.a = std::move(arg);
    return Init_Halfplanes_b(msg_);
  }

private:
  ::drone_interfaces::msg::Halfplanes msg_;
};

class Init_Halfplanes_origin_feasible
{
public:
  explicit Init_Halfplanes_origin_feasible(::drone_interfaces::msg::Halfplanes & msg)
  : msg_(msg)
  {}
  Init_Halfplanes_a origin_feasible(::drone_interfaces::msg::Halfplanes::_origin_feasible_type arg)
  {
    msg_.origin_feasible = std::move(arg);
    return Init_Halfplanes_a(msg_);
  }

private:
  ::drone_interfaces::msg::Halfplanes msg_;
};

class Init_Halfplanes_reason
{
public:
  explicit Init_Halfplanes_reason(::drone_interfaces::msg::Halfplanes & msg)
  : msg_(msg)
  {}
  Init_Halfplanes_origin_feasible reason(::drone_interfaces::msg::Halfplanes::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_Halfplanes_origin_feasible(msg_);
  }

private:
  ::drone_interfaces::msg::Halfplanes msg_;
};

class Init_Halfplanes_valid
{
public:
  explicit Init_Halfplanes_valid(::drone_interfaces::msg::Halfplanes & msg)
  : msg_(msg)
  {}
  Init_Halfplanes_reason valid(::drone_interfaces::msg::Halfplanes::_valid_type arg)
  {
    msg_.valid = std::move(arg);
    return Init_Halfplanes_reason(msg_);
  }

private:
  ::drone_interfaces::msg::Halfplanes msg_;
};

class Init_Halfplanes_header
{
public:
  Init_Halfplanes_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Halfplanes_valid header(::drone_interfaces::msg::Halfplanes::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Halfplanes_valid(msg_);
  }

private:
  ::drone_interfaces::msg::Halfplanes msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::msg::Halfplanes>()
{
  return drone_interfaces::msg::builder::Init_Halfplanes_header();
}

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__BUILDER_HPP_
