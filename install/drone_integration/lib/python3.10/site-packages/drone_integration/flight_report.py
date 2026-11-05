"""Offline JSONL flight plots and time-aligned LiDAR/obstacle GIF (no ROS needed)."""
import argparse
from bisect import bisect_right
import json
import math
from pathlib import Path
import numpy as np

TOPICS = ('/navigation/state', '/control/velocity_cmd', '/lidar/processed',
          '/control/obstacles', '/fmu/out/vehicle_status_v1', '/control/reference')


def source_time(record):
    stamp = record['data'].get('header', {}).get('stamp', {})
    value = stamp.get('sec', 0) + stamp.get('nanosec', 0) * 1e-9
    return value if value > 0 else record['received_ns'] * 1e-9


def load_records(path):
    """Stream all messages, retaining at most 10 Hz per plotted topic."""
    series = {topic: [] for topic in TOPICS}
    malformed = 0
    with Path(path).open() as stream:
        for line in stream:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            topic = record.get('topic')
            if topic not in series or record.get('missing'):
                continue
            t = source_time(record)
            items = series[topic]
            if not items or t - items[-1][0] >= .099 or topic.endswith('vehicle_status_v1'):
                items.append((t, record['data']))
    for items in series.values():
        items.sort(key=lambda item: item[0])
    return series, malformed


def recent(items, times, timestamp, max_age=.3):
    index = bisect_right(times, timestamp) - 1
    if index < 0 or timestamp - times[index] > max_age:
        return None
    return items[index][1]


def xy_points(data):
    xy = np.asarray(data.get('xy', []), dtype=float).reshape(-1, 2)
    return xy[np.all(np.isfinite(xy), axis=1)]


def to_world(points, nav):
    q = nav['pose']['orientation']
    # Full body FRD -> NED quaternion rotation for body points with z=0.
    x, y, z, w = (q[k] for k in ('x', 'y', 'z', 'w'))
    norm = math.sqrt(x*x + y*y + z*z + w*w)
    if not math.isfinite(norm) or norm < 1e-9:
        raise ValueError('Invalid navigation quaternion')
    x, y, z, w = x/norm, y/norm, z/norm, w/norm
    rotation = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w)],
                         [2*(x*y+z*w), 1-2*(x*x+z*z)]])
    p = nav['pose']['position']
    return points @ rotation.T + [p['x'], p['y']]


def reference_segments(records, fallback=None):
    """Return distinct recorded NED mission segments, or an explicit legacy fallback."""
    segments = []
    for _, data in records:
        if data.get('header', {}).get('frame_id') != 'map_ned':
            continue
        poses = data.get('poses', [])
        if len(poses) != 2:
            continue
        try:
            segment = np.array([[p['position'][k] for k in ('x', 'y', 'z')]
                                for p in poses], dtype=float)
        except (KeyError, TypeError, ValueError):
            continue
        if np.isfinite(segment).all() and not any(np.allclose(segment, s) for s in segments):
            segments.append(segment)
    if not segments and fallback is not None:
        segment = np.asarray(fallback, dtype=float)
        if segment.shape != (2, 3) or not np.isfinite(segment).all():
            raise ValueError('reference fallback must contain two finite NED 3D points')
        segments.append(segment)
    return segments


