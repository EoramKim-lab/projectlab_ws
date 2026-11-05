"""ROS adapter for Cartesian [x, y, vx, vy] MPC (map NED / body FRD)."""
from collections import deque
from dataclasses import fields
import math
import numpy as np
from geometry_msgs.msg import TwistStamped, Pose, PoseArray
from std_msgs.msg import Empty
from drone_interfaces.msg import NavigationState, ProcessedScan, ObstacleCircles
from ..common import Base, run, seconds
from ..math_utils import rotation
from .mpc_controller import MPCConfig, MPCController
from .obstacle_detection import DetectedCircle, _enclosing_circle


# Experiment reference: edit these map NED coordinates, rebuild, and restart.
# Horizontal reference is the fixed straight segment START -> GOAL.
REFERENCE_START_NED = (0.0, 0.0, -1.0)  # local NED meters
GOAL_NED = (0.0, 6.0, -1.0)             # meters; z is held by altitude control
REFERENCE_SPEED = 0.5                  # meters/second


def circles_from_points(xy, gap, padding, max_range=4.0):
    """Keep every processed return, including sparse single-point clusters.

    ProcessedScan preserves scan order but has no beam indices. Split on spatial
    gaps; unlike raw scan detection, missing beams cannot be identified here.
    """
    points = np.asarray(xy, dtype=float).reshape(-1, 2)
    if not np.isfinite(points).all():
        raise ValueError('nonfinite scan points')
    if len(points) == 0:
        raise ValueError('empty processed scan')
    points = points[np.linalg.norm(points, axis=1) <= max_range]
    if len(points) == 0:
        return []  # Valid scan, but no returns inside the obstacle range.
    cuts = np.flatnonzero(np.linalg.norm(np.diff(points, axis=0), axis=1) > gap) + 1
    clusters = list(np.split(points, cuts))
    if len(clusters) > 1 and np.linalg.norm(points[0] - points[-1]) <= gap:
        clusters = [np.concatenate((clusters[-1], clusters[0]))] + clusters[1:-1]
    return [DetectedCircle(*_enclosing_circle(p, padding)) for p in clusters]


