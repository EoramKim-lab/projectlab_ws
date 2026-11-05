# PX4 v1.16 + Gazebo Harmonic SILS

This workspace uses the PX4-supported `x500_lidar_2d` vehicle target. The local model overlay places the 2D LiDAR above the X500 frame and adds a separate visible GPS module on the upper rear deck. The X500 base supplies the single simulated NavSat measurement sensor, avoiding a duplicate GNSS receiver. The ROS navigation node consumes PX4 EKF2's NED local position and checks the raw GNSS sample separately.

## 1. PX4 source and model

Use PX4-Autopilot v1.16.0 with its submodules:

```bash
git clone --recursive --branch v1.16.0 https://github.com/PX4/PX4-Autopilot.git ~/PX4-Autopilot
cd ~/PX4-Autopilot
```

The workspace provides a local `lidar_2d_v2` model overlay. It keeps the upstream model and link names so `x500_lidar_2d` can use it, but changes the simulated sensor characteristics to approximate the physical RPLIDAR C1:

| Parameter | Overlay value | C1 nominal specification |
|---|---:|---:|
| Horizontal field of view | 360° | 360° |
| Samples per revolution | 500 | 5 kHz / 10 Hz ≈ 500 |
| Update rate | 10 Hz | 8–12 Hz (10 Hz typical) |
| Minimum range | 0.05 m | 0.05 m |
| Maximum range | 12 m | 12 m on 70% reflective targets; 6 m on 10% reflective targets |
| Range noise standard deviation | 0.015 m | Approximation of ±0.03 m accuracy |

The Gazebo model is a sensor approximation, not a bit-exact C1 hardware model. In particular, it does not reproduce reflectivity-dependent black-target range loss, the C1's 2.5D pitch behavior, UART transport, or its internal signal processing.

The PX4 `x500_lidar_2d` model is top-mounted. Its default scan is a Hokuyo-like 270-degree model; this workspace overrides the included `lidar_2d_v2` resource with a C1-like 360-degree scan. The overlay must be first in `GZ_SIM_RESOURCE_PATH` when Gazebo resolves `model://lidar_2d_v2`.

Run:

```bash
cd ~/drone_integration_ws
PX4_DIR=~/PX4-Autopilot ./simulation/scripts/run_px4_sils.sh
```

The script exports the workspace model overlay and runs:

```bash
make px4_sitl gz_x500_lidar_2d
```

If Gazebo still loads the upstream sensor parameters, inspect `GZ_SIM_RESOURCE_PATH` and make sure this workspace's `simulation/gz/models` directory precedes the PX4 model repository. You can confirm the actual scan topic with `gz topic -l`.

## 2. XRCE-DDS agent

In a separate terminal, start the Micro XRCE-DDS Agent:

```bash
MicroXRCEAgent udp4 -p 8888
```

Then start the PX4 SITL/Gazebo command above. PX4 SITL must connect to the agent before the ROS PX4 topics become available.

## 3. Build the ROS workspace

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install \
  --packages-select px4_msgs drone_interfaces drone_integration
source install/setup.bash
```

The `src/px4_msgs` checkout must be on `release/1.16` (this archive pins commit `392e831`; the v1.16.0, v1.16.1 and v1.16.2 tags point to that same commit). PX4 v1.16.0's default `dds_topics.yaml` already exposes the package's required topics:

- `/fmu/out/sensor_combined`
- `/fmu/out/vehicle_attitude`
- `/fmu/out/vehicle_local_position`
- `/fmu/out/vehicle_gps_position` (`SensorGps`)
- `/fmu/out/estimator_status_flags` (`EstimatorStatusFlags`, including `cs_gnss_pos`)
- `/fmu/out/vehicle_status_v1` (`VehicleStatus.MESSAGE_VERSION = 1`)
- `/fmu/out/vehicle_command_ack`
- `/fmu/in/offboard_control_mode`
- `/fmu/in/trajectory_setpoint`
- `/fmu/in/vehicle_command`

No custom DDS additions are required for the default GPS/IMU/Offboard path. Do not replace the firmware's `dds_topics.yaml` with `config/px4_dds_additions.yaml`. `config/px4_dds_optional_flow.yaml` is only for the retained, inactive optical-flow receiver.

## 4. Launch ROS 2 integration

```bash
source /opt/ros/humble/setup.bash
source ~/drone_integration_ws/install/setup.bash
ros2 launch drone_integration sils.launch.py
```

The launch file bridges the default Gazebo sensor topic:

```text
/world/default/model/x500_lidar_2d_0/link/link/sensor/lidar_2d_v2/scan
```

to `/scan_gz`, then `gz_scan_time_adapter_node` republishes it as `/scan` with the ROS host receipt time. This adapter is used because the workspace's PX4 timestamp guard expects PX4 uXRCE-DDS timestamps to share the host ROS clock; Gazebo sensor stamps may instead use simulation time. The adapter is only for SILS. The real C1 driver publishes directly to `/scan` and must not use this adapter.

For another world or a different Gazebo entity name:

```bash
ros2 launch drone_integration sils.launch.py \
  gz_scan_topic:=/world/<world>/model/<model_instance>/link/link/sensor/lidar_2d_v2/scan
