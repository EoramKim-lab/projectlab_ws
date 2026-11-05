"""Real-message epoch/reset checks; no DDS nodes or flight commands."""
import unittest
from collections import deque
from types import SimpleNamespace as NS
from px4_msgs.msg import SensorCombined, VehicleOpticalFlow, DistanceSensor
from drone_integration.sensor.px4_imu_receiver_node import Px4ImuReceiverNode
from drone_integration.sensor.optical_flow_receiver_node import OpticalFlowReceiverNode
from drone_integration.control.mpc_node import MpcNode


class Capture:
    def __init__(self): self.messages = []
    def publish(self, msg): self.messages.append(msg)


class ResetTests(unittest.TestCase):
    def make(self, cls):
        from builtin_interfaces.msg import Time
        n=cls.__new__(cls)
        n.body='base_link_frd';n.frame='map_ned'
        n._px4_sample_timeout=.25
        n.get_clock=lambda: NS(now=lambda: NS(nanoseconds=10_000_000_000,to_msg=lambda: Time(sec=10)))
        n.get_logger=lambda: NS(error=lambda message: None, warning=lambda *args, **kwargs: None)
        n._px4_reset_pub=Capture()
        return n

    def test_imu_reboot_publishes_reset_and_resumes_samples(self):
        n=self.make(Px4ImuReceiverNode);n.imu_pub=Capture()
        msg=SensorCombined();msg.accelerometer_m_s2=[0.,0.,-9.80665]
        for stamp in (10_000_000,1000,2000,3000,4000):
            msg.timestamp=stamp;n.imu(msg)
        self.assertEqual(len(n.imu_pub.messages),1)  # Unsynchronized post-reset samples rejected.
        self.assertEqual(len(n._px4_reset_pub.messages),1)
        self.assertAlmostEqual(n.imu_pub.messages[-1].linear_acceleration.z,-9.80665,places=5)

    def test_flow_and_range_reboot_restore_both_outputs(self):
        n=self.make(OpticalFlowReceiverNode)
        n.quality=100;n.device=-1;n.flow_pub=Capture();n.range_pub=Capture()
        n.range_timeout=.5;n.last_distance=None
        f=VehicleOpticalFlow();f.quality=200;f.integration_timespan_us=20000
        f.delta_angle=[0.,0.,0.];f.distance_m=1.
        r=DistanceSensor();r.orientation=25;r.signal_quality=100
        r.min_distance=.1;r.max_distance=5.;r.current_distance=1.
        f.timestamp_sample=10_000_000;n.flow(f)
        r.timestamp=10_000_000;n.distance(r)
        for stamp in (1000,2000,3000,4000):
            f.timestamp_sample=stamp;n.flow(f)
            r.timestamp=stamp;n.distance(r)
        self.assertIsNone(n.last_distance)  # Reset clears cached range.
        self.assertEqual(len(n._px4_reset_pub.messages),1)
        self.assertEqual(len(n.flow_pub.messages),1)
        self.assertEqual(len(n.range_pub.messages),1)

    def test_mpc_reset_removes_old_pose_history_and_goal_reference(self):
        import numpy as np
        n=MpcNode.__new__(MpcNode)
        n.state=n.scan=object();n.history=deque([(10.,[4.,2.,0.])])
        n.reference_mode='forward';n.reference_initialized=True
        from drone_integration.control.mpc_controller import MPCController, MPCConfig
        n.controller=MPCController(MPCConfig())
        n.controller.last_acceleration[:]=1.
        n.controller._branch_initialized=True
        n.get_logger=lambda: NS(warning=lambda message: None)
        n.receive_px4_reset(None)
        self.assertFalse(n.history)
        self.assertIsNone(n.state)
        self.assertIsNone(n.scan)
        self.assertFalse(n.reference_initialized)
        np.testing.assert_allclose(n.controller.last_acceleration,0.)
        self.assertFalse(n.controller._branch_initialized)


if __name__ == '__main__':
    unittest.main()
