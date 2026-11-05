// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from drone_interfaces:msg/ObstacleCircles.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__TRAITS_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "drone_interfaces/msg/detail/obstacle_circles__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace drone_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObstacleCircles & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: xy
  {
    if (msg.xy.size() == 0) {
      out << "xy: []";
    } else {
      out << "xy: [";
      size_t pending_items = msg.xy.size();
      for (auto item : msg.xy) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: radius
  {
    if (msg.radius.size() == 0) {
      out << "radius: []";
    } else {
      out << "radius: [";
      size_t pending_items = msg.radius.size();
      for (auto item : msg.radius) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: safe_radius
  {
    if (msg.safe_radius.size() == 0) {
      out << "safe_radius: []";
    } else {
      out << "safe_radius: [";
      size_t pending_items = msg.safe_radius.size();
      for (auto item : msg.safe_radius) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: over_capacity
  {
    out << "over_capacity: ";
    rosidl_generator_traits::value_to_yaml(msg.over_capacity, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObstacleCircles & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: xy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.xy.size() == 0) {
      out << "xy: []\n";
    } else {
      out << "xy:\n";
      for (auto item : msg.xy) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: radius
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.radius.size() == 0) {
      out << "radius: []\n";
    } else {
      out << "radius:\n";
      for (auto item : msg.radius) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: safe_radius
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.safe_radius.size() == 0) {
      out << "safe_radius: []\n";
    } else {
      out << "safe_radius:\n";
      for (auto item : msg.safe_radius) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: over_capacity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "over_capacity: ";
    rosidl_generator_traits::value_to_yaml(msg.over_capacity, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObstacleCircles & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace drone_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use drone_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const drone_interfaces::msg::ObstacleCircles & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::msg::ObstacleCircles & msg)
{
  return drone_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::msg::ObstacleCircles>()
{
  return "drone_interfaces::msg::ObstacleCircles";
}

template<>
inline const char * name<drone_interfaces::msg::ObstacleCircles>()
{
  return "drone_interfaces/msg/ObstacleCircles";
}

template<>
struct has_fixed_size<drone_interfaces::msg::ObstacleCircles>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<drone_interfaces::msg::ObstacleCircles>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<drone_interfaces::msg::ObstacleCircles>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DRONE_INTERFACES__MSG__DETAIL__OBSTACLE_CIRCLES__TRAITS_HPP_
