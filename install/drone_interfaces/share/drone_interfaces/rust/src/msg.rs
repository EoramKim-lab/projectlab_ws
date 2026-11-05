#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to drone_interfaces__msg__ObstacleCircles
/// Generated circles in map NED, before capacity and solver checks.
/// Only published for valid scans aligned with navigation; silence is not free space.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObstacleCircles {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// Interleaved center x/y (m); array index is not a persistent tracking ID.
    pub xy: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub radius: Vec<f64>,

    /// Observed radius + drone radius + safety margin (m).
    pub safe_radius: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub over_capacity: bool,

}



impl Default for ObstacleCircles {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ObstacleCircles::default())
  }
}

impl rosidl_runtime_rs::Message for ObstacleCircles {
  type RmwMsg = super::msg::rmw::ObstacleCircles;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        xy: msg.xy.as_slice().into(),
        radius: msg.radius.as_slice().into(),
        safe_radius: msg.safe_radius.as_slice().into(),
        over_capacity: msg.over_capacity,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        xy: msg.xy.as_slice().into(),
        radius: msg.radius.as_slice().into(),
        safe_radius: msg.safe_radius.as_slice().into(),
      over_capacity: msg.over_capacity,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      xy: msg.xy.into(),
      radius: msg.radius.into(),
      safe_radius: msg.safe_radius.into(),
      over_capacity: msg.over_capacity,
    }
  }
}


// Corresponds to drone_interfaces__msg__ProcessedScan

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ProcessedScan {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub raw_count: u32,

    /// Interleaved body FRD xy, meters. Origin = body reference point at scan time.
    pub xy: Vec<f64>,

}



impl Default for ProcessedScan {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ProcessedScan::default())
  }
}

impl rosidl_runtime_rs::Message for ProcessedScan {
  type RmwMsg = super::msg::rmw::ProcessedScan;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        valid: msg.valid,
        reason: msg.reason.as_str().into(),
        raw_count: msg.raw_count,
        xy: msg.xy.as_slice().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      valid: msg.valid,
        reason: msg.reason.as_str().into(),
      raw_count: msg.raw_count,
        xy: msg.xy.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      valid: msg.valid,
      reason: msg.reason.to_string(),
      raw_count: msg.raw_count,
      xy: msg.xy.into(),
    }
  }
}


// Corresponds to drone_interfaces__msg__Halfplanes

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Halfplanes {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub origin_feasible: bool,

    /// A has shape (len(b),2), row-major. A * p_body_frd_at_scan <= b.
    pub a: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub b: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sector_ids: Vec<i32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub nearest_range: Vec<f64>,

}



impl Default for Halfplanes {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Halfplanes::default())
  }
}

impl rosidl_runtime_rs::Message for Halfplanes {
  type RmwMsg = super::msg::rmw::Halfplanes;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        valid: msg.valid,
        reason: msg.reason.as_str().into(),
        origin_feasible: msg.origin_feasible,
        a: msg.a.as_slice().into(),
        b: msg.b.as_slice().into(),
        sector_ids: msg.sector_ids.as_slice().into(),
        nearest_range: msg.nearest_range.as_slice().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      valid: msg.valid,
        reason: msg.reason.as_str().into(),
      origin_feasible: msg.origin_feasible,
        a: msg.a.as_slice().into(),
        b: msg.b.as_slice().into(),
        sector_ids: msg.sector_ids.as_slice().into(),
        nearest_range: msg.nearest_range.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      valid: msg.valid,
      reason: msg.reason.to_string(),
      origin_feasible: msg.origin_feasible,
      a: msg.a.into(),
      b: msg.b.into(),
      sector_ids: msg.sector_ids.into(),
      nearest_range: msg.nearest_range.into(),
    }
  }
}


// Corresponds to drone_interfaces__msg__FlowMeasurement
/// PX4 optical flow and gyro integrals expressed about body FRD axes.
/// Downward range is a positive distance, not a NED z position.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlowMeasurement {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::FlowMeasurement::default())
  }
}

