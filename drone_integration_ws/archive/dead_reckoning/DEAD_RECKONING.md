# 데드레코닝 항법으로 수동 호버링 후 MPC 시작

## 좌표계: PX4 NED / FRD

- 세계 프레임 `map_ned`: x=북, y=동, z=아래. 바디 `base_link_frd`: x=앞, y=오른쪽, z=아래.
- 자세는 FRD→NED 회전입니다. PX4 wxyz를 ROS 메시지 xyzw 순서로만 재배열합니다.
- yaw=0은 북쪽, +π/2는 동쪽이며 양의 yaw rate는 위에서 볼 때 오른쪽 회전입니다.
- 정지·수평 IMU specific force는 `(0,0,-9.80665)`이고 NED 중력 `(0,0,+9.80665)`를 더합니다.
- `/navigation/state` 위치·선속도·가속도는 NED, 각속도는 FRD입니다.
- `/lidar/processed`와 `/collision/halfplanes`는 FRD, `/control/obstacles`와 `/control/velocity_cmd`는 NED입니다.
- PX4 출력에서 축 교환 또는 z/yaw 부호 반전을 하지 않습니다.
- 축 방향은 PX4와 같지만 데드레코닝 원점은 독립적입니다. XY는 초기 위치, 지면 z=0이며 PX4 EKF의 위치 원점과 동일하다는 뜻은 아닙니다. 현재 출력은 속도 명령입니다.
- `mission_height`는 양의 지상 높이(m)로 유지하고 목표 NED z는 그 음수입니다. 상승 vz<0, 하강 vz>0입니다.
- `range_offset_flu`는 `range_offset_frd`로 변경했습니다. 이전 오프셋은 `[x,-y,-z]`로 변환해서 넣습니다.
- 고정 목표 상수는 `REFERENCE_START_NED` / `GOAL_NED`입니다. 이전 ENU `(6,0,1)`의 물리 위치를 보존한 NED `(0,6,-1)`을 사용합니다. 기본 `forward` 모드는 시작 기수 방향 6m입니다.

이전 실행 프로세스는 종료하고 다시 빌드·source한 뒤 모든 노드를 재시작하세요.
기존 ENU/FLU rosbag과 `map`/`base_link` 설정을 새 노드에 그대로 사용하지 않습니다.
`strict_sensor_checks=false`는 기존처럼 항법 입력 프레임 검사도 생략하므로 생산자 노드를 모두 함께 전환해야 합니다.

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select drone_interfaces drone_integration
source install/setup.bash
```

RPLIDAR C1의 데이터시트 +X(케이블 반대쪽)가 기체 전방이고, X축을 중심으로
180° 뒤집힌 장착을 기본으로 합니다. PX4 바디 좌표는 FRD(+X 앞, +Y 오른쪽, +Z 아래)입니다.
드라이버 `inverted=false`, 전처리 `upside_down=true`, `yaw_offset=0.0`입니다.
데이터시트의 시계 방향 각도 θ를 드라이버가 `/scan` 각도 α=π−θ로 발행하므로,
수신부가 θ=π−α를 복원한 뒤 뒤집힌 장착을 적용합니다.
최종 좌표는 x=d·cosθ, y=−d·sinθ이며, 정방향 장착은 y=+d·sinθ입니다.
따라서 `/scan`의 180°가 기체 앞쪽이고 0°는 뒤쪽입니다.
드라이버에서 이미 `inverted=true`로 보정했다면 이 기본 설정을 그대로 적용하면 안 됩니다.

```bash
ros2 run sllidar_ros2 sllidar_node --ros-args \
  -p serial_port:=/dev/ttyUSB1 \
  -p serial_baudrate:=460800 \
  -p angle_compensate:=true \
  -p scan_mode:=Standard \
  -p inverted:=false