```

## 5. Verify before flight control

### Projectlab workspace

After building `~/projectlab_ws/drone_integration_ws`, run these in separate
terminals. The Gazebo world already includes `x500_lidar_2d_0`; PX4 attaches
to that existing model.

```bash
MicroXRCEAgent udp4 -p 8888
~/projectlab_ws/sils_sim/run_gazebo.sh
~/projectlab_ws/sils_sim/run_px4.sh
~/projectlab_ws/sils_sim/run_ros.sh
```

`run_ros.sh` selects the `projectlab` scan topic, uses one BLAS/OpenMP thread
by default, and writes data logs under `sils_sim/results`.
`run_px4.sh` runs the existing SITL binary from its rootfs; build PX4 separately
after firmware changes. This avoids invoking optional Gazebo plugin rebuilds
from an older CMake cache on every simulation start.

An infeasible/failed MPC solve publishes zero horizontal velocity and yaw rate,
retains altitude control, and retries on the next cycle. With healthy sensors,
an enabled command node also keeps sending zero velocity and the Offboard
heartbeat during missing/stale/invalid MPC commands or an infeasible collision
margin. Fresh valid commands resume automatically. This is a velocity stop,
not a PX4 mode change or a latched position target. Invalid/stale navigation or
scan constraints, PX4 resets, explicit disable, and pilot takeover retain their
existing stream-stop behavior.

```bash
# PX4 raw GNSS and EKF2 local state
ros2 topic echo /fmu/out/vehicle_gps_position --once
ros2 topic echo /fmu/out/vehicle_local_position --once

