"""Real ROS callback checks, without creating DDS nodes or sending flight commands."""
import unittest
import math
from types import SimpleNamespace as NS
import numpy as np
from geometry_msgs.msg import QuaternionStamped
from sensor_msgs.msg import Imu, Range
from drone_interfaces.msg import FlowMeasurement
from drone_integration.navigation.dead_reckoning_node import DeadReckoningNode
from drone_integration.navigation.estimator import Estimator


class DeadReckoningTests(unittest.TestCase):
    def make(self):
        n = DeadReckoningNode.__new__(DeadReckoningNode)
        n.frame, n.body = 'map_ned', 'base_link_frd'
        n.timeout, n.max_skew = .25, .08
        n.strict_sensor_checks = True
        n.offset = np.zeros(3)
        n.ground_z, n.height_gain = 0., .5
        n.core = Estimator(flow_velocity_gain=1.)
        n.stamps = {}
        n.last_range = n.previous_height = None
        n.flow_good = False
        n.now = 10.
        n.get_clock = lambda: NS(now=lambda: NS(nanoseconds=int(n.now*1e9), to_msg=lambda: self.header(n).stamp))
        n.pub = NS(messages=[])
        n.pub.publish = n.pub.messages.append
        return n

    def header(self, n, body=False):
        from std_msgs.msg import Header
        h = Header()
        h.frame_id = n.body if body else n.frame
        h.stamp.sec = int(n.now)
        h.stamp.nanosec = round((n.now-int(n.now))*1e9)
        return h

    def feed(self, n, height=1., pixel=0.):
        a = QuaternionStamped();a.header=self.header(n);a.quaternion.w=1.
        n.attitude(a)
        r = Range();r.header=self.header(n,True)
        r.min_range=.01;r.max_range=10.;r.range=height;n.distance(r)
        i=Imu();i.header=self.header(n,True);i.linear_acceleration.z=-9.80665;n.imu(i)
        f=FlowMeasurement();f.header=self.header(n,True)
        f.valid=True;f.integration_dt=.02;f.distance_m=height
        f.pixel_flow=[0.,pixel];f.delta_angle=[0.,0.,0.];n.flow(f)

    def test_initial_origin_and_stale_sensors_block(self):
        n=self.make();self.feed(n);n.publish()
        self.assertTrue(n.pub.messages[-1].valid)
        np.testing.assert_allclose(n.core.p,[0.,0.,-1.])
        self.assertEqual(n.core.p[0],0.)
        n.now+=.3;n.publish()
        self.assertFalse(n.pub.messages[-1].valid)
        self.assertIn('flow',n.pub.messages[-1].reason)

    def test_flow_moves_position_and_range_bounds_vertical_drift(self):
        n=self.make();self.feed(n,pixel=.01)
        for _ in range(40):
            n.now+=.02;self.feed(n,pixel=.01)
        self.assertGreater(np.linalg.norm(n.core.p[:2]),.3)
        self.assertAlmostEqual(n.core.p[2],-1.)
        self.assertAlmostEqual(n.core.v[2],0.)

    def test_duplicate_and_invalid_range_do_not_initialize(self):
        n=self.make()
        r=Range();r.header=self.header(n,True);r.range=1.;r.min_range=.01;r.max_range=10.
        n.distance(r);self.assertFalse(n.core.initialized)
        self.feed(n)
        old=n.core.p.copy();n.distance(r)
        np.testing.assert_allclose(n.core.p,old)
        n.now+=.02;r.header=self.header(n,True);r.range=float('nan')
        n.distance(r);np.testing.assert_allclose(n.core.p,old)

    def test_climbing_produces_negative_down_velocity(self):
        n=self.make();self.feed(n,height=1.)
        n.now+=.1;self.feed(n,height=1.1)
        self.assertLess(n.core.p[2],-1.)
        self.assertLess(n.core.v[2],0.)

    def test_duplicate_and_wrong_frame_flow_preserve_valid_observation(self):
        n=self.make();self.feed(n)
        f=FlowMeasurement();f.header=self.header(n,True)
        # Even an invalid duplicate cannot replace the already accepted sample.
        n.flow(f);n.publish()
        self.assertTrue(n.pub.messages[-1].valid)
        n.now+=.02;f.header=self.header(n)
        n.flow(f);n.publish()
        self.assertTrue(n.pub.messages[-1].valid)
        f.header=self.header(n,True)
        n.flow(f);n.publish()
        self.assertFalse(n.pub.messages[-1].valid)
        self.assertIn('flow_invalid',n.pub.messages[-1].reason)

    def test_imu_gap_latches_invalid_even_after_regular_samples_resume(self):
        n=self.make();self.feed(n,pixel=.01)
        n.now+=.15;self.feed(n,pixel=.01);n.publish()
        self.assertFalse(n.pub.messages[-1].valid)
        self.assertIn('imu_prediction_gap',n.pub.messages[-1].reason)
        n.now+=.02;self.feed(n,pixel=.01);n.publish()
        self.assertFalse(n.pub.messages[-1].valid)

    def test_px4_reset_clears_origin_and_requires_fresh_sensors(self):
        n=self.make();self.feed(n,pixel=.01)
        n.core.p[0]=4.
        n.get_logger=lambda: NS(warning=lambda message: None)
        n.receive_px4_reset(None);n.publish()
        self.assertFalse(n.pub.messages[-1].valid)
        self.assertFalse(n.core.initialized)
        np.testing.assert_allclose(n.core.p,0.)
        n.now+=.02;self.feed(n);n.publish()
        self.assertTrue(n.pub.messages[-1].valid)

    def relaxed(self):
        n=self.make();n.strict_sensor_checks=False
        n.core=Estimator(flow_velocity_gain=1.,max_prediction_dt=None)
        return n

    def test_relaxed_150ms_imu_updates_position(self):
        n=self.relaxed();self.feed(n,pixel=.01)
        for _ in range(10):
            n.now+=.15;self.feed(n,pixel=.01)
        n.publish()
        self.assertTrue(n.pub.messages[-1].valid)
        self.assertAlmostEqual(n.core.p[0],.75,places=6)
        self.assertFalse(n.core.prediction_gap)

    def test_relaxed_frame_age_and_attitude_skew_do_not_block_prediction(self):
        n=self.relaxed();self.feed(n,pixel=.01)
        # Old stamp and arbitrary frame label: accept data but retain its age.
        i=Imu();i.header=self.header(n,True);i.header.frame_id='other_body'
        i.linear_acceleration.z=-9.80665
        n.now+=.2;i.header.stamp.nanosec=200_000_000
        n.now+=1.
        n.imu(i)
        self.assertAlmostEqual(n.core.p[0],.1,places=6)
        n.publish()
        self.assertFalse(n.pub.messages[-1].valid)
        self.assertIn('imu',n.pub.messages[-1].reason)

    def test_relaxed_duplicate_and_reverse_imu_never_double_integrate(self):
        n=self.relaxed();self.feed(n,pixel=.01)
        n.now+=.15;self.feed(n,pixel=.01)
        p=n.core.p.copy()
        self.feed(n,pixel=.01)
        n.now-=.05;self.feed(n,pixel=.01)
        np.testing.assert_allclose(n.core.p,p)

    def test_relaxed_reset_retains_unlimited_prediction_dt(self):
        n=self.relaxed();n.get_logger=lambda: NS(warning=lambda message: None)
        n.receive_px4_reset(None)
        self.assertIsNone(n.core.max_prediction_dt)

    def test_relaxed_flow_can_use_range_outside_skew_limit(self):
        n=self.relaxed();self.feed(n)
        n.now+=.2
        f=FlowMeasurement();f.header=self.header(n,True)
        f.valid=True;f.integration_dt=.02;f.distance_m=float('nan')
        f.pixel_flow=[0.,.01];f.delta_angle=[0.,0.,0.]
        n.flow(f)
        self.assertTrue(n.flow_good)
        self.assertAlmostEqual(n.core.v[0],.5)