```

센서 확인 시 `/lidar/processed`에서 앞 물체 x>0, 오른쪽 물체 y>0인지 확인합니다.
원시 θ=0°/90°/180°/270°는 뒤집힌 장착에서 각각 앞/왼쪽/뒤/오른쪽입니다.
`yaw_offset`은 이 변환 이후 추가 장착 yaw에만 적용합니다(오른쪽 회전이 양수).


각 터미널에서 다음 환경을 로드합니다.

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

PX4 DDS Agent와 LiDAR `/scan` 드라이버를 먼저 실행합니다.
PX4에서 `sensor_optical_flow`, `distance_sensor`, `sensor_combined`,
`vehicle_attitude`, `vehicle_local_position`, `vehicle_status` 출력이 필요합니다.
`config/px4_dds_additions.yaml`도 확인하세요.

아래 노드들을 각각 별도 터미널에서 실행합니다. 항법은 dead_reckoning_node만 사용합니다.

```bash
ros2 run drone_integration px4_imu_receiver_node --ros-args --params-file src/drone_integration/config/integration.yaml
ros2 run drone_integration optical_flow_receiver_node --ros-args --params-file src/drone_integration/config/integration.yaml
ros2 run drone_integration dead_reckoning_node --ros-args --params-file src/drone_integration/config/integration.yaml
ros2 run drone_integration lidar_receiver_node --ros-args --params-file src/drone_integration/config/integration.yaml
ros2 run drone_integration collision_constraints_node --ros-args --params-file src/drone_integration/config/integration.yaml
ros2 run drone_integration mpc_node --ros-args --params-file src/drone_integration/config/integration.yaml
```

항법 노드는 정지 상태에서 시작합니다. 수평 위치는 첫 정상 거리 측정 때 `(0,0)`으로
초기화하며, NED 위치 `z`는 바닥에서 기체까지의 거리의 음수입니다 (1m 높이 → z=-1m). 축은 PX4 NED를 유지합니다.
IMU를 적분하고 flow로 수평 속도, 거리 센서로 높이 및 수직 속도를 보정합니다.
모캡 보정과 IMU 바이어스 추정은 없으며 수평 위치 오차는 누적됩니다.
거리 센서의 바닥 가시성과 충분한 flow 품질이 필요합니다.

플로우 receiver 기본값은 `flow_source: sensor`입니다. 원시
`/fmu/out/sensor_optical_flow`를 항법용 `/sensors/flow`로 발행하며,
플로우 메시지의 `distance_m`/`distance_available`은 사용하지 않습니다.
속도 환산과 높이에 사용하는 1D 거리는 `/fmu/out/distance_sensor`의
하향 `current_distance`로 받습니다. 정상 거리를 캐시해 다음 플로우에서
사용하고, 새 거리 측정으로 갱신합니다. 거리 미수신 또는 수신 후
`range_timeout`(기본 0.5초) 경과 시 flow는 `distance_m=nan`, `valid=false`입니다.
불량 거리 패킷 하나는 직전 정상 거리를 즉시 지우지 않습니다.

원시 센서의 축과 기체 FRD 축의 yaw 차이는 `sensor_yaw_offset`(rad)로
설정합니다. 기본 0은 두 축이 일치한다는 가정이며, 실제 장착 방향을 자동
추정하지 않습니다. 이 옵션은 하향 센서의 yaw 장착 차이만 보정합니다.
PX4가 기체 축으로 보정한 flow를 받으려면 `flow_source: vehicle`로 설정합니다.
이 경우에도 거리는 별도 `/fmu/out/distance_sensor`를 사용합니다.

### 입력 오류와 재시작

현재 기본값은 `dead_reckoning_node.strict_sensor_checks: false`입니다.
이 모드에서는 센서 frame_id 일치, 메시지 나이, 자세와의 시간차 및
flow/range 시간차로 입력을 거부하지 않습니다. IMU 간격이 100ms를 넘어도
실제 양의 dt 전체를 `p += v*dt + 0.5*a*dt*dt`에 사용합니다. 거리 차분
수직 속도도 250ms 상한 없이 보정합니다. 긴 구간에서는 마지막 측정 가속도를
전체 구간에 적용하는 근사입니다. 프레임 이름만 무시하며 실제 축을 자동 변환하지는
않으므로 입력 값은 기존 NED/FRD 규약을 따라야 합니다.

중복/역순/0 타임스탬프, NaN/잘못된 쿼터니언과 거리, flow 품질/기울기
모델 제한은 유지합니다. 입력 수신이 끊기면 위치 계산과 별개로 항법 valid는
false가 되며 MPC/PX4의 freshness·watchdog도 계속 적용됩니다.

엄격한 검사를 다시 사용하려면 YAML 값을 true로 바꾸거나 다음처럼 실행합니다.

```bash
ros2 run drone_integration dead_reckoning_node --ros-args \
  --params-file src/drone_integration/config/integration.yaml \
  -p strict_sensor_checks:=true
