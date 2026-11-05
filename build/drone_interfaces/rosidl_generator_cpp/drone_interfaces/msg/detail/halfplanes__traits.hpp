// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from drone_interfaces:msg/Halfplanes.idl
// generated code does not contain a copyright notice

#ifndef DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__TRAITS_HPP_
#define DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "drone_interfaces/msg/detail/halfplanes__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace drone_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Halfplanes & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
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

  // member: origin_feasible
  {
    out << "origin_feasible: ";
    rosidl_generator_traits::value_to_yaml(msg.origin_feasible, out);
    out << ", ";
  }

  // member: a
  {
    if (msg.a.size() == 0) {
      out << "a: []";
    } else {
      out << "a: [";
      size_t pending_items = msg.a.size();
      for (auto item : msg.a) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: b
  {
    if (msg.b.size() == 0) {
      out << "b: []";
    } else {
      out << "b: [";
      size_t pending_items = msg.b.size();
      for (auto item : msg.b) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: sector_ids
  {
    if (msg.sector_ids.size() == 0) {
      out << "sector_ids: []";
    } else {
      out << "sector_ids: [";
      size_t pending_items = msg.sector_ids.size();
      for (auto item : msg.sector_ids) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: nearest_range
  {
    if (msg.nearest_range.size() == 0) {
      out << "nearest_range: []";
    } else {
      out << "nearest_range: [";
      size_t pending_items = msg.nearest_range.size();
      for (auto item : msg.nearest_range) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Halfplanes & msg,
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

  // member: origin_feasible
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "origin_feasible: ";
    rosidl_generator_traits::value_to_yaml(msg.origin_feasible, out);
    out << "\n";
  }

  // member: a
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.a.size() == 0) {
      out << "a: []\n";
    } else {
      out << "a:\n";
      for (auto item : msg.a) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: b
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.b.size() == 0) {
      out << "b: []\n";
    } else {
      out << "b:\n";
      for (auto item : msg.b) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: sector_ids
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.sector_ids.size() == 0) {
      out << "sector_ids: []\n";
    } else {
      out << "sector_ids:\n";
      for (auto item : msg.sector_ids) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: nearest_range
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.nearest_range.size() == 0) {
      out << "nearest_range: []\n";
    } else {
      out << "nearest_range:\n";
      for (auto item : msg.nearest_range) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Halfplanes & msg, bool use_flow_style = false)
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
  const drone_interfaces::msg::Halfplanes & msg,
  std::ostream & out, size_t indentation = 0)
{
  drone_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use drone_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const drone_interfaces::msg::Halfplanes & msg)
{
  return drone_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<drone_interfaces::msg::Halfplanes>()
{
  return "drone_interfaces::msg::Halfplanes";
}

template<>
inline const char * name<drone_interfaces::msg::Halfplanes>()
{
  return "drone_interfaces/msg/Halfplanes";
}

template<>
struct has_fixed_size<drone_interfaces::msg::Halfplanes>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<drone_interfaces::msg::Halfplanes>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<drone_interfaces::msg::Halfplanes>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DRONE_INTERFACES__MSG__DETAIL__HALFPLANES__TRAITS_HPP_
