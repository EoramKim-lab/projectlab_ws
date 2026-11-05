"""Screen weight candidates across all distinct saved perturbations; stop on failure."""
import argparse,json
from dataclasses import replace
from pathlib import Path
import numpy as np
from drone_integration.control.mpc_controller import MPCConfig
from search_robust_weights import run_case
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--candidate',action='append')
parser.add_argument('--clean',action='store_true',help='Require zero failed internal solver calls too')
args=parser.parse_args()
root=Path(__file__).resolve().parents[3]/'sils_sim/results'
source=root/'solver_repeatability';out=root/('robust_weight_suite_clean' if args.clean else 'robust_weight_suite');out.mkdir(exist_ok=True)
saved=json.loads((source/'summary.json').read_text());base=MPCConfig(**saved['config'])
refs={i:np.array(json.loads((root/f'terminal_tuning_v2/{name}/comparison.json').read_text())['reference']) for i,name in [(0,'latest'),(1,'previous')]}
costs=['q_position','q_velocity','q_terminal_position','q_terminal_velocity','r_acceleration','r_delta_acceleration','safety_slack_linear','safety_slack_quadratic']
candidates=[
 dict(name='velocity_q4',weights={'q_velocity':4.,'q_terminal_velocity':16.}),
 dict(name='terminal_v32',weights={'q_terminal_velocity':32.}),
 dict(name='terminal_v8',weights={'q_terminal_velocity':8.}),
 dict(name='terminal_v4',weights={'q_terminal_velocity':4.}),
 dict(name='scale_all_0p1',weights={k:getattr(base,k)*.1 for k in costs}),
 dict(name='velocity4_buffer20',weights={'q_velocity':4.,'q_terminal_velocity':16.,'safety_slack_linear':20.,'safety_slack_quadratic':200.}),
 dict(name='velocity4_terminal32_buffer10',weights={'q_velocity':4.,'q_terminal_velocity':32.,'safety_slack_linear':10.,'safety_slack_quadratic':100.}),
 dict(name='position16_velocity4',weights={'q_position':16.,'q_velocity':4.,'q_terminal_position':48.,'q_terminal_velocity':16.}),
]
cases=['s0_r07','s0_r09','s0_r05','s1_r08','s0_r00','s1_r00','s0_r06','s0_r08','s1_r05','s1_r06','s1_r07','s1_r09']
if args.candidate:
 candidates=sorted([c for c in candidates if c['name'] in args.candidate],key=lambda c:args.candidate.index(c['name']))
rows=[]
for candidate in candidates:
 cfg=replace(base,**candidate['weights']);passed=[]
 for name in cases:
  case=json.loads((source/f'{name}.json').read_text());result=run_case(cfg,case,refs[int(name[1])])
  (out/f"{candidate['name']}_{name}.json").write_text(json.dumps(dict(candidate=candidate,case=name,result=result),indent=2))
  rows.append(dict(candidate=candidate,case=name,**{k:v for k,v in result.items() if k!='trajectory'}))
  (out/'summary.json').write_text(json.dumps(dict(base_config=saved['config'],runs=rows),indent=2))
  print(candidate['name'],name,'PASS',result['passed'],'failed calls',result['failed_solver_calls'],flush=True)
  if not result['passed'] or (args.clean and result['failed_solver_calls']):break
  passed.append(name)
 if len(passed)==len(cases):
  (out/'candidate.json').write_text(json.dumps(candidate,indent=2))
  print('ALL DISTINCT CASES PASS',candidate['name'],flush=True);break
