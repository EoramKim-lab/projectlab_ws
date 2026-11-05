"""Frozen fresh paired cases after weight selection. No changed conditions or gate."""
import json,hashlib
from dataclasses import replace,asdict
from pathlib import Path
import numpy as np
from response_trial import run
from tune_px4_response_weights import ROOT,PKG,base
out=ROOT/'sils_sim/results/acados_weight_holdout';out.mkdir(exist_ok=True)
if (out/'plan.json').exists():raise RuntimeError('Refusing to overwrite holdout')
selection=ROOT/'sils_sim/results/acados_weight_safety_refine';name=json.loads((selection/'selection.json').read_text())['selected'];weights=json.loads((selection/'plan.json').read_text())['profiles'][name];rng=np.random.default_rng(20261106);cases=[]
for gain,delay in [(1.1400490155,.15),(.885965096,0),(1.1690876,.2),(.8,.2)]:
 for scenario in ['latest','previous']:
  src=json.loads((ROOT/f'sils_sim/results/terminal_tuning_v2/{scenario}/comparison.json').read_text());ref=np.array(src['reference']);cases.append(dict(initial=np.r_[ref[0]+rng.uniform(-.02,.02,2),rng.uniform(-.03,.03,2)].tolist(),start=ref[0].tolist(),goal=ref[1].tolist(),gain=gain,delay=delay,obstacle=dict(center=(np.array(src['center'])+rng.uniform(-.05,.05,2)).tolist(),radius=src['radius']+rng.uniform(-.02,.02))))
plan=dict(seed=20261106,description=__doc__,weights=weights,base=asdict(base),cases=cases,duration=60,hold_s=10,accuracy=.05,unchanged_gate=.15,deadline_ms=50,source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PKG/'drone_integration/control').glob('*.py')});(out/'plan.json').write_text(json.dumps(plan,indent=2));rows=[]
for i,case in enumerate(cases):
 for label,w in [('baseline',{}),('candidate',weights)]:
  result=run(replace(base,**w),case);(out/f'{label}_{i}.json').write_text(json.dumps(result));row=dict(case=i,label=label,**{k:v for k,v in result.items() if k not in ['trajectory','failure_reasons']});row['time_pass']=result['compute']['over50']==0;row['basic_joint_pass']=result['passed'] and row['time_pass'];row['strict_joint_pass']=result['strict_5cm_pass'] and row['time_pass'];rows.append(row);(out/'summary.json').write_text(json.dumps(rows,indent=2));print(label,i,'pass',row['basic_joint_pass'],'5cm',row['strict_joint_pass'],'end error',round(row['final_error'],4),'max ms',round(row['compute']['max_ms'],2),flush=True)
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in plan['source_hashes'].items())
