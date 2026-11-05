"""Offline weight search: fixed geometry, ideal dynamics, strict final hold check.
No PX4, sensor delay, actuator lag, or changing obstacle estimation is modeled.
"""
import argparse,json,time
from dataclasses import replace
from pathlib import Path
import numpy as np
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.obstacle_detection import DetectedCircle


def run_case(cfg,case,ref):
    controller=MPCController(cfg,reference_start=ref[0]);controller.warmup()
    state=np.array(case['initial']);center=np.array(case['center']);radius=case['radius']
    original=controller.opti.solve;call_times=[];call_failures=[]
    def solve():
        start=time.perf_counter_ns();ok=False
        try:result=original();ok=True;return result
        finally:call_times.append((time.perf_counter_ns()-start)/1e6);call_failures.append(not ok)
    controller.opti.solve=solve
    trajectory=[state.copy()];elapsed=[];failure=None
    for k in range(round(30/cfg.control_dt)):
        result=controller.compute(state,ref[1],[DetectedCircle(center-state[:2],radius)])
        elapsed.append(result.solve_time*1000)
        if not result.success:
            failure={'step':k,'reason':result.reason};break
        state=result.predicted_states[1].copy();trajectory.append(state.copy())
    x=np.array(trajectory);goal_errors=np.linalg.norm(x[:,:2]-ref[1],axis=1);speeds=np.linalg.norm(x[:,2:],axis=1)
    valid=(goal_errors<=.05)&(speeds<=.05);hold=round(2/cfg.control_dt)+1
    gap=np.linalg.norm(x[:,:2]-center,axis=1)-radius-cfg.drone_radius
    direction=(ref[1]-ref[0])/np.linalg.norm(ref[1]-ref[0]);normal=np.array([-direction[1],direction[0]])
    lateral=(x[:,:2]-ref[0])@normal;outside=np.flatnonzero(~valid)
    passed=failure is None and len(x)>=hold and valid[-hold:].all() and gap.min()>=-.003
    return dict(passed=bool(passed),failure=failure,failed_solver_calls=sum(call_failures),
                cycles=len(elapsed),solver_calls=len(call_times),
                final_error_m=float(goal_errors[-1]),last2s_max_error_m=float(goal_errors[-hold:].max()),
                last2s_max_speed_mps=float(speeds[-hold:].max()),
                settle_5cm_s=float((outside[-1]+1)*cfg.control_dt) if valid[-1] and len(outside) else None,
                max_lateral_m=float(abs(lateral).max()),lateral_rmse_m=float(np.sqrt(np.mean(lateral**2))),
                goal_overshoot_m=float(max(0.,np.max((x[:,:2]-ref[1])@direction))),
                min_physical_gap_m=float(gap.min()),
                solver_median_ms=float(np.median(call_times)),solver_max_ms=float(max(call_times)),
                compute_median_ms=float(np.median(elapsed)),compute_max_ms=float(max(elapsed)),trajectory=x.tolist())


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--validate',type=Path,help='Validate selected weights JSON against all saved cases')
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    saved=json.loads((args.root/'summary.json').read_text());base=MPCConfig(**saved['config'])
    scenario_root=args.root.parent/'terminal_tuning_v2'
    refs={0:np.array(json.loads((scenario_root/'latest/comparison.json').read_text())['reference']),
          1:np.array(json.loads((scenario_root/'previous/comparison.json').read_text())['reference'])}
    if args.validate:
        candidates=[json.loads(args.validate.read_text())]
        case_names=[f's{s}_r{r:02}' for s in (0,1) for r in range(10)]
    else:
        candidates=[
          dict(name='current',weights={}),
          dict(name='terminal_v4',weights={'q_terminal_velocity':4.}),
          dict(name='terminal_v8',weights={'q_terminal_velocity':8.}),
          dict(name='terminal_v32',weights={'q_terminal_velocity':32.}),
          dict(name='terminal_p96_v16',weights={'q_terminal_position':96.,'q_terminal_velocity':16.}),
          dict(name='velocity_q4',weights={'q_velocity':4.,'q_terminal_velocity':16.}),
          dict(name='velocity_q8',weights={'q_velocity':8.,'q_terminal_velocity':32.}),
          dict(name='position_q16_velocity4',weights={'q_position':16.,'q_velocity':4.,'q_terminal_position':48.,'q_terminal_velocity':16.}),
        ]
        case_names=['s0_r07']
    summary=[]
    for candidate in candidates:
        cfg=replace(base,**candidate['weights'])
        for name in case_names:
            case=json.loads((args.root/f'{name}.json').read_text());ref=refs[int(name[1])]
            result=run_case(cfg,case,ref)
            key=f"{candidate['name']}_{name}"
            (args.output/f'{key}.json').write_text(json.dumps(dict(candidate=candidate,case=name,result=result),indent=2))
            row=dict(candidate=candidate,case=name,**{k:v for k,v in result.items() if k!='trajectory'})
            summary.append(row)
            (args.output/'summary.json').write_text(json.dumps(dict(model=__doc__,position_tolerance_m=.05,
               speed_tolerance_mps=.05,hold_s=2.,base_config=saved['config'],runs=summary),indent=2))
            print(candidate['name'],name,'PASS',result['passed'],'failed calls',result['failed_solver_calls'],
                  'error',round(result['final_error_m'],5),'settle',result['settle_5cm_s'],
                  'lateral',round(result['max_lateral_m'],3),'gap',round(result['min_physical_gap_m'],3),flush=True)


if __name__=='__main__':main()
