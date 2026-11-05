#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "drone_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__ObstacleCircles() -> *const std::ffi::c_void;
}

#[link(name = "drone_interfaces__rosidl_generator_c")]
extern "C" {
    fn drone_interfaces__msg__ObstacleCircles__init(msg: *mut ObstacleCircles) -> bool;
    fn drone_interfaces__msg__ObstacleCircles__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ObstacleCircles>, size: usize) -> bool;
    fn drone_interfaces__msg__ObstacleCircles__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ObstacleCircles>);
    fn drone_interfaces__msg__ObstacleCircles__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ObstacleCircles>, out_seq: *mut rosidl_runtime_rs::Sequence<ObstacleCircles>) -> bool;
}

// Corresponds to drone_interfaces__msg__ObstacleCircles
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Generated circles in map NED, before capacity and solver checks.
/// Only published for valid scans aligned with navigation; silence is not free space.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObstacleCircles {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// Interleaved center x/y (m); array index is not a persistent tracking ID.
    pub xy: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub radius: rosidl_runtime_rs::Sequence<f64>,

    /// Observed radius + drone radius + safety margin (m).
    pub safe_radius: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub over_capacity: bool,

}



impl Default for ObstacleCircles {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !drone_interfaces__msg__ObstacleCircles__init(&mut msg as *mut _) {
        panic!("Call to drone_interfaces__msg__ObstacleCircles__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ObstacleCircles {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__ObstacleCircles__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__ObstacleCircles__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__ObstacleCircles__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ObstacleCircles {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ObstacleCircles where Self: Sized {
  const TYPE_NAME: &'static str = "drone_interfaces/msg/ObstacleCircles";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__ObstacleCircles() }
  }
}


#[link(name = "drone_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__ProcessedScan() -> *const std::ffi::c_void;
}

#[link(name = "drone_interfaces__rosidl_generator_c")]
extern "C" {
    fn drone_interfaces__msg__ProcessedScan__init(msg: *mut ProcessedScan) -> bool;
    fn drone_interfaces__msg__ProcessedScan__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ProcessedScan>, size: usize) -> bool;
    fn drone_interfaces__msg__ProcessedScan__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ProcessedScan>);
    fn drone_interfaces__msg__ProcessedScan__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ProcessedScan>, out_seq: *mut rosidl_runtime_rs::Sequence<ProcessedScan>) -> bool;
}

// Corresponds to drone_interfaces__msg__ProcessedScan
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ProcessedScan {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub raw_count: u32,

    /// Interleaved body FRD xy, meters. Origin = body reference point at scan time.
    pub xy: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for ProcessedScan {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !drone_interfaces__msg__ProcessedScan__init(&mut msg as *mut _) {
        panic!("Call to drone_interfaces__msg__ProcessedScan__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ProcessedScan {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__ProcessedScan__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__ProcessedScan__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__ProcessedScan__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ProcessedScan {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ProcessedScan where Self: Sized {
  const TYPE_NAME: &'static str = "drone_interfaces/msg/ProcessedScan";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__ProcessedScan() }
  }
}


#[link(name = "drone_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__Halfplanes() -> *const std::ffi::c_void;
}

#[link(name = "drone_interfaces__rosidl_generator_c")]
extern "C" {
    fn drone_interfaces__msg__Halfplanes__init(msg: *mut Halfplanes) -> bool;
    fn drone_interfaces__msg__Halfplanes__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Halfplanes>, size: usize) -> bool;
    fn drone_interfaces__msg__Halfplanes__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Halfplanes>);
    fn drone_interfaces__msg__Halfplanes__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Halfplanes>, out_seq: *mut rosidl_runtime_rs::Sequence<Halfplanes>) -> bool;
}