class ForwardReferenceTests(unittest.TestCase):
    def test_initial_heading_defines_six_meter_goal_once(self):
        from collections import deque
        from drone_interfaces.msg import NavigationState
        from drone_integration.control.mpc_node import MpcNode
        n=MpcNode.__new__(MpcNode)
        n.frame='map_ned';n.timeout=.25;n.history=deque(maxlen=200)
        n.reference_initialized=False;n.forward_distance=6.;n.mission_height=1.
        n.controller=NS(reference_start=None)
        n.get_clock=lambda: NS(now=lambda: NS(nanoseconds=10_000_000_000))
        n.get_logger=lambda: NS(info=lambda message: None)
        msg=NavigationState();msg.header.frame_id='map_ned';msg.header.stamp.sec=10
        msg.pose.orientation.z=math.sin(math.pi/4)
        msg.pose.orientation.w=math.cos(math.pi/4)
        msg.pose.position.x=2.;msg.pose.position.y=4.
        msg.valid=False;n.on_state(msg)
        self.assertFalse(n.reference_initialized)
        msg.valid=True;n.on_state(msg)
        np.testing.assert_allclose(n.goal,[2.,10.,-1.],atol=1e-12)
        np.testing.assert_allclose(n.controller.reference_start,[2.,4.])
        msg.pose.position.x=8.;n.on_state(msg)
        np.testing.assert_allclose(n.goal,[2.,10.,-1.],atol=1e-12)


if __name__ == '__main__':
    unittest.main()
