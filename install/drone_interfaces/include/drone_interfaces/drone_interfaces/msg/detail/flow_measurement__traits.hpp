// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from drone_interfaces:msg/FlowMeasurement.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__TRAITS_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "drone_interfaces/msg/detail/flow_measurement__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace drone_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const FlowMeasurement & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: px4_timestamp_sample
  {
    out << "px4_timestamp_sample: ";
    rosidl_generator_traits::value_to_yaml(msg.px4_timestamp_sample, out);
    out << ", ";
  }

  // member: pixel_flow
  {
    if (msg.pixel_flow.size() == 0) {
      out << "pixel_flow: []";
    } else {
      out << "pixel_flow: [";
      size_t pending_items = msg.pixel_flow.size();
      for (auto item : msg.pixel_flow) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: delta_angle
  {
    if (msg.delta_angle.size() == 0) {
      out << "delta_angle: []";
    } else {
      out << "delta_angle: [";
      size_t pending_items = msg.delta_angle.size();
      for (auto item : msg.delta_angle) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: integration_dt
  {
    out << "integration_dt: ";
    rosidl_generator_traits::value_to_yaml(msg.integration_dt, out);
    out << ", ";
  }

  // member: distance_m
  {
    out << "distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_m, out);
    out << ", ";
  }

  // member: quality
  {
    out << "quality: ";
    rosidl_generator_traits::value_to_yaml(msg.quality, out);
    out << ", ";
  }

  // member: valid
  {
    out << "valid: ";
    rosidl_generator_traits::value_to_yaml(msg.valid, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FlowMeasurement & msg,
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

  // member: px4_timestamp_sample
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "px4_timestamp_sample: ";
    rosidl_generator_traits::value_to_yaml(msg.px4_timestamp_sample, out);
    out << "\n";
  }

  // member: pixel_flow
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.pixel_flow.size() == 0) {
      out << "pixel_flow: []\n";
    } else {
      out << "pixel_flow:\n";
      for (auto item : msg.pixel_flow) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: delta_angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.delta_angle.size() == 0) {
      out << "delta_angle: []\n";
    } else {
      out << "delta_angle:\n";
      for (auto item : msg.delta_angle) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: integration_dt
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "integration_dt: ";
    rosidl_generator_traits::value_to_yaml(msg.integration_dt, out);
    out << "\n";
  }

  // member: distance_m
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_m, out);
    out << "\n";
  }

  // member: quality
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "quality: ";
    rosidl_generator_traits::value_to_yaml(msg.quality, out);
    out << "\n";
  }

  // member: valid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "valid: ";
    rosidl_generator_traits::value_to_yaml(msg.valid, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FlowMeasurement & msg, bool use_flow_style = false)
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
  const drone_interfaces::msg::FlowMeasurement & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::msg::FlowMeasurement & msg)
{
  return drone_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::msg::FlowMeasurement>()
{
  return "drone_interfaces::msg::FlowMeasurement";
}

template<>
inline const char * name<drone_interfaces::msg::FlowMeasurement>()
{
  return "drone_interfaces/msg/FlowMeasurement";
}

template<>
struct has_fixed_size<drone_interfaces::msg::FlowMeasurement>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<drone_interfaces::msg::FlowMeasurement>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<drone_interfaces::msg::FlowMeasurement>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DRONE_INTERFACES__MSG__DETAIL__FLOW_MEASUREMENT__TRAITS_HPP_
