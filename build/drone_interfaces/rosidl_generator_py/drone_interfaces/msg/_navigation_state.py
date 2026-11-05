# generated from rosidl_generator_py/resource/_idl.py.em
# with input from drone_interfaces:msg/NavigationState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_NavigationState(type):
    """Metaclass of message 'NavigationState'."""

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
                'drone_interfaces.msg.NavigationState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__navigation_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__navigation_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__navigation_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__navigation_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__navigation_state

            from geometry_msgs.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

            from geometry_msgs.msg import Twist
            if Twist.__class__._TYPE_SUPPORT is None:
                Twist.__class__.__import_type_support__()

            from geometry_msgs.msg import Vector3
            if Vector3.__class__._TYPE_SUPPORT is None:
                Vector3.__class__.__import_type_support__()

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


class NavigationState(metaclass=Metaclass_NavigationState):
    """Message class 'NavigationState'."""

    __slots__ = [
        '_header',
        '_child_frame_id',
        '_pose',
        '_twist',
        '_acceleration',
        '_valid',
        '_reason',
        '_local_position_age',
        '_gps_age',
        '_estimator_flags_age',
        '_attitude_age',
        '_imu_age',
        '_gps_eph',
        '_gps_epv',
        '_gps_fix_type',
        '_gps_satellites_used',
        '_gnss_aided',
        '_ekf_gnss_fusion',
        '_eph',
        '_epv',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'child_frame_id': 'string',
        'pose': 'geometry_msgs/Pose',
        'twist': 'geometry_msgs/Twist',
        'acceleration': 'geometry_msgs/Vector3',
        'valid': 'boolean',
        'reason': 'string',
        'local_position_age': 'double',
        'gps_age': 'double',
        'estimator_flags_age': 'double',
        'attitude_age': 'double',
        'imu_age': 'double',
        'gps_eph': 'double',
        'gps_epv': 'double',
        'gps_fix_type': 'uint8',
        'gps_satellites_used': 'uint8',
        'gnss_aided': 'boolean',
        'ekf_gnss_fusion': 'boolean',
        'eph': 'double',
        'epv': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Vector3'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.child_frame_id = kwargs.get('child_frame_id', str())
        from geometry_msgs.msg import Pose
        self.pose = kwargs.get('pose', Pose())
        from geometry_msgs.msg import Twist
        self.twist = kwargs.get('twist', Twist())
        from geometry_msgs.msg import Vector3
        self.acceleration = kwargs.get('acceleration', Vector3())
        self.valid = kwargs.get('valid', bool())
        self.reason = kwargs.get('reason', str())
        self.local_position_age = kwargs.get('local_position_age', float())
        self.gps_age = kwargs.get('gps_age', float())
        self.estimator_flags_age = kwargs.get('estimator_flags_age', float())
        self.attitude_age = kwargs.get('attitude_age', float())
        self.imu_age = kwargs.get('imu_age', float())
        self.gps_eph = kwargs.get('gps_eph', float())
        self.gps_epv = kwargs.get('gps_epv', float())
        self.gps_fix_type = kwargs.get('gps_fix_type', int())
        self.gps_satellites_used = kwargs.get('gps_satellites_used', int())
        self.gnss_aided = kwargs.get('gnss_aided', bool())
        self.ekf_gnss_fusion = kwargs.get('ekf_gnss_fusion', bool())
        self.eph = kwargs.get('eph', float())
        self.epv = kwargs.get('epv', float())

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
        if self.child_frame_id != other.child_frame_id:
            return False
        if self.pose != other.pose:
            return False
        if self.twist != other.twist:
            return False
        if self.acceleration != other.acceleration:
            return False
        if self.valid != other.valid:
            return False
        if self.reason != other.reason:
            return False
        if self.local_position_age != other.local_position_age:
            return False
        if self.gps_age != other.gps_age:
            return False
        if self.estimator_flags_age != other.estimator_flags_age:
            return False
        if self.attitude_age != other.attitude_age:
            return False
        if self.imu_age != other.imu_age:
            return False
        if self.gps_eph != other.gps_eph:
            return False
        if self.gps_epv != other.gps_epv:
            return False
        if self.gps_fix_type != other.gps_fix_type:
            return False
        if self.gps_satellites_used != other.gps_satellites_used:
            return False
        if self.gnss_aided != other.gnss_aided:
            return False
        if self.ekf_gnss_fusion != other.ekf_gnss_fusion:
            return False
        if self.eph != other.eph:
            return False
        if self.epv != other.epv:
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
    def child_frame_id(self):
        """Message field 'child_frame_id'."""
        return self._child_frame_id

    @child_frame_id.setter
    def child_frame_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'child_frame_id' field must be of type 'str'"
        self._child_frame_id = value

    @builtins.property
    def pose(self):
        """Message field 'pose'."""
        return self._pose

    @pose.setter
    def pose(self, value):
        if __debug__:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'pose' field must be a sub message of type 'Pose'"
        self._pose = value

    @builtins.property
    def twist(self):
        """Message field 'twist'."""
        return self._twist

    @twist.setter
    def twist(self, value):
        if __debug__:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'twist' field must be a sub message of type 'Twist'"
        self._twist = value

    @builtins.property
    def acceleration(self):
        """Message field 'acceleration'."""
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        if __debug__:
            from geometry_msgs.msg import Vector3
            assert \
                isinstance(value, Vector3), \
                "The 'acceleration' field must be a sub message of type 'Vector3'"
        self._acceleration = value

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

    @builtins.property
    def reason(self):
        """Message field 'reason'."""
        return self._reason

    @reason.setter
    def reason(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'reason' field must be of type 'str'"
        self._reason = value

    @builtins.property
    def local_position_age(self):
        """Message field 'local_position_age'."""
        return self._local_position_age

    @local_position_age.setter
    def local_position_age(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'local_position_age' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'local_position_age' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._local_position_age = value

    @builtins.property
    def gps_age(self):
        """Message field 'gps_age'."""
        return self._gps_age

    @gps_age.setter
    def gps_age(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gps_age' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'gps_age' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._gps_age = value

    @builtins.property
    def estimator_flags_age(self):
        """Message field 'estimator_flags_age'."""
        return self._estimator_flags_age

    @estimator_flags_age.setter
    def estimator_flags_age(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'estimator_flags_age' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'estimator_flags_age' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._estimator_flags_age = value

    @builtins.property
    def attitude_age(self):
        """Message field 'attitude_age'."""
        return self._attitude_age

    @attitude_age.setter
    def attitude_age(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'attitude_age' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'attitude_age' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._attitude_age = value

    @builtins.property
    def imu_age(self):
        """Message field 'imu_age'."""
        return self._imu_age

    @imu_age.setter
    def imu_age(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'imu_age' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'imu_age' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._imu_age = value

    @builtins.property
    def gps_eph(self):
        """Message field 'gps_eph'."""
        return self._gps_eph

    @gps_eph.setter
    def gps_eph(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gps_eph' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'gps_eph' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._gps_eph = value

    @builtins.property
    def gps_epv(self):
        """Message field 'gps_epv'."""
        return self._gps_epv

    @gps_epv.setter
    def gps_epv(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gps_epv' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'gps_epv' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._gps_epv = value

    @builtins.property
    def gps_fix_type(self):
        """Message field 'gps_fix_type'."""
        return self._gps_fix_type

    @gps_fix_type.setter
    def gps_fix_type(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'gps_fix_type' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'gps_fix_type' field must be an unsigned integer in [0, 255]"
        self._gps_fix_type = value

    @builtins.property
    def gps_satellites_used(self):
        """Message field 'gps_satellites_used'."""
        return self._gps_satellites_used

    @gps_satellites_used.setter
    def gps_satellites_used(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'gps_satellites_used' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'gps_satellites_used' field must be an unsigned integer in [0, 255]"
        self._gps_satellites_used = value

    @builtins.property
    def gnss_aided(self):
        """Message field 'gnss_aided'."""
        return self._gnss_aided

    @gnss_aided.setter
    def gnss_aided(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'gnss_aided' field must be of type 'bool'"
        self._gnss_aided = value

    @builtins.property
    def ekf_gnss_fusion(self):
        """Message field 'ekf_gnss_fusion'."""
        return self._ekf_gnss_fusion

    @ekf_gnss_fusion.setter
    def ekf_gnss_fusion(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'ekf_gnss_fusion' field must be of type 'bool'"
        self._ekf_gnss_fusion = value

    @builtins.property
    def eph(self):
        """Message field 'eph'."""
        return self._eph

    @eph.setter
    def eph(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'eph' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'eph' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._eph = value

    @builtins.property
    def epv(self):
        """Message field 'epv'."""
        return self._epv

    @epv.setter
    def epv(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'epv' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'epv' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._epv = value
