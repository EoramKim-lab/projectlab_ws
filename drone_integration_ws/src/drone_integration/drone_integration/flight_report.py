"""Offline ENU flight plots and interactive LiDAR/obstacle HTML (no ROS needed)."""
import argparse
from bisect import bisect_right
import json
import math
from pathlib import Path
import numpy as np
from .world_scene import ned_to_enu, snapshot_world
from .flight_animation import save_animation

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


def render(path, output=None, max_frames=240, reference_ned=None, world_sdf=None, ned_origin_enu=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    if max_frames < 2:
        raise ValueError('max_frames must be >= 2')
    path = Path(path)
    output = Path(output) if output else path.with_suffix('')
    output.mkdir(parents=True, exist_ok=True)
    sidecar = path.with_suffix('.scene.json')
    scene = (snapshot_world(world_sdf, ned_origin_enu if ned_origin_enu is not None else (0., 0., 0.)) if world_sdf else
             json.loads(sidecar.read_text()) if sidecar.exists() else None)
    origin = (ned_origin_enu if ned_origin_enu is not None else
              scene['ned_origin_enu'] if scene else (0., 0., 0.))
    ned_to_enu(np.zeros((1, 3)), origin)
    shapes = scene['shapes'] if scene else []
    def draw_scene(ax):
        for i, shape in enumerate(shapes):
            ax.add_patch(Polygon(shape['points'], closed=True, facecolor='gray',
                                 edgecolor='dimgray', alpha=.6,
                                 label='World obstacles (SDF)' if i == 0 else None))
    series, malformed = load_records(path)
    available = [t for items in series.values() for t, _ in items]
    if not available:
        raise ValueError('No plottable messages in log')
    start, end = min(available), max(available)
    nav = series['/navigation/state']
    cmd = series['/control/velocity_cmd']
    recorded_references = reference_segments(series['/control/reference'])
    references = recorded_references or reference_segments([], reference_ned)
    references_enu = [ned_to_enu(segment, origin) for segment in references]
    positions_enu = np.empty((0, 3))
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    draw_scene(axes[0,0])
    axes[0,0].set(xlabel="World East [m]", ylabel="World North [m]", title="Trajectory (Gazebo ENU)")
    axes[0,0].set_aspect("equal", adjustable="datalim")
    if nav:
        times = np.array([t-start for t, d in nav])
        positions = np.array([[d['pose']['position'][k] for k in ('x','y','z')]
                              if d.get('valid') else [np.nan]*3 for t,d in nav], dtype=float)
        velocity = np.array([[d['twist']['linear'][k] for k in ('x','y','z')]
                             if d.get('valid') else [np.nan]*3 for t,d in nav], dtype=float)
        positions_enu = ned_to_enu(positions, origin)
        axes[0,0].plot(positions_enu[:,0], positions_enu[:,1], label='Measured (NED converted)')
        axes[0,0].axis('equal')
        axes[0,1].plot(times, positions_enu[:,2], label='World height (ENU z)')
        axes[0,1].set(xlabel='Time [s]', ylabel='Height [m]')
        for j in range(2):
            axes[1,j].plot(times, velocity[:,j], label='Measured')
    for i, segment in enumerate(references_enu):
        label = 'Reference' if len(references) == 1 else f'Reference {i+1}'
        axes[0,0].plot(segment[:,0], segment[:,1], '--', color='tab:green',
                       linewidth=2, label=label)
        axes[0,0].scatter(segment[0,0], segment[0,1], color='tab:green', marker='o',
                          label='Reference start' if i == 0 else None, zorder=4)
        axes[0,0].scatter(segment[1,0], segment[1,1], color='tab:red', marker='*', s=100,
                          label='Reference goal' if i == 0 else None, zorder=4)
    for j, k in enumerate(('x','y')):
        if cmd:
            axes[1,j].plot([t-start for t,d in cmd],
                           [float(d['twist']['linear'][k]) for t,d in cmd], label='MPC command', alpha=.7)
        axes[1,j].set(xlabel='Time [s]', ylabel=('North velocity [m/s]' if j == 0 else 'East velocity [m/s]'))
    for ax in axes.flat:
        ax.grid(alpha=.3)
        if ax.lines:
            ax.legend()
    fig.suptitle(path.name)
    fig.tight_layout()
    fig.savefig(output/'flight_plots.png', dpi=150)
    plt.close(fig)

    # A separate full-size world trajectory is useful alongside the time plots.
    fig, ax = plt.subplots(figsize=(13, 5))
    draw_scene(ax)
    if len(positions_enu):
        ax.plot(positions_enu[:, 0], positions_enu[:, 1], label='Measured (NED converted)')
    for i, segment in enumerate(references_enu):
        ax.plot(segment[:, 0], segment[:, 1], '--', color='tab:green', label='Reference' if i == 0 else None)
        ax.scatter(segment[-1, 0], segment[-1, 1], color='tab:red', marker='*', s=90)
    ax.set(xlabel='Gazebo world East [m]', ylabel='Gazebo world North [m]',
           title=path.name + ' — world ENU')
    ax.set_aspect('equal', adjustable='datalim'); ax.grid(alpha=.3)
    if ax.lines or ax.patches: ax.legend()
    fig.tight_layout(); fig.savefig(output/'trajectory_world.png', dpi=160); plt.close(fig)

    scans = series['/lidar/processed']
    obstacles = series['/control/obstacles']
    nav_times = [t for t, d in nav]
    scan_times = [t for t, d in scans]
    obstacle_times = [t for t, d in obstacles]
    frame_count = min(max_frames, max(2, int((end-start)*5)+1))
    frame_times = np.linspace(start, end, frame_count)
    frames = []
    trajectory = []
    for timestamp, data in nav:
        if data.get('valid') and data.get('header', {}).get('frame_id') == 'map_ned':
            point = ned_to_enu([data['pose']['position'][k] for k in ('x','y')], origin)
            if np.isfinite(point).all():
                trajectory.append(dict(t=timestamp-start, xy=point.tolist()))
    for timestamp in frame_times:
        scan = recent(scans, scan_times, timestamp)
        scan_index = bisect_right(scan_times, timestamp)-1
        scan_stamp = scan_times[scan_index] if scan is not None else timestamp
        pose = recent(nav, nav_times, scan_stamp)
        current_pose = recent(nav, nav_times, timestamp)
        detection = recent(obstacles, obstacle_times, timestamp)
        points = np.empty((0, 2)); world = np.empty((0, 2)); drone = None; fitted = []
        if scan and scan.get('valid') and scan.get('header', {}).get('frame_id') == 'base_link_frd':
            points = xy_points(scan)
        if pose and pose.get('valid') and pose.get('header', {}).get('frame_id') == 'map_ned':
            world = ned_to_enu(to_world(points, pose), origin)
            world = world[np.isfinite(world).all(axis=1)]
        if current_pose and current_pose.get('valid') and current_pose.get('header', {}).get('frame_id') == 'map_ned':
            point = ned_to_enu([current_pose['pose']['position'][k] for k in ('x','y')], origin)
            if np.isfinite(point).all(): drone = point.tolist()
        if detection and detection.get('header', {}).get('frame_id') == 'map_ned':
            for center, radius, safe in zip(np.asarray(detection['xy']).reshape(-1, 2),
                                            detection['radius'], detection['safe_radius']):
                if np.all(np.isfinite([*center, radius, safe])) and min(radius, safe) >= 0:
                    fitted.append(dict(center=ned_to_enu(center, origin).tolist(),
                                       radius=float(radius), safe=float(safe)))
        frames.append(dict(t=float(timestamp-start), body=points.tolist(), world=world.tolist(),
                           drone=drone, obstacles=fitted))
    extent = [item['xy'] for item in trajectory]
    extent += [point[:2].tolist() for segment in references_enu for point in segment]
    extent += [point for shape in shapes for point in shape['points']]
    extent += [ob['center'] for frame in frames for ob in frame['obstacles']]
    extent = np.asarray(extent or [[-5., -5.], [5., 5.]])
    lo, hi = extent.min(axis=0)-2., extent.max(axis=0)+2.
    scene_note = ('월드 장애물: 저장된 SDF 배치. ' if scene else
                  '월드 배치 사본이 없어 실제 장애물 모양은 표시하지 않음. ')
    save_animation(output/'lidar_obstacles.html', dict(
        name=path.name, duration=float(end-start), frames=frames, trajectory=trajectory,
        references=[segment[:, :2].tolist() for segment in references_enu], shapes=shapes,
        bounds=[float(lo[0]), float(hi[0]), float(lo[1]), float(hi[1])],
        note=scene_note + 'ENU 원점 보정: ' + str(list(origin)) +
             '. 궤적은 PX4 추정 NED를 변환한 값이며 Gazebo ground truth가 아님. '
             'LiDAR와 추정 장애물은 최대 0.3초 이내 과거 표본만 사용. '
             f'애니메이션 표본 간격 {(end-start)/(frame_count-1):.3f}초.'))
    summary = {'source': str(path.resolve()), 'duration_s': end-start,
               'reference_source': ('/control/reference' if recorded_references else
                                    'explicit NED fallback' if references else 'unavailable'),
               'reference_segments_ned': [s.tolist() for s in references],
               'reference_segments_enu': [s.tolist() for s in references_enu],
               'coordinate_frame': 'Gazebo world ENU (converted estimated NED)',
               'ned_origin_enu': list(origin),
               'world_scene': scene,
               'world_scene_source': ('explicit SDF' if world_sdf else 'recorded sidecar' if scene else 'unavailable'),
               'plot_samples': {k:len(v) for k,v in series.items()},
               'malformed_lines_skipped': malformed, 'animation_frames': frame_count,
               'animation_format': 'interactive standalone HTML',
               'default_playback_speed': '1x log time', 'animation_sim_seconds_per_frame': (end-start)/(frame_count-1),
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
    parser.add_argument('--world-sdf', type=Path, help='Explicit world SDF for legacy logs; must match that flight')
    parser.add_argument('--ned-origin-enu', type=float, nargs=3, help='Gazebo ENU position of the local NED origin')
    args = parser.parse_args()
    reference = np.array(args.reference_ned).reshape(2, 3) if args.reference_ned else None
    render(args.log, args.output, args.max_frames, reference, args.world_sdf, args.ned_origin_enu)


if __name__ == '__main__':
    main()
