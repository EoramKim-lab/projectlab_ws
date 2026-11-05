"""Module 3: horizontal points -> convex halfplanes A @ p <= b. No ROS.
The set is an inner approximation relative to the supplied points, not a
certificate for unobserved surfaces, unknown space, or moving obstacles.
"""
from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class HalfplaneConfig:
    # 360도 구간 나누기
    num_sectors: int = 36
    # 제약 평면 생성 범위
    constraint_range: float = 2.0
    drone_radius: float = 0.35
    safety_margin: float = 0.20

    def __post_init__(self):
        if self.num_sectors < 1:
            raise ValueError('num_sectors must be positive')
        if not all(math.isfinite(v) for v in (self.constraint_range, self.drone_radius, self.safety_margin)):
            raise ValueError('configuration values must be finite')
        if self.constraint_range <= 0 or self.drone_radius < 0 or self.safety_margin < 0:
            raise ValueError('invalid range/radius/margin')


@dataclass
class Halfplanes:
    # 평면 파라미터
    A: np.ndarray           # (M,2), outward unit normals; M <= num_sectors
    b: np.ndarray           # (M,), meters
    # 섹터 번호
    sector_ids: np.ndarray  # (M,)
    # 장애물과 직선거리
    nearest_range: np.ndarray

    # 예외처리
    @property
    def origin_feasible(self):
        # This only tests p=0, not whether a nonempty feasible set exists elsewhere.
        return bool(np.all(self.b >= 0))


def build_halfplanes(points, cfg=None):
    """One halfplane per occupied angular sector; empty sectors add no row.
    u = direction of nearest point in the sector.
    b = min(q @ u for ALL points in that sector) - safe_distance.
    Using minimum projection keeps the bound conservative for off-axis points.
    p is expressed in the current scan's body FRD frame, with p0=(0,0).
    """
    cfg = cfg or HalfplaneConfig()
    
    # 장애물 점들의 바디 FRD 좌표 (x: 앞, y: 오른쪽)
    q = np.asarray(points, dtype=float) # [[m],[m]]

    # 예외처리
    if q.ndim != 2 or q.shape[1] != 2 or not np.isfinite(q).all():
        raise ValueError('points must be finite (N,2)')

    # 장애물 점들의 직선 거리
    r = np.linalg.norm(q, axis=1) # [m]

    # 설정 거리 이내의 점만 유지
    keep = r <= cfg.constraint_range
    q, r = q[keep], r[keep] # [m]

    # 섹션의 각도 폭
    width = 2*math.pi/cfg.num_sectors # 10 도

    # 섹터 번호 (0~35)
    sectors = (np.floor(np.mod(np.arctan2(q[:,1],q[:,0]) + width/2, 2*math.pi)/width).astype(int) % cfg.num_sectors)

    # 순서대로 A행, b, 섹터 번호, 거리
    rows, bounds, ids, ranges = [], [], [], []

    # 드론 + 안전 마진
    safe = cfg.drone_radius + cfg.safety_margin

    for sector in np.unique(sectors):
        # 현재 for문에서 sector에 해당하는 점들의 인덱스
        m = sectors == sector

        # 현재 섹터 좌표값과 직선거리
        local_q, local_r = q[m], r[m]

        # 가장 가까운 점의 인덱스
        k = int(np.argmin(local_r))

        # 가장 가까운 점의 단위벡터
        u = local_q[k]/local_r[k] if local_r[k] > 1e-12 else np.array([1.,0.])
        
        rows.append(u)
        bounds.append(float(np.min(local_q @ u)-safe))
        ids.append(sector)
        ranges.append(local_r[k])

    return Halfplanes(np.asarray(rows,dtype=float).reshape(-1,2),
                      np.asarray(bounds,dtype=float), np.asarray(ids,dtype=int),
                      np.asarray(ranges,dtype=float))
