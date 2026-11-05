import json,time
from pathlib import Path
from dataclasses import fields
import numpy as np,yaml
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.obstacle_detection import DetectedCircle
p=yaml.safe_load(Path('drone_integration_ws/src/drone_integration/config/sils.yaml').read_text())['mpc_node']['ros__parameters'];cfg=MPCConfig(**dict({f.name:p[f.name] for f in fields(MPCConfig) if f.name in p},control_dt=1/p['publish_rate']))
# NED horizontal coordinates: [north,east] = [ENU y,ENU x].
centers=np.array([[.2,4],[-.2,8]]);radius=.35;goal=np.array([0.,12.]);state=np.zeros(4);c=MPCController(cfg,reference_start=[0,0]);queue=[np.zeros(2) for _ in range(3)];trajectory=[state.tolist()];failures=[];times=[];gap=100.;solver=[]
orig=c.backend.solver.solve
def solve():
 t=time.perf_counter()
 try:return orig()
 finally:solver.append((time.perf_counter()-t)*1000)
c.backend.solver.solve=solve
for k in range(1600):
 cmd=np.zeros(2)
 if np.linalg.norm(state[:2]-goal)>.15 or np.linalg.norm(state[2:])>.05:
  detections=[DetectedCircle(center-state[:2],radius) for center in centers if np.linalg.norm(center-state[:2])<=4.]
  t=time.perf_counter();r=c.compute(state,goal,detections);times.append((time.perf_counter()-t)*1000)
  if r.success:cmd=r.velocity_command
  else:failures.append(k)
 else:c.last_acceleration[:]=0
 norm=np.linalg.norm(cmd)
 if norm>1:cmd=cmd/norm
 queue.append(cmd);u=queue.pop(0);a=1.1400490155*(u-state[2:]);state[:2]+=.05*state[2:]+.5*.05**2*a;state[2:]+=.05*a;trajectory.append(state.tolist());gap=min(gap,float(np.linalg.norm(centers-state[:2],axis=1).min()-radius-cfg.drone_radius))
a=np.array(trajectory);cross=[int(np.argmin(abs(a[:,1]-v))) for v in (4,8)]
r=dict(description='Offline lag-model trial with conservative radius 0.35m obstacle circles, 4m detection range, 1m/s command cap; NOT Gazebo or LiDAR validation.',trajectory=trajectory,centers=centers.tolist(),radius=radius,goal=goal.tolist(),failures=failures,min_gap=gap,at_obstacles_north=a[cross,0].tolist(),final_error=float(np.linalg.norm(state[:2]-goal)),last10s_error=float(np.linalg.norm(a[-200:,:2]-goal,axis=1).max()),solver_median_ms=float(np.median(solver)),solver_max_ms=max(solver),compute_median_ms=float(np.median(times)),compute_max_ms=max(times),over50=sum(t>50 for t in times))
Path('sils_sim/results/two_obstacle_s_turn/trial.json').write_text(json.dumps(r));print(json.dumps({k:v for k,v in r.items() if k!='trajectory'},indent=2))
