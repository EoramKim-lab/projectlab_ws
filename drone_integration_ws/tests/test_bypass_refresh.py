"""Regression checks for obstacle-scoped bypass decisions, independent of QP costs."""
import unittest
from unittest.mock import patch
import numpy as np
from drone_integration.control.mpc_controller import MPCConfig,MPCController,MPCResult
from drone_integration.control.obstacle_detection import DetectedCircle

class BypassRefreshTests(unittest.TestCase):
    def setUp(self):
        self.c=MPCController(MPCConfig(horizon_steps=20,soft_safety_margin=True))
        self.c.reference_start=np.zeros(2)
        self.centers=np.array([[.2,4.],[-.2,8.]])
        self.calls=[]
        self.identical=False
        self.mock=patch.object(self.c,'_solve_branch',side_effect=self.solve)
        self.mock.start();self.addCleanup(self.mock.stop)

    def solve(self,state,pref,vref,obstacles,direction,side):
        self.calls.append(side)
        states=np.tile(state,(self.c.N+1,1))
        states[1:,0]+=0 if self.identical else side*.2
        preferred=1 if state[1]<5 else -1
        return MPCResult(True,np.zeros(2),states,branch=side,
                         objective=1. if side==preferred else 2.)

    def compute(self,east,missing=False,reverse=False):
        state=np.array([0.,east,0.,0.])
        centers=self.centers[::-1] if reverse else self.centers
        detections=[] if missing else [DetectedCircle(x-state[:2],.35) for x in centers]
        self.calls.clear()
        return self.c.compute(state,[0,12],detections)

    def test_next_obstacle_gets_fresh_comparison_and_can_reverse_direction(self):
        self.compute(0)
        self.assertEqual(len(self.calls),2)
        self.assertFalse(self.c._branch_initialized)
        first=self.compute(2)
        self.assertEqual(len(self.calls),2)
        self.assertEqual(first.branch,1)
        np.testing.assert_array_equal(self.c._bypass_obstacle.center,self.centers[0])
        self.compute(3,reverse=True)
        self.assertEqual(self.calls,[1])
        self.compute(4.8)  # still inside first obstacle's longitudinal safety extent
        self.assertEqual(self.calls,[1])
        self.compute(5)
        self.assertEqual(len(self.calls),2)
        self.assertFalse(self.c._branch_initialized)
        second=self.compute(6)
        self.assertEqual(len(self.calls),2)
        self.assertEqual(second.branch,-1)
        np.testing.assert_array_equal(self.c._bypass_obstacle.center,self.centers[1])
        self.compute(7)
        self.assertEqual(self.calls,[-1])

    def test_detection_dropout_does_not_unlock_mid_pass(self):
        self.compute(2)
        self.compute(3,missing=True)
        self.assertEqual(self.calls,[1])
        self.assertTrue(self.c._branch_initialized)
        self.compute(5,missing=True)
        self.assertEqual(len(self.calls),2)
        self.assertFalse(self.c._branch_initialized)

    def test_equivalent_candidates_do_not_lock_before_avoidance(self):
        self.identical=True
        self.compute(2)
        self.assertFalse(self.c._branch_initialized)
        self.compute(2.1)
        self.assertEqual(len(self.calls),2)
        self.identical=False
        self.compute(2.2)
        self.assertTrue(self.c._branch_initialized)

    def test_reset_and_warmup_preserve_encounter_lifecycle(self):
        self.compute(2)
        obstacle=self.c._bypass_obstacle
        self.c.warmup()
        self.assertTrue(self.c._branch_initialized)
        self.assertIs(self.c._bypass_obstacle,obstacle)
        self.c.reset()
        self.assertFalse(self.c._branch_initialized)
        self.assertIsNone(self.c._bypass_obstacle)
        self.assertIsNone(self.c._bypass_direction)

if __name__=='__main__':unittest.main()
