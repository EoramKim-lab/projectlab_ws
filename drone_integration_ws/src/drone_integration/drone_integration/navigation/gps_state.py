"""ROS-independent validation helpers for PX4 EKF2 + GNSS navigation."""
import math


def gps_quality_reasons(gps, min_satellites=6, max_eph=5.0, max_epv=8.0):
    """Return reasons why a raw PX4 SensorGps sample is unsuitable for navigation."""
    reasons = []
    if gps is None:
        return ['gps_missing']

    fix_type = int(getattr(gps, 'fix_type', 0))
    fix_3d = int(getattr(gps, 'FIX_TYPE_3D', 3))
    if fix_type < fix_3d:
        reasons.append('gps_no_3d_fix')

    satellites = int(getattr(gps, 'satellites_used', 0))
    if satellites < int(min_satellites):
        reasons.append('gps_too_few_satellites')

    for field, limit, reason in (
            ('eph', max_eph, 'gps_horizontal_accuracy'),
            ('epv', max_epv, 'gps_vertical_accuracy')):
        value = float(getattr(gps, field, float('inf')))
        if not math.isfinite(value) or value < 0 or value > limit:
            reasons.append(reason)

    return reasons


def local_position_reasons(local, require_gnss=True):
    """Validate the fused PX4 VehicleLocalPosition state and its GNSS reference."""
    if local is None:
        return ['local_position_missing']

    reasons = []
    for field, reason in (
            ('xy_valid', 'local_xy_invalid'),
            ('z_valid', 'local_z_invalid'),
            ('v_xy_valid', 'local_vxy_invalid'),
            ('v_z_valid', 'local_vz_invalid')):
        if not bool(getattr(local, field, False)):
            reasons.append(reason)

    values = [getattr(local, name, float('nan')) for name in
              ('x', 'y', 'z', 'vx', 'vy', 'vz', 'ax', 'ay', 'az')]
    try:
        finite = all(math.isfinite(float(value)) for value in values)
    except (TypeError, ValueError):
        finite = False
    if not finite:
        reasons.append('local_position_nonfinite')

    if require_gnss:
        if not bool(getattr(local, 'xy_global', False)):
            reasons.append('gnss_global_reference_invalid')
        if bool(getattr(local, 'dead_reckoning', True)):
            reasons.append('ekf_dead_reckoning_active')

    return reasons


def gnss_aided(local, gps, gps_reasons, estimator_flags=None):
    """True only when GNSS is healthy and EKF2 explicitly intends GNSS fusion."""
    return bool(local is not None and gps is not None and estimator_flags is not None
                and not gps_reasons and getattr(local, 'xy_global', False)
                and not getattr(local, 'dead_reckoning', True)
                and getattr(estimator_flags, 'cs_gnss_pos', False))
