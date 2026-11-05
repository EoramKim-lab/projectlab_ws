"""Repeat ideal closed-loop solves with measured scenario geometry.

10 identical repeats (five per scenario), plus 10 seeded perturbed cases.
This does not run Gazebo, PX4, or sensors and cannot establish flight stability.
The perturbations are fixed per run, not time-varying sensor noise.
"""
import argparse,csv,json,time
from dataclasses import fields,asdict
from pathlib import Path
import numpy as np
import yaml
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.obstacle_detection import DetectedCircle


def stats(values):
    a=np.asarray(values,dtype=float)
    return dict(n=len(a),median_ms=float(np.median(a)),p95_ms=float(np.percentile(a,95)),
                max_ms=float(a.max()),over50=int(np.sum(a>50))) if len(a) else None


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario',type=Path,action='append',required=True)
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    p=yaml.safe_load(args.config.read_text())['mpc_node']['ros__parameters']
    cfg=MPCConfig(**dict({f.name:p[f.name] for f in fields(MPCConfig) if f.name in p},control_dt=1/p['publish_rate']))
    rng=np.random.default_rng(20261102)
    summaries=[];all_calls=[];all_cycles=[]
    for scenario_index,path in enumerate(args.scenario):
        source=json.loads(path.read_text());ref=np.array(source['reference'])
        for repeat in range(10):
            center=np.array(source['center']);radius=source['radius'];state=np.r_[ref[0],0.,0.]
            if repeat>=5:
                state[:2]+=rng.uniform(-.02,.02,2)
                state[2:]+=rng.uniform(-.03,.03,2)
                center+=rng.uniform(-.05,.05,2)
                radius=max(.01,radius+rng.uniform(-.02,.02))
            initial=state.copy();controller=MPCController(cfg,reference_start=ref[0])
            original=controller.opti.solve;calls=[]
            def solve():
                t=time.perf_counter_ns();ok=False
                try:
                    result=original();ok=True;return result
                finally:
                    calls.append(dict(ms=(time.perf_counter_ns()-t)/1e6,success=ok))
            controller.opti.solve=solve
            controller.warmup();calls.clear()
            trajectory=[state.copy()];cycles=[];failure=''
            for step in range(round(30/cfg.control_dt)):
                before=len(calls)
                result=controller.compute(state,ref[1],[DetectedCircle(center-state[:2],radius)])
                cycles.append(dict(compute_ms=result.solve_time*1000,solver_ms=sum(x['ms'] for x in calls[before:]),success=result.success))
                if not result.success:failure=result.reason;break
                state=result.predicted_states[1].copy();trajectory.append(state.copy())
                if np.linalg.norm(state[:2]-ref[1])<.15 and np.linalg.norm(state[2:])<.05:break
            x=np.array(trajectory);gap=np.linalg.norm(x[:,:2]-center,axis=1)-radius-cfg.drone_radius
            reached=np.linalg.norm(state[:2]-ref[1])<.15 and np.linalg.norm(state[2:])<.05
            row=dict(scenario=str(path),repeat=repeat,kind='identical' if repeat<5 else 'perturbed',
                     initial=initial.tolist(),center=center.tolist(),radius=radius,reached=bool(reached),
                     failure=failure,cycles=len(cycles),solver_calls=len(calls),
                     failed_solver_calls=sum(not a['success'] for a in calls),
                     min_physical_gap_m=float(gap.min()),model_duration_s=len(cycles)*cfg.control_dt,
                     final_goal_error_m=float(np.linalg.norm(state[:2]-ref[1])),
                     per_solver_call=stats([a['ms'] for a in calls]),
                     per_cycle_compute=stats([a['compute_ms'] for a in cycles]),
                     trajectory=x.tolist())
            run_id=f's{scenario_index}_r{repeat:02}'
            (args.output/f'{run_id}.json').write_text(json.dumps(dict(row,solver_samples=calls,cycle_samples=cycles),indent=2))
            summaries.append({k:v for k,v in row.items() if k!='trajectory'})
            all_calls.extend(calls);all_cycles.extend(cycles)
            print(run_id,row['kind'],'reached=',reached,'failed_solves=',row['failed_solver_calls'],
                  'gap=',round(row['min_physical_gap_m'],4),'median/max ms=',
                  round(row['per_solver_call']['median_ms'],2),round(row['per_solver_call']['max_ms'],2),flush=True)
            report=dict(description=__doc__,config=asdict(cfg),seed=20261102,
                        runs=summaries,reached=sum(r['reached'] for r in summaries),
                        controller_failures=sum(bool(r['failure']) for r in summaries),
                        failed_solver_calls=sum(not a['success'] for a in all_calls),
                        solver=stats([a['ms'] for a in all_calls]),
                        cycle_solver_total=stats([a['solver_ms'] for a in all_cycles]),
                        cycle_compute=stats([a['compute_ms'] for a in all_cycles]))
            (args.output/'summary.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ('runs','config','description')},indent=2))


if __name__=='__main__':main()