class MpcNode(Base):
    def __init__(self):
        super().__init__('mpc_node')
        self.frame = self.param('map_frame', 'map_ned')
        self.body = self.param('body_frame', 'base_link_frd')
        rate = self.param('publish_rate', 20.0)
        if not math.isfinite(rate) or rate <= 0:
            raise ValueError('publish_rate must be positive')
        defaults = MPCConfig(reference_speed=REFERENCE_SPEED, max_speed=1.0)
        self.cfg = MPCConfig(**{f.name: (1.0 / rate if f.name == 'control_dt'
                                          else self.param(f.name, getattr(defaults, f.name)))
                                for f in fields(defaults)})
        self.timeout = self.param('sensor_timeout', 0.25)
        self.skew = self.param('max_scan_state_skew', 0.08)
        self.gap = self.param('cluster_gap', 0.25)
        self.obstacle_range = self.param('obstacle_range', 4.0)
        self.padding = self.param('circle_padding', 0.01)
        self.goal_tolerance = self.param('goal_tolerance', 0.15)
        self.z_gain = self.param('altitude_gain', 1.0)
        self.z_max = self.param('max_vertical_speed', 0.5)
        if not all(math.isfinite(v) and v > 0 for v in
                   (self.timeout, self.skew, self.gap, self.obstacle_range, self.goal_tolerance, self.z_gain, self.z_max)):
            raise ValueError('MPC adapter limits must be finite and positive')
        if not math.isfinite(self.padding) or self.padding < 0:
            raise ValueError('invalid circle padding')
        self.reference_mode = self.param('reference_mode', 'forward')
        self.forward_distance = self.param('forward_distance', 6.0)
        self.mission_height = self.param('mission_height', 1.0)
        if (self.reference_mode not in ('forward', 'fixed') or
                not all(math.isfinite(x) and x > 0 for x in (self.forward_distance, self.mission_height))):
            raise ValueError('invalid mission reference')
        self.reference_initialized = self.reference_mode == 'fixed'
        self.goal = np.asarray(GOAL_NED, dtype=float).copy()
        self.controller = MPCController(self.cfg, reference_start=REFERENCE_START_NED[:2])
        elapsed = self.controller.warmup()
        self.get_logger().info(f'Cartesian MPC ready (warmup {elapsed:.3f}s); state=[x,y,vx,vy], reference_mode={self.reference_mode}, speed={self.cfg.reference_speed}m/s')
        self.start_monitor('mpc')
        self.state = self.scan = None
        self.history = deque(maxlen=200)
        self.create_subscription(Empty, 'sensors/px4_reset', self.receive_px4_reset, 10)
        self.create_subscription(Empty, 'navigation/reset', self.on_navigation_reset, 10)
        self.obstacles_pub = self.create_publisher(ObstacleCircles, 'control/obstacles', 10)
        self.velocity_pub = self.create_publisher(TwistStamped, 'control/velocity_cmd', 10)
        self.reference_pub = self.create_publisher(PoseArray, 'control/reference', 1)
        self.create_timer(1.0, self.publish_reference)
        self.create_subscription(NavigationState, 'navigation/state', self.on_state, 10)
        self.create_subscription(ProcessedScan, 'lidar/processed', self.on_scan, 10)
        self.create_timer(1.0 / rate, self.solve)

    def publish_reference(self):
        """Expose the actual mission segment, including forward-mode initialization."""
        out = PoseArray()
        out.header.frame_id = self.frame
        out.header.stamp = self.get_clock().now().to_msg()
        if self.reference_initialized:
            for xy in (self.controller.reference_start, self.goal[:2]):
                pose = Pose()
                pose.position.x, pose.position.y = map(float, xy)
                pose.position.z = float(self.goal[2])
                pose.orientation.w = 1.0
                out.poses.append(pose)
        self.reference_pub.publish(out)

    def on_navigation_reset(self, msg):
        self.state = self.scan = None
        self.history.clear()
        self.reference_initialized = self.reference_mode == 'fixed'
        self.controller.reset()
        self.get_logger().warning('PX4 EKF local-position reset: MPC history and forward reference cleared')

    def on_px4_reset(self):
        self.state = self.scan = None
        self.history.clear()
        self.reference_initialized = self.reference_mode == 'fixed'
        self.controller.reset()
        self.get_logger().warning('PX4 reset: MPC history and forward reference cleared')

    def publish_obstacles(self, scan, detections, scan_pose):
        out = ObstacleCircles()
        out.header.stamp = scan.header.stamp
        out.header.frame_id = self.frame
        rotation = self.controller._rotation(scan_pose[2])
        out.xy = [float(v) for obs in detections
                  for v in scan_pose[:2] + rotation @ obs.center]
        out.radius = [float(obs.radius) for obs in detections]
        out.safe_radius = [r + self.cfg.drone_radius + self.cfg.safety_margin for r in out.radius]
        out.over_capacity = len(detections) > self.cfg.max_obstacles
        self.obstacles_pub.publish(out)

    @staticmethod
    def pose(msg):
        p, q = msg.pose.position, msg.pose.orientation
        values = np.array([p.x, p.y, p.z, q.x, q.y, q.z, q.w])
        if not np.isfinite(values).all() or np.linalg.norm(values[3:]) < 1e-6:
            raise ValueError('invalid navigation pose')
        R = rotation(values[3:])
        return np.array([p.x, p.y, math.atan2(R[1, 0], R[0, 0])])

    def on_state(self, msg):
        self.state = msg
        if msg.valid and msg.header.frame_id == self.frame:
            try:
                pose = self.pose(msg)
                if not self.reference_initialized and self.fresh(msg.header.stamp, self.timeout):
                    self.controller.reference_start = pose[:2].copy()
                    self.goal = np.r_[pose[:2] + self.forward_distance * np.array([math.cos(pose[2]), math.sin(pose[2])]), -self.mission_height]
                    self.reference_initialized = True
                    self.get_logger().info(f'Forward reference: {self.controller.reference_start} -> {self.goal}')
                t = seconds(msg.header.stamp)
                if not self.history or t > self.history[-1][0]:
                    self.history.append((t, pose))
            except ValueError:
                pass

    def on_scan(self, msg):
        self.scan = msg

    @staticmethod
    def planar_state(msg):
        p, v = msg.pose.position, msg.twist.linear
        state = np.array([p.x, p.y, v.x, v.y], dtype=float)
        if not np.isfinite(state).all():
            raise ValueError('invalid planar position/velocity')
        return state

    def solve(self):
        state, scan = self.state, self.scan
        if state is None or scan is None:
            missing = [name for name, value in [('navigation', state), ('lidar', scan)] if value is None]
            self.observe('mpc', 'WAITING: ' + ','.join(missing))
            return
        if (not state.valid or not scan.valid or state.header.frame_id != self.frame
                or scan.header.frame_id != self.body or not self.history or not self.reference_initialized
                or not self.fresh(state.header.stamp, self.timeout)
                or not self.fresh(scan.header.stamp, self.timeout)):
            self.controller.last_acceleration[:] = 0.0
            self.observe('mpc', f'BLOCKED navigation_valid={state.valid} reason={state.reason} scan_valid={scan.valid} reason={scan.reason}; check frames/ages/history')
            return
        try:
            current = self.pose(state)
            planar = self.planar_state(state)
            scan_time = seconds(scan.header.stamp)
            t, scan_pose = min(self.history, key=lambda entry: abs(entry[0] - scan_time))
            if abs(t - scan_time) > self.skew:
                self.observe('mpc', f'BLOCKED scan/state skew={abs(t-scan_time):.3f}s')
                self.controller.last_acceleration[:] = 0.0
                return
            detections = circles_from_points(scan.xy, self.gap, self.padding, self.obstacle_range)
            self.publish_obstacles(scan, detections, scan_pose)
            # Convert using pose at acquisition, then re-express for compute(),
            # which accepts circles in the current body frame.
            Rscan = self.controller._rotation(scan_pose[2])
            Rnow = self.controller._rotation(current[2])
            for obs in detections:
                obs.center = Rnow.T @ (scan_pose[:2] + Rscan @ obs.center - current[:2])
            # The supplied solver truncates obstacles. Refuse overflow instead
            # of silently planning through an obstacle outside its fixed slots.
            if len(detections) > self.cfg.max_obstacles:
                raise ValueError('obstacle capacity exceeded; increase max_obstacles')
            control = np.zeros(2)
            solve_time = 0.0
            safety_violation = 0.0
            hold_reason = ''
            if (np.linalg.norm(self.goal[:2] - planar[:2]) > self.goal_tolerance
                    or np.linalg.norm(planar[2:]) > 0.05):
                try:
                    result = self.controller.compute(planar, self.goal[:2], detections,
                                                     body_yaw=current[2])
                    solve_time = result.solve_time
                    safety_violation = result.max_safety_violation
                    if not result.success:
                        hold_reason = result.reason or 'solver unsuccessful'
                    elif (np.shape(result.velocity_command) != (2,)
                          or not np.isfinite(result.velocity_command).all()):
                        hold_reason = 'nonfinite solver output'
                    else:
                        control = result.velocity_command
                except (ValueError, RuntimeError) as exc:
                    hold_reason = str(exc)
                if hold_reason:
                    # Keep retrying the optimization every cycle. Never replay
                    # a moving command after a failed solve.
                    self.controller.last_acceleration[:] = 0.0
                    self.get_logger().warning(
                        f'MPC HOLD: {hold_reason}; zero horizontal speed/yaw rate, altitude control retained',
                        throttle_duration_sec=2.0)
            else:
                self.controller.last_acceleration[:] = 0.0
            if not np.isfinite(control).all():
                raise ValueError('nonfinite solver output')
            # Retain the oldest input timestamp: solve latency must not make
            # stale sensor data appear fresh to the PX4 command watchdog.
            stamp = min((state.header.stamp, scan.header.stamp), key=seconds)
            if not self.fresh(stamp, self.timeout):
                self.observe('mpc', f'BLOCKED input stale after solve ({solve_time:.3f}s)')
                self.controller.last_acceleration[:] = 0.0
                return
            out = TwistStamped()
            out.header.frame_id, out.header.stamp = self.frame, stamp
            out.twist.linear.x = float(control[0])
            out.twist.linear.y = float(control[1])
            out.twist.linear.z = float(np.clip(self.z_gain * (self.goal[2] - state.pose.position.z),
                                               -self.z_max, self.z_max))
            out.twist.angular.z = 0.0
            self.observe('mpc', f'mode={"HOLD: " + hold_reason if hold_reason else "TRACK"} nav={state.reason} goal_NED={np.round(self.goal, 3).tolist()} v_NED=({out.twist.linear.x:.3f},{out.twist.linear.y:.3f},{out.twist.linear.z:.3f})m/s yaw_rate={out.twist.angular.z:.3f}rad/s obstacles={len(detections)} safety_violation={safety_violation:.3f}m solve={solve_time:.3f}s')
            self.velocity_pub.publish(out)
        except (ValueError, RuntimeError) as exc:
            self.observe('mpc', f'BLOCKED {exc}')
            self.controller.last_acceleration[:] = 0.0
            self.get_logger().warning(f'MPC command withheld: {exc}', throttle_duration_sec=2.0)


def main(args=None):
    run(MpcNode, args)