```

엄격 모드에서는 IMU의 연속 측정 간격이 100ms를 넘으면 해당 구간을 적분하지 않고
`navigation/state.reason`에 `imu_prediction_gap`을 표시합니다. 샘플이 다시
들어와도 누락 구간의 위치를 복원할 수 없어 데드레코닝의 무효 상태를 유지합니다.
센서 수신률과 clipping 거부 원인을 해결한 뒤 정지 상태에서 항법·MPC·커맨드
노드를 재시작하세요. 항법 원점이 바뀌므로 항법 노드만 재시작하지 않습니다.
모캡 항법에서는 새로운 절대 위치 관측으로 이 오류를 해제할 수 있습니다.

PX4 원시 타임스탬프가 1초 넘게 역행하고 새 시간대에서 증가하는 샘플이
3개 확인되면 재부팅/시간 초기화로 판단합니다. 첫 2개는 격리하고 이후
입력을 복구하며 `sensors/px4_reset` (`std_msgs/Empty`) 이벤트를 발행합니다.
일반적인 중복·작은 역순 샘플은 시간 초기화로 처리하지 않습니다.
이는 타임스탬프 기반 감지이며 펌웨어 boot ID를 확인하는 방식은 아닙니다.

이 이벤트를 받으면 데드레코닝은 원점과 센서 상태를, MPC는 이전 위치 이력과
전방 목표 기준을 지웁니다. 커맨드 노드는 자동 전환도 취소하고 OFF에 고정합니다.
센서 입력의 복구는 Offboard 자동 재진입을 의미하지 않습니다. 원점과 목표를
확인한 뒤 커맨드 노드를 명시적으로 재시작하거나 기존 enable 서비스를 사용합니다.
`sensors/px4_reset`은 진단용으로 관찰하며 수동으로 발행하지 않습니다.

중복/역순 flow는 직전 정상 관측을 덮어쓰지 않습니다. 새 타임스탬프의 실제
품질 불량은 계속 항법을 무효화합니다. 잘못된 frame_id와 자세 시간차로
인한 거부는 엄격 모드에서만 적용합니다.

MPC는 첫 정상 항법 상태의 위치·기수 방향으로 전방 6m 직선을 설정하고
1m 높이를 유지합니다. 장애물 원은 기체에서 4m 이내의 LiDAR 점들로 생성합니다. `mpc_node.reference_mode`, `forward_distance`,
`mission_height`를 YAML에서 변경할 수 있습니다. 로컬 NED 고정 목표는
`reference_mode: fixed`로 선택할 수 있습니다.

직접 시동을 걸고 약 1m에서 Hold, Position 또는 Altitude 모드로 호버링한 뒤,
마지막으로 커맨드 노드를 실행합니다.

```bash
ros2 run drone_integration px4_command_node --ros-args --params-file src/drone_integration/config/integration.yaml
```

정상 항법·MPC 명령·충돌 제약·PX4 EKF 속도·armed 상태가 확인되면
setpoint를 1.1초 이상 송신하고 자동 Offboard 요청을 보냅니다.
실제 전환은 PX4가 승인해야 합니다. 자동 ARM이나 이륙은 하지 않습니다.
목표 도달 후 수평 정지·고도 유지를 하며, 착륙은 직접 수행합니다.

Offboard 확인 후 RC로 다른 모드로 바꾸면 stream을 중단하고 재진입하지 않습니다.
준비 stream 중 다른 허용 호버 모드로 바꾸는 것은 전환 취소로 처리되지 않습니다.
센서 오류 등으로 stream을 중단한 경우 PX4 Offboard-loss 설정을 따릅니다.
재시작하려면 커맨드 노드를 종료 후 다시 실행하세요.

오프라인 검사:

```bash
PYTHONPATH=src/drone_integration python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=src/drone_integration:$PYTHONPATH python3 tests/check_dead_reckoning_ros.py
PYTHONPATH=src/drone_integration:$PYTHONPATH python3 tests/check_px4_reset_ros.py
PYTHONPATH=src/drone_integration:$PYTHONPATH python3 tests/check_optical_distance_ros.py
```

## 센서 수신 진단

제어 노드 없이 다음을 실행하면 raw PX4 입력과 변환 결과의 publisher 수·수신률을 비교합니다.

```bash
python3 scripts/check_sensor_inputs.py --seconds 10
```

진단 결과와 현재 펌웨어의 PX4 콘솔 출력 `ver all`,
`listener sensor_combined 1`, `listener vehicle_optical_flow 1`,
`listener distance_sensor 1`, `uxrce_dds_client status`를 함께 확인합니다.
이 진단은 ARM이나 Offboard 요청을 보내지 않습니다.

진단 스크립트는 raw/변환 센서 외에 자세, 항법, PX4 local position/status,
충돌 제약과 MPC 명령도 비교합니다. 로거 기본 토픽에도 raw PX4 센서,
VehicleStatus, 시간 초기화 이벤트를 추가했습니다. 다음 로그에서는 raw 입력이
없는 경우와 receiver에서 거부한 경우를 구분할 수 있습니다. 초기화 이벤트는
발생할 때만 오는 토픽이므로 평상시 미수신은 정상입니다.

PX4 어댑터는 완화 모드에서도 측정 나이가 250ms를 넘거나 시계가 맞지 않는 입력을 거부합니다.
