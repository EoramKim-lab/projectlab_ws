"""Time only CasADi Opti.solve() calls in one ideal closed-loop scenario.

This is an offline benchmark, not PX4/Gazebo flight. Opti.solve wall time includes
CasADi/IPOPT invocation overhead, but excludes set_value, set_initial, path/plane
construction and solution extraction. Startup warmup is reported separately.
"""
import argparse
import csv
from dataclasses import asdict, fields
import json
from pathlib import Path
import time
import numpy as np
import yaml
from drone_integration.control.mpc_controller import MPCConfig, MPCController
from drone_integration.control.obstacle_detection import DetectedCircle


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('scenario', 'config', 'output'):
        p.add_argument('--'+arg, type=Path, required=True)
    args = p.parse_args()
    scenario = json.loads(args.scenario.read_text())
    params = yaml.safe_load(args.config.read_text())['mpc_node']['ros__parameters']
    cfg = MPCConfig(**dict({f.name: params[f.name] for f in fields(MPCConfig) if f.name in params},
                          control_dt=1./params['publish_rate']))
    ref, center = np.array(scenario['reference']), np.array(scenario['center'])
    c = MPCController(cfg, reference_start=ref[0])
    call_times = []
    original_solve = c.opti.solve

    def measured_solve():
        t = time.perf_counter_ns()
        try:
            return original_solve()
        finally:
            call_times.append((time.perf_counter_ns()-t)/1e6)

    c.opti.solve = measured_solve
    warmup_compute_s = c.warmup()
    warmup_calls = call_times.copy()
    call_times.clear()
    rows, calls, trajectory = [], [], []
    state = np.r_[ref[0], 0., 0.]
    for step in range(round(30/cfg.control_dt)):
        call_times.clear()
        result = c.compute(state, ref[1], [DetectedCircle(center-state[:2], scenario['radius'])])
        for index, elapsed in enumerate(call_times):
            calls.append(dict(step=step, call=index, solve_ms=elapsed))
        rows.append(dict(step=step, success=result.success, calls=len(call_times),
                         solver_total_ms=sum(call_times), compute_ms=result.solve_time*1000,
                         reason=result.reason))
        if not result.success:
            break
        state = result.predicted_states[1].copy()
        trajectory.append(state.tolist())
        if np.linalg.norm(state[:2]-ref[1]) < .15 and np.linalg.norm(state[2:]) < .05:
            break

    def stats(values):
        return dict(count=len(values), median_ms=float(np.median(values)),
                    p95_ms=float(np.percentile(values, 95)), max_ms=float(max(values)),
                    over_50ms=sum(v>50 for v in values))

    report = dict(measurement=__doc__, scenario=str(args.scenario.resolve()),
                  config=asdict(cfg), reference=ref.tolist(), center=center.tolist(), radius=scenario['radius'],
                  reached=bool(np.linalg.norm(state[:2]-ref[1])<.15 and np.linalg.norm(state[2:])<.05),
                  failures=sum(not r['success'] for r in rows), model_duration_s=len(rows)*cfg.control_dt,
                  warmup_compute_ms=warmup_compute_s*1000, warmup_solve_ms=warmup_calls,
                  per_solver_call=stats([r['solve_ms'] for r in calls]),
                  per_control_cycle_solver_total=stats([r['solver_total_ms'] for r in rows]),
                  per_control_cycle_compute_total=stats([r['compute_ms'] for r in rows]),
                  trajectory=trajectory)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'summary.json').write_text(json.dumps(report, indent=2))
    for filename, records in [('solver_calls.csv', calls), ('control_cycles.csv', rows)]:
        with (args.output/filename).open('w') as stream:
            writer = csv.DictWriter(stream, fieldnames=records[0].keys())
            writer.writeheader(); writer.writerows(records)
    print(json.dumps({k:v for k,v in report.items() if k not in ('trajectory','config','measurement')}, indent=2))


if __name__ == '__main__':
    main()
