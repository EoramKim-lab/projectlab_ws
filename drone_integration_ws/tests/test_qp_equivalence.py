"""Direct QP compared with an independently assembled relaxed IPOPT oracle."""
import importlib.util
from pathlib import Path
import sys
import unittest
import numpy as np
import casadi as ca
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.qp_backend import stage_matrices

path=Path(__file__).parent/'fixtures/mpc_controller_ipopt_reference.py'
spec=importlib.util.spec_from_file_location('drone_integration.control._ipopt_reference',path)
reference=importlib.util.module_from_spec(spec);sys.modules[spec.name]=reference;source=path.read_text()
for bound in ('opti.subject_to(ca.sumsqr(X[2:, k + 1]) <= cfg.max_speed**2)', 'opti.subject_to(ca.sumsqr(U[:, k]) <= cfg.max_acceleration**2)'):
    assert source.count(bound)==1
    source=source.replace(bound,'pass  # Deliberately removed norm bound')
exec(compile(source,str(path),'exec'),reference.__dict__)

class QpEquivalence(unittest.TestCase):
    def test_stage_cost_and_dynamics_match_original_formula(self):
        rng=np.random.default_rng(1102)
        for soft in (False,True):
            cfg=MPCConfig(horizon_steps=5,max_obstacles=3,soft_safety_margin=soft)
            for h in (.05,.15):
                A,B,Q,R,S,W=stage_matrices(cfg,h)
                H=np.block([[Q,S.T],[S,R]])
                self.assertGreaterEqual(np.linalg.eigvalsh(H).min(),-1e-12)
                for _ in range(10):
                    state=rng.normal(size=6);control=rng.normal(size=B.shape[1]);ref=rng.normal(size=4)
                    if soft:control[2:]=rng.uniform(0,.2,3)
                    a=control[:2];nxt=np.r_[state[:2]+h*state[2:4]+.5*h*h*a,state[2:4]+h*a]
                    expected=h*(cfg.q_position*np.sum((nxt[:2]-ref[:2])**2)+cfg.q_velocity*np.sum((nxt[2:]-ref[2:])**2)+cfg.r_acceleration*np.sum(a*a)+cfg.r_delta_acceleration*np.sum((a-state[4:])**2))
                    q=-2*h*A[:4].T@W@ref;r=-2*h*B[:4].T@W@ref
                    if soft:
                        expected+=h*np.sum(cfg.safety_slack_linear*control[2:]+cfg.safety_slack_quadratic*control[2:]**2)
                        r[2:]+=h*cfg.safety_slack_linear
                    z=np.r_[state,control]
                    got=.5*z@H@z+q@state+r@control+h*ref@W@ref
                    np.testing.assert_allclose(A@state+B@control,np.r_[nxt,a],atol=1e-12)
                    self.assertAlmostEqual(got,expected,places=10)

    def test_norm_bounds_are_removed(self):
        c=MPCController(MPCConfig(horizon_steps=20,max_speed=1,max_acceleration=1,soft_safety_margin=True))
        result=c.compute([0,0,2,0],[0,0],[])
        self.assertTrue(result.success,result.reason)
        self.assertGreater(np.linalg.norm(result.predicted_states[1:,2:],axis=1).max(),1.)
        self.assertGreater(np.linalg.norm(result.predicted_accelerations,axis=1).max(),1.)

    def test_contradictory_planes_fail_and_next_solve_recovers(self):
        c=MPCController(MPCConfig(horizon_steps=20,max_obstacles=2,soft_safety_margin=True))
        state=np.zeros(4);pref,vref,_,direction=c._reference(state,[3,0])
        u=np.zeros((c.N,2));nominal=c._rollout(state,u,c.step_sizes)
        normals=np.zeros((2,2*c.N));normals[0,:c.N]=1;normals[0,c.N:]=-1
        planes=(normals,np.zeros((2,2)),np.ones(2),np.ones(2))
        with self.assertRaises(RuntimeError):c._solve_once(state,pref,vref,u,nominal,planes)
        result=c.compute(state,[3,0],[])
        self.assertTrue(result.success,result.reason)

    def test_same_frozen_problem_has_same_optimum(self):
        from dataclasses import asdict
        cfg=MPCConfig(horizon_steps=20,max_obstacles=2,max_speed=1.,max_acceleration=1.,soft_safety_margin=True,safety_slack_linear=5.,safety_slack_quadratic=50.,q_terminal_velocity=16.)
        actual=MPCController(cfg,reference_start=[0,0]);oracle=reference.MPCController(reference.MPCConfig(**asdict(cfg)),reference_start=[0,0])
        for initial,goal,center,radius in [([0,0,0,0],[3,0],[2,.7],.3),([.1,-.1,.2,.05],[2,1],[1.5,-.8],.3),([0,0,.3,0],[0,0],[3,2],.3)]:
            actual.reset();oracle.reset();state=np.array(initial,float);pref,vref,_,direction=actual._reference(state,goal)
            from drone_integration.control.obstacle_detection import DetectedCircle
            obs=actual._transform_obstacles(state,[DetectedCircle(np.array(center)-state[:2],radius)],0.)
            acceleration=actual._seed_controls(state,pref,direction,obs,1);nominal=actual._rollout(state,acceleration,actual.step_sizes);planes=actual._make_planes(nominal,obs,1,direction)
            a=actual._solve_once(state,pref,vref,acceleration,nominal,planes);b=oracle._solve_once(state,pref,vref,acceleration,nominal,planes)
            self.assertAlmostEqual(a[2],b[2],delta=2e-3*max(1,abs(b[2])))
            np.testing.assert_allclose(a[0],b[0],atol=2e-3,rtol=2e-3)
            np.testing.assert_allclose(a[1],b[1],atol=5e-3,rtol=5e-3)

if __name__=='__main__':unittest.main()
