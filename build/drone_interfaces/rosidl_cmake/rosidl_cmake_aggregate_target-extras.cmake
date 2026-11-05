# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target drone_interfaces::drone_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${drone_interfaces_TARGETS}.
if(drone_interfaces_TARGETS AND NOT TARGET drone_interfaces::drone_interfaces)
  add_library(drone_interfaces::drone_interfaces INTERFACE IMPORTED)
  set_target_properties(drone_interfaces::drone_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${drone_interfaces_TARGETS}")
endif()