# ROS pipeline
ros2 topic echo /navigation/state
ros2 topic echo /scan
ros2 topic echo /lidar/processed
ros2 topic echo /collision/halfplanes
ros2 topic echo /control/velocity_cmd
```

`/navigation/state.valid` must be true, `gnss_aided` must be true, and `ekf_gnss_fusion` must be true. Check `gps_fix_type`, `gps_satellites_used`, `gps_eph`, `gps_epv`, `local_position_age`, and `gps_age`. If it is invalid, read `reason`; do not relax the validity gates without identifying the cause.

The command node does not arm or take off. It waits for an armed PX4 vehicle in a supported hover/position mode and healthy navigation, LiDAR constraints, and MPC command before requesting Offboard. Perform initial checks with props removed or with a safe SITL setup. Do not use automatic Offboard handover on a real aircraft until the complete sensor and failsafe behavior has been verified.

## SILS 안전 여유 소프트 제약

`sils.yaml`의 MPC는 `soft_safety_margin: true`를 사용한다. 장애물 인식 원의
반경과 기체 반경(0.35 m)의 합은 하드 경계로 유지하고, 추가 안전 여유
0.20 m만 슬랙 `s`로 완화한다. 각 예측 지점/장애물에서
`nᵀ(p-c) >= R_safe - s`, `0 <= s <= 0.20`을 적용하고 비용에
`h * (5*s + 50*s²)`를 더한다. 가중치는 `safety_slack_linear`와
`safety_slack_quadratic`으로 조절한다. 제어 로그의 `safety_violation`은
예측 지점에서 안전 원 안으로 들어간 최대 거리(m)이며, 접선 슬랙과는 다르다.

명령 노드가 안전 여유 진입만으로 정지시키지 않도록 SILS의
`collision_constraints_node.safety_margin`은 0.0으로 설정한다.
스캔 기반 기체 반경 경계 및 센서/명령 유효성 검사는 유지한다.
기본 `MPCConfig`와 실기용 `integration.yaml`은 기존 하드 제약을 유지한다.
SILS도 하드 모드로 되돌리려면 MPC의 `soft_safety_margin: false`와
collision node의 `safety_margin: 0.20`을 함께 복구한다.

이 제약은 인식된 장애물과 이산 예측 위치에 대한 모델상의 제약이다.
수치 검증의 기존 3 mm 허용 오차는 유지하며, 실제 기체 궤적의 연속적인
충돌 방지를 보증하지 않는다. 설정/코드 변경 후 ROS launch를 재시작해야 한다.

가중치 비교는 `simulation/scripts/tune_soft_safety.py`로 재현한다.
`--log`에 reference 토픽이 기록된 비행 JSONL, `--config`에 `sils.yaml`,
`--output`에 결과 디렉터리를 지정한다. `OPENBLAS_NUM_THREADS=1`로 실행하며,
워크스페이스를 source하거나 `PYTHONPATH=src/drone_integration`을 설정한다.
이 비교는 초기 로그의 장애물 원을 고정한 이상적인 이중 적분기 모델이며,
PX4 응답 지연·센서 지연·장애물 추정 변화는 포함하지 않는다.
2026-11-02의 `08:46:07Z` 비행 기준 100/1000 대비 5/50에서 횡오차 RMS는
0.337→0.315 m, 최대 횡오차는 0.826→0.735 m였다. 모델의 최소 물리 경계
여유는 약 0.10 m였다. Gazebo 재비행 검증은 별도로 필요하다.

종단 가중치 재비교에서는 SILS의 `q_terminal_position: 24.0`을 유지하고
`q_terminal_velocity: 16.0`으로 설정했다(기존 속도 가중치 4.0).
충돌 슬랙 비용은 5/50으로 유지한다. `tune_soft_safety.py --sweep terminal`에
`--terminal-pair 24 4 --terminal-pair 24 16`처럼 위치/속도 쌍을 반복 지정하면
독립 비교할 수 있다. 종단 비교는 30초 동안 계산하며 위치 오차 0.15 m,
속력 0.05 m/s 미만을 마지막까지 유지한 시점을 정착 시간으로 기록한다.
2026-11-02의 09:23:23Z와 08:46:07Z 로그 기반 고정 장애물·이상적 모델에서
정착 시간은 각각 13.45→13.40 s, 15.15→14.90 s였다. 실제 Gazebo 재검증은
필요하다. 종단 비용은 항상 최종 임무 목표점이 아니라 예측 구간 마지막의
레퍼런스 위치·속도에 적용되며, 목표점이 예측 구간 안에 들어오면 기준 속도는 0이다.

## Gazebo 레퍼런스 궤적 표시

SILS launch는 `gz_reference_node`도 실행한다. MPC의 실제 시작점과 목표점을
`/control/reference` (`geometry_msgs/PoseArray`, `map_ned`)로 받아 청록색
기준선, 초록색 시작점, 분홍색 목표점을 Gazebo GUI에 표시한다.
`forward` 모드는 유효한 navigation으로 기준선이 초기화된 뒤 표시한다.
이 선은 장애물 회피 후의 예측 경로가 아니라 MPC의 원래 직선 레퍼런스다.
GUI 전용 마커이며 Gazebo `/marker_array` 서비스를 사용한다.

Harmonic Python 패키지 `python3-gz-transport13`, `python3-gz-msgs10`이 필요하다.
기존 `sils_sim/run_ros.sh`로 함께 실행된다. NED→ENU 변환은 `(y, x, -z)`이며,
PX4 로컬 원점이 Gazebo 원점과 다르면 `gz_reference_node`의
`ned_origin_enu: [east, north, up]` 파라미터에 그 오프셋(m)을 설정한다.
기본값은 `[0.0, 0.0, 0.0]`이다. 수신 중단 시 마커는 시뮬레이션 시간
3초 뒤 만료되고, 미초기화/리셋 상태는 해당 마커를 지운다.

오프라인 좌표 변환 확인:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 tests/test_gz_reference.py
```

## 비행별 로그 및 자동 그래프

`data_logger_node`는 전체 세션 JSONL과 함께, PX4의 armed 상태를 처음 받은
시점부터 disarmed 상태를 받을 때까지 각 비행을 별도 저장한다.
기본 `auto_flight_report: true`이며, 착륙 후 자동 disarm되면 별도 프로세스가
보고서를 생성한다. 착륙만 하고 armed 상태가 유지되면 기록도 계속된다.
비행 중 로거를 정상 종료하면 불완전 비행으로 표시하고 보고서를 만든다.
강제 종료(SIGKILL)/전원 차단 시에는 자동 생성되지 않으므로 수동 생성한다.

