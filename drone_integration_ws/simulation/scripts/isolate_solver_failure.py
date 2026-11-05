"""Isolate initial-position sensitivity in the saved failing offline case."""
import json
from pathlib import Path
import numpy as np
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.obstacle_detection import DetectedCircle
root=Path(__file__).resolve().parents[3]/'sils_sim/results/solver_repeatability'
r=json.loads((root/'s0_r07.json').read_text());report=json.loads((root/'summary.json').read_text())
b=json.loads((root.parent/'terminal_tuning_v2/latest/comparison.json').read_text())
ref=np.array(b['reference']);cfg=MPCConfig(**report['config']);out=[]
for label,pos,velocity,center,radius in [
 ('baseline',ref[0],[0.,0.],b['center'],b['radius']),
 ('initial_position_only',r['initial'][:2],[0.,0.],b['center'],b['radius']),
 ('all_except_initial_position',ref[0],r['initial'][2:],r['center'],r['radius']),
 ('all_changes',r['initial'][:2],r['initial'][2:],r['center'],r['radius'])]:
 c=MPCController(cfg,reference_start=ref[0]);c.warmup();state=np.r_[pos,velocity];center=np.array(center)
 failure=None
 for k in range(600):
  prev=c.last_acceleration.copy();side=c.preferred_side;initialized=c._branch_initialized
  result=c.compute(state,ref[1],[DetectedCircle(center-state[:2],radius)])
  if not result.success:
   failure=dict(step=k,time_s=k*cfg.control_dt,reason=result.reason,state=state.tolist(),
                previous_acceleration=prev.tolist(),preferred_side=side,branch_initialized=initialized)
   break
  state=result.predicted_states[1].copy()
  if np.linalg.norm(state[:2]-ref[1])<.15 and np.linalg.norm(state[2:])<.05:break
 reached=np.linalg.norm(state[:2]-ref[1])<.15 and np.linalg.norm(state[2:])<.05
 row=dict(case=label,reached=bool(reached),failure=failure,steps=k+1,center=center.tolist(),radius=radius)
 out.append(row);print(label,'reached=',reached,'failed_step=',failure['step'] if failure else None,flush=True)
 (root/'initial_position_ablation.json').write_text(json.dumps(out,indent=2))
