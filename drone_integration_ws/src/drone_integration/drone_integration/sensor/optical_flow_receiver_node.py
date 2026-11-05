"""Holybro via Pixhawk. Export the two uORB outputs in firmware dds_topics.yaml first."""
import math
import numpy as np
from sensor_msgs.msg import Range
from px4_msgs.msg import SensorOpticalFlow, VehicleOpticalFlow, DistanceSensor
from drone_interfaces.msg import FlowMeasurement
from ..common import Base, SENSOR_QOS, run

class OpticalFlowReceiverNode(Base):
    def __init__(self):
        super().__init__('optical_flow_receiver_node')
        self.quality = self.param('minimum_quality',70)
        self.device = self.param('range_device_id',-1)
        self.body = self.param('body_frame','base_link_frd')
        self.flow_source = self.param('flow_source', 'sensor')
        self.range_timeout = self.param('range_timeout', .5)
        self.sensor_yaw = self.param('sensor_yaw_offset', 0.)
        if self.flow_source not in ('sensor', 'vehicle'):
            raise ValueError('flow_source must be sensor or vehicle')
        if not math.isfinite(self.range_timeout) or self.range_timeout <= 0 or not math.isfinite(self.sensor_yaw):
            raise ValueError('invalid range timeout or sensor yaw offset')
        self.last_distance = None
        self.watch_px4_clock()
        self.start_monitor('flow', 'raw_flow', 'range')
        self.flow_pub = self.create_publisher(FlowMeasurement,'sensors/flow',10)
        self.range_pub = self.create_publisher(Range,'sensors/range',10)
        self.create_subscription(SensorOpticalFlow,'/fmu/out/sensor_optical_flow',self.raw_flow,SENSOR_QOS)
        if self.flow_source == 'vehicle':
            self.create_subscription(VehicleOpticalFlow,'/fmu/out/vehicle_optical_flow',self.flow,SENSOR_QOS)
        self.create_subscription(DistanceSensor,'/fmu/out/distance_sensor',self.distance,SENSOR_QOS)

    def raw_flow(self, msg):
        # Sensor mode explicitly rotates sensor axes into body FRD before fusion.
        self.observe('raw_flow', f'RAW_SENSOR_AXES quality={msg.quality} '
                     f'pixel_flow={np.round(msg.pixel_flow, 4).tolist()}rad '
                     f'delta_angle={np.round(msg.delta_angle, 4).tolist()}rad '
                     f'gyro_available={msg.delta_angle_available} '
                     f'distance={msg.distance_m:.3f}m distance_available={msg.distance_available} '
                     f'dt={msg.integration_timespan_us*1e-6:.4f}s source={self.flow_source}')
        if self.flow_source == 'sensor':
            self.flow(msg, sensor_axes=True)

    def on_px4_reset(self):
        self.last_distance = None

    def flow(self,msg, sensor_axes=False):
        if not self.px4_increasing('flow',msg.timestamp_sample):
            return
        stamp = self.px4_sample_stamp(msg.timestamp_sample)
        if stamp is None:
            return
        out = FlowMeasurement()
        out.header.stamp = stamp
        out.header.frame_id = self.body
        out.px4_timestamp_sample = msg.timestamp_sample
        pixel = np.asarray(msg.pixel_flow, dtype=float)
        delta = np.asarray(msg.delta_angle, dtype=float)
        if sensor_axes:
            c, s = math.cos(self.sensor_yaw), math.sin(self.sensor_yaw)
            R = np.array([[c,-s],[s,c]])
            pixel = R @ pixel
            delta = np.r_[R @ delta[:2], delta[2]]
        out.pixel_flow = pixel.tolist()
        out.delta_angle = delta.tolist()
        out.integration_dt = msg.integration_timespan_us*1e-6
        # Always use the independent downward 1-D range, never optical distance_m.
        distance = self.last_distance
        out.distance_m = (float(distance.range) if distance is not None
                          and self.fresh(distance.header.stamp, self.range_timeout)
                          else float('nan'))
        out.quality = int(msg.quality)
        out.valid = bool((not sensor_axes or msg.delta_angle_available)
                         and math.isfinite(out.distance_m) and out.distance_m > 0
                         and msg.quality >= self.quality and 0.0001 <= out.integration_dt <= .2
                         and np.isfinite(out.pixel_flow).all() and np.isfinite(out.delta_angle).all())
        # Missing gyro compensation invalidates flow; never treat NaN as zero.
        self.observe('flow', f'valid={out.valid} quality={out.quality} pixel_flow={np.round(out.pixel_flow, 4).tolist()}rad delta_angle={np.round(out.delta_angle, 4).tolist()}rad dt={out.integration_dt:.4f}s distance={out.distance_m:.3f}m distance_source=/fmu/out/distance_sensor')
        self.flow_pub.publish(out)

    def distance(self,msg):
        if self.device >= 0 and msg.device_id != self.device:
            return
        if msg.orientation != DistanceSensor.ROTATION_DOWNWARD_FACING:
            self.observe('range', f'REJECTED orientation={msg.orientation}; expected downward')
            return
        if (msg.signal_quality == 0 or not math.isfinite(msg.current_distance)
                or not msg.min_distance <= msg.current_distance <= msg.max_distance):
            self.observe('range', f'REJECTED distance={msg.current_distance} quality={msg.signal_quality}')
            return
        if not self.px4_increasing('range',msg.timestamp):
            return
        stamp = self.px4_sample_stamp(msg.timestamp)
        if stamp is None:
            return
        out = Range()
        out.header.stamp = stamp
        out.header.frame_id = self.body  # adapter contract: sensor boresight is body +z
        out.radiation_type = Range.INFRARED
        out.field_of_view = float(max(msg.h_fov,msg.v_fov))
        out.min_range,out.max_range,out.range = map(float,(msg.min_distance,msg.max_distance,msg.current_distance))
        self.last_distance = out
        self.observe('range', f'downward={out.range:.3f}m')
        self.range_pub.publish(out)

def main(args=None): run(OpticalFlowReceiverNode,args)
