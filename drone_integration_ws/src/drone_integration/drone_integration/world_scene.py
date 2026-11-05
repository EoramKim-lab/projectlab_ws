"""Configured SDF geometry snapshots and local-NED to Gazebo-ENU conversion."""
import hashlib
import itertools
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np


def ned_to_enu(points, origin=(0., 0., 0.)):
    p = np.asarray(points, dtype=float)
    origin = np.asarray(origin, dtype=float)
    if origin.shape != (3,) or not np.isfinite(origin).all():
        raise ValueError('ENU origin must contain three finite coordinates')
    if p.shape[-1] == 2:
        return p[..., [1, 0]] + origin[:2]
    if p.shape[-1] == 3:
        return p[..., [1, 0, 2]] * [1., 1., -1.] + origin
    raise ValueError('NED points must be 2D or 3D')


def _pose(element):
    node = element.find('pose')
    if node is None:
        return np.eye(4)
    if node.get('relative_to') or node.get('degrees') == 'true':
        raise ValueError('Scene snapshot requires parent-relative poses in radians')
    p = np.array(list(map(float, (node.text or '').split())))
    if p.shape != (6,) or not np.isfinite(p).all():
        raise ValueError('Invalid SDF pose')
    roll, pitch, yaw = p[3:]
    cr, cp, cy = np.cos([roll, pitch, yaw]); sr, sp, sy = np.sin([roll, pitch, yaw])
    transform = np.eye(4)
    transform[:3, :3] = [[cy*cp, cy*sp*sr-sy*cr, cy*sp*cr+sy*sr],
                         [sy*cp, sy*sp*sr+cy*cr, sy*sp*cr-cy*sr],
                         [-sp, cp*sr, cp*cr]]
    transform[:3, 3] = p[:3]
    return transform


def _hull(points):
    points = sorted(set(map(tuple, points)))
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    def half(sequence):
        result = []
        for point in sequence:
            while len(result) >= 2 and cross(result[-2], result[-1], point) <= 0:
                result.pop()
            result.append(point)
        return result
    return half(points)[:-1] + half(reversed(points))[:-1]


def snapshot_world(path, origin=(0., 0., 0.)):
    path = Path(path).expanduser().resolve()
    raw = path.read_bytes()
    world = ET.fromstring(raw).find('world')
    if world is None:
        raise ValueError('SDF has no world')
    ned_to_enu(np.zeros((1, 3)), origin)
    shapes, omitted = [], []
    for model in world.findall('model'):
        if model.findtext('static', 'false').strip() not in ('true', '1'):
            continue
        for link in model.findall('link'):
            for collision in link.findall('collision'):
                geometry = collision.find('geometry')
                if geometry is None or geometry.find('plane') is not None:
                    continue
                transform = _pose(model) @ _pose(link) @ _pose(collision)
                box = geometry.find('box/size')
                if box is None:
                    omitted.append(model.get('name') + '/' + collision.get('name'))
                    continue
                size = np.array(list(map(float, box.text.split())))
                if size.shape != (3,) or not np.isfinite(size).all() or np.any(size <= 0):
                    raise ValueError('Invalid SDF box size')
                vertices = np.array(list(itertools.product((-1., 1.), repeat=3))) * size/2
                vertices = vertices @ transform[:3, :3].T + transform[:3, 3]
                shapes.append(dict(model=model.get('name'), type='polygon',
                                   points=[list(point) for point in _hull(vertices[:, :2])],
                                   z_min=float(vertices[:, 2].min()), z_max=float(vertices[:, 2].max())))
    return dict(version=1, frame='gazebo_world_enu', world=world.get('name'),
                source_sdf=str(path), source_sha256=hashlib.sha256(raw).hexdigest(),
                ned_origin_enu=list(map(float, origin)), shapes=shapes, omitted_geometry=omitted,
                provenance='Configured SDF file snapshot; not live Gazebo ground truth')