impl rosidl_runtime_rs::Message for FlowMeasurement {
  type RmwMsg = super::msg::rmw::FlowMeasurement;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        px4_timestamp_sample: msg.px4_timestamp_sample,
        pixel_flow: msg.pixel_flow,
        delta_angle: msg.delta_angle,
        integration_dt: msg.integration_dt,
        distance_m: msg.distance_m,
        quality: msg.quality,
        valid: msg.valid,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      px4_timestamp_sample: msg.px4_timestamp_sample,
        pixel_flow: msg.pixel_flow,
        delta_angle: msg.delta_angle,
      integration_dt: msg.integration_dt,
      distance_m: msg.distance_m,
      quality: msg.quality,
      valid: msg.valid,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      px4_timestamp_sample: msg.px4_timestamp_sample,
      pixel_flow: msg.pixel_flow,
      delta_angle: msg.delta_angle,
      integration_dt: msg.integration_dt,
      distance_m: msg.distance_m,
      quality: msg.quality,
      valid: msg.valid,
    }
  }
}


// Corresponds to drone_interfaces__msg__NavigationState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavigationState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub child_frame_id: std::string::String,

    /// pose: map NED, quaternion xyzw (FRD body -> NED world).
    /// twist linear: map NED; angular: body FRD.
    pub pose: geometry_msgs::msg::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub twist: geometry_msgs::msg::Twist,

    /// PX4 EKF2 acceleration estimate in map NED.
    pub acceleration: geometry_msgs::msg::Vector3,


    // This member is not documented.
    #[allow(missing_docs)]
    pub valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::NavigationState::default())
  }
}

impl rosidl_runtime_rs::Message for NavigationState {
  type RmwMsg = super::msg::rmw::NavigationState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        child_frame_id: msg.child_frame_id.as_str().into(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(msg.twist)).into_owned(),
        acceleration: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Owned(msg.acceleration)).into_owned(),
        valid: msg.valid,
        reason: msg.reason.as_str().into(),
        local_position_age: msg.local_position_age,
        gps_age: msg.gps_age,
        estimator_flags_age: msg.estimator_flags_age,
        attitude_age: msg.attitude_age,
        imu_age: msg.imu_age,
        gps_eph: msg.gps_eph,
        gps_epv: msg.gps_epv,
        gps_fix_type: msg.gps_fix_type,
        gps_satellites_used: msg.gps_satellites_used,
        gnss_aided: msg.gnss_aided,
        ekf_gnss_fusion: msg.ekf_gnss_fusion,
        eph: msg.eph,
        epv: msg.epv,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        child_frame_id: msg.child_frame_id.as_str().into(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(&msg.twist)).into_owned(),
        acceleration: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Borrowed(&msg.acceleration)).into_owned(),
      valid: msg.valid,
        reason: msg.reason.as_str().into(),
      local_position_age: msg.local_position_age,
      gps_age: msg.gps_age,
      estimator_flags_age: msg.estimator_flags_age,
      attitude_age: msg.attitude_age,
      imu_age: msg.imu_age,
      gps_eph: msg.gps_eph,
      gps_epv: msg.gps_epv,
      gps_fix_type: msg.gps_fix_type,
      gps_satellites_used: msg.gps_satellites_used,
      gnss_aided: msg.gnss_aided,
      ekf_gnss_fusion: msg.ekf_gnss_fusion,
      eph: msg.eph,
      epv: msg.epv,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      child_frame_id: msg.child_frame_id.to_string(),
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      twist: geometry_msgs::msg::Twist::from_rmw_message(msg.twist),
      acceleration: geometry_msgs::msg::Vector3::from_rmw_message(msg.acceleration),
      valid: msg.valid,
      reason: msg.reason.to_string(),
      local_position_age: msg.local_position_age,
      gps_age: msg.gps_age,
      estimator_flags_age: msg.estimator_flags_age,
      attitude_age: msg.attitude_age,
      imu_age: msg.imu_age,
      gps_eph: msg.gps_eph,
      gps_epv: msg.gps_epv,
      gps_fix_type: msg.gps_fix_type,
      gps_satellites_used: msg.gps_satellites_used,
      gnss_aided: msg.gnss_aided,
      ekf_gnss_fusion: msg.ekf_gnss_fusion,
      eph: msg.eph,
      epv: msg.epv,
    }
  }
}


