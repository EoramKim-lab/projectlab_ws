"""Repeated validation of per-obstacle bypass refresh; all weights unchanged.
Offline log-fitted velocity lag model, not Gazebo/LiDAR validation.
"""
import hashlib,json,time
from dataclasses import asdict,fields,replace
from pathlib import Path
import numpy as np,yaml
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.obstacle_detection import DetectedCircle
ROOT=Path(__file__).resolve().parents[3];out=ROOT/'sils_sim/results/bypass_refresh_repeated';out.mkdir(exist_ok=True)
config=ROOT/'drone_integration_ws/src/drone_integration/config/sils.yaml';p=yaml.safe_load(config.read_text())['mpc_node']['ros__parameters'];base=MPCConfig(**dict({f.name:p[f.name] for f in fields(MPCConfig) if f.name in p},control_dt=1/p['publish_rate']))
cases=[dict(name='nominal',initial=[0,0,0,0],gain=1.1400490155,delay=.15),dict(name='initial_left',initial=[.02,-.02,.03,-.03],gain=1.1400490155,delay=.15),dict(name='initial_right',initial=[-.02,.02,-.03,.03],gain=1.1400490155,delay=.15),dict(name='slower',initial=[0,0,0,0],gain=.8,delay=.2),dict(name='delay_200ms',initial=[0,0,0,0],gain=1.1690876,delay=.2)]
paths=[config,ROOT/'sils_sim/worlds/projectlab.sdf',*list((ROOT/'drone_integration_ws/src/drone_integration/drone_integration/control').glob('*.py'))]
plan=dict(description=__doc__,base=asdict(base),weights=[8.],repeats=2,cases=cases,duration_s=80,goal=[0,12],centers=[[.2,4],[-.2,8]],radius=.35,hold_s=10,position_gate=.15,speed_gate=.05,strict_accuracy=.05,deadline_ms=50,hashes={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths})
if (out/'plan.json').exists():
 assert json.loads((out/'plan.json').read_text())==plan,'Refuse mixing different conditions in existing results'
else:(out/'plan.json').write_text(json.dumps(plan,indent=2))
def stats(x):
 return dict(n=len(x),median_ms=float(np.median(x)),max_ms=max(x),over50=sum(t>50 for t in x))
def run(q,case):
 cfg=replace(base,q_position=q);centers=np.array(plan['centers']);radius=plan['radius'];goal=np.array(plan['goal']);x=np.array(case['initial'],float);c=MPCController(cfg,reference_start=[0,0]);c.warmup();queue=[x[2:].copy() for _ in range(round(case['delay']/.05))];traj=[x.tolist()];fail=[];times=[];solver=[];gap=100.;slack=0.;orig=c.backend.solver.solve
 def solve():
  t=time.perf_counter()
  try:return orig()
  finally:solver.append((time.perf_counter()-t)*1000)
 c.backend.solver.solve=solve
 for k in range(1600):
  cmd=np.zeros(2)
  if np.linalg.norm(x[:2]-goal)>.15 or np.linalg.norm(x[2:])>.05:
   det=[DetectedCircle(center-x[:2],radius) for center in centers if np.linalg.norm(center-x[:2])<=4.]
   t=time.perf_counter();r=c.compute(x,goal,det);times.append((time.perf_counter()-t)*1000)
   if r.success:cmd=r.velocity_command;slack=max(slack,r.max_safety_violation)
   else:fail.append(dict(step=k,reason=r.reason))
  else:c.last_acceleration[:]=0
  norm=np.linalg.norm(cmd)
  if norm>1:cmd=cmd/norm
  queue.append(cmd);u=queue.pop(0);acc=case['gain']*(u-x[2:]);x[:2]+=.05*x[2:]+.5*.05**2*acc;x[2:]+=.05*acc;traj.append(x.tolist());gap=min(gap,float(np.linalg.norm(centers-x[:2],axis=1).min()-radius-cfg.drone_radius))
 a=np.array(traj);cross=[]
 for along in (4.,8.):
  idx=np.flatnonzero((a[:-1,1]<along)&(a[1:,1]>=along))
  if len(idx):
   i=idx[0];alpha=(along-a[i,1])/(a[i+1,1]-a[i,1]);cross.append(float(a[i,0]+alpha*(a[i+1,0]-a[i,0])))
  else:cross.append(None)
 err=np.linalg.norm(a[:,:2]-goal,axis=1);speed=np.linalg.norm(a[:,2:],axis=1);s_turn=all(v is not None for v in cross) and cross[0]<0 and cross[1]>0
 return dict(trajectory=traj,failures=fail,s_turn=bool(s_turn),crossing_north=cross,physical_min_gap=gap,max_slack=slack,max_lateral=float(abs(a[:,0]).max()),path_length=float(np.linalg.norm(np.diff(a[:,:2],axis=0),axis=1).sum()),final_error=float(err[-1]),last10s_max_error=float(err[-200:].max()),last10s_max_speed=float(speed[-200:].max()),hold_pass=bool((err[-200:]<=.15).all() and (speed[-200:]<=.05).all()),strict_5cm=bool((err[-200:]<=.05).all() and (speed[-200:]<=.05).all()),solver=stats(solver),compute=stats(times))
rows=[]
for q in plan['weights']:
 for i,case in enumerate(cases):
  for rep in range(plan['repeats']):
   path=out/f'q{q:g}_case{i}_repeat{rep}.json'
   r=json.loads(path.read_text()) if path.exists() else run(q,case)
   path.write_text(json.dumps(r));row=dict(q_position=q,case=case['name'],repeat=rep,failed_cycles=len(r['failures']),**{k:v for k,v in r.items() if k not in ('trajectory','failures')});rows.append(row);(out/'summary.json').write_text(json.dumps(rows,indent=2))
   print('q',q,case['name'],rep,'S',r['s_turn'],'cross',r['crossing_north'],'gap',round(r['physical_min_gap'],3),'hold',r['hold_pass'],'err',round(r['final_error'],3),'max_ms',round(r['compute']['max_ms'],2),flush=True)
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in plan['hashes'].items())
