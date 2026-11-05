"""Cartesian double-integrator MPC with scan-derived circular obstacles.

State [north, east, v_north, v_east] and acceleration input [a_north, a_east]
are expressed in map NED. Yaw only transforms body-frame detections.
The ROS adapter sends the first predicted velocity to PX4.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import time
from typing import Sequence
import numpy as np

try:
    import casadi as ca
except ImportError as exc:
    raise ImportError('CasADi is required: python -m pip install casadi') from exc

from .obstacle_detection import DetectedCircle


@dataclass(frozen=True)
class MPCConfig:
    dt: float = 0.15
    control_dt: float = 0.05
    horizon_steps: int = 100
    reference_speed: float = 0.5
    max_speed: float = 5.0
    max_acceleration: float = 3.0
    drone_radius: float = 0.35
    safety_margin: float = 0.20
    soft_safety_margin: bool = False
    safety_slack_linear: float = 100.0
    safety_slack_quadratic: float = 1000.0
    max_obstacles: int = 8
    max_plane_iterations: int = 3
    plane_tolerance: float = 0.04
    q_position: float = 8.0
    q_velocity: float = 1.0
    q_terminal_position: float = 24.0
    q_terminal_velocity: float = 4.0
    r_acceleration: float = 0.25
    r_delta_acceleration: float = 0.05
    ipopt_max_iter: int = 160
    ipopt_tolerance: float = 1e-4

    def __post_init__(self):
        positive = (self.dt, self.control_dt, self.reference_speed, self.max_speed,
                    self.max_acceleration, self.plane_tolerance, self.ipopt_tolerance,
                    self.safety_slack_linear, self.safety_slack_quadratic)
        if not all(math.isfinite(v) and v > 0 for v in positive):
            raise ValueError('MPC time, speed, acceleration and tolerances must be positive')
        if self.horizon_steps < 2 or self.max_obstacles < 1 or self.max_plane_iterations < 1 or self.ipopt_max_iter < 1:
            raise ValueError('invalid horizon/obstacle/iteration count')
        costs = (self.drone_radius, self.safety_margin, self.q_position, self.q_velocity,
                 self.q_terminal_position, self.q_terminal_velocity,
                 self.r_acceleration, self.r_delta_acceleration)
        if not all(math.isfinite(v) and v >= 0 for v in costs):
            raise ValueError('MPC radii and costs must be finite and nonnegative')


@dataclass
class WorldObstacle:
    center: np.ndarray
    safe_radius: float


@dataclass
class MPCResult:
    success: bool
    velocity_command: np.ndarray
    predicted_states: np.ndarray
    acceleration: np.ndarray = field(default_factory=lambda: np.zeros(2))
    predicted_accelerations: np.ndarray = field(default_factory=lambda: np.empty((0, 2)))
    objective: float = math.inf
    branch: int = 0
    solve_time: float = 0.0
    reason: str = ''
    max_safety_violation: float = 0.0


class MPCController:
    """IPOPT MPC with sequential obstacle tangent-plane updates.

    p_next = p + h*v + h*h*a/2; v_next = v + h*a.
    Speed and acceleration limits bound Euclidean norms, including diagonals.
    The first interval is control_dt; subsequent intervals use prediction dt.
    Yaw and steering do not appear in the optimization state or constraints.
    """

    def __init__(self, cfg: MPCConfig | None = None, reference_start: Sequence[float] | None = None):
        self.cfg = cfg or MPCConfig()
        self.reference_start = None if reference_start is None else np.asarray(reference_start, dtype=float).reshape(2)
        if self.reference_start is not None and not np.isfinite(self.reference_start).all():
            raise ValueError('reference start must be finite')
        self.N, self.dt = self.cfg.horizon_steps, self.cfg.dt
        self.step_sizes = np.r_[self.cfg.control_dt, np.full(self.N - 1, self.dt)]
        self.prediction_times = np.r_[0., np.cumsum(self.step_sizes)]
        self.reset()
        self._build_optimizer()

    def reset(self):
        self.last_acceleration = np.zeros(2)
        self.preferred_side = 1
        self._branch_initialized = False

    def _build_optimizer(self):
        cfg, N = self.cfg, self.N
        opti = ca.Opti()
        X, U = opti.variable(4, N + 1), opti.variable(2, N)
        slack = opti.variable(cfg.max_obstacles, N) if cfg.soft_safety_margin else None
        if slack is not None:
            # Only the extra safety buffer is relaxable; physical clearance stays hard.
            opti.subject_to(opti.bounded(0., ca.vec(slack), cfg.safety_margin))
        x0 = opti.parameter(4)
        pref, vref = opti.parameter(2, N + 1), opti.parameter(2, N + 1)
        previous_acceleration = opti.parameter(2)
        centers = opti.parameter(2, cfg.max_obstacles)
        radii, masks = opti.parameter(cfg.max_obstacles), opti.parameter(cfg.max_obstacles)
        normals = opti.parameter(2, cfg.max_obstacles * N)
        opti.subject_to(X[:, 0] == x0)
        objective = 0
        for k, h in enumerate(self.step_sizes):
            opti.subject_to(X[:2, k + 1] == X[:2, k] + h * X[2:, k] + .5 * h**2 * U[:, k])
            opti.subject_to(X[2:, k + 1] == X[2:, k] + h * U[:, k])
            opti.subject_to(ca.sumsqr(X[2:, k + 1]) <= cfg.max_speed**2)
            opti.subject_to(ca.sumsqr(U[:, k]) <= cfg.max_acceleration**2)
            previous = previous_acceleration if k == 0 else U[:, k - 1]
            objective += h * (cfg.q_position * ca.sumsqr(X[:2, k + 1] - pref[:, k + 1])
                              + cfg.q_velocity * ca.sumsqr(X[2:, k + 1] - vref[:, k + 1])
                              + cfg.r_acceleration * ca.sumsqr(U[:, k])
                              + cfg.r_delta_acceleration * ca.sumsqr(U[:, k] - previous))
            for j in range(cfg.max_obstacles):
                normal = normals[:, j * N + k]
                margin = ca.dot(normal, X[:2, k + 1] - centers[:, j]) - radii[j]
                if slack is None:
                    opti.subject_to(masks[j] * margin >= 0.)
                else:
                    opti.subject_to(masks[j] * (margin + slack[j, k]) >= 0.)
                    objective += h * (cfg.safety_slack_linear * slack[j, k]
                                      + cfg.safety_slack_quadratic * slack[j, k]**2)
        objective += cfg.q_terminal_position * ca.sumsqr(X[:2, N] - pref[:, N])
        objective += cfg.q_terminal_velocity * ca.sumsqr(X[2:, N] - vref[:, N])
        opti.minimize(objective)
        opti.solver('ipopt', {'expand': True, 'print_time': False},
                    {'print_level': 0, 'max_iter': cfg.ipopt_max_iter,
                     'tol': cfg.ipopt_tolerance, 'acceptable_tol': 5 * cfg.ipopt_tolerance})
        self.opti, self.X, self.U = opti, X, U
        self.slack = slack
        self.x0_param, self.pref_param, self.vref_param = x0, pref, vref
        self.previous_acceleration_param = previous_acceleration
        self.centers_param, self.radii_param, self.masks_param = centers, radii, masks
        self.normals_param, self.objective = normals, objective

    @staticmethod
    def _rotation(yaw):
        c, s = math.cos(yaw), math.sin(yaw)
        return np.array([[c, -s], [s, c]])

    def _transform_obstacles(self, state, detections, body_yaw=0.):
        rotation = self._rotation(body_yaw)
        result = []
        for detection in detections:
            center = np.asarray(detection.center, dtype=float).reshape(2)
            radius = float(detection.radius)
            if not np.isfinite(center).all() or not math.isfinite(radius) or radius < 0:
                raise ValueError('invalid obstacle circle')
            result.append(WorldObstacle(state[:2] + rotation @ center,
                                         radius + self.cfg.drone_radius + self.cfg.safety_margin))
        if len(result) > self.cfg.max_obstacles:
            raise ValueError('obstacle capacity exceeded')
        return sorted(result, key=lambda obs: float(np.linalg.norm(obs.center - state[:2])))

    def _reference(self, state, goal):
        p0 = np.asarray(state[:2], dtype=float).copy()
        goal = np.asarray(goal, dtype=float).reshape(2)
        if self.reference_start is not None:
            segment = goal - self.reference_start
            length = float(np.linalg.norm(segment))
            if length > 1e-8:
                along = np.clip((p0 - self.reference_start) @ (segment / length), 0., length)
                p0 = self.reference_start + along * segment / length
            else:
                p0 = goal.copy()
        delta = goal - p0
        distance = float(np.linalg.norm(delta))
        direction = delta / distance if distance > 1e-8 else np.array([1., 0.])
        speed = min(self.cfg.reference_speed, self.cfg.max_speed,
                    math.sqrt(2 * self.cfg.max_acceleration * distance))
        progress = np.minimum(speed * self.prediction_times, distance)
        pref = p0 + progress[:, None] * direction
        vref = np.tile(speed * direction, (self.N + 1, 1))
        vref[progress >= distance - 1e-8] = 0.
        return pref, vref, speed, direction

    @staticmethod
    def _rollout(state, accelerations, step_sizes):
        steps = np.broadcast_to(step_sizes, (len(accelerations),))
        X = np.zeros((len(accelerations) + 1, 4))
        X[0] = state
        for k, (acceleration, h) in enumerate(zip(accelerations, steps)):
            X[k + 1, :2] = X[k, :2] + h * X[k, 2:] + .5 * h**2 * acceleration
            X[k + 1, 2:] = X[k, 2:] + h * acceleration
        return X

    def _seed_controls(self, state, pref, direction, obstacles, side):
        """Generate an acceleration seed from a smooth lateral bypass path."""
        right = np.array([-direction[1], direction[0]])
        progress = np.maximum(0., (pref - state[:2]) @ direction)
        path = pref.copy()
        for obstacle in obstacles:
            relative = obstacle.center - state[:2]
            along, lateral = float(relative @ direction), float(relative @ right)
            width = max(1., 1.45 * obstacle.safe_radius)
            if along < -width or along > progress[-1] + width or abs(lateral) > obstacle.safe_radius + .65:
                continue
            phase = (progress - along) / width
            bump = np.where(np.abs(phase) <= 1., .5 * (1. + np.cos(np.pi * phase)), 0.)
            ramp = np.clip(self.prediction_times / .5, 0., 1.)
            path += (bump * ramp * (lateral + side * (obstacle.safe_radius + .3)))[:, None] * right
        controls = np.zeros((self.N, 2))
        predicted = np.asarray(state, dtype=float).copy()
        for k, h in enumerate(self.step_sizes):
            desired_velocity = (path[k + 1] - predicted[:2]) / max(h, .3)
            norm = np.linalg.norm(desired_velocity)
            if norm > self.cfg.max_speed:
                desired_velocity *= self.cfg.max_speed / norm
            acceleration = (desired_velocity - predicted[2:]) / h
            norm = np.linalg.norm(acceleration)
            if norm > self.cfg.max_acceleration:
                acceleration *= self.cfg.max_acceleration / norm
            controls[k] = acceleration
            predicted = self._rollout(predicted, controls[k:k + 1], h)[1]
        return controls

    def _make_planes(self, nominal, obstacles, side, direction):
        normals = np.zeros((2, self.cfg.max_obstacles * self.N))
        centers = np.zeros((2, self.cfg.max_obstacles))
        radii, masks = np.zeros(self.cfg.max_obstacles), np.zeros(self.cfg.max_obstacles)
        right = np.array([-direction[1], direction[0]])
        for j, obstacle in enumerate(obstacles):
            centers[:, j], radii[j], masks[j] = obstacle.center, obstacle.safe_radius, 1.
            for k in range(1, self.N + 1):
                delta = nominal[k, :2] - obstacle.center
                distance = np.linalg.norm(delta)
                normals[:, j * self.N + k - 1] = delta / distance if distance > 1e-7 else side * right
        return normals, centers, radii, masks

    def _solve_once(self, state, pref, vref, accelerations, nominal, plane_data):
        normals, centers, radii, masks = plane_data
        for parameter, value in ((self.x0_param, state), (self.pref_param, pref.T),
                                 (self.vref_param, vref.T),
                                 (self.previous_acceleration_param, self.last_acceleration),
                                 (self.centers_param, centers), (self.radii_param, radii),
                                 (self.masks_param, masks), (self.normals_param, normals)):
            self.opti.set_value(parameter, value)
        self.opti.set_initial(self.X, nominal.T)
        self.opti.set_initial(self.U, accelerations.T)
        if self.slack is not None:
            self.opti.set_initial(self.slack, 0.)
        solution = self.opti.solve()
        return (np.asarray(solution.value(self.X)).T, np.asarray(solution.value(self.U)).T,
                float(solution.value(self.objective)), str(self.opti.stats().get('return_status', 'unknown')))

    def _solve_branch(self, state, pref, vref, obstacles, direction, side):
        started = time.perf_counter()
        accelerations = self._seed_controls(state, pref, direction, obstacles, side)
        nominal = self._rollout(state, accelerations, self.step_sizes)
        objective, status = math.inf, 'not_solved'
        for _ in range(self.cfg.max_plane_iterations):
            planes = self._make_planes(nominal, obstacles, side, direction)
            try:
                states, new_accelerations, objective, status = self._solve_once(
                    state, pref, vref, accelerations, nominal, planes)
            except (RuntimeError, ValueError) as exc:
                return MPCResult(False, np.zeros(2), nominal, branch=side,
                                 solve_time=time.perf_counter() - started, reason=f'IPOPT failed: {exc}')
            new_planes = self._make_planes(states, obstacles, side, direction)
            change = float(np.max(np.linalg.norm(new_planes[0] - planes[0], axis=0)))
            nominal, accelerations = states, new_accelerations
            if change < self.cfg.plane_tolerance:
                break
        margin = min((float(np.min(np.linalg.norm(nominal[1:, :2] - obs.center, axis=1) - obs.safe_radius))
                      for obs in obstacles), default=math.inf)
        relaxation = self.cfg.safety_margin if self.cfg.soft_safety_margin else 0.
        feasible = (np.isfinite(nominal).all() and np.isfinite(accelerations).all()
                    and margin + relaxation >= -3e-3)
        return MPCResult(
            success=bool(feasible), velocity_command=nominal[1, 2:].copy() if feasible else np.zeros(2),
            predicted_states=nominal, acceleration=accelerations[0].copy() if feasible else np.zeros(2),
            predicted_accelerations=accelerations, objective=objective, branch=side,
            solve_time=time.perf_counter() - started,
            max_safety_violation=max(0., -margin),
            reason=status if feasible else f'hard obstacle margin violated ({margin + relaxation:.4f} m)')

    def warmup(self):
        previous = self.last_acceleration.copy(), self.preferred_side, self._branch_initialized
        started = time.perf_counter()
        try:
            self.compute(np.zeros(4), [2., 0.], [])
        finally:
            self.last_acceleration, self.preferred_side, self._branch_initialized = previous
        return time.perf_counter() - started

    def compute(self, state, goal, detections, *, body_yaw=0.):
        """Solve from measured [x, y, vx, vy]; return map-NED velocity.

        Detections are body FRD. body_yaw only transforms their coordinates and
        does not constrain the direction of commanded motion. Failed solves
        return zero velocity; the adapter retains altitude control and retries.
        """
        started = time.perf_counter()
        state = np.asarray(state, dtype=float).reshape(4)
        goal = np.asarray(goal, dtype=float).reshape(2)
        if not np.isfinite(state).all() or not np.isfinite(goal).all() or not math.isfinite(body_yaw):
            raise ValueError('state, goal and body yaw must be finite')
        obstacles = self._transform_obstacles(state, detections, body_yaw)
        pref, vref, _, direction = self._reference(state, goal)
        results = []
        for side in (self.preferred_side, -self.preferred_side):
            result = self._solve_branch(state, pref, vref, obstacles, direction, side)
            results.append(result)
            if self._branch_initialized and result.success:
                break
        feasible = [result for result in results if result.success]
        if not feasible:
            self.last_acceleration[:] = 0.
            return MPCResult(False, np.zeros(2), results[0].predicted_states,
                             solve_time=time.perf_counter() - started,
                             reason='both bypass branches failed: ' + '; '.join(r.reason for r in results))
        best = min(feasible, key=lambda result: result.objective)
        self.last_acceleration = best.acceleration.copy()
        self.preferred_side, self._branch_initialized = best.branch, True
        best.solve_time = time.perf_counter() - started
        return best
