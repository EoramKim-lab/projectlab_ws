import time
import numpy as np
from drone_integration.control.mpc_controller import MPCController
from drone_integration.control.obstacle_detection import DetectedCircle
def stats(values):
 a=np.asarray(values)*1000
 return dict(n=len(a),median_ms=float(np.median(a)),p95_ms=float(np.percentile(a,95)),max_ms=float(a.max()),over50=int(np.sum(a>50))) if len(a) else None

def run(cfg,case):
 # Mirror the existing PX4 command-node horizontal cap (1 m/s); no plant/controller changes.
 c=MPCController(cfg,reference_start=case['start']);c.warmup();calls=[];failed_calls=[];cycle=[];reasons=[];orig=c.backend.solver.solve
 def solve():
  before=time.perf_counter();ok=False
  try:r=orig();ok=(r==0);return r
  finally:calls.append(time.perf_counter()-before);failed_calls.append(not ok)
 c.backend.solver.solve=solve;x=np.array(case['initial'],float);goal=np.array(case['goal']);obs=case.get('obstacle');gain=case['gain'];delay=case['delay'];queue=[x[2:].copy() for _ in range(round(delay/.05))];traj=[x.tolist()];gap=None;failures=0;clipped=0;max_acc=0.;max_pred_speed=0.
 for k in range(1200):
  cmd=np.zeros(2)
  if np.linalg.norm(x[:2]-goal)>.15 or np.linalg.norm(x[2:])>.05:
   det=[] if obs is None else [DetectedCircle(np.array(obs['center'])-x[:2],obs['radius'])];before=time.perf_counter();r=c.compute(x,goal,det);cycle.append(time.perf_counter()-before)
   if r.success:
    cmd=r.velocity_command
    max_acc=max(max_acc,float(np.linalg.norm(r.predicted_accelerations,axis=1).max()))
    max_pred_speed=max(max_pred_speed,float(np.linalg.norm(r.predicted_states[:,2:],axis=1).max()))
   else:failures+=1;reasons.append(dict(step=k,reason=r.reason));c.last_acceleration[:]=0
  else:c.last_acceleration[:]=0
  norm=np.linalg.norm(cmd)
  if norm>1.:
   clipped+=1;cmd=cmd/norm
  queue.append(cmd);u=queue.pop(0);acc=gain*(u-x[2:]);x[:2]+=.05*x[2:]+.5*.05**2*acc;x[2:]+=.05*acc;traj.append(x.tolist())
  if obs is not None:
   clearance=float(np.linalg.norm(x[:2]-obs['center'])-obs['radius']-cfg.drone_radius);gap=clearance if gap is None else min(gap,clearance)
   if gap<-.003:break
 a=np.array(traj);err=np.linalg.norm(a[:,:2]-goal,axis=1);speed=np.linalg.norm(a[:,2:],axis=1);complete=len(a)==1201;valid=(err<=.15)&(speed<=.05);bad=np.flatnonzero(~valid);safe=gap is None or gap>=-.003
 return dict(clipped_cycles=clipped,max_predicted_acceleration=max_acc,max_predicted_speed=max_pred_speed,last10s_position_span=float(np.linalg.norm(np.ptp(a[-200:,:2],axis=0))) if complete else None,completed=complete,simulated_s=(len(a)-1)*.05,passed=bool(complete and safe and failures==0 and valid[-200:].all()),strict_5cm_pass=bool(complete and safe and failures==0 and (err[-200:]<=.05).all() and (speed[-200:]<=.05).all()),last10s_max_error=float(err[-200:].max()) if complete else None,last10s_max_speed=float(speed[-200:].max()) if complete else None,final_error=float(err[-1]),final_speed=float(speed[-1]),settle_s=float((bad[-1]+1)*.05) if valid[-1] and len(bad) else None,min_gap=gap,failed_cycles=failures,failed_solver_calls=sum(failed_calls),solver=stats(calls),compute=stats(cycle),trajectory=traj,failure_reasons=reasons)
