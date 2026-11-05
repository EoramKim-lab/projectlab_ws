"""LaserScan fields -> horizontal body FRD points [m].

The hardware profile handles the physical RPLIDAR C1 / sllidar angle convention
and its current mounting roll. The SILS profile handles standard Gazebo
LaserScan angles from the upright, top-mounted 2D sensor. No attitude
compensation or scan deskew is applied in this planar preprocessing stage.
"""
from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class PreprocessConfig:

    # 라이다 인정 범위
    min_range: float = 0.15
    max_range: float = 8.0

    # 라이다 회전 각도 보정
    yaw_offset: float = 0.0  # Positive about body +z (down), turning right.
    
    # Mount roll correction. For the upright top-mounted Gazebo sensor this is False.
    upside_down: bool = True

    # 'sllidar_c1': physical RPLIDAR C1 driver angle convention;
    # 'gazebo': standard Gazebo LaserScan (+angle is sensor-left).
    scan_convention: str = 'sllidar_c1'

    # 위치 보정
    offset_x: float = 0.0
    offset_y: float = 0.0

    # 
    step: int = 2

    neighbor_radius: float = 0.20
    min_neighbors: int = 2
    neighbor_window: int = 4

    # 대출 샘플링 + 예외처리 인듯?
    def __post_init__(self):
        if not all(math.isfinite(v) for v in (self.min_range, self.max_range,
                self.yaw_offset, self.offset_x, self.offset_y, self.neighbor_radius)):
            raise ValueError('configuration values must be finite')
        if not 0 <= self.min_range < self.max_range:
            raise ValueError('require 0 <= min_range < max_range')
        if self.step < 1 or self.neighbor_window < 1 or self.neighbor_radius < 0:
            raise ValueError('invalid sampling/neighbor settings')
        if self.scan_convention not in ('sllidar_c1', 'gazebo'):
            raise ValueError('scan_convention must be sllidar_c1 or gazebo')
        if not 0 <= self.min_neighbors <= 2 * self.neighbor_window:
            raise ValueError('invalid min_neighbors')


def preprocess_scan(ranges, angle_min, angle_increment, range_min=0.0,
                    range_max=float('inf'), cfg=None):

    cfg = cfg or PreprocessConfig()

    # 라이다 측정값
    r = np.asarray(ranges, dtype=float)

    # 예외 처리
    if r.ndim != 1:
        raise ValueError('ranges must be one-dimensional')
    
    if not math.isfinite(angle_min) or not math.isfinite(angle_increment) or angle_increment == 0:
        raise ValueError('invalid scan angles')
    
    if not math.isfinite(range_min) or range_min < 0 or math.isnan(range_max) or range_max <= range_min:
        raise ValueError('invalid sensor range limits')

    # 라이다 측정값 범위 제한
    lo, hi = max(cfg.min_range, range_min), min(cfg.max_range, range_max)

    # 라이다 측정값 각도 계산
    angles = angle_min + angle_increment * np.arange(r.size)
    if cfg.scan_convention == 'sllidar_c1':
        # Physical C1 + sllidar driver (inverted=false): the driver's angle is
        # alpha = pi - theta relative to the C1 datasheet's forward axis.
        theta = math.pi - angles
        # The real sensor is mounted rolled 180 deg about its forward axis.
        body_angles = -theta if cfg.upside_down else theta
    else:
        # Gazebo LaserScan uses +angle toward sensor-left (+y in FLU).
        # Navigation points are represented in PX4 body FRD (+y right), hence
        # the sign reversal. An upside-down roll reverses it once more.
        body_angles = -angles if not cfg.upside_down else angles
    angles = body_angles + cfg.yaw_offset

    # 측정값마다 유효한 범위인지 확인
    good = np.isfinite(r) & (r > 0) & (r >= lo) & (r <= hi)

    # 유효한 측정값을 기반으로 2D 좌표 계산 (x: 앞, y: 오른쪽)
    points = np.column_stack((r[good]*np.cos(angles[good]) + cfg.offset_x,
                              r[good]*np.sin(angles[good]) + cfg.offset_y))

    # 유효한 점의 개수 계산
    n = len(points)

    # 이웃 점 수 확인 & 중복된 이웃 점 제거
    if cfg.min_neighbors and n:
        counts = np.zeros(n, dtype=int)
        # Unique circular neighbors; no duplicate counting for small scans.
        shifts = {s % n for k in range(1, cfg.neighbor_window+1) for s in (k, -k)} - {0}
        for shift in shifts:
            counts += np.linalg.norm(points-np.roll(points, shift, axis=0), axis=1) <= cfg.neighbor_radius
        points = points[counts >= cfg.min_neighbors]
    
    return points[::cfg.step].copy()


# Receiver and preprocessing are deliberately in the same node/module.
from dataclasses import fields
from sensor_msgs.msg import LaserScan
from drone_interfaces.msg import ProcessedScan
from ..common import Base, SENSOR_QOS, run

class LidarReceiverNode(Base):
    def __init__(self):
        super().__init__('lidar_receiver_node')
        defaults = PreprocessConfig()
        self.cfg = PreprocessConfig(**{f.name:self.param(f.name,getattr(defaults,f.name)) for f in fields(defaults)})
        self.timeout = self.param('scan_timeout',.3)
        self.minimum = self.param('min_points',3)
        self.body = self.param('body_frame','base_link_frd')
        self.start_monitor('lidar')
        self.last = None
        self.pub = self.create_publisher(ProcessedScan,'lidar/processed',10)
        self.create_subscription(LaserScan,self.param('scan_topic','/scan'),self.scan,SENSOR_QOS)
        self.create_timer(.1,self.watchdog)

    def scan(self,msg):
        out = ProcessedScan()
        out.header.stamp = msg.header.stamp
        out.header.frame_id = self.body
        out.raw_count = len(msg.ranges)
        self.last = msg.header.stamp
        out.reason = 'invalid_or_stale_scan'
        if self.fresh(msg.header.stamp,self.timeout) and self.increasing('scan',msg.header.stamp.sec*1e9+msg.header.stamp.nanosec):
            try:
                points = preprocess_scan(msg.ranges,msg.angle_min,msg.angle_increment,
                                         msg.range_min,msg.range_max,self.cfg)
                out.xy = points.reshape(-1).tolist()
                out.valid = len(points) >= self.minimum
                out.reason = 'ok' if out.valid else 'too_few_points'
            except ValueError as exc:
                out.reason = str(exc)
        pts = np.asarray(out.xy).reshape(-1, 2)
        nearest = float(np.linalg.norm(pts, axis=1).min()) if len(pts) else float('nan')
        self.observe('lidar', f'valid={out.valid} reason={out.reason} raw={out.raw_count} points={len(pts)} nearest_body={nearest:.3f}m')
        self.pub.publish(out)

    def watchdog(self):
        if self.last is None or not self.fresh(self.last,self.timeout):
            out = ProcessedScan()
            out.header.stamp = self.last if self.last is not None else self.get_clock().now().to_msg()
            out.header.frame_id = self.body
            out.reason = 'scan_timeout'
            self.pub.publish(out)

def main(args=None): run(LidarReceiverNode,args)

