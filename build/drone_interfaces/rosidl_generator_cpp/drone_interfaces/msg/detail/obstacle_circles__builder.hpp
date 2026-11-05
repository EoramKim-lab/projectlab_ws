// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from drone_interfaces:msg/ObstacleCircles.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__BUILDER_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "drone_interfaces/msg/detail/obstacle_circles__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace drone_interfaces
{

namespace msg
{

namespace builder
{

class Init_ObstacleCircles_over_capacity
{
public:
  explicit Init_ObstacleCircles_over_capacity(::drone_interfaces::msg::ObstacleCircles & msg)
  : msg_(msg)
  {}
  ::drone_interfaces::msg::ObstacleCircles over_capacity(::drone_interfaces::msg::ObstacleCircles::_over_capacity_type arg)
  {
    msg_.over_capacity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_interfaces::msg::ObstacleCircles msg_;
};

class Init_ObstacleCircles_safe_radius
{
public:
  explicit Init_ObstacleCircles_safe_radius(::drone_interfaces::msg::ObstacleCircles & msg)
  : msg_(msg)
  {}
  Init_ObstacleCircles_over_capacity safe_radius(::drone_interfaces::msg::ObstacleCircles::_safe_radius_type arg)
  {
    msg_.safe_radius = std::move(arg);
    return Init_ObstacleCircles_over_capacity(msg_);
  }

private:
  ::drone_interfaces::msg::ObstacleCircles msg_;
};

class Init_ObstacleCircles_radius
{
public:
  explicit Init_ObstacleCircles_radius(::drone_interfaces::msg::ObstacleCircles & msg)
  : msg_(msg)
  {}
  Init_ObstacleCircles_safe_radius radius(::drone_interfaces::msg::ObstacleCircles::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return Init_ObstacleCircles_safe_radius(msg_);
  }

private:
  ::drone_interfaces::msg::ObstacleCircles msg_;
};

class Init_ObstacleCircles_xy
{
public:
  explicit Init_ObstacleCircles_xy(::drone_interfaces::msg::ObstacleCircles & msg)
  : msg_(msg)
  {}
  Init_ObstacleCircles_radius xy(::drone_interfaces::msg::ObstacleCircles::_xy_type arg)
  {
    msg_.xy = std::move(arg);
    return Init_ObstacleCircles_radius(msg_);
  }

private:
  ::drone_interfaces::msg::ObstacleCircles msg_;
};

class Init_ObstacleCircles_header
{
public:
  Init_ObstacleCircles_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObstacleCircles_xy header(::drone_interfaces::msg::ObstacleCircles::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ObstacleCircles_xy(msg_);
  }

private:
  ::drone_interfaces::msg::ObstacleCircles msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_interfaces::msg::ObstacleCircles>()
{
  return drone_interfaces::msg::builder::Init_ObstacleCircles_header();
}

}  // namespace drone_interfaces

#endif  // DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__BUILDER_HPP_
