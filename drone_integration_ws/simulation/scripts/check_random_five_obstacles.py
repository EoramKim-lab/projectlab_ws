"""Frozen random world trial using a log-fitted lag model, not Gazebo/LiDAR."""
import json,time,hashlib
from pathlib import Path
from dataclasses import fields,asdict
import numpy as np,yaml
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.obstacle_detection import DetectedCircle
ROOT=Path(__file__).resolve().parents[3];out=ROOT/'sils_sim/results/random_five_obstacles';plan=json.loads((out/'plan.json').read_text())
p=yaml.safe_load((ROOT/'drone_integration_ws/src/drone_integration/config/sils.yaml').read_text())['mpc_node']['ros__parameters'];cfg=MPCConfig(**dict({f.name:p[f.name] for f in fields(MPCConfig) if f.name in p},control_dt=1/p['publish_rate']))
centers=np.array([o['center_enu'][::-1] for o in plan['obstacles']]);radius=plan['conservative_circle_radius'];goal=np.array(plan['reference_enu'][-1][:2][::-1]);cases=[dict(name='nominal',initial=[0,0,0,0],gain=1.1400490155,delay=.15),dict(name='initial_offset',initial=[.02,-.02,.03,-.03],gain=1.1400490155,delay=.15),dict(name='slow_response',initial=[0,0,0,0],gain=.8,delay=.2)]
(out/'test_plan.json').write_text(json.dumps(dict(description=__doc__,cases=cases,config=asdict(cfg),duration_s=140,hold_s=10,command_speed_cap=1.,detection_range=4.,source_sha256=hashlib.sha256((ROOT/'drone_integration_ws/src/drone_integration/drone_integration/control/mpc_controller.py').read_bytes()).hexdigest()),indent=2))
rows=[]
for case in cases:
 state=np.array(case['initial'],float);c=MPCController(cfg,reference_start=[0,0]);c.warmup();queue=[state[2:].copy() for _ in range(round(case['delay']/.05))];trajectory=[state.tolist()];failures=[];times=[];gap=100.;solver=[];events=[];max_visible=0;orig=c.backend.solver.solve
 def solve():
  t=time.perf_counter()
  try:return orig()
  finally:solver.append((time.perf_counter()-t)*1000)
 c.backend.solver.solve=solve
 for k in range(2800):
  cmd=np.zeros(2)
  if np.linalg.norm(state[:2]-goal)>.15 or np.linalg.norm(state[2:])>.05:
   detections=[DetectedCircle(center-state[:2],radius) for center in centers if np.linalg.norm(center-state[:2])<=4.];max_visible=max(max_visible,len(detections));old=c._bypass_obstacle
   t=time.perf_counter();r=c.compute(state,goal,detections);times.append((time.perf_counter()-t)*1000)
   if r.success:cmd=r.velocity_command
   else:failures.append(dict(step=k,reason=r.reason))
   if c._bypass_obstacle is not None and c._bypass_obstacle is not old:events.append(dict(time=k*.05,state=state.tolist(),center=c._bypass_obstacle.center.tolist(),side=r.branch))
  else:c.last_acceleration[:]=0
  norm=np.linalg.norm(cmd)
  if norm>1:cmd=cmd/norm
  queue.append(cmd);u=queue.pop(0);a=case['gain']*(u-state[2:]);state[:2]+=.05*state[2:]+.5*.05**2*a;state[2:]+=.05*a;trajectory.append(state.tolist());gap=min(gap,float(np.linalg.norm(centers-state[:2],axis=1).min()-radius-cfg.drone_radius))
 a=np.array(trajectory);err=np.linalg.norm(a[:,:2]-goal,axis=1);speed=np.linalg.norm(a[:,2:],axis=1)
 r=dict(description=__doc__,case=case['name'],trajectory=trajectory,centers=centers.tolist(),radius=radius,goal=goal.tolist(),failures=failures,min_gap=gap,final_error=float(err[-1]),last10s_error=float(err[-200:].max()),last10s_speed=float(speed[-200:].max()),hold_pass=bool((err[-200:]<=.15).all() and (speed[-200:]<=.05).all()),path_length=float(np.linalg.norm(np.diff(a[:,:2],axis=0),axis=1).sum()),solver_median_ms=float(np.median(solver)),solver_max_ms=max(solver),compute_median_ms=float(np.median(times)),compute_max_ms=max(times),over50=sum(t>50 for t in times),compute_cycles=len(times),max_visible_obstacles=max_visible,branch_events=events)
 (out/f'{case["name"]}.json').write_text(json.dumps(r));row={k:v for k,v in r.items() if k not in ('trajectory','failures','branch_events')};row['failed_cycles']=len(failures);rows.append(row);(out/'summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)
