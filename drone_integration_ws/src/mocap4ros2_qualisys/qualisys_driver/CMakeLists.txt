cmake_minimum_required(VERSION 3.5)

project(qualisys_driver)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH};${CMAKE_SOURCE_DIR}/cmake/modules")

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(mocap4r2_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)


include(FetchContent)
# Use the SDK supplied as a ZIP in this workspace, including offline builds.
get_filename_component(WORKSPACE_QUALISYS_SDK
  "${CMAKE_CURRENT_SOURCE_DIR}/../../../vendor/qualisys_cpp_sdk" ABSOLUTE)
if(EXISTS "${WORKSPACE_QUALISYS_SDK}/CMakeLists.txt" AND
   NOT DEFINED FETCHCONTENT_SOURCE_DIR_QUALISYS_CPP_SDK)
  set(FETCHCONTENT_SOURCE_DIR_QUALISYS_CPP_SDK "${WORKSPACE_QUALISYS_SDK}")
endif()
if (NOT TARGET qualisys_cpp_sdk)
  message(STATUS "${PROJECT_NAME}: `qualisys_cpp_sdk` targets not found. Attempting to fetch contents...")
  FetchContent_Declare(
    qualisys_cpp_sdk
    GIT_REPOSITORY https://github.com/qualisys/qualisys_cpp_sdk
    GIT_TAG        rt_protocol_1.23
  )
  FetchContent_MakeAvailable(qualisys_cpp_sdk)
else()
  message(STATUS "qualisys_cpp_sdk: `qualisys_cpp_sdk` targets found.")
endif()

set(dependencies
  rclcpp
  rclcpp_lifecycle
  tf2
  tf2_ros
  mocap4r2_msgs
)

include_directories(
  include
)

add_library(${PROJECT_NAME} STATIC src/qualisys_driver.cpp)
ament_target_dependencies(${PROJECT_NAME} ${dependencies})

add_executable(qualisys_driver_main
  src/qualisys_driver_main.cpp
)

ament_target_dependencies(qualisys_driver_main ${dependencies})
target_link_libraries(qualisys_driver_main
  ${PROJECT_NAME}
  qualisys_cpp_sdk
)

ament_target_dependencies(qualisys_driver ${dependencies})
target_link_libraries(qualisys_driver
  qualisys_cpp_sdk
)

install(DIRECTORY include/
  DESTINATION include/
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS
  ${PROJECT_NAME}
  qualisys_driver_main
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(${dependencies})
ament_package()
