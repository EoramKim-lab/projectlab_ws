"""Weight-only tests with a log-fitted PX4 velocity response; no runtime controller edits.
Fixed plant: v_dot=1.14005*(delayed velocity command-v), delay .15s.
This is a local empirical surrogate, not a Gazebo validation.
Preserves the ROS node's 0.15m / 0.05m/s goal gate.
"""
import json,hashlib,time,argparse
from dataclasses import fields,replace,asdict
from pathlib import Path
import numpy as np,yaml
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.obstacle_detection import DetectedCircle
ROOT=Path('/home/yjh/projectlab_ws');PKG=ROOT/'drone_integration_ws/src/drone_integration'
OUT=ROOT/'sils_sim/results/px4_response_weight_tuning';OUT.mkdir(exist_ok=True)
p=yaml.safe_load((PKG/'config/sils.yaml').read_text())['mpc_node']['ros__parameters']
base=MPCConfig(**dict({f.name:p[f.name] for f in fields(MPCConfig) if f.name in p},control_dt=1/p['publish_rate']))
weights=[('baseline',{}),('v4',dict(q_velocity=4.)),('v16',dict(q_velocity=16.,q_terminal_velocity=32.)),('v64',dict(q_velocity=64.,q_terminal_velocity=64.)),('v256',dict(q_velocity=256.,q_terminal_velocity=128.)),('v1024',dict(q_velocity=1024.,q_terminal_velocity=256.))]
def run(cfg,initial,goal,start,gain=1.1400490155,delay=.15,duration=60,obstacle=None,stop_on_collision=False):
 c=MPCController(cfg,reference_start=start);c.warmup();x=np.array(initial,dtype=float);queue=[x[2:].copy() for _ in range(round(delay/.05))];traj=[x.tolist()];failed=0;times=[];gap=1000.
 for step in range(round(duration/.05)):
  cmd=np.zeros(2)
  if np.linalg.norm(x[:2]-goal)>.15 or np.linalg.norm(x[2:])>.05:
   det=[] if obstacle is None else [DetectedCircle(np.array(obstacle['center'])-x[:2],obstacle['radius'])]
   r=c.compute(x,goal,det);times.append(r.solve_time)
   if r.success:cmd=r.velocity_command
   else:failed+=1;c.last_acceleration[:]=0
  else:c.last_acceleration[:]=0
  queue.append(cmd);u=queue.pop(0);acc=gain*(u-x[2:]);x[:2]+=.05*x[2:]+.5*.05**2*acc;x[2:]+=.05*acc;traj.append(x.tolist())
  if obstacle:
   gap=min(gap,np.linalg.norm(x[:2]-obstacle['center'])-obstacle['radius']-cfg.drone_radius)
   if stop_on_collision and gap < -.003:break
 a=np.array(traj);err=np.linalg.norm(a[:,:2]-goal,axis=1);speed=np.linalg.norm(a[:,2:],axis=1);valid=(err<=.15)&(speed<=.05);bad=np.flatnonzero(~valid)
 return dict(completed=bool(len(traj)==round(duration/.05)+1),simulated_seconds=(len(traj)-1)*.05,passed=bool(valid[-200:].all() and failed==0 and gap>=-.003),last10s_max_error=float(err[-200:].max()),last10s_max_speed=float(speed[-200:].max()),last10s_5cm=bool((err[-200:]<=.05).all()),strict_5cm_pass=bool((err[-200:]<=.05).all() and (speed[-200:]<=.05).all() and failed==0 and gap>=-.003),settle_s=float((bad[-1]+1)*.05) if valid[-1] and len(bad) else None,failures=failed,min_gap=gap,max_error=float(err.max()),compute_max_s=max(times,default=0),trajectory=traj)
def main():
 global OUT
 parser=argparse.ArgumentParser();parser.add_argument('--validate',action='store_true');parser.add_argument('--buffer',type=float);parser.add_argument('--velocity',type=float);parser.add_argument('--terminal-velocity',type=float);args=parser.parse_args()
 sources=list((PKG/'drone_integration/control').glob('*.py'));hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
 if not args.validate:
  plan=dict(description=__doc__,base=asdict(base),weights=weights,source_hashes=hashes,initial=[-.276,5.564,-.021,.456],goal=[-.6321283533,5.9591849132],start=[.00010855,-.00741181],duration=60)
  (OUT/'plan.json').write_text(json.dumps(plan,indent=2));rows=[]
  for name,w in weights:
   r=run(replace(base,**w),plan['initial'],np.array(plan['goal']),plan['start']);(OUT/f'{name}.json').write_text(json.dumps(r));row=dict(name=name,weights=w,**{k:v for k,v in r.items() if k!='trajectory'});rows.append(row);(OUT/'summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)
 else:
  rows=json.loads((OUT/'summary.json').read_text());ok=[r for r in rows if r['passed']]
  if not ok:raise RuntimeError('No candidate passed; do not apply weights')
  chosen=min(ok,key=lambda r:r['settle_s'] or 999)
  if args.buffer is not None:
   chosen=dict(chosen,weights=dict(chosen['weights'],safety_slack_linear=args.buffer,safety_slack_quadratic=10*args.buffer));OUT=OUT/f'buffer{args.buffer:g}';OUT.mkdir(exist_ok=True)
  if args.velocity is not None:
   chosen=dict(chosen,weights=dict(chosen['weights'],q_velocity=args.velocity,q_terminal_velocity=args.terminal_velocity));OUT=OUT/f'v{args.velocity:g}';OUT.mkdir(exist_ok=True)
  rng=np.random.default_rng(20261104);cases=[]
  for gain,delay in [(1.1400490155,.15),(.885965096,0),(1.1690876,.2),(.8,.2)]:
   for scenario in ['latest','previous']:
    src=json.loads((ROOT/f'sils_sim/results/terminal_tuning_v2/{scenario}/comparison.json').read_text());ref=np.array(src['reference']);initial=np.r_[ref[0]+rng.uniform(-.02,.02,2),rng.uniform(-.03,.03,2)];obs=dict(center=(np.array(src['center'])+rng.uniform(-.05,.05,2)).tolist(),radius=src['radius']+rng.uniform(-.02,.02));cases.append(dict(gain=gain,delay=delay,initial=initial.tolist(),goal=ref[1].tolist(),start=ref[0].tolist(),obstacle=obs))
  (OUT/'validation_plan.json').write_text(json.dumps(dict(chosen=chosen,cases=cases,source_hashes=hashes),indent=2));res=[]
  for i,case in enumerate(cases):
   r=run(replace(base,**chosen['weights']),**case);(OUT/f'validation_{i}.json').write_text(json.dumps(r));row=dict(case=i,**{k:v for k,v in r.items() if k!='trajectory'});res.append(row);(OUT/'validation_summary.json').write_text(json.dumps(res,indent=2));print(json.dumps(row),flush=True)
 assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in hashes.items())
if __name__=='__main__':main()
