"""Numerical MPC checks with the real solver, independent of ROS/flight hardware."""
import math
import unittest
import numpy as np

from drone_integration.control.mpc_controller import MPCConfig, MPCController
from drone_integration.control.obstacle_detection import DetectedCircle


class CartesianMpcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller = MPCController()

    def setUp(self):
        self.controller.reset()
        self.controller.reference_start = None

    def test_prediction_obeys_double_integrator(self):
        c = self.controller
        initial = np.array([.2,-.3,.25,-.1])
        result = c.compute(initial,[3.,2.],[])
        self.assertTrue(result.success,result.reason)
        X, A = result.predicted_states, result.predicted_accelerations
        self.assertEqual(X.shape,(c.N+1,4))
        self.assertEqual(A.shape,(c.N,2))
        np.testing.assert_allclose(X[0],initial,atol=1e-8)
        h = c.step_sizes[:,None]
        np.testing.assert_allclose(X[1:,:2],X[:-1,:2]+h*X[:-1,2:]+.5*h*h*A,atol=1e-8)
        np.testing.assert_allclose(X[1:,2:],X[:-1,2:]+h*A,atol=1e-8)
        self.assertTrue(np.isfinite(X).all() and np.isfinite(A).all())
        np.testing.assert_allclose(result.velocity_command,X[1,2:])

    def test_sideways_and_reverse_motion_do_not_require_yaw(self):
        c = self.controller
        for goal in ([0.,3.],[-3.,0.],[2.,2.]):
            c.reset()
            result = c.compute(np.zeros(4),goal,[],body_yaw=math.pi/2)
            self.assertTrue(result.success,result.reason)
            direction = np.array(goal)/np.linalg.norm(goal)
            self.assertGreater(float(result.velocity_command@direction),0.)
            np.testing.assert_allclose(result.velocity_command,
                                       np.linalg.norm(result.velocity_command)*direction,atol=1e-5)

    def test_yaw_does_not_rotate_map_velocity_command(self):
        c = self.controller
        a = c.compute([0.,0.,.1,.05],[2.,1.],[],body_yaw=0.)
        c.reset()
        b = c.compute([0.,0.,.1,.05],[2.,1.],[],body_yaw=math.pi/2)
        self.assertTrue(a.success and b.success)
        np.testing.assert_allclose(a.velocity_command,b.velocity_command,atol=1e-6)

    def test_measured_velocity_changes_first_command(self):
        c = self.controller
        result = c.compute([0.,0.,0.,.4],[3.,0.],[])
        self.assertTrue(result.success,result.reason)
        c.reset()
        stationary=c.compute([0.,0.,0.,0.],[3.,0.],[])
        self.assertGreater(result.velocity_command[1],stationary.velocity_command[1])
        self.assertLess(result.acceleration[1],0.)

    def test_goal_brakes_measured_motion(self):
        c = self.controller
        result = c.compute([0.,0.,.3,0.],[0.,0.],[])
        self.assertTrue(result.success,result.reason)
        self.assertLess(result.velocity_command[0],.3)
        self.assertLess(result.acceleration[0],0.)

    def test_infeasible_problem_holds_and_next_feasible_problem_recovers(self):
        c = self.controller
        from unittest.mock import patch
        with patch.object(c.backend,'solve',side_effect=RuntimeError('infeasible QP')):
            impossible = c.compute(np.zeros(4),[3.,0.],[])
        self.assertFalse(impossible.success)
        np.testing.assert_allclose(impossible.velocity_command,0.)
        np.testing.assert_allclose(c.last_acceleration,0.)
        recovered = c.compute(np.zeros(4),[3.,0.],[])
        self.assertTrue(recovered.success,recovered.reason)
        self.assertGreater(recovered.velocity_command[0],0.)

    def test_bad_state_and_obstacle_capacity_are_rejected(self):
        c = self.controller
        for state in ([0.,0.,0.],[0.,0.,float('nan'),0.]):
            with self.assertRaises(ValueError):
                c.compute(state,[2.,0.],[])
        with self.assertRaises(ValueError):
            c.compute(np.zeros(4),[2.,0.],[DetectedCircle(np.array([2.,0.]),.1)]*(c.cfg.max_obstacles+1))

    def test_receding_horizon_bypasses_obstacle_and_rejoins_reference(self):
        c = MPCController(MPCConfig(control_dt=.1),reference_start=[0.,0.])
        state, goal, center = np.zeros(4), np.array([4.,0.]), np.array([2.,0.])
        minimum, lateral = math.inf, 0.
        for _ in range(120):
            result = c.compute(state,goal,[DetectedCircle(center-state[:2],.2)])
            self.assertTrue(result.success,result.reason)
            state = result.predicted_states[1].copy()
            minimum = min(minimum,float(np.linalg.norm(state[:2]-center)))
            lateral = max(lateral,abs(state[1]))
            if np.linalg.norm(state[:2]-goal)<.12 and np.linalg.norm(state[2:])<.1:
                break
        self.assertLess(float(np.linalg.norm(state[:2]-goal)),.12)
        self.assertGreater(lateral,.5)
        self.assertGreaterEqual(minimum,.2+c.cfg.drone_radius+c.cfg.safety_margin-.003)


class SoftSafetyTests(unittest.TestCase):
    def test_soft_buffer_preserves_physical_clearance_and_slack_cap(self):
        obstacle = DetectedCircle(np.array([.55, 0.]), .1)
        hard = MPCController(MPCConfig(horizon_steps=20, max_obstacles=1))
        hard_result=hard.compute(np.zeros(4), [-2., 0.], [obstacle])
        self.assertTrue(hard_result.success,hard_result.reason)
        self.assertLessEqual(hard_result.max_safety_violation,.003)
        soft = MPCController(MPCConfig(horizon_steps=20, max_obstacles=1,
                                       soft_safety_margin=True))
        result = soft.compute(np.zeros(4), [-2., 0.], [obstacle])
        self.assertTrue(result.success, result.reason)
        self.assertLess(result.velocity_command[0], 0.)
        self.assertGreater(result.max_safety_violation, .05)
        self.assertLessEqual(result.max_safety_violation, .20 + .003)
        distance = np.linalg.norm(result.predicted_states[1:, :2] - obstacle.center, axis=1)
        self.assertGreaterEqual(distance.min(), .45 - .003)

    def test_future_positions_respect_physical_radius_from_overlapping_initial_state(self):
        soft = MPCController(MPCConfig(horizon_steps=20, max_obstacles=1,
                                       soft_safety_margin=True))
        result = soft.compute(np.zeros(4), [-2., 0.],
                              [DetectedCircle(np.array([.3, 0.]), .1)])
        self.assertTrue(result.success,result.reason)
        distance=np.linalg.norm(result.predicted_states[1:,:2]-[.3,0.],axis=1)
        self.assertGreaterEqual(distance.min(),.45-.003)
        self.assertLessEqual(soft.backend.last_slacks.max(),.2+1e-7)
        self.assertGreaterEqual(soft.backend.last_slacks.min(),-1e-7)

    def test_penalty_must_be_positive_and_finite(self):
        for name in ('safety_slack_linear', 'safety_slack_quadratic'):
            for value in (0., -1., float('nan')):
                with self.assertRaises(ValueError):
                    MPCConfig(**{name: value})


if __name__=='__main__':
    unittest.main()