// Corresponds to drone_interfaces__msg__Halfplanes
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Halfplanes {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub origin_feasible: bool,

    /// A has shape (len(b),2), row-major. A * p_body_frd_at_scan <= b.
    pub a: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub b: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sector_ids: rosidl_runtime_rs::Sequence<i32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub nearest_range: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for Halfplanes {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !drone_interfaces__msg__Halfplanes__init(&mut msg as *mut _) {
        panic!("Call to drone_interfaces__msg__Halfplanes__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Halfplanes {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__Halfplanes__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__Halfplanes__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__Halfplanes__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Halfplanes {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Halfplanes where Self: Sized {
  const TYPE_NAME: &'static str = "drone_interfaces/msg/Halfplanes";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__Halfplanes() }
  }
}


#[link(name = "drone_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__FlowMeasurement() -> *const std::ffi::c_void;
}

#[link(name = "drone_interfaces__rosidl_generator_c")]
extern "C" {
    fn drone_interfaces__msg__FlowMeasurement__init(msg: *mut FlowMeasurement) -> bool;
    fn drone_interfaces__msg__FlowMeasurement__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<FlowMeasurement>, size: usize) -> bool;
    fn drone_interfaces__msg__FlowMeasurement__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<FlowMeasurement>);
    fn drone_interfaces__msg__FlowMeasurement__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<FlowMeasurement>, out_seq: *mut rosidl_runtime_rs::Sequence<FlowMeasurement>) -> bool;
}

// Corresponds to drone_interfaces__msg__FlowMeasurement
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// PX4 optical flow and gyro integrals expressed about body FRD axes.
/// Downward range is a positive distance, not a NED z position.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlowMeasurement {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub px4_timestamp_sample: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pixel_flow: [f64; 2],


    // This member is not documented.
    #[allow(missing_docs)]
    pub delta_angle: [f64; 3],


    // This member is not documented.
    #[allow(missing_docs)]
    pub integration_dt: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub distance_m: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub quality: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub valid: bool,

}



impl Default for FlowMeasurement {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !drone_interfaces__msg__FlowMeasurement__init(&mut msg as *mut _) {
        panic!("Call to drone_interfaces__msg__FlowMeasurement__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for FlowMeasurement {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__FlowMeasurement__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__FlowMeasurement__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__FlowMeasurement__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for FlowMeasurement {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for FlowMeasurement where Self: Sized {
  const TYPE_NAME: &'static str = "drone_interfaces/msg/FlowMeasurement";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__FlowMeasurement() }
  }
}


#[link(name = "drone_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__NavigationState() -> *const std::ffi::c_void;
}

#[link(name = "drone_interfaces__rosidl_generator_c")]
extern "C" {
    fn drone_interfaces__msg__NavigationState__init(msg: *mut NavigationState) -> bool;
    fn drone_interfaces__msg__NavigationState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<NavigationState>, size: usize) -> bool;
    fn drone_interfaces__msg__NavigationState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<NavigationState>);
    fn drone_interfaces__msg__NavigationState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<NavigationState>, out_seq: *mut rosidl_runtime_rs::Sequence<NavigationState>) -> bool;
}

// Corresponds to drone_interfaces__msg__NavigationState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavigationState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub child_frame_id: rosidl_runtime_rs::String,

    /// pose: map NED, quaternion xyzw (FRD body -> NED world).
    /// twist linear: map NED; angular: body FRD.
    pub pose: geometry_msgs::msg::rmw::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub twist: geometry_msgs::msg::rmw::Twist,

    /// PX4 EKF2 acceleration estimate in map NED.
    pub acceleration: geometry_msgs::msg::rmw::Vector3,


    // This member is not documented.
    #[allow(missing_docs)]
    pub valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,

    /// Freshness of source measurements, seconds.
    pub local_position_age: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gps_age: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub estimator_flags_age: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attitude_age: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_age: f64,

    /// Raw PX4 SensorGps quality indicators.
    pub gps_eph: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gps_epv: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gps_fix_type: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gps_satellites_used: u8,

    /// True only when the raw GNSS fix is healthy and EKF2 has a global, non-dead-reckoning reference.
    pub gnss_aided: bool,

    /// PX4 EKF2 EstimatorStatusFlags.cs_gnss_pos (GNSS position fusion intended).
    pub ekf_gnss_fusion: bool,

    /// PX4 EKF2 local position accuracy estimates.
    pub eph: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub epv: f64,

}



impl Default for NavigationState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !drone_interfaces__msg__NavigationState__init(&mut msg as *mut _) {
        panic!("Call to drone_interfaces__msg__NavigationState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for NavigationState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__NavigationState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__NavigationState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_interfaces__msg__NavigationState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for NavigationState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for NavigationState where Self: Sized {
  const TYPE_NAME: &'static str = "drone_interfaces/msg/NavigationState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__drone_interfaces__msg__NavigationState() }
  }
}


