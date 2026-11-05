"""Horizon30 and weight-only tuning with frozen response-model scenarios.
No controller/gate/speed-limit changes. Only N and declared weights vary.
A surrogate experiment, not a Gazebo flight or realtime scheduling simulation.
"""
import argparse,hashlib,json,time
from dataclasses import asdict,replace
from pathlib import Path
import numpy as np
from tune_px4_response_weights import base,ROOT,PKG
from drone_integration.control.mpc_controller import MPCController
from drone_integration.control.obstacle_detection import DetectedCircle
out=ROOT/'sils_sim/results/horizon30_tuning';out.mkdir(exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['screen','validate','terminal']);args=parser.parse_args()
if not (out/'plan.json').exists():
 cases=json.loads((ROOT/'sils_sim/results/px4_response_weight_tuning/buffer20/validation_plan.json').read_text())['cases']
 profiles={'N20_current':{},'N30_current':{'horizon_steps':30}}
 for name,v,tv,soft in [('v16',16,32,20),('v64',64,64,20),('v64_tv128',64,128,20),('v256',256,128,20),('v256_buffer50',256,128,50)]:profiles['N30_'+name]=dict(horizon_steps=30,q_velocity=float(v),q_terminal_velocity=float(tv),safety_slack_linear=float(soft),safety_slack_quadratic=10.*soft)
 plan=dict(description=__doc__,base=asdict(base),profiles=profiles,cases=cases,screen_cases=[0,6],duration=60,hold_seconds=10,position_gate=.15,speed_gate=.05,strict_accuracy=.05,physical_tolerance=.003,source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PKG/'drone_integration/control').glob('*.py')},config_hash=hashlib.sha256((PKG/'config/sils.yaml').read_bytes()).hexdigest(),selection='Fewest failed cases, then fewest collision cases, then fewest failed cycles, then lowest worst last10s error. Independent flight verification still required.')
 (out/'plan.json').write_text(json.dumps(plan,indent=2))
plan=json.loads((out/'plan.json').read_text())
def stats(values):
 a=np.asarray(values)*1000
 return dict(n=len(a),median_ms=float(np.median(a)),p95_ms=float(np.percentile(a,95)),max_ms=float(a.max()),over50=int(np.sum(a>50))) if len(a) else None

def run(cfg,case):
 c=MPCController(cfg,reference_start=case['start']);c.warmup();calls=[];failed_calls=[];cycle=[];reasons=[];orig=c.opti.solve
 def solve():
  before=time.perf_counter();ok=False
  try:r=orig();ok=True;return r
  finally:calls.append(time.perf_counter()-before);failed_calls.append(not ok)
 c.opti.solve=solve;x=np.array(case['initial'],float);goal=np.array(case['goal']);obs=case.get('obstacle');gain=case['gain'];delay=case['delay'];queue=[x[2:].copy() for _ in range(round(delay/.05))];traj=[x.tolist()];gap=None;failures=0
 for k in range(1200):
  cmd=np.zeros(2)
  if np.linalg.norm(x[:2]-goal)>.15 or np.linalg.norm(x[2:])>.05:
   det=[] if obs is None else [DetectedCircle(np.array(obs['center'])-x[:2],obs['radius'])];before=time.perf_counter();r=c.compute(x,goal,det);cycle.append(time.perf_counter()-before)
   if r.success:cmd=r.velocity_command
   else:failures+=1;reasons.append(dict(step=k,reason=r.reason));c.last_acceleration[:]=0
  else:c.last_acceleration[:]=0
  queue.append(cmd);u=queue.pop(0);acc=gain*(u-x[2:]);x[:2]+=.05*x[2:]+.5*.05**2*acc;x[2:]+=.05*acc;traj.append(x.tolist())
  if obs is not None:
   clearance=float(np.linalg.norm(x[:2]-obs['center'])-obs['radius']-cfg.drone_radius);gap=clearance if gap is None else min(gap,clearance)
   if gap<-.003:break
 a=np.array(traj);err=np.linalg.norm(a[:,:2]-goal,axis=1);speed=np.linalg.norm(a[:,2:],axis=1);complete=len(a)==1201;valid=(err<=.15)&(speed<=.05);bad=np.flatnonzero(~valid);safe=gap is None or gap>=-.003
 return dict(completed=complete,simulated_s=(len(a)-1)*.05,passed=bool(complete and safe and failures==0 and valid[-200:].all()),strict_5cm_pass=bool(complete and safe and failures==0 and (err[-200:]<=.05).all() and (speed[-200:]<=.05).all()),last10s_max_error=float(err[-200:].max()) if complete else None,last10s_max_speed=float(speed[-200:].max()) if complete else None,final_error=float(err[-1]),final_speed=float(speed[-1]),settle_s=float((bad[-1]+1)*.05) if valid[-1] and len(bad) else None,min_gap=gap,failed_cycles=failures,failed_solver_calls=sum(failed_calls),solver=stats(calls),compute=stats(cycle),trajectory=traj,failure_reasons=reasons)
rows=[]
def one(name,index,case):
 f=out/f'{name}_{index}.json'
 if f.exists():r=json.loads(f.read_text())
 else:r=run(replace(base,**plan['profiles'][name]),case);f.write_text(json.dumps(r))
 row=dict(profile=name,case=index,**{k:v for k,v in r.items() if k not in ['trajectory','failure_reasons']});rows.append(row);(out/f'{args.stage}_summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)
if args.stage=='screen':
 for name in plan['profiles']:
  for i in plan['screen_cases']:one(name,i,plan['cases'][i])
else:
 screen=json.loads((out/'screen_summary.json').read_text());rank=[]
 for name in plan['profiles']:
  if not name.startswith('N30'):continue
  r=[x for x in screen if x['profile']==name];rank.append((sum(not x['passed'] for x in r),sum(not x['completed'] for x in r),sum(x['failed_cycles'] for x in r),max(x['last10s_max_error'] if x['last10s_max_error'] is not None else 1e6 for x in r),name))
 selected=min(rank)[-1];(out/'selection.json').write_text(json.dumps(dict(selected=selected,ranking=rank),indent=2))
 if args.stage=='validate':
  for i,case in enumerate(plan['cases']):one(selected,i,case)
 else:
  case=dict(initial=[0.,0.,0.,0.],start=[0.,0.],goal=[0.,6.],gain=1.1400490155,delay=.15)
  for name in dict.fromkeys(['N20_current','N30_current',selected]):one(name,'terminal',case)
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in plan['source_hashes'].items())
assert hashlib.sha256((PKG/'config/sils.yaml').read_bytes()).hexdigest()==plan['config_hash']