`run_ros.sh` 사용 시 저장 위치:

```text
/home/yjh/projectlab_ws/sils_sim/results/
  drone_<UTC>_<unique>.jsonl          # 전체 세션; /scan 원본도 기록
  drone_<UTC>_<unique>/flight_001/
    flight.jsonl                    # 비행 구간의 전체 메시지
    flight_metadata.json            # 종료 원인/완료 여부
    flight.scene.json               # 로거 시작 당시 설정된 월드 장애물/ENU 원점 사본
    flight_plots.png                # ENU 궤적, 고도, N/E 속도 실측 및 MPC 명령
    trajectory_world.png            # 월드 ENU 궤적 + 레퍼런스 + SDF 장애물
    lidar_obstacles.html            # 재생/정지/시간 탐색/속도 조절 가능한 독립 HTML
    summary.json                   # 시간 범위, 샘플 수, 재생 배속 정보
    report.log                     # 렌더링 출력/오류
```

HTML 왼쪽은 body FRD LiDAR 점, 오른쪽은 Gazebo ENU 좌표의 비행 궤적,
레퍼런스 및 장애물이다. 회색은 SDF 장애물, 주황색 원은 인식 결과,
빨간 점선은 추정 안전 반경이다. 시간 슬라이더로 이동하고 재생/일시정지,
0.25~16배 재생 속도를 선택할 수 있다. 기본 1배속은 로그 경과 시간 기준이며,
표시 데이터는 최대 240개 시각으로 샘플링한다. 인터넷이나 외부 JS 라이브러리는 필요 없다.
LiDAR 점은 스캔 시각 이전의 최신 navigation pose로 변환하고,
0.3초 이상 오래된 데이터는 표시하지 않는다. 전처리된 점을 시각화한다.

`run_ros.sh`는 설정된 SDF 경로를 로거에 전달한다. 로거 시작 때 배치와
파일 해시를 저장하고 각 비행에도 복사하므로, 이후 월드 파일을 편집해도
과거 보고서의 배치는 바뀌지 않는다. 이는 실행 중인 Gazebo에서 읽은
실측 배치가 아니므로, 월드 변경 후에는 Gazebo와 ROS를 함께 재시작한다.
궤적은 PX4 추정 NED를 ENU로 변환한 값이며 Gazebo ground truth는 아니다.
원점 보정은 `ned_origin_enu`로 지정하며, Gazebo 레퍼런스 표시 노드와 같은 값을 사용한다.

플롯 데이터는 최대 약 10Hz로 줄이고 JSONL 원본은 그대로 유지한다.

기존 로그 재생성(ROS 노드를 실행하지 않아도 가능):

```bash
cd /home/yjh/projectlab_ws/drone_integration_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run drone_integration flight_report /absolute/path/to/flight.jsonl --output /absolute/path/to/report
```

`--max-frames 600`으로 애니메이션 샘플 수를 늘릴 수 있다.
XY 궤적에는 `/control/reference`로 기록된 실제 MPC 기준선을 초록색 점선으로,
시작점/목표점을 초록색 원/빨간색 별로 표시한다. 로거 재시작 후 새 로그부터
해당 토픽을 기록한다. 기준선이 없는 과거 로그는 임의로 추정하지 않는다.
당시 MPC 로그의 `Forward reference` 시작점/목표점을 확인한 경우
`--reference-ned START_N START_E START_D GOAL_N GOAL_E GOAL_D`로 명시할 수 있다.
수평 시작점의 D 값은 목표 고도로 지정한다. 사용한 기준선과 출처는
`summary.json`에 저장한다.
월드 사본이 없는 과거 로그에는 현재 장애물을 자동으로 덧씌우지 않는다.
당시 배치가 확인된 경우에만 `--world-sdf /path/to/that_world.sdf`로 명시한다.
원점은 `--ned-origin-enu EAST NORTH UP`으로 보정할 수 있다. 원점 정보가 없으면
(0, 0, 0)을 가정하며, 사용한 원점과 배치 출처는 `summary.json`에 기록한다.
보고서 생성에는 matplotlib가 필요하며 ffmpeg는 필요하지 않다.
로거 시작 이전의 비행 구간은 복원되지 않는다.
