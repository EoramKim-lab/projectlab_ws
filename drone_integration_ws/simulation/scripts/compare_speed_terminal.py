"""Separate obstacle-free diagnostic; not a successful obstacle-avoidance scenario."""
import json
from dataclasses import replace,asdict
from tune_px4_response_weights import run,base,ROOT
out=ROOT/'sils_sim/results/speed_limit_comparison_v2'
case=dict(initial=[0.,0.,0.,0.],start=[0.,0.],goal=[0.,6.],gain=1.1400490155,delay=.15,duration=60)
(out/'terminal_plan.json').write_text(json.dumps(dict(description=__doc__,case=case,base=asdict(base),caps=[1.,.3]),indent=2))
rows=[]
for cap in [1.,.3]:
 r=run(replace(base,max_speed=cap),**case);(out/f'terminal_cap{cap:g}.json').write_text(json.dumps(r));row=dict(max_speed=cap,**{k:v for k,v in r.items() if k!='trajectory'});rows.append(row);(out/'terminal_summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)
