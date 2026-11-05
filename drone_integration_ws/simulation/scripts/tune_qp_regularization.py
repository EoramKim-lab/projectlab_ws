"""Weight-only QP search with frozen cases, existing goal gate and output speed cap.
Log-fitted lag surrogate, NOT a Gazebo flight. All failed trials are retained.
"""
import argparse,hashlib,json
from dataclasses import asdict,replace
from pathlib import Path
from qp_response_trial import run
from drone_integration.control.mpc_controller import MPCConfig
from tune_px4_response_weights import ROOT,PKG,base
parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['screen','validate','holdout']);args=parser.parse_args()
out=ROOT/'sils_sim/results/qp_weight_tuning';out.mkdir(exist_ok=True)
if not (out/'plan.json').exists():
 cases=json.loads((ROOT/'sils_sim/results/px4_response_weight_tuning/buffer20/validation_plan.json').read_text())['cases']
 profiles={'baseline':{}}
 for v in (16.,64.,128.,256.,320.,512.):
  profiles[f'v{int(v)}']=dict(q_velocity=v,q_terminal_velocity=v/2,safety_slack_linear=300.,safety_slack_quadratic=3000.)
 for ra,rd in ((1.,.2),(4.,1.),(.05,.01)):
  profiles[f'v256_a{ra:g}']=dict(profiles['v256'],r_acceleration=ra,r_delta_acceleration=rd)
 profiles['p16_v256']=dict(profiles['v256'],q_position=16.,q_terminal_position=48.)
 profiles['p4_v128']=dict(profiles['v128'],q_position=4.,q_terminal_position=12.)
 plan=dict(description=__doc__,base=asdict(base),profiles=profiles,cases=cases,screen_cases=[0,3,6],duration=60,hold_s=10,position_gate=.15,speed_gate=.05,strict_accuracy=.05,deadline_ms=50,command_speed_cap=1.,source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PKG/'drone_integration/control').glob('*.py')},config_hash=hashlib.sha256((PKG/'config/sils.yaml').read_bytes()).hexdigest())
 (out/'plan.json').write_text(json.dumps(plan,indent=2))
plan=json.loads((out/'plan.json').read_text());base=MPCConfig(**plan['base']);rows=[]
config_at_start=hashlib.sha256((PKG/'config/sils.yaml').read_bytes()).hexdigest()
def one(name,i,case=None):
 file=out/f'{args.stage}_{name}_{i}.json'
 if file.exists():r=json.loads(file.read_text())
 else:
  r=run(replace(base,**plan['profiles'][name]),plan['cases'][i] if case is None else case);file.write_text(json.dumps(r))
 row=dict(profile=name,case=i,**{k:v for k,v in r.items() if k not in ['trajectory','failure_reasons']});row['time_pass']=r['compute']['over50']==0;row['basic_joint_pass']=r['passed'] and row['time_pass'];row['strict_joint_pass']=r['strict_5cm_pass'] and row['time_pass'];rows.append(row);(out/f'{args.stage}_summary.json').write_text(json.dumps(rows,indent=2))
 print(args.stage,name,i,'pass',row['basic_joint_pass'],'5cm',row['strict_joint_pass'],'gap',round(row['min_gap'],4),'error',round(row['final_error'],4),'span',row['last10s_position_span'],'max_ms',round(row['compute']['max_ms'],2),flush=True)
if args.stage=='screen':
 for name in plan['profiles']:
  for i in plan['screen_cases']:one(name,i)
elif args.stage=='validate':
 screen=json.loads((out/'screen_summary.json').read_text());rank=[]
 for name in plan['profiles']:
  r=[x for x in screen if x['profile']==name]
  rank.append((sum(not x['basic_joint_pass'] for x in r),sum(not x['completed'] for x in r),sum(x['failed_cycles'] for x in r),max(x['last10s_max_error'] if x['last10s_max_error'] is not None else 1e6 for x in r),name))
 selected=min(rank)[-1];(out/'selection.json').write_text(json.dumps(dict(selected=selected,ranking=rank),indent=2))
 for name in ['baseline',selected]:
  for i in range(len(plan['cases'])):one(name,i)
else:
 # Frozen held-out initial position/velocity and obstacles; never used in selection.
 cases=json.loads((out/'holdout_cases.json').read_text()) if (out/'holdout_cases.json').exists() else json.loads((ROOT/'sils_sim/results/acados_weight_holdout/plan.json').read_text())['cases']
 (out/'holdout_cases.json').write_text(json.dumps(cases,indent=2))
 selected=json.loads((out/'selection.json').read_text())['selected']
 for name in ['baseline',selected]:
  for i,case in enumerate(cases):one(name,i,case)
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in plan['source_hashes'].items())
assert hashlib.sha256((PKG/'config/sils.yaml').read_bytes()).hexdigest()==config_at_start
