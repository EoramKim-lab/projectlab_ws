# Drone Integration Workspace

ROS 2 Humble integration for **PX4 v1.16 + Gazebo Harmonic** and the matching real-aircraft PX4 interface.
The active navigation path uses PX4 EKF2 local position, raw GNSS quality, PX4 attitude and IMU data.
The ROS-side dead-reckoning estimator is no longer the default navigation source.

## Target stack

| Component | Target |
|---|---|
| OS | Ubuntu 22.04 LTS |
| ROS 2 | Humble |
| PX4 | v1.16.0 |
| `px4_msgs` | `release/1.16` (v1.16.0/1.16.1/1.16.2 tags share one commit) |
| Simulator | Gazebo Harmonic 8.x |
| ROS-Gazebo bridge | `ros_gz_bridge` for Harmonic |
| Vehicle | PX4 `x500_lidar_2d` |
| GNSS | X500 base model's Gazebo NavSat sensor, fused by PX4 EKF2; separate GPS module is shown on the upper deck |
| 2D LiDAR | Top-mounted C1-like 360-degree sensor overlay |

## Active data flow

```text
Gazebo X500 + visible top GPS module + NavSat + IMU + barometer
                 |
                 v
              PX4 EKF2
                 |
     +-----------+---------------------+
     |                                 |
     v                                 v
VehicleLocalPosition (NED)        SensorGps + EstimatorStatusFlags
     |                                 |
     +---------------+-----------------+
                     v
             gps_navigation_node <--- PX4 attitude + IMU adapter
                     |
                     v
              NavigationState
                     |
Gazebo 2D LiDAR -> ros_gz_bridge -> scan time adapter -> /scan
                     |
                     v
               lidar_receiver_node
                     |
                     v
              ProcessedScan
                     |
            +--------+---------+
            v                  v
      MPC obstacle map   Half-plane constraints
            |                  |
            +--------+---------+
                     v
             px4_command_node
                     |
                     v
             PX4 Offboard (NED)
```

`gps_navigation_node` does **not** integrate raw GPS coordinates itself. It consumes PX4's EKF2-fused `VehicleLocalPosition` in NED and independently checks the raw `SensorGps` fix type, satellite count and reported accuracy, and requires `EstimatorStatusFlags.cs_gnss_pos` to confirm that EKF2 intends to fuse GNSS position. The navigation state is invalid unless the GNSS sample is healthy, EKF2 has a valid global horizontal reference, and EKF2 is not reporting dead reckoning.

## Build

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash

# px4_msgs source is pinned to the PX4 v1.16 message branch.
colcon build --symlink-install \
  --packages-select px4_msgs drone_interfaces drone_integration
source install/setup.bash
```

Install the Harmonic ROS bridge if it is not already installed:

```bash
sudo apt install ros-humble-ros-gzharmonic
```

## SILS: PX4 v1.16 + Gazebo Harmonic

See [simulation/README.md](simulation/README.md). The short sequence is:

1. Start `MicroXRCEAgent udp4 -p 8888`.
2. Start PX4 SITL with `simulation/scripts/run_px4_sils.sh`.
3. In another terminal, source ROS and the workspace, then run:

```bash
ros2 launch drone_integration sils.launch.py
```

The launch defaults to the Gazebo topic emitted by the default-world `x500_lidar_2d` instance. Override `gz_scan_topic` if the world or model instance name differs.

## Real aircraft profile

`src/drone_integration/config/integration.yaml` is the hardware profile:

- `use_sim_time: false`
- physical RPLIDAR C1 scan convention (`scan_convention: sllidar_c1`)
- physical C1 mounting correction (`upside_down: true`, matching the current hardware mount)
- GPS/EKF2 navigation with the same `NavigationState` interface used by SILS

The physical C1 mounting correction must be rechecked against the final mechanical installation. If the real LiDAR is upright rather than rolled 180 degrees, set `upside_down: false`.

## Navigation and coordinate conventions

### Cartesian MPC

The horizontal MPC state is `[x, y, vx, vy]` in local NED, initialized from
`NavigationState.pose.position` and `twist.linear`. Inputs are `[ax, ay]` with
piecewise constant acceleration:

```text
p[k+1] = p[k] + h[k] v[k] + 0.5 h[k]^2 a[k]
v[k+1] = v[k] + h[k] a[k]
||v[k+1]|| <= max_speed; ||a[k]|| <= max_acceleration
```

The cost penalizes position/velocity reference errors, acceleration and its
changes. Scan-derived obstacle circles retain the tangent-plane constraints
and nonlinear clearance check. The first prediction interval is `1/publish_rate`
(0.05 s at 20 Hz); the other 19 use `dt=0.15 s`, giving a 2.9 s horizon.
PX4 receives `v[1]` directly as map-NED `vx, vy`, with zero yaw rate and separate
altitude control. Body yaw is used only for scan coordinate transforms and
the initial forward-reference direction; it does not constrain lateral motion.
`reference_speed` is configurable in the hardware/SILS YAML profiles.
Failed solves continue sending zero horizontal velocity while retaining altitude
control; fresh valid solutions resume automatically.

- World frame: `map_ned` (North, East, Down).
- Body frame: `base_link_frd` (Forward, Right, Down).
- `VehicleLocalPosition.x/y/z` and `vx/vy/vz` are used directly in NED; no ENU conversion is applied.
- PX4 attitude is the FRD-body-to-NED-world quaternion.
- PX4 IMU angular velocity remains in body FRD.
- GPS latitude/longitude are not sent directly to the MPC. EKF2's local NED estimate is used instead.
- EKF position reset counters trigger `navigation/reset`, clearing MPC history/reference and latching the Offboard stream off. Re-enable only after the new local solution is valid.

## Verification

Offline tests (no running ROS graph required):

```bash
PYTHONPATH=src/drone_integration python3 -m unittest discover -s tests -p 'test_*.py' -v
```

After building in a ROS 2 Humble environment, verify topic availability before enabling Offboard:

```bash
ros2 topic echo /fmu/out/vehicle_gps_position --once
ros2 topic echo /fmu/out/vehicle_local_position --once
ros2 topic echo /navigation/state
ros2 topic echo /scan
ros2 topic echo /lidar/processed
ros2 topic echo /collision/halfplanes
```

A successful Python build or offline test does not verify the live PX4 DDS link, the Gazebo sensor topic, EKF2 GNSS fusion, or flight behavior. Those must be checked on the target host before arming.

## Legacy files

The old ROS-side dead-reckoning implementation is retained only as historical reference and is not installed as an active console entry point. Optical-flow receiver code is also retained for optional future hardware use, but it is not part of the default GPS navigation pipeline. If it is re-enabled, merge `config/px4_dds_optional_flow.yaml` into the PX4 v1.16 DDS topic configuration; do not add those topics to the default SILS profile.