def render(path, output=None, max_frames=240, reference_ned=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter
    from matplotlib.patches import Circle
    if max_frames < 2:
        raise ValueError('max_frames must be >= 2')
    path = Path(path)
    output = Path(output) if output else path.with_suffix('')
    output.mkdir(parents=True, exist_ok=True)
    series, malformed = load_records(path)
    available = [t for items in series.values() for t, _ in items]
    if not available:
        raise ValueError('No plottable messages in log')
    start, end = min(available), max(available)
    nav = series['/navigation/state']
    cmd = series['/control/velocity_cmd']
    recorded_references = reference_segments(series['/control/reference'])
    references = recorded_references or reference_segments([], reference_ned)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    if nav:
        times = np.array([t-start for t, d in nav])
        positions = np.array([[d['pose']['position'][k] for k in ('x','y','z')]
                              if d.get('valid') else [np.nan]*3 for t,d in nav], dtype=float)
        velocity = np.array([[d['twist']['linear'][k] for k in ('x','y','z')]
                             if d.get('valid') else [np.nan]*3 for t,d in nav], dtype=float)
        axes[0,0].plot(positions[:,0], positions[:,1], label='Measured')
        axes[0,0].set(xlabel='North x [m]', ylabel='East y [m]', title='Trajectory (NED)')
        axes[0,0].axis('equal')
        axes[0,1].plot(times, -positions[:,2], label='Height (-NED z)')
        axes[0,1].set(xlabel='Time [s]', ylabel='Height [m]')
        for j in range(2):
            axes[1,j].plot(times, velocity[:,j], label='Measured')
    for i, segment in enumerate(references):
        label = 'Reference' if len(references) == 1 else f'Reference {i+1}'
        axes[0,0].plot(segment[:,0], segment[:,1], '--', color='tab:orange',
                       linewidth=2, label=label)
        axes[0,0].scatter(segment[0,0], segment[0,1], color='tab:green', marker='o',
                          label='Reference start' if i == 0 else None, zorder=4)
        axes[0,0].scatter(segment[1,0], segment[1,1], color='tab:red', marker='*', s=100,
                          label='Reference goal' if i == 0 else None, zorder=4)
    for j, k in enumerate(('x','y')):
        if cmd:
            axes[1,j].plot([t-start for t,d in cmd],
                           [float(d['twist']['linear'][k]) for t,d in cmd], label='MPC command', alpha=.7)
        axes[1,j].set(xlabel='Time [s]', ylabel=f'v{k} [m/s]')
    for ax in axes.flat:
        ax.grid(alpha=.3)
        if ax.lines:
            ax.legend()
    fig.suptitle(path.name)
    fig.tight_layout()
    fig.savefig(output/'flight_plots.png', dpi=150)
    plt.close(fig)

    scans = series['/lidar/processed']
    obstacles = series['/control/obstacles']
    nav_times = [t for t,d in nav]
    scan_times = [t for t,d in scans]
    obstacle_times = [t for t,d in obstacles]
    frame_count = min(max_frames, max(2, int((end-start)*5)+1))
    frame_times = np.linspace(start, end, frame_count)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
    def draw(timestamp):
        for ax in axes:
            ax.clear()
            ax.grid(alpha=.25)
            ax.set_aspect('equal')
        scan = recent(scans, scan_times, timestamp)
        # Transform at the scan timestamp, never using a future pose.
        scan_index = bisect_right(scan_times, timestamp)-1
        scan_stamp = scan_times[scan_index] if scan is not None else timestamp
        pose = recent(nav, nav_times, scan_stamp)
        detection = recent(obstacles, obstacle_times, timestamp)
        points = np.empty((0,2))
        if scan and scan.get('valid') and scan.get('header',{}).get('frame_id') == 'base_link_frd':
            points = xy_points(scan)
        axes[0].scatter(points[:,0], points[:,1], s=3, label='Processed LiDAR')
        axes[0].plot(0,0,'r^')
        axes[0].set(xlim=(-8,8), ylim=(-8,8), xlabel='Forward [m]', ylabel='Right [m]',
                    title='LiDAR (body FRD)' if len(points) else 'LiDAR: no fresh valid points')
        if pose and pose.get('valid') and pose.get('header',{}).get('frame_id') == 'map_ned':
            world = to_world(points, pose)
            axes[1].scatter(world[:,0], world[:,1], s=3, color='gray', label='LiDAR in NED')
            p = pose['pose']['position']
            axes[1].plot(p['x'],p['y'],'r^',label='Drone')
            axes[1].set(xlim=(p['x']-5,p['x']+5), ylim=(p['y']-5,p['y']+5))
        else:
            axes[1].set(xlim=(-5,5), ylim=(-5,5))
        count = 0
        if detection and detection.get('header',{}).get('frame_id') == 'map_ned':
            for center, radius, safe in zip(np.asarray(detection['xy']).reshape(-1,2),
                                            detection['radius'], detection['safe_radius']):
                if not np.all(np.isfinite([*center, radius, safe])):
                    continue
                axes[1].add_patch(Circle(center, radius, fill=False, color='tab:orange', lw=2))
                axes[1].add_patch(Circle(center, safe, fill=False, color='tab:red', ls='--'))
                count += 1
        axes[1].set(xlabel='North x [m]', ylabel='East y [m]',
                    title=f'Obstacles: {count}' if detection else 'Obstacles: no fresh data')
        fig.suptitle(f't = {timestamp-start:.2f} s / {end-start:.2f} s | orange: fitted, red: safety radius')
        fig.tight_layout()
    animation = FuncAnimation(fig, draw, frames=frame_times, repeat=False)
    animation.save(output/'lidar_obstacles.gif', writer=PillowWriter(fps=5), dpi=80)
    plt.close(fig)
    summary = {'source': str(path.resolve()), 'duration_s': end-start,
               'reference_source': ('/control/reference' if recorded_references else
                                    'explicit NED fallback' if references else 'unavailable'),
               'reference_segments_ned': [s.tolist() for s in references],
               'plot_samples': {k:len(v) for k,v in series.items()},
               'malformed_lines_skipped': malformed, 'animation_frames': frame_count,
               'animation_fps': 5, 'animation_sim_seconds_per_frame': (end-start)/(frame_count-1),
               'alignment': 'header timestamp; latest past sample; maximum age 0.3 s',
               'lidar': 'processed body FRD points; raw scan is not displayed',
               'note': 'Observed log interval; does not imply complete takeoff-to-landing coverage.'}
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(output.resolve(), flush=True)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--max-frames', type=int, default=240)
    parser.add_argument('--reference-ned', type=float, nargs=6,
                        metavar=('START_N', 'START_E', 'START_D', 'GOAL_N', 'GOAL_E', 'GOAL_D'),
                        help='Legacy log fallback: actual mission endpoints from its MPC log')
    args = parser.parse_args()
    reference = np.array(args.reference_ned).reshape(2, 3) if args.reference_ned else None
    render(args.log, args.output, args.max_frames, reference)


if __name__ == '__main__':
    main()
