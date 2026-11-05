"""Run separately with ROS/install sourced; uses real generated ROS messages.
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 tests/check_mpc_ros.py
No PX4 commands, services or arming are sent.
"""
import math
import unittest
import numpy as np
import rclpy
from drone_interfaces.msg import NavigationState, ProcessedScan
from drone_integration.control.mpc_node import MpcNode, circles_from_points, GOAL_NED, REFERENCE_START_NED


class MpcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = MpcNode()
        cls.received = []
        # Capture adapter output without publishing to any vehicle topic.
        cls.node.velocity_pub = type('Capture', (), {'publish': lambda _, m: cls.received.append(m)})()

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def setUp(self):
        n = self.node
        self.received.clear()
        n.history.clear()
        n.controller.reset()
        n.reference_initialized = True
        n.goal = np.asarray(GOAL_NED).copy()
        n.controller.reference_start = np.asarray(REFERENCE_START_NED[:2])
        state = NavigationState()
        state.header.frame_id = 'map_ned'
        state.header.stamp = n.get_clock().now().to_msg()
        state.pose.orientation.w = 1.
        state.valid = True
        n.on_state(state)
        scan = ProcessedScan()
        scan.header.frame_id = 'base_link_frd'
        scan.header.stamp = state.header.stamp
        scan.valid = True
        scan.xy = [5., 3., 5.05, 3.]
        n.on_scan(scan)

    def test_command_and_limits(self):
        self.node.solve()
        self.assertEqual(len(self.received), 1)
        cmd = self.received[-1]
        self.assertEqual(cmd.header.frame_id, 'map_ned')
        self.assertGreater(cmd.twist.linear.y, 0.)
        self.assertLessEqual(np.hypot(cmd.twist.linear.x, cmd.twist.linear.y), .0501)
        self.assertEqual(cmd.twist.angular.z, 0.)
        self.assertAlmostEqual(cmd.twist.linear.z, -.5)
        self.assertEqual(cmd.header.stamp, self.node.scan.header.stamp)

    def test_invalid_stale_and_unaligned(self):
        n = self.node
        n.scan.valid = False
        n.solve()
        self.assertFalse(self.received)
        n.scan.valid = True
        n.scan.header.stamp.sec -= 2
        n.solve()
        self.assertFalse(self.received)
        n.scan.header.stamp = n.state.header.stamp
        n.history.clear()
        n.history.append((0., np.zeros(3)))
        n.solve()
        self.assertFalse(self.received)

    def test_fixed_reference_and_no_goal_subscription(self):
        n = self.node
        self.assertNotIn('/control/goal', [sub.topic_name for sub in n.subscriptions])
        np.testing.assert_allclose(n.goal, GOAL_NED)
        pref, _, _, _ = n.controller._reference(np.array([.5, .4, 0., 0.]), n.goal[:2])
        start = np.asarray(REFERENCE_START_NED[:2])
        segment = n.goal[:2] - start
        length = np.linalg.norm(segment)
        direction = segment / length
        along = (pref - start) @ direction
        projected = np.clip((np.array([.5, .4]) - start) @ direction, 0., length)
        np.testing.assert_allclose(pref, start + along[:, None] * direction, atol=1e-12)
        self.assertAlmostEqual(along[0], projected)
        self.assertTrue(np.all(np.diff(along) >= -1e-12))
        self.assertTrue(np.all((along >= 0.) & (along <= length + 1e-12)))

    def test_sparse_points_retained_and_overflow(self):
        circles = circles_from_points([1., 0., 1.4, 0., 1.8, 0.], .25, .01)
        self.assertEqual(len(circles), 3)
        angles = np.linspace(0., 2. * np.pi, 10, endpoint=False)
        self.node.scan.xy = (1.5 * np.column_stack((np.cos(angles), np.sin(angles)))).ravel().tolist()
        self.node.solve()
        self.assertFalse(self.received)

    def test_four_meter_range(self):
        circles = circles_from_points([4., 0., 4.001, 0., 5., 0.], .25, .01)
        self.assertEqual(len(circles), 1)
        np.testing.assert_allclose(circles[0].center, [4., 0.])
        self.assertEqual(circles_from_points([4.001, 0.], .25, .01), [])
        self.node.solve()  # setUp scan is entirely beyond 4 m: still valid input.
        self.assertEqual(len(self.received), 1)

    def test_goal_reached(self):
        self.node.goal[:] = 0
        self.node.solve()
        self.assertEqual(len(self.received), 1)
        self.assertEqual(self.received[0].twist.linear.x, 0.)

    def test_solver_failure_holds_and_recovers(self):
        from types import SimpleNamespace
        n = self.node
        original = n.controller.compute
        try:
            n.controller.compute = lambda *args, **kwargs: SimpleNamespace(success=False, reason='infeasible', solve_time=.001, max_safety_violation=0.0)
            for _ in range(3):
                n.controller.last_acceleration[:] = [.5, .2]
                n.solve()
                cmd = self.received[-1]
                self.assertEqual(cmd.twist.linear.x, 0.)
                self.assertEqual(cmd.twist.linear.y, 0.)
                self.assertEqual(cmd.twist.angular.z, 0.)
                self.assertAlmostEqual(cmd.twist.linear.z, -.5)
                self.assertEqual(cmd.header.stamp, n.scan.header.stamp)
                np.testing.assert_allclose(n.controller.last_acceleration, 0.)
            n.controller.compute = lambda *args, **kwargs: SimpleNamespace(success=True, velocity_command=np.array([.1,.05]), solve_time=.001, max_safety_violation=0.0)
            n.solve()
            self.assertAlmostEqual(self.received[-1].twist.linear.x,.1)
            self.assertAlmostEqual(self.received[-1].twist.linear.y,.05)
            self.assertEqual(self.received[-1].twist.angular.z,0.)
        finally:
            n.controller.compute = original

    def test_solver_exception_and_nonfinite_result_hold(self):
        from types import SimpleNamespace
        n = self.node
        original = n.controller.compute
        def fail(*args, **kwargs):
            raise RuntimeError('IPOPT infeasible')
        try:
            for compute in (fail, lambda *args, **kwargs: SimpleNamespace(
                    success=True, velocity_command=np.array([float('nan'),.2]), solve_time=.001, max_safety_violation=0.0)):
                n.controller.compute = compute
                n.solve()
                self.assertEqual(self.received[-1].twist.linear.x,0.)
                self.assertEqual(self.received[-1].twist.angular.z,0.)
        finally:
            n.controller.compute = original

    def test_real_infeasible_solver_publishes_hold(self):
        n = self.node
        # With an obstacle surrounding the initial pose, bounded first-step
        # motion cannot reach the required clearance. Exercise actual IPOPT.
        n.scan.xy = [.2,0.,.21,0.]
        n.solve()
        self.assertEqual(len(self.received),1)
        cmd = self.received[-1]
        self.assertEqual(cmd.twist.linear.x,0.)
        self.assertEqual(cmd.twist.linear.y,0.)
        self.assertEqual(cmd.twist.angular.z,0.)
        np.testing.assert_allclose(n.controller.last_acceleration,0.)

    def test_lateral_velocity_is_independent_of_body_yaw(self):
        n = self.node
        n.state.pose.orientation.z = math.sin(math.pi / 4)
        n.state.pose.orientation.w = math.cos(math.pi / 4)
        n.history.clear()
        n.on_state(n.state)
        n.goal[:] = [0., 2., 0.]
        n.solve()
        self.assertEqual(len(self.received), 1)
        self.assertAlmostEqual(self.received[0].twist.linear.x, 0., places=5)
        self.assertGreater(self.received[0].twist.linear.y, 0.)
        self.assertEqual(self.received[0].twist.angular.z,0.)
        # Keep the same map goal while pointing north instead of east.
        n.state.pose.orientation.z, n.state.pose.orientation.w = 0., 1.
        n.history.clear()
        n.on_state(n.state)
        n.solve()
        self.assertAlmostEqual(self.received[-1].twist.linear.x,0.,places=5)
        self.assertGreater(self.received[-1].twist.linear.y,0.)

    def test_obstacle_publication(self):
        from drone_integration.control.obstacle_detection import DetectedCircle
        n = self.node
        original = n.obstacles_pub
        captured = []
        try:
            n.obstacles_pub = type('Capture', (), {'publish': lambda _, msg: captured.append(msg)})()
            circles = [DetectedCircle(np.array([1., 0.]), .3)] * (n.cfg.max_obstacles + 1)
            n.publish_obstacles(n.scan, circles, np.array([2., 3., math.pi / 2]))
            msg = captured[0]
            self.assertEqual(msg.header.stamp, n.scan.header.stamp)
            self.assertEqual(msg.header.frame_id, 'map_ned')
            np.testing.assert_allclose(np.asarray(msg.xy).reshape(-1, 2), [[2., 4.]] * len(circles))
            self.assertTrue(msg.over_capacity)
            self.assertAlmostEqual(msg.safe_radius[0], .3 + n.cfg.drone_radius + n.cfg.safety_margin)
        finally:
            n.obstacles_pub = original

    def test_obstacle_constraints(self):
        from drone_integration.control.obstacle_detection import DetectedCircle
        c = self.node.controller
        obstacle = DetectedCircle(np.array([1.5, 0.]), .3)
        result = c.compute([0., 0., 0., 0.], [4., 0.], [obstacle])
        self.assertTrue(result.success, result.reason)
        distances = np.linalg.norm(result.predicted_states[1:, :2] - obstacle.center, axis=1)
        self.assertGreaterEqual(float(distances.min()), .3 + c.cfg.drone_radius + c.cfg.safety_margin - .003)
        self.assertLessEqual(np.linalg.norm(result.velocity_command), c.cfg.max_speed + 1e-5)
        self.assertLessEqual(np.linalg.norm(result.acceleration), c.cfg.max_acceleration + 1e-5)

    def test_frd_right_obstacle_at_east_heading_is_south(self):
        from drone_integration.control.obstacle_detection import DetectedCircle
        obstacles = self.node.controller._transform_obstacles(
            np.array([2.,3.,0.,0.]), [DetectedCircle(np.array([0.,2.]), .1)], body_yaw=math.pi/2)
        np.testing.assert_allclose(obstacles[0].center, [0.,3.], atol=1e-12)

    def test_altitude_hold_climb_and_descend_ned(self):
        n = self.node
        n.goal[:] = [0.,0.,-1.]
        for down, expected in ((-.5,-.5), (-1.,0.), (-1.5,.5)):
            n.state.pose.position.z = down
            n.solve()
            self.assertAlmostEqual(self.received[-1].twist.linear.z, expected)

    def test_legacy_flu_scan_is_rejected(self):
        self.node.scan.header.frame_id = 'base_link'
        self.node.solve()
        self.assertFalse(self.received)

    def test_measured_velocity_is_used_and_yaw_is_only_a_transform(self):
        from types import SimpleNamespace
        n = self.node
        original = n.controller.compute
        captured = []
        def compute(state, goal, detections, **kwargs):
            captured.append((state.copy(), kwargs))
            return SimpleNamespace(success=True, velocity_command=np.array([.12,-.08]), solve_time=.001, max_safety_violation=0.0)
        try:
            n.state.twist.linear.x, n.state.twist.linear.y = .3,-.2
            n.controller.compute = compute
            n.solve()
            np.testing.assert_allclose(captured[-1][0],[0.,0.,.3,-.2])
            self.assertIn('body_yaw',captured[-1][1])
            cmd = self.received[-1]
            np.testing.assert_allclose([cmd.twist.linear.x,cmd.twist.linear.y],[.12,-.08])
            self.assertEqual(cmd.twist.angular.z,0.)
        finally:
            n.controller.compute = original

    def test_invalid_measured_velocity_is_rejected(self):
        self.node.state.twist.linear.x = float('nan')
        self.node.solve()
        self.assertFalse(self.received)


if __name__ == '__main__':
    unittest.main()
