"""Summarize all tracking-weight trials without dropping failures."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[3];out=root/'sils_sim/results/s_turn_tracking_sweep';plan=json.loads((out/'plan.json').read_text());rows=json.loads((out/'summary.json').read_text());groups=[]
for q in plan['weights']:
 r=[x for x in rows if x['q_position']==q]
 groups.append(dict(q=q,trials=len(r),s_turn=sum(x['s_turn'] for x in r),hold_pass=sum(x['hold_pass'] for x in r),strict_5cm=sum(x['strict_5cm'] for x in r),failed_cycles=sum(x['failed_cycles'] for x in r),collision_trials=sum(x['physical_min_gap']<-.003 for x in r),minimum_physical_clearance=min(x['physical_min_gap'] for x in r),max_lateral=max(x['max_lateral'] for x in r),mean_path_length=float(np.mean([x['path_length'] for x in r])),max_last10s_error=max(x['last10s_max_error'] for x in r),solver_max_ms=max(x['solver']['max_ms'] for x in r),compute_max_ms=max(x['compute']['max_ms'] for x in r),over50=sum(x['compute']['over50'] for x in r),compute_calls=sum(x['compute']['n'] for x in r)))
(out/'group_summary.json').write_text(json.dumps(groups,indent=2));print(json.dumps(groups,indent=2))
fig,axes=plt.subplots(3,2,figsize=(14,11));colors=['tab:blue','tab:orange','tab:green','tab:red']
for i,case in enumerate(plan['cases']):
 ax=axes.flat[i];ax.plot([0,12],[0,0],'k--',label='Reference')
 for q,color in zip(plan['weights'],colors):
  r=json.loads((out/f'q{q:g}_case{i}_repeat0.json').read_text());a=np.array(r['trajectory']);ax.plot(a[:,1],a[:,0],color=color,label=f'q_position={q:g}')
 for center in plan['centers']:
  ax.add_patch(plt.Circle(center[::-1],plan['radius'],color='gray',alpha=.5));ax.add_patch(plt.Circle(center[::-1],plan['radius']+plan['base']['drone_radius'],fill=False,color='gray',linestyle=':'))
 ax.set_title(case['name']);ax.set_xlabel('ENU east [m]');ax.set_ylabel('ENU north [m]');ax.set_aspect('equal',adjustable='datalim');ax.grid(alpha=.3)
axes.flat[0].legend(fontsize=8);axes.flat[-1].axis('off');axes.flat[-1].text(.05,.8,'Offline lag-model trial, NOT Gazebo\nIdentical two obstacles and reference in every trial\nOnly q_position changes; terminal q_position=24\nExisting bypass-branch selection remains unchanged',va='top',fontsize=11);fig.tight_layout();fig.savefig(out/'tracking_paths.png',dpi=150);plt.close(fig)
