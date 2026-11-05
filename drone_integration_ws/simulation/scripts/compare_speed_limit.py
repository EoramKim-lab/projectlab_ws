"""Paired speed-limit comparison using frozen cases and the current runtime weights.
Only MPC max_speed differs; reference_speed, PX4 output limit, controller and gate stay fixed.
Log-fitted response surrogate, not a Gazebo flight.
"""
import json, hashlib
from dataclasses import asdict,replace
from pathlib import Path
from tune_px4_response_weights import run,base,ROOT,PKG
out=ROOT/'sils_sim/results/speed_limit_comparison_v2';out.mkdir(exist_ok=True)
if (out/'plan.json').exists():raise RuntimeError('Refusing to overwrite frozen experiment')
source=ROOT/'sils_sim/results/px4_response_weight_tuning/buffer20/validation_plan.json'
cases=json.loads(source.read_text())['cases']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PKG/'drone_integration/control').glob('*.py')}
config=(PKG/'config/sils.yaml').read_bytes()
plan=dict(description=__doc__,base=asdict(base),caps=[1.,.3],duration=60,cases=cases,source_hashes=hashes,config_sha256=hashlib.sha256(config).hexdigest(),early_stop='Both arms stop and fail at physical penetration beyond3mm; no success can result from early stop. Previous run interrupted before any case completed.',acceptance='Final10s continuously <=15cm and <=.05m/s, no failed MPC cycles, physical gap>=-3mm. Strict5cm separately.')
(out/'plan.json').write_text(json.dumps(plan,indent=2));rows=[]
for i,case in enumerate(cases):
 for cap in plan['caps']:
  r=run(replace(base,max_speed=cap),stop_on_collision=True,**case)
  if not r["completed"]:
   r["passed"]=r["strict_5cm_pass"]=False
   r["last10s_max_error"]=r["last10s_max_speed"]=None
   r["last10s_5cm"]=False
   r["settle_s"]=None
  (out/f'case{i}_cap{cap:g}.json').write_text(json.dumps(r))
  row=dict(case=i,max_speed=cap,**{k:v for k,v in r.items() if k!='trajectory'});rows.append(row)
  (out/'summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in hashes.items())
assert (PKG/'config/sils.yaml').read_bytes()==config
aggregate={}
for cap in plan['caps']:
 r=[x for x in rows if x['max_speed']==cap]
 aggregate[str(cap)]=dict(runs=len(r),passed=sum(x['passed'] for x in r),strict_5cm_pass=sum(x['strict_5cm_pass'] for x in r),failed_cycles=sum(x['failures'] for x in r),worst_last10s_error_m=max((x['last10s_max_error'] for x in r if x['completed']),default=None),worst_last10s_speed_mps=max((x['last10s_max_speed'] for x in r if x['completed']),default=None),min_physical_gap_m=min(x['min_gap'] for x in r))
(out/'aggregate.json').write_text(json.dumps(dict(controller_unchanged=True,config_unchanged=True,results=aggregate),indent=2));print(json.dumps(aggregate,indent=2),flush=True)
