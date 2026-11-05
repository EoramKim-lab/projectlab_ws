"""Paired measured-state replay: same problem/history for both solver backends.
Warmup/codegen excluded. Whole compute() includes outer plane/side solves;
individual solve time excludes Python parameter setup. Not a Gazebo flight.
"""
import argparse,importlib.util,json,sys,time
from dataclasses import asdict,fields
from pathlib import Path
import numpy as np,yaml
from drone_integration.control.mpc_controller import MPCController,MPCConfig
from drone_integration.control.obstacle_detection import DetectedCircle
parser=argparse.ArgumentParser();parser.add_argument('--repeats',type=int,default=3);args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[3];out=ROOT/'sils_sim/results/acados_swap';out.mkdir(exist_ok=True)
refpath=ROOT/'drone_integration_ws/tests/fixtures/mpc_controller_ipopt_reference.py';spec=importlib.util.spec_from_file_location('drone_integration.control._ipopt_oracle',refpath);ref=importlib.util.module_from_spec(spec);sys.modules[spec.name]=ref;spec.loader.exec_module(ref)
p=yaml.safe_load((ROOT/'drone_integration_ws/src/drone_integration/config/sils.yaml').read_text())['mpc_node']['ros__parameters'];cfg=MPCConfig(**dict({f.name:p[f.name] for f in fields(MPCConfig) if f.name in p},control_dt=1/p['publish_rate']))
source=ROOT/'sils_sim/results/drone_20261102T111202Z_qmxyadtp.jsonl';latest={};cases=[]
for line in source.open():
 try:r=json.loads(line)
 except json.JSONDecodeError:continue
 if r.get('missing') or not r.get('data'):continue
 latest[r['topic']]=(r['received_ns']/1e9,r['data'])
 if r['topic']!='/navigation/state':continue
 nav=r['data'];ob=latest.get('/control/obstacles');reference=latest.get('/control/reference');status=latest.get('/fmu/out/vehicle_status_v1')
 if not nav['valid'] or not ob or not reference or not reference[1]['poses'] or not status or status[1]['nav_state']!=14:continue
 if abs(r['received_ns']/1e9-ob[0])>.25 or ob[1]['over_capacity']:continue
 state=[nav['pose']['position'][k] for k in ['x','y']]+[nav['twist']['linear'][k] for k in ['x','y']]
 goal=[reference[1]['poses'][-1]['position'][k] for k in ['x','y']];start=[reference[1]['poses'][0]['position'][k] for k in ['x','y']]
 if np.linalg.norm(np.array(state[:2])-goal)<=.15 and np.linalg.norm(state[2:])<=.05:continue
 cases.append(dict(t=r['received_ns']/1e9,state=state,goal=goal,start=start,xy=ob[1]['xy'],radius=ob[1]['radius']))
cases=[cases[i] for i in np.linspace(0,len(cases)-1,min(160,len(cases)),dtype=int)]
(out/'plan.json').write_text(json.dumps(dict(description=__doc__,config=asdict(cfg),cases=cases,repeats=args.repeats,source=str(source)),indent=2))
a=MPCController(cfg,reference_start=cases[0]['start']);b=ref.MPCController(ref.MPCConfig(**asdict(cfg)),reference_start=cases[0]['start']);a.warmup();b.warmup();calls={'acados':[],'ipopt':[]};rows=[]
def wrap(obj,name):
 orig=obj.solve
 def solve(*args,**kwargs):
  t=time.perf_counter()
  try:return orig(*args,**kwargs)
  finally:calls[name].append((time.perf_counter()-t)*1000)
 obj.solve=solve
wrap(a.backend.solver,'acados');wrap(b.opti,'ipopt')
for repeat in range(args.repeats):
 a.reset();b.reset()
 for i,case in enumerate(cases):
  state=np.array(case['state']);det=[DetectedCircle(center-state[:2],radius) for center,radius in zip(np.array(case['xy']).reshape(-1,2),case['radius'])]
  previous=b.last_acceleration.copy();side=b.preferred_side;initialized=b._branch_initialized;results={};record=dict(repeat=repeat,case=i)
  for name,c in [('ipopt',b),('acados',a)]:
   c.last_acceleration=previous.copy();c.preferred_side=side;c._branch_initialized=initialized;c.reference_start=np.array(case['start']);before=len(calls[name]);t=time.perf_counter();result=c.compute(state,case['goal'],det);elapsed=(time.perf_counter()-t)*1000;results[name]=result;record[name]=dict(success=result.success,compute_ms=elapsed,solver_calls=len(calls[name])-before,reason=result.reason,velocity=result.velocity_command.tolist(),objective=result.objective if np.isfinite(result.objective) else None)
  record['velocity_difference']=float(np.linalg.norm(results['acados'].velocity_command-results['ipopt'].velocity_command)) if all(r.success for r in results.values()) else None;rows.append(record)
  if i%40==0:print('repeat',repeat,'case',i,'IPOPT/acados ms',round(record['ipopt']['compute_ms'],2),round(record['acados']['compute_ms'],2),'success',record['ipopt']['success'],record['acados']['success'],flush=True)
def stats(x):
 x=np.array(x);return dict(n=len(x),median_ms=float(np.median(x)),p95_ms=float(np.percentile(x,95)),max_ms=float(x.max()),over50=int((x>50).sum()))
summary=dict(config=asdict(cfg),description=__doc__,samples=len(cases),repeats=args.repeats,results={name:dict(solver=stats(calls[name]),compute=stats([r[name]['compute_ms'] for r in rows]),failed_cycles=sum(not r[name]['success'] for r in rows)) for name in calls},success_disagreements=sum(r['acados']['success']!=r['ipopt']['success'] for r in rows),max_velocity_difference=max((r['velocity_difference'] for r in rows if r['velocity_difference'] is not None),default=None))
(out/'samples.json').write_text(json.dumps(dict(rows=rows,solve_ms=calls)));(out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
