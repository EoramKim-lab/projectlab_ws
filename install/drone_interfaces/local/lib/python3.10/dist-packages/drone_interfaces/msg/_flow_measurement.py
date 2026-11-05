# generated from rosidl_generator_py/resource/_idl.py.em
# with input from drone_interfaces:msg/FlowMeasurement.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

# Member 'pixel_flow'
# Member 'delta_angle'
import numpy  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_FlowMeasurement(type):
    """Metaclass of message 'FlowMeasurement'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('drone_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'drone_interfaces.msg.FlowMeasurement')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__flow_measurement
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__flow_measurement
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__flow_measurement
            cls._TYPE_SUPPORT = module.type_support_msg__msg__flow_measurement
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__flow_measurement

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FlowMeasurement(metaclass=Metaclass_FlowMeasurement):
    """Message class 'FlowMeasurement'."""

    __slots__ = [
        '_header',
        '_px4_timestamp_sample',
        '_pixel_flow',
        '_delta_angle',
        '_integration_dt',
        '_distance_m',
        '_quality',
        '_valid',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'px4_timestamp_sample': 'uint64',
        'pixel_flow': 'double[2]',
        'delta_angle': 'double[3]',
        'integration_dt': 'double',
        'distance_m': 'double',
        'quality': 'uint8',
        'valid': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('double'), 2),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('double'), 3),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.px4_timestamp_sample = kwargs.get('px4_timestamp_sample', int())
        if 'pixel_flow' not in kwargs:
            self.pixel_flow = numpy.zeros(2, dtype=numpy.float64)
        else:
            self.pixel_flow = kwargs.get('pixel_flow')
        if 'delta_angle' not in kwargs:
            self.delta_angle = numpy.zeros(3, dtype=numpy.float64)
        else:
            self.delta_angle = kwargs.get('delta_angle')
        self.integration_dt = kwargs.get('integration_dt', float())
        self.distance_m = kwargs.get('distance_m', float())
        self.quality = kwargs.get('quality', int())
        self.valid = kwargs.get('valid', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.px4_timestamp_sample != other.px4_timestamp_sample:
            return False
        if any(self.pixel_flow != other.pixel_flow):
            return False
        if any(self.delta_angle != other.delta_angle):
            return False
        if self.integration_dt != other.integration_dt:
            return False
        if self.distance_m != other.distance_m:
            return False
        if self.quality != other.quality:
            return False
        if self.valid != other.valid:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def px4_timestamp_sample(self):
        """Message field 'px4_timestamp_sample'."""
        return self._px4_timestamp_sample

    @px4_timestamp_sample.setter
    def px4_timestamp_sample(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'px4_timestamp_sample' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'px4_timestamp_sample' field must be an unsigned integer in [0, 18446744073709551615]"
        self._px4_timestamp_sample = value

    @builtins.property
    def pixel_flow(self):
        """Message field 'pixel_flow'."""
        return self._pixel_flow

    @pixel_flow.setter
    def pixel_flow(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float64, \
                "The 'pixel_flow' numpy.ndarray() must have the dtype of 'numpy.float64'"
            assert value.size == 2, \
                "The 'pixel_flow' numpy.ndarray() must have a size of 2"
            self._pixel_flow = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 2 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'pixel_flow' field must be a set or sequence with length 2 and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._pixel_flow = numpy.array(value, dtype=numpy.float64)

    @builtins.property
    def delta_angle(self):
        """Message field 'delta_angle'."""
        return self._delta_angle

    @delta_angle.setter
    def delta_angle(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float64, \
                "The 'delta_angle' numpy.ndarray() must have the dtype of 'numpy.float64'"
            assert value.size == 3, \
                "The 'delta_angle' numpy.ndarray() must have a size of 3"
            self._delta_angle = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 3 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'delta_angle' field must be a set or sequence with length 3 and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._delta_angle = numpy.array(value, dtype=numpy.float64)

    @builtins.property
    def integration_dt(self):
        """Message field 'integration_dt'."""
        return self._integration_dt

    @integration_dt.setter
    def integration_dt(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'integration_dt' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'integration_dt' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._integration_dt = value

    @builtins.property
    def distance_m(self):
        """Message field 'distance_m'."""
        return self._distance_m

    @distance_m.setter
    def distance_m(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'distance_m' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'distance_m' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._distance_m = value

    @builtins.property
    def quality(self):
        """Message field 'quality'."""
        return self._quality

    @quality.setter
    def quality(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'quality' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'quality' field must be an unsigned integer in [0, 255]"
        self._quality = value

    @builtins.property
    def valid(self):
        """Message field 'valid'."""
        return self._valid

    @valid.setter
    def valid(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'valid' field must be of type 'bool'"
        self._valid = value
