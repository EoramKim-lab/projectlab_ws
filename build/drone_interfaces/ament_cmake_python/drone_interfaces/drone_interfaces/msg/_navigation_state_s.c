// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from drone_interfaces:msg/NavigationState.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "drone_interfaces/msg/detail/navigation_state__struct.h"
#include "drone_interfaces/msg/detail/navigation_state__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool geometry_msgs__msg__pose__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * geometry_msgs__msg__pose__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool geometry_msgs__msg__twist__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * geometry_msgs__msg__twist__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool geometry_msgs__msg__vector3__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * geometry_msgs__msg__vector3__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool drone_interfaces__msg__navigation_state__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[55];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("drone_interfaces.msg._navigation_state.NavigationState", full_classname_dest, 54) == 0);
  }
  drone_interfaces__msg__NavigationState * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // child_frame_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "child_frame_id");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->child_frame_id, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // pose
    PyObject * field = PyObject_GetAttrString(_pymsg, "pose");
    if (!field) {
      return false;
    }
    if (!geometry_msgs__msg__pose__convert_from_py(field, &ros_message->pose)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // twist
    PyObject * field = PyObject_GetAttrString(_pymsg, "twist");
    if (!field) {
      return false;
    }
    if (!geometry_msgs__msg__twist__convert_from_py(field, &ros_message->twist)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // acceleration
    PyObject * field = PyObject_GetAttrString(_pymsg, "acceleration");
    if (!field) {
      return false;
    }
    if (!geometry_msgs__msg__vector3__convert_from_py(field, &ros_message->acceleration)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // valid
    PyObject * field = PyObject_GetAttrString(_pymsg, "valid");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->valid = (Py_True == field);
    Py_DECREF(field);
  }
  {  // reason
    PyObject * field = PyObject_GetAttrString(_pymsg, "reason");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->reason, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // local_position_age
    PyObject * field = PyObject_GetAttrString(_pymsg, "local_position_age");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->local_position_age = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // gps_age
    PyObject * field = PyObject_GetAttrString(_pymsg, "gps_age");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->gps_age = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // estimator_flags_age
    PyObject * field = PyObject_GetAttrString(_pymsg, "estimator_flags_age");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->estimator_flags_age = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // attitude_age
    PyObject * field = PyObject_GetAttrString(_pymsg, "attitude_age");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->attitude_age = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // imu_age
    PyObject * field = PyObject_GetAttrString(_pymsg, "imu_age");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->imu_age = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // gps_eph
    PyObject * field = PyObject_GetAttrString(_pymsg, "gps_eph");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->gps_eph = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // gps_epv
    PyObject * field = PyObject_GetAttrString(_pymsg, "gps_epv");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->gps_epv = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // gps_fix_type
    PyObject * field = PyObject_GetAttrString(_pymsg, "gps_fix_type");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->gps_fix_type = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // gps_satellites_used
    PyObject * field = PyObject_GetAttrString(_pymsg, "gps_satellites_used");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->gps_satellites_used = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // gnss_aided
    PyObject * field = PyObject_GetAttrString(_pymsg, "gnss_aided");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->gnss_aided = (Py_True == field);
    Py_DECREF(field);
  }
  {  // ekf_gnss_fusion
    PyObject * field = PyObject_GetAttrString(_pymsg, "ekf_gnss_fusion");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->ekf_gnss_fusion = (Py_True == field);
    Py_DECREF(field);
  }
  {  // eph
    PyObject * field = PyObject_GetAttrString(_pymsg, "eph");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->eph = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // epv
    PyObject * field = PyObject_GetAttrString(_pymsg, "epv");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->epv = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * drone_interfaces__msg__navigation_state__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of NavigationState */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("drone_interfaces.msg._navigation_state");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "NavigationState");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  drone_interfaces__msg__NavigationState * ros_message = (drone_interfaces__msg__NavigationState *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // child_frame_id
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->child_frame_id.data,
      strlen(ros_message->child_frame_id.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "child_frame_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // pose
    PyObject * field = NULL;
    field = geometry_msgs__msg__pose__convert_to_py(&ros_message->pose);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "pose", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // twist
    PyObject * field = NULL;
    field = geometry_msgs__msg__twist__convert_to_py(&ros_message->twist);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "twist", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // acceleration
    PyObject * field = NULL;
    field = geometry_msgs__msg__vector3__convert_to_py(&ros_message->acceleration);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "acceleration", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // valid
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->valid ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "valid", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // reason
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->reason.data,
      strlen(ros_message->reason.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "reason", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // local_position_age
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->local_position_age);
    {
      int rc = PyObject_SetAttrString(_pymessage, "local_position_age", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // gps_age
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->gps_age);
    {
      int rc = PyObject_SetAttrString(_pymessage, "gps_age", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // estimator_flags_age
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->estimator_flags_age);
    {
      int rc = PyObject_SetAttrString(_pymessage, "estimator_flags_age", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // attitude_age
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->attitude_age);
    {
      int rc = PyObject_SetAttrString(_pymessage, "attitude_age", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // imu_age
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->imu_age);
    {
      int rc = PyObject_SetAttrString(_pymessage, "imu_age", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // gps_eph
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->gps_eph);
    {
      int rc = PyObject_SetAttrString(_pymessage, "gps_eph", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // gps_epv
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->gps_epv);
    {
      int rc = PyObject_SetAttrString(_pymessage, "gps_epv", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // gps_fix_type
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->gps_fix_type);
    {
      int rc = PyObject_SetAttrString(_pymessage, "gps_fix_type", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // gps_satellites_used
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->gps_satellites_used);
    {
      int rc = PyObject_SetAttrString(_pymessage, "gps_satellites_used", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // gnss_aided
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->gnss_aided ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "gnss_aided", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // ekf_gnss_fusion
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->ekf_gnss_fusion ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "ekf_gnss_fusion", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // eph
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->eph);
    {
      int rc = PyObject_SetAttrString(_pymessage, "eph", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // epv
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->epv);
    {
      int rc = PyObject_SetAttrString(_pymessage, "epv", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
