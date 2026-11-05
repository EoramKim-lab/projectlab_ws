"""Check a command gap on the running, disarmed projectlab SITL.

Source ROS and the workspace, then pass the running mpc_node PID. This briefly
enables the velocity stream, pauses only that MPC process, checks zero setpoints
and continuing heartbeats, resumes MPC, and disables the stream. No arming or
mode-change command is sent.
"""
import argparse
import json
import os
from pathlib import Path
import signal
import time

import numpy as np
import rclpy
from rclpy.qos import qos_profile_sensor_data
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleStatus
from std_srvs.srv import SetBool


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mpc-pid', type=int, required=True)
    args = parser.parse_args()
    command = Path('/proc', str(args.mpc_pid), 'cmdline').read_bytes().split(b'\0')
    expected = Path(__file__).resolve().parents[1] / 'install/drone_integration/lib/drone_integration/mpc_node'
    if str(expected).encode() not in command:
        parser.error(f'PID {args.mpc_pid} does not run {expected}')

    rclpy.init()
    node = rclpy.create_node('sils_command_hold_check')
    heartbeats, setpoints, statuses = [], [], []
    node.create_subscription(OffboardControlMode, '/fmu/in/offboard_control_mode',
                             lambda msg: heartbeats.append((time.monotonic(), msg)), qos_profile_sensor_data)
    node.create_subscription(TrajectorySetpoint, '/fmu/in/trajectory_setpoint',
                             lambda msg: setpoints.append((time.monotonic(), msg)), qos_profile_sensor_data)
    node.create_subscription(VehicleStatus, '/fmu/out/vehicle_status_v1',
                             lambda msg: statuses.append((time.monotonic(), msg)), qos_profile_sensor_data)
    client = node.create_client(SetBool, '/control/enable')
    paused = enabled = False

    def spin_for(seconds):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=.02)

    def enable(value):
        request = SetBool.Request()
        request.data = value
        future = client.call_async(request)
        rclpy.spin_until_future_complete(node, future, timeout_sec=5.)
        if not future.done() or not future.result().success:
            raise RuntimeError(f'control/enable({value}) failed: {future.result() if future.done() else "timeout"}')

    try:
        spin_for(2.)
        assert statuses and time.monotonic() - statuses[-1][0] < 2., 'VehicleStatus missing/stale'
        assert all(m.arming_state == VehicleStatus.ARMING_STATE_DISARMED for _, m in statuses), 'Vehicle must be disarmed'
        assert not heartbeats, 'A control stream is already active'
        assert client.wait_for_service(timeout_sec=3.), 'control/enable unavailable'
        enable(True)
        enabled = True
        spin_for(1.)
        assert len(heartbeats) >= 10, 'No sustained Offboard heartbeat'
        assert any(np.linalg.norm(m.velocity[:2]) > .01 for _, m in setpoints), 'No normal MPC output'

        os.kill(args.mpc_pid, signal.SIGSTOP)
        paused = True
        pause_start = time.monotonic()
        spin_for(2.)
        held = [(t, m) for t, m in setpoints if t > pause_start + .5]
        assert len(held) >= 20, 'Setpoints stopped during MPC gap'
        assert all(np.allclose(m.velocity, 0.) and m.yawspeed == 0. for _, m in held), 'MPC gap did not produce zero commands'
        gaps = np.diff([t for t, _ in heartbeats if t >= pause_start])
        assert len(gaps) >= 20 and max(gaps) < .2, 'Heartbeat interrupted during MPC gap'

        os.kill(args.mpc_pid, signal.SIGCONT)
        paused = False
        resume_start = time.monotonic()
        spin_for(1.5)
        assert any(t > resume_start and np.linalg.norm(m.velocity[:2]) > .01 for t, m in setpoints), 'MPC output did not resume'
        assert all(m.arming_state == VehicleStatus.ARMING_STATE_DISARMED for _, m in statuses), 'Unexpected arming'
        result = {
            'passed': True,
            'zero_setpoints_during_gap': len(held),
            'max_heartbeat_gap_seconds': round(float(max(gaps)), 4),
            'recovered': True,
            'vehicle_remained_disarmed': True,
        }
        print(json.dumps(result, indent=2))
    finally:
        if paused:
            os.kill(args.mpc_pid, signal.SIGCONT)
        if enabled:
            enable(False)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
