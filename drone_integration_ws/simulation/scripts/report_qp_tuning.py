"""Render held-out QP weight comparisons, including the reference trajectory."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[3];out=root/'sils_sim/results/qp_weight_tuning'
plan=json.loads((out/'plan.json').read_text());selected=json.loads((out/'selection.json').read_text())['selected']
cases=json.loads((root/'sils_sim/results/acados_weight_holdout/plan.json').read_text())['cases']
rows=json.loads((out/'holdout_summary.json').read_text());fig,axes=plt.subplots(2,4,figsize=(16,8))
for i,(ax,case) in enumerate(zip(axes.flat,cases)):
 ref=np.array([case['start'],case['goal']]);ax.plot(ref[:,0],ref[:,1],'k--',label='Reference')
 for label,color in [('baseline','tab:red'),(selected,'tab:blue')]:
  trial=json.loads((out/f'holdout_{label}_{i}.json').read_text());xy=np.array(trial['trajectory'])[:,:2];ax.plot(xy[:,0],xy[:,1],color=color,label=label)
 obs=case['obstacle'];ax.add_patch(plt.Circle(obs['center'],obs['radius']+plan['base']['drone_radius'],color='gray',alpha=.3));ax.scatter(*case['goal'],marker='x',color='black');ax.set_title(f"Case {i}: gain={case['gain']:.2f}, delay={case['delay']:.2f}s");ax.axis('equal');ax.grid(alpha=.3)
axes.flat[0].legend();fig.suptitle('QP weight tuning: held-out lag-model simulations (not Gazebo)');fig.tight_layout();fig.savefig(out/'holdout_paths.png',dpi=150);plt.close(fig)
fig,axes=plt.subplots(2,4,figsize=(16,8))
for i,(ax,case) in enumerate(zip(axes.flat,cases)):
 for label,color in [('baseline','tab:red'),(selected,'tab:blue')]:
  trial=json.loads((out/f'holdout_{label}_{i}.json').read_text());xy=np.array(trial['trajectory'])[:,:2];err=np.linalg.norm(xy-case['goal'],axis=1);ax.plot(np.arange(len(err))*.05,err,color=color,label=label)
 baseline=json.loads((out/f'holdout_baseline_{i}.json').read_text())
 ax.text(.03,.94,f"Baseline stopped at {baseline['simulated_s']:.1f}s (collision)",transform=ax.transAxes,va='top',fontsize=8,color='tab:red')
 ax.axhline(.15,color='black',linestyle='--',label='Existing 15 cm gate');ax.axhline(.05,color='green',linestyle=':',label='5 cm criterion');ax.set_ylim(0,.5);ax.set_xlim(35,60);ax.set_title(f'Case {i} terminal position error');ax.set_xlabel('Time [s]');ax.set_ylabel('Error [m]');ax.grid(alpha=.3)
axes.flat[0].legend();fig.tight_layout();fig.savefig(out/'holdout_terminal.png',dpi=150);plt.close(fig)
summary={'selected':selected,'weights':plan['profiles'][selected],'groups':{}}
for name in ('baseline',selected):
 r=[x for x in rows if x['profile']==name];summary['groups'][name]=dict(cases=len(r),passed=sum(x['basic_joint_pass'] for x in r),strict_5cm=sum(x['strict_joint_pass'] for x in r),failed_cycles=sum(x['failed_cycles'] for x in r),minimum_clearance=min(x['min_gap'] for x in r),max_final_error=max(x['final_error'] for x in r),max_last10s_error=max((x['last10s_max_error'] for x in r if x['completed']),default=None),max_last10s_span=max((x['last10s_position_span'] for x in r if x['completed']),default=None),compute_max_ms=max(x['compute']['max_ms'] for x in r),solver_max_ms=max(x['solver']['max_ms'] for x in r),over50=sum(x['compute']['over50'] for x in r))
(out/'final_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
