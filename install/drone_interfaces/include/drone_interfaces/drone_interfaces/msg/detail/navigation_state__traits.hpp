// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from drone_interfaces:msg/NavigationState.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__TRAITS_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "drone_interfaces/msg/detail/navigation_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"
// Member 'twist'
#include "geometry_msgs/msg/detail/twist__traits.hpp"
// Member 'acceleration'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"

namespace drone_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const NavigationState & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: child_frame_id
  {
    out << "child_frame_id: ";
    rosidl_generator_traits::value_to_yaml(msg.child_frame_id, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: twist
  {
    out << "twist: ";
    to_flow_style_yaml(msg.twist, out);
    out << ", ";
  }

  // member: acceleration
  {
    out << "acceleration: ";
    to_flow_style_yaml(msg.acceleration, out);
    out << ", ";
  }

  // member: valid
  {
    out << "valid: ";
    rosidl_generator_traits::value_to_yaml(msg.valid, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << ", ";
  }

  // member: local_position_age
  {
    out << "local_position_age: ";
    rosidl_generator_traits::value_to_yaml(msg.local_position_age, out);
    out << ", ";
  }

  // member: gps_age
  {
    out << "gps_age: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_age, out);
    out << ", ";
  }

  // member: estimator_flags_age
  {
    out << "estimator_flags_age: ";
    rosidl_generator_traits::value_to_yaml(msg.estimator_flags_age, out);
    out << ", ";
  }

  // member: attitude_age
  {
    out << "attitude_age: ";
    rosidl_generator_traits::value_to_yaml(msg.attitude_age, out);
    out << ", ";
  }

  // member: imu_age
  {
    out << "imu_age: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_age, out);
    out << ", ";
  }

  // member: gps_eph
  {
    out << "gps_eph: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_eph, out);
    out << ", ";
  }

  // member: gps_epv
  {
    out << "gps_epv: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_epv, out);
    out << ", ";
  }

  // member: gps_fix_type
  {
    out << "gps_fix_type: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_fix_type, out);
    out << ", ";
  }

  // member: gps_satellites_used
  {
    out << "gps_satellites_used: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_satellites_used, out);
    out << ", ";
  }

  // member: gnss_aided
  {
    out << "gnss_aided: ";
    rosidl_generator_traits::value_to_yaml(msg.gnss_aided, out);
    out << ", ";
  }

  // member: ekf_gnss_fusion
  {
    out << "ekf_gnss_fusion: ";
    rosidl_generator_traits::value_to_yaml(msg.ekf_gnss_fusion, out);
    out << ", ";
  }

  // member: eph
  {
    out << "eph: ";
    rosidl_generator_traits::value_to_yaml(msg.eph, out);
    out << ", ";
  }

  // member: epv
  {
    out << "epv: ";
    rosidl_generator_traits::value_to_yaml(msg.epv, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const NavigationState & msg,
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

  // member: child_frame_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "child_frame_id: ";
    rosidl_generator_traits::value_to_yaml(msg.child_frame_id, out);
    out << "\n";
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: twist
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "twist:\n";
    to_block_style_yaml(msg.twist, out, indentation + 2);
  }

  // member: acceleration
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "acceleration:\n";
    to_block_style_yaml(msg.acceleration, out, indentation + 2);
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

  // member: reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << "\n";
  }

  // member: local_position_age
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "local_position_age: ";
    rosidl_generator_traits::value_to_yaml(msg.local_position_age, out);
    out << "\n";
  }

  // member: gps_age
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gps_age: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_age, out);
    out << "\n";
  }

  // member: estimator_flags_age
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "estimator_flags_age: ";
    rosidl_generator_traits::value_to_yaml(msg.estimator_flags_age, out);
    out << "\n";
  }

  // member: attitude_age
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "attitude_age: ";
    rosidl_generator_traits::value_to_yaml(msg.attitude_age, out);
    out << "\n";
  }

  // member: imu_age
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "imu_age: ";
    rosidl_generator_traits::value_to_yaml(msg.imu_age, out);
    out << "\n";
  }

  // member: gps_eph
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gps_eph: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_eph, out);
    out << "\n";
  }

  // member: gps_epv
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gps_epv: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_epv, out);
    out << "\n";
  }

  // member: gps_fix_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gps_fix_type: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_fix_type, out);
    out << "\n";
  }

  // member: gps_satellites_used
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gps_satellites_used: ";
    rosidl_generator_traits::value_to_yaml(msg.gps_satellites_used, out);
    out << "\n";
  }

  // member: gnss_aided
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gnss_aided: ";
    rosidl_generator_traits::value_to_yaml(msg.gnss_aided, out);
    out << "\n";
  }

  // member: ekf_gnss_fusion
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "ekf_gnss_fusion: ";
    rosidl_generator_traits::value_to_yaml(msg.ekf_gnss_fusion, out);
    out << "\n";
  }

  // member: eph
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "eph: ";
    rosidl_generator_traits::value_to_yaml(msg.eph, out);
    out << "\n";
  }

  // member: epv
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "epv: ";
    rosidl_generator_traits::value_to_yaml(msg.epv, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const NavigationState & msg, bool use_flow_style = false)
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
  const drone_interfaces::msg::NavigationState & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::msg::NavigationState & msg)
{
  return drone_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::msg::NavigationState>()
{
  return "drone_interfaces::msg::NavigationState";
}

template<>
inline const char * name<drone_interfaces::msg::NavigationState>()
{
  return "drone_interfaces/msg/NavigationState";
}

template<>
struct has_fixed_size<drone_interfaces::msg::NavigationState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<drone_interfaces::msg::NavigationState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<drone_interfaces::msg::NavigationState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DRONE_INTERFACES__MSG__DETAIL__NAVIGATION_STATE__TRAITS_HPP_
