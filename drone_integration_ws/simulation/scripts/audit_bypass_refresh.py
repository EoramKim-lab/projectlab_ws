import json
from pathlib import Path
from dataclasses import fields
import numpy as np,yaml
from drone_integration.control.mpc_controller import MPCController,MPCConfig
from drone_integration.control.obstacle_detection import DetectedCircle
root=Path('/home/yjh/projectlab_ws');out=root/'sils_sim/results/two_obstacle_s_turn'
p=yaml.safe_load((root/'drone_integration_ws/src/drone_integration/config/sils.yaml').read_text())['mpc_node']['ros__parameters'];cfg=MPCConfig(**dict({f.name:p[f.name] for f in fields(MPCConfig) if f.name in p},control_dt=1/p['publish_rate']))
trial=json.loads((out/'trial.json').read_text());states=np.array(trial['trajectory']);centers=np.array(trial['centers']);goal=np.array(trial['goal']);c=MPCController(cfg,reference_start=[0,0]);c.warmup();orig=c._solve_branch;calls=[];trace=[];probes=[]
def wrapped(*args):
 r=orig(*args);calls.append(dict(side=int(args[-1]),success=r.success,objective=float(r.objective)));return r
c._solve_branch=wrapped
indices={int(np.argmin(abs(states[:,1]-distance))):distance for distance in (0,3,4,5,6,6.5,7,8,9)}
for k,x in enumerate(states[:-1]):
 if np.linalg.norm(x[:2]-goal)<=.15 and np.linalg.norm(x[2:])<=.05:
  c.last_acceleration[:]=0;continue
 det=[DetectedCircle(center-x[:2],trial['radius']) for center in centers if np.linalg.norm(center-x[:2])<=4.]
 before_side=c.preferred_side;before_initialized=c._branch_initialized;previous_acceleration=c.last_acceleration.copy();calls.clear();r=c.compute(x,goal,det)
 trace.append(dict(step=k,east=float(x[1]),initialized_before=before_initialized,preferred_before=before_side,selected=r.branch,calls=list(calls)))
 if k in indices:
  # Diagnostic only: solve both candidates with precisely the same state/history.
  updated_acceleration=c.last_acceleration.copy();c.last_acceleration=previous_acceleration
  obs=c._transform_obstacles(x,det);pref,vref,_,direction=c._reference(x,goal);candidates=[]
  for side in (1,-1):
   alt=orig(x,pref,vref,obs,direction,side);candidates.append(dict(side=side,success=alt.success,objective=float(alt.objective),velocity=alt.velocity_command.tolist()))
  c.last_acceleration=updated_acceleration
  probes.append(dict(east=float(x[1]),north=float(x[0]),actual_side=r.branch,candidates=candidates))
summary=dict(description='Offline replay of saved two-obstacle lag-model states. Diagnostic candidate solves do not change the selected branch or acceleration history.',cycles=len(trace),both_candidates_cycles=sum(len(x['calls'])==2 for x in trace),after_first_both_candidates_cycles=sum(len(x['calls'])==2 and x['east']>4.7 for x in trace),selected_sides=sorted(set(x['selected'] for x in trace)),probes=probes)
(out/'branch_refresh_audit.json').write_text(json.dumps(dict(summary=summary,trace=trace),indent=2));print(json.dumps(summary,indent=2))
