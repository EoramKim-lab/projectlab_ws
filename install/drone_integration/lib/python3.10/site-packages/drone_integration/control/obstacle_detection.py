"""Obstacle circles enclosing preprocessed body-frame LiDAR points."""
from dataclasses import dataclass
import numpy as np


@dataclass
class DetectedCircle:
    center: np.ndarray
    radius: float


def _enclosing_circle(points: np.ndarray, padding: float = 0.0):
    """Ritter enclosing circle. It is not necessarily minimum, but contains all points."""
    p = np.asarray(points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 2 or len(p) == 0:
        raise ValueError("points must have shape (N,2), N >= 1")
    if not np.isfinite(p).all():
        raise ValueError("points must be finite")

    # First try a least-squares circle fit. It recovers the center of a curved
    # LiDAR surface even when only the front half of a circular object is visible.
    # The final radius is expanded to the farthest measured point, so containment
    # is guaranteed even when the fitted circle is not exact.
    center = None
    if len(p) >= 3:
        design = np.column_stack((2.0 * p[:, 0], 2.0 * p[:, 1], np.ones(len(p))))
        rhs = np.sum(p * p, axis=1)
        try:
            if np.linalg.cond(design) < 1e8:
                coeff, *_ = np.linalg.lstsq(design, rhs, rcond=None)
                candidate = coeff[:2]
                radius_sq = float(coeff[2] + candidate @ candidate)
                if radius_sq > 1e-12 and np.isfinite(candidate).all():
                    center = candidate
        except np.linalg.LinAlgError:
            center = None

    if center is None:
        # Fallback: Ritter's enclosing-circle construction for nearly straight
        # clusters or ill-conditioned point configurations.
        p0 = p[0]
        p1 = p[int(np.argmax(np.sum((p - p0) ** 2, axis=1)))]
        p2 = p[int(np.argmax(np.sum((p - p1) ** 2, axis=1)))]
        center = 0.5 * (p1 + p2)
        radius = 0.5 * float(np.linalg.norm(p2 - p1))
        for point in p:
            delta = point - center
            distance = float(np.linalg.norm(delta))
            if distance > radius:
                new_radius = 0.5 * (radius + distance)
                if distance > 1e-12:
                    center = center + ((new_radius - radius) / distance) * delta
                radius = new_radius

    # Recompute from all points to remove any undercoverage.
    radius = float(np.max(np.linalg.norm(p - center, axis=1))) + padding
    return np.asarray(center, dtype=float), radius
