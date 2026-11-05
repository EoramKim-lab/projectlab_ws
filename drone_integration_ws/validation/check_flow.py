"""Real ROS message/callback check; no DDS transport or hardware verification."""
import importlib.util
from pathlib import Path
import rclpy
from rclpy.serialization import serialize_message, deserialize_message
from px4_msgs.msg import VehicleOpticalFlow
from drone_interfaces.msg import FlowMeasurement
from drone_integration.sensor.optical_flow_receiver_node import OpticalFlowReceiverNode

class Capture:
    def __init__(self):
        self.messages = []
    def publish(self, msg):
        self.messages.append(deserialize_message(serialize_message(msg), type(msg)))

reference = Path('/home/jetson1/Projectlab/qendy_slam_ws/optical_flow_test/optical_flow_test.py')
spec = importlib.util.spec_from_file_location('reference_flow', reference)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
rclpy.init()
nodes = []
try:
    diagnostic = module.OpticalFlowTest()
    nodes.append(diagnostic)
    receiver = OpticalFlowReceiverNode()
    nodes.append(receiver)
    receiver.flow_pub = Capture()
    msg = VehicleOpticalFlow()
    msg.timestamp_sample = 1000000
    msg.integration_timespan_us = 10000
    msg.pixel_flow = [0.01, -0.02]
    msg.delta_angle = [0.0, 0.0, 0.0]
    msg.distance_m = 1.0
    msg.quality = 200
    diagnostic.on_flow(msg)
    diagnostic.show()
    receiver.flow(msg)
    out = receiver.flow_pub.messages[-1]
    assert isinstance(out, FlowMeasurement) and out.valid
    assert abs(out.integration_dt - 0.01) < 1e-9
    assert out.header.frame_id == 'base_link'
    receiver.flow(msg)
    assert len(receiver.flow_pub.messages) == 1, 'duplicate sample accepted'
    msg.timestamp_sample += 10000
    msg.quality = 0
    receiver.flow(msg)
    assert not receiver.flow_pub.messages[-1].valid
    msg.timestamp_sample += 10000
    msg.quality = 200
    msg.delta_angle = [float('nan'), 0.0, 0.0]
    receiver.flow(msg)
    assert not receiver.flow_pub.messages[-1].valid
    print('PASS: reference diagnostic, real message serialization, valid conversion, duplicate rejection, low quality and NaN gyro invalidation')
finally:
    for node in reversed(nodes):
        node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()
