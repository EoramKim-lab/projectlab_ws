"""Offline numerical checks. No ROS runtime/message generator required."""
import math
from pathlib import Path
import types
import sys
import unittest
import numpy as np
from drone_integration.math_utils import (rotation, quaternion, px4_attitude,
    flow_velocity, limited_velocity)
from drone_integration.navigation.estimator import Estimator
from drone_integration.control.halfplanes import build_halfplanes, HalfplaneConfig

# Test the merged preprocessing functions without importing its ROS node section.
p = Path(__file__).parents[1]/'src/drone_integration/drone_integration/sensor/lidar_receiver_node.py'
pre = types.ModuleType('merged_preprocessing')
sys.modules[pre.__name__] = pre
exec(compile(p.read_text(encoding='utf-8').split('# Receiver and preprocessing')[0], str(p),'exec'),pre.__dict__)

class CoreTests(unittest.TestCase):
    def test_quaternion_roundtrip(self):
        rng = np.random.default_rng(42)
        for _ in range(100):
            q = rng.normal(size=4)
            np.testing.assert_allclose(rotation(quaternion(rotation(q))),rotation(q),atol=1e-12)

    def test_px4_attitude_north(self):
        R = rotation(px4_attitude([1,0,0,0]))
        np.testing.assert_allclose(R @ [1,0,0],[1,0,0],atol=1e-12)
        np.testing.assert_allclose(R @ [0,1,0],[0,1,0],atol=1e-12)

    def test_px4_attitude_east(self):
        R = rotation(px4_attitude([math.cos(math.pi/4),0,0,math.sin(math.pi/4)]))
        np.testing.assert_allclose(R @ [1,0,0],[0,1,0],atol=1e-12)
        np.testing.assert_allclose(R @ [0,1,0],[-1,0,0],atol=1e-12)

    def test_px4_attitude_preserves_arbitrary_roll_pitch_yaw(self):
        rng = np.random.default_rng(17)
        for _ in range(30):
            q = rng.normal(size=4)
            q /= np.linalg.norm(q)
            np.testing.assert_allclose(px4_attitude(q[[3,0,1,2]]), q)
        for bad in ([0,0,0,0], [1,0,float('nan'),0]):
            with self.assertRaises(ValueError):
                px4_attitude(bad)

    def test_tilted_rest_and_body_acceleration_in_ned(self):
        e = Estimator()
        e.q = np.array([.1, -.2, .3, .9])
        R = rotation(e.q)
        gravity = np.array([0., 0., 9.80665])
        e.predict(1., -R.T @ gravity, [1.,2.,3.])
        np.testing.assert_allclose(e.a, 0., atol=1e-12)
        np.testing.assert_allclose(e.w, [1.,2.,3.])
        e.predict(1.01, -R.T @ gravity + [1.,0.,0.], [0.,0.,0.])
        np.testing.assert_allclose(e.a, R[:,0], atol=1e-12)

    def test_rightward_flow_at_east_heading_moves_south(self):
        e = Estimator(flow_velocity_gain=1.)
        e.q = px4_attitude([math.cos(math.pi/4),0,0,math.sin(math.pi/4)])
        self.assertTrue(e.flow([-.01,0.], [0.,0.,0.], .02, 2.))
        np.testing.assert_allclose(e.v, [-1.,0.,0.], atol=1e-12)

    def test_lidar_mounting_and_right_obstacle_halfplane(self):
        # Datasheet theta=0,90,180,270 -> driver alpha=pi-theta.
        # Roll 180 about X: raw 90 degrees is body left, 270 is body right.
        cfg = pre.PreprocessConfig(step=1, min_neighbors=0)
        points = pre.preprocess_scan([2.]*4, math.pi, -math.pi/2, cfg=cfg)
        np.testing.assert_allclose(points, [[2,0],[0,-2],[-2,0],[0,2]], atol=1e-12)
        # The driver publishes ascending alpha with reversed range order.
        ascending = pre.preprocess_scan([2.]*4, -math.pi/2, math.pi/2, cfg=cfg)
        np.testing.assert_allclose(ascending, points[::-1], atol=1e-12)
        h = build_halfplanes(points[3:4])
        np.testing.assert_allclose(h.A, [[0.,1.]], atol=1e-12)
        self.assertFalse(bool(np.all(h.A @ [0.,2.] <= h.b)))
        self.assertTrue(bool(np.all(h.A @ [0.,-2.] <= h.b)))
        upright = pre.PreprocessConfig(step=1, min_neighbors=0, upside_down=False)
        p = pre.preprocess_scan([2.], math.pi/2, .1, cfg=upright)
        np.testing.assert_allclose(p, [[0.,2.]], atol=1e-12)

    def test_gazebo_lidar_scan_converts_flu_angles_to_body_frd(self):
        cfg = pre.PreprocessConfig(step=1, min_neighbors=0,
                                   scan_convention='gazebo', upside_down=False)
        # Gazebo +pi/2 is sensor-left; PX4 FRD represents left as negative y.
        points = pre.preprocess_scan([2.]*4, -math.pi, math.pi/2, cfg=cfg)
        np.testing.assert_allclose(points, [[-2,0],[0,2],[2,0],[0,-2]], atol=1e-12)

    def test_range_initialization_preserves_height_and_does_not_rezero_motion(self):
        e = Estimator()
        e.range_height(1.2, 0., [0., 0., 0.])
        e.initialize_height()
        self.assertTrue(e.initialized)
        np.testing.assert_allclose(e.p, [0., 0., -1.2])
        e.p[0], e.v[0] = 2., .5
        e.initialize_height()
        self.assertEqual(e.p[0], 2.)
        self.assertEqual(e.v[0], .5)

    def test_rest_gravity_removed(self):
        e=Estimator();e.initialized=True;e.p[2]=-1.
        for t in np.arange(1,2,.01): e.predict(t,[0,0,-9.80665],[0,0,0])
        np.testing.assert_allclose(e.p,[0,0,-1]);np.testing.assert_allclose(e.v,0,atol=1e-12)

    def test_acceleration_prediction(self):
        e=Estimator();e.initialized=True;e.predict(1,[1,0,-9.80665],[0,0,0])
        for k in range(1,101):e.predict(1+k*.01,[1,0,-9.80665],[0,0,0])
        np.testing.assert_allclose(e.v,[1,0,0],atol=1e-12)
        np.testing.assert_allclose(e.p,[.5,0,0],atol=1e-12)

    def test_large_imu_gap_not_integrated(self):
        e=Estimator();e.initialized=True;e.predict(1,[1,0,-9.80665],[0,0,0])
        e.predict(3,[1,0,-9.80665],[0,0,0]);np.testing.assert_allclose(e.v,0)
        self.assertTrue(e.prediction_gap)
        e.predict(3.02,[1,0,-9.80665],[0,0,0])
        self.assertTrue(e.prediction_gap)
        e.range_height(1.,0.,[0.,0.,0.])
        self.assertTrue(e.prediction_gap)  # Height cannot restore lost horizontal position.

    def test_unlimited_prediction_uses_full_dt_and_preserves_time_anchor(self):
        e=Estimator(max_prediction_dt=None);e.initialized=True;e.v[0]=1.
        e.predict(10.,[0,0,-9.80665],[0,0,0])
        e.predict(10.5,[0,0,-9.80665],[0,0,0])
        e.predict(10.4,[0,0,-9.80665],[0,0,0])
        e.predict(10.5,[0,0,-9.80665],[0,0,0])
        e.predict(11.,[0,0,-9.80665],[0,0,0])
        np.testing.assert_allclose(e.p,[1.,0.,0.])
        self.assertEqual(e.prediction_time,11.)
        self.assertFalse(e.prediction_gap)

    def test_range_height_tilt_offset(self):
        e=Estimator();e.q=np.array([math.sin(.1),0,0,math.cos(.1)])
        self.assertTrue(e.range_height(2,1,[0,0,.1]))
        self.assertAlmostEqual(e.p[2],1-2.1*math.cos(.2))

    def test_flow_compensation_and_sign(self):
        np.testing.assert_allclose(flow_velocity([.01,.03],[.01,.02,0],.02,2),[1,0])
        np.testing.assert_allclose(flow_velocity([-.01,0],[0,0,0],.02,2),[0,1])
        with self.assertRaises(ValueError):flow_velocity([0,0],[float('nan'),0,0],.02,2)

    def test_speed_limits(self):
        np.testing.assert_allclose(limited_velocity([3,4,2],1,.5),[.6,.8,.5])
        with self.assertRaises(ValueError):limited_velocity([float('nan'),0,0],1,1)

    def test_preprocess_mount_and_outliers(self):
        cfg=pre.PreprocessConfig(step=1,min_neighbors=0,yaw_offset=math.pi)
        pts=pre.preprocess_scan([1,float('inf'),0,float('nan')],math.pi,.1,.1,10,cfg)
        np.testing.assert_allclose(pts,[[-1,0]],atol=1e-12)

    def test_halfplanes_safety_margin(self):
        h=build_halfplanes(np.array([[2.,0.],[2.1,.1]]))
        self.assertTrue(h.origin_feasible)
        np.testing.assert_allclose(h.A,[[1,0]])
        np.testing.assert_allclose(h.b,[1.45])
        self.assertFalse(build_halfplanes([[.2,0]]).origin_feasible)

    def test_empty_halfplanes_shape(self):
        h=build_halfplanes(np.empty((0,2)))
        self.assertEqual(h.A.shape,(0,2));self.assertEqual(len(h.b),0)

if __name__=='__main__':unittest.main()
