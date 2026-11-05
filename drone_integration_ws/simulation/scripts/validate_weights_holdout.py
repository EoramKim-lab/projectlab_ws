"""Frozen, paired held-out comparison. No controller/constraint modifications.

Same ideal-model assumptions as previous tests. This is not a full ROS/PX4 flight.
All generated cases are retained; weights are fixed before results are observed.
"""
import hashlib,json
from dataclasses import asdict,fields,replace
from pathlib import Path
import numpy as np
import yaml
from drone_integration.control.mpc_controller import MPCConfig
from search_robust_weights import run_case

root=Path(__file__).resolve().parents[3]
results=root/'sils_sim/results';output=results/'weight_holdout_20261103';output.mkdir(exist_ok=True)
workspace=root/'drone_integration_ws'
config=workspace/'src/drone_integration/config/sils.yaml'
p=yaml.safe_load(config.read_text())['mpc_node']['ros__parameters']
base=MPCConfig(**dict({f.name:p[f.name] for f in fields(MPCConfig) if f.name in p},control_dt=1/p['publish_rate']))
candidate=json.loads((results/'robust_weight_suite_clean/candidate.json').read_text())
trial=replace(base,**candidate['weights'])
paths=[workspace/'src/drone_integration/drone_integration/control'/name for name in
       ('mpc_controller.py','mpc_node.py','px4_command_node.py','collision_constraints_node.py')]
def hashes():return {str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
seed=20261103;rng=np.random.default_rng(seed);cases=[]
for scenario_index,name in enumerate(('latest','previous')):
 source=json.loads((results/f'terminal_tuning_v2/{name}/comparison.json').read_text());ref=np.array(source['reference'])
 for repetition in range(10):
  state=np.r_[ref[0],0.,0.]
  state[:2]+=rng.uniform(-.02,.02,2);state[2:]+=rng.uniform(-.03,.03,2)
  center=np.array(source['center'])+rng.uniform(-.05,.05,2)
  radius=source['radius']+rng.uniform(-.02,.02)
  cases.append(dict(id=f's{scenario_index}_r{repetition:02}',initial=state.tolist(),center=center.tolist(),
                    radius=radius,reference=ref.tolist()))
plan=dict(seed=seed,description=__doc__,baseline=asdict(base),candidate=asdict(trial),
          controller_hashes=hashes(),cases=cases,position_tolerance_m=.05,speed_tolerance_mps=.05,
          final_hold_s=2.,model_duration_s=30.,production_goal_tolerance=p['goal_tolerance'],
          perturbations=dict(position_axis_m=.02,velocity_axis_mps=.03,center_axis_m=.05,radius_m=.02))
plan_path=output/'plan.json'
if plan_path.exists():raise RuntimeError('Existing holdout output: use a new directory for another run')
plan_path.write_text(json.dumps(plan,indent=2))
rows=[]
for case in cases:
 for label,cfg in [('baseline',base),('candidate',trial)]:
  result=run_case(cfg,case,np.array(case['reference']))
  (output/f"{case['id']}_{label}.json").write_text(json.dumps(result,indent=2))
  rows.append(dict(case=case['id'],configuration=label,**{k:v for k,v in result.items() if k!='trajectory'}))
  (output/'summary.json').write_text(json.dumps(dict(plan=str(plan_path),runs=rows),indent=2))
  print(case['id'],label,'PASS',result['passed'],'internal failures',result['failed_solver_calls'],
        'settle',result['settle_5cm_s'],'gap',round(result['min_physical_gap_m'],3),flush=True)
after=hashes()
assert after==plan['controller_hashes'],'Controller source changed during experiment'
aggregate={}
for label in ('baseline','candidate'):
 rs=[r for r in rows if r['configuration']==label]
 aggregate[label]=dict(runs=len(rs),passed=sum(r['passed'] for r in rs),
                      controller_failures=sum(r['failure'] is not None for r in rs),
                      internal_solver_failures=sum(r['failed_solver_calls'] for r in rs),
                      solver_calls=sum(r['solver_calls'] for r in rs),cycles=sum(r['cycles'] for r in rs),
                      max_solver_ms=max(r['solver_max_ms'] for r in rs),
                      max_goal_overshoot_m=max(r['goal_overshoot_m'] for r in rs),
                      min_physical_gap_m=min(r['min_physical_gap_m'] for r in rs),
                      max_last2s_goal_error_passed_m=max((r['last2s_max_error_m'] for r in rs if r['passed']),default=None))
(output/'aggregate.json').write_text(json.dumps(dict(controller_unchanged=True,results=aggregate),indent=2))
print(json.dumps(aggregate,indent=2),flush=True)
