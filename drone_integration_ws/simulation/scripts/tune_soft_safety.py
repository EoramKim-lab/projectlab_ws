"""Compare slack or terminal costs with a log-derived circle and ideal MPC dynamics.
Not a PX4/Gazebo flight: omits sensor/actuator delay and changing obstacle fits.
"""
import argparse,json,time
from dataclasses import asdict,fields
from pathlib import Path
import numpy as np
import yaml
from drone_integration.control.mpc_controller import MPCConfig,MPCController
from drone_integration.control.obstacle_detection import DetectedCircle

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('log','config','output'):parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--sweep', choices=('slack', 'terminal'), default='slack')
    parser.add_argument('--terminal-pair', type=float, nargs=2, action='append',
                        metavar=('POSITION', 'VELOCITY'),
                        help='Explicit terminal weights; repeat to compare independently')
    args=parser.parse_args()
    if args.terminal_pair and args.sweep != 'terminal':
        parser.error('--terminal-pair requires --sweep terminal')
    ref,obs,nav=None,[],[]
    for line in args.log.open():
        r=json.loads(line)
        if r.get('missing'):continue
        d,t=r['data'],r['received_ns']/1e9
        if r['topic']=='/control/reference' and len(d.get('poses',[]))==2 and ref is None:
            ref=np.array([[p['position'][k] for k in ('x','y')] for p in d['poses']])
        if r['topic']=='/control/obstacles' and len(d['radius'])==1:obs.append((t,d))
        if r['topic']=='/navigation/state' and d.get('valid'):nav.append((t,d))
    if ref is None or not nav or not obs:raise ValueError('Reference/navigation/circle data required')
    early=[d for t,d in obs if t<nav[0][0]+15]
    center=np.median([d['xy'] for d in early],axis=0)
    radius=float(np.median([d['radius'][0] for d in early]))
    p=yaml.safe_load(args.config.read_text())['mpc_node']['ros__parameters']
    params={f.name:p[f.name] for f in fields(MPCConfig) if f.name in p}
    params['control_dt']=1./p['publish_rate']
    direction=(ref[1]-ref[0])/np.linalg.norm(ref[1]-ref[0]);lateral=np.array([-direction[1],direction[0]])
    rows=[];args.output.mkdir(parents=True,exist_ok=True)
    base = MPCConfig(**params)
    if args.sweep == 'terminal':
        pairs = args.terminal_pair or [(base.q_terminal_position*m, base.q_terminal_velocity*m)
                                      for m in (1,2,4,8)]
        candidates = [dict(q_terminal_position=a, q_terminal_velocity=b) for a,b in pairs]
    else:
        candidates = [dict(safety_slack_linear=a,safety_slack_quadratic=b)
                      for a,b in ((100.,1000.),(20.,200.),(5.,50.),(1.,10.))]
    for weights in candidates:
        cfg=MPCConfig(**dict(params,**weights))
        c=MPCController(cfg,reference_start=ref[0]);state=np.r_[ref[0],0.,0.]
        trajectory,solve_times,failures=[state.copy()],[],[];started=time.monotonic()
        for k in range(round(30/cfg.control_dt)):
            result=c.compute(state,ref[1],[DetectedCircle(center-state[:2],radius)])
            solve_times.append(result.solve_time)
            if not result.success:
                failures.append({'step':k,'reason':result.reason});break
            state=result.predicted_states[1].copy();trajectory.append(state.copy())
            if args.sweep == 'slack' and np.linalg.norm(state[:2]-ref[1])<.15 and np.linalg.norm(state[2:])<.05:break
        x=np.array(trajectory);errors=(x[:,:2]-ref[0])@lateral
        gap=np.linalg.norm(x[:,:2]-center,axis=1)-radius-cfg.drone_radius
        reached=np.linalg.norm(state[:2]-ref[1])<.15 and np.linalg.norm(state[2:])<.05
        near_goal = (np.linalg.norm(x[:,:2]-ref[1],axis=1)<.15) & (np.linalg.norm(x[:,2:],axis=1)<.05)
        outside = np.flatnonzero(~near_goal)
        settling = ((int(outside[-1])+1)*cfg.control_dt if len(outside) and near_goal[-1]
                    else 0. if near_goal.all() else None)
        row=dict(linear=cfg.safety_slack_linear,quadratic=cfg.safety_slack_quadratic,
                 terminal_position=cfg.q_terminal_position,terminal_velocity=cfg.q_terminal_velocity,
                 settling_time_s=settling,
                 longitudinal_overshoot_m=float(max(0.,np.max((x[:,:2]-ref[1])@direction))),
                 reached=bool(reached),failures=failures,
                 elapsed_model_s=(len(x)-1)*cfg.control_dt,lateral_rmse_m=float(np.sqrt(np.mean(errors**2))),
                 max_lateral_m=float(np.max(np.abs(errors))),min_physical_gap_m=float(gap.min()),
                 max_buffer_violation_m=float(max(0.,cfg.safety_margin-gap.min())),
                 final_goal_error_m=float(np.linalg.norm(state[:2]-ref[1])),
                 solve_p95_ms=float(np.percentile(solve_times,95)*1000),wall_s=time.monotonic()-started,
                 trajectory=x.tolist())
        rows.append(row)
        report=dict(source=str(args.log.resolve()),model=__doc__,reference=ref.tolist(),center=center.tolist(),
                    radius=radius,sweep=args.sweep,base_config=asdict(base),candidates=rows)
        (args.output/'comparison.json').write_text(json.dumps(report,indent=2))
        print(json.dumps({k:v for k,v in row.items() if k not in ('trajectory','failures')}),flush=True)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    axes[0].plot(ref[:,0],ref[:,1],'k--',label='Reference')
    axes[0].add_patch(Circle(center,radius+cfg.drone_radius,fill=False,color='red',label='Hard boundary'))
    axes[0].add_patch(Circle(center,radius+cfg.drone_radius+cfg.safety_margin,fill=False,color='gray',linestyle=':',label='Soft buffer'))
    for row in rows:
        x=np.array(row['trajectory'])
        label=(f"{row['terminal_position']:g} / {row['terminal_velocity']:g}" if args.sweep=='terminal'
               else f"{row['linear']:g} / {row['quadratic']:g}")
        axes[0].plot(x[:,0],x[:,1],label=label)
        error = np.linalg.norm(x[:,:2]-ref[1],axis=1) if args.sweep=='terminal' else (x[:,:2]-ref[0])@lateral
        axes[1].plot(np.arange(len(x))*cfg.control_dt,error,label=label)
    axes[0].set(xlabel='North [m]',ylabel='East [m]',title='Ideal closed-loop weight comparison');axes[0].axis('equal')
    axes[1].set(xlabel='Time [s]',ylabel='Goal distance [m]' if args.sweep=='terminal' else 'Cross-track error [m]',
                title='Terminal position / velocity weights' if args.sweep=='terminal' else 'Linear / quadratic slack weights')
    for ax in axes:ax.grid(alpha=.3);ax.legend()
    fig.tight_layout();fig.savefig(args.output/'comparison.png',dpi=150)

if __name__=='__main__':main()
