"""Frozen 0.4/0.5 m/s comparisons and weight-only damping candidates.
Uses the same 60s response-surrogate scenarios and unchanged runtime goal gate.
No Gazebo execution; no runtime source/config changes.
"""
import argparse,json,hashlib
from dataclasses import replace,asdict
from pathlib import Path
from tune_px4_response_weights import run,base,ROOT,PKG
out=ROOT/'sils_sim/results/speed_terminal_045';out.mkdir(exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['baseline','screen','validate']);args=parser.parse_args()
planpath=out/'plan.json'
if not planpath.exists():
 cases=json.loads((ROOT/'sils_sim/results/px4_response_weight_tuning/buffer20/validation_plan.json').read_text())['cases']
 profiles={}
 for cap in [.4,.5]:
  profiles[f'base_{cap}']=dict(max_speed=cap)
  profiles[f'damped_{cap}']=dict(max_speed=cap,q_velocity=256.,q_terminal_velocity=128.,safety_slack_linear=20.,safety_slack_quadratic=200.)
  profiles[f'gentle_{cap}']=dict(max_speed=cap,q_position=1.,q_terminal_position=3.,q_velocity=256.,q_terminal_velocity=128.,safety_slack_linear=20.,safety_slack_quadratic=200.)
 plan=dict(base=asdict(base),profiles=profiles,cases=cases,screen_cases=[0,6],duration=60,gate=dict(position=.15,speed=.05),strict_accuracy=.05,hold_s=10,early_stop='Physical penetration beyond3mm fails and stops both arms.',source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PKG/'drone_integration/control').glob('*.py')},config_hash=hashlib.sha256((PKG/'config/sils.yaml').read_bytes()).hexdigest())
 planpath.write_text(json.dumps(plan,indent=2))
plan=json.loads(planpath.read_text());rows=[]
def one(name,caseid,case):
 path=out/f'{name}_{caseid}.json'
 if path.exists():r=json.loads(path.read_text())
 else:
  r=run(replace(base,**plan['profiles'][name]),stop_on_collision=True,**case)
  if not r['completed']:
   r.update(passed=False,strict_5cm_pass=False,last10s_max_error=None,last10s_max_speed=None,last10s_5cm=False,settle_s=None)
  path.write_text(json.dumps(r))
 row=dict(profile=name,case=caseid,**{k:v for k,v in r.items() if k!='trajectory'});rows.append(row);(out/f'{args.stage}_summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)
if args.stage=='baseline':
 for i,case in enumerate(plan['cases']):
  for name in ['base_0.4','base_0.5']:one(name,i,case)
 for name in ['base_0.4','base_0.5']:one(name,'terminal',dict(initial=[0.,0.,0.,0.],start=[0.,0.],goal=[0.,6.],gain=1.1400490155,delay=.15,duration=60))
elif args.stage=='screen':
 for name in [n for n in plan['profiles'] if not n.startswith('base')]:
  for i in plan['screen_cases']:one(name,i,plan['cases'][i])
else:
 screen=json.loads((out/'screen_summary.json').read_text());names=sorted(set(x['profile'] for x in screen));rank=[]
 for name in names:
  rr=[x for x in screen if x['profile']==name];rank.append((sum(not x['passed'] for x in rr),max((x['last10s_max_error'] or 1e3) for x in rr),name))
 selected=min(rank)[-1];(out/'selection.json').write_text(json.dumps(dict(selected=selected,ranking=rank,rule='Fewest failed screening cases, then smallest worst final10s error; no claim of success from selection alone.'),indent=2))
 for i,case in enumerate(plan['cases']):one(selected,i,case)
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in plan['source_hashes'].items())
assert hashlib.sha256((PKG/'config/sils.yaml').read_bytes()).hexdigest()==plan['config_hash']
