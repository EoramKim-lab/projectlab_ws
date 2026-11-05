> 과거 ENU/FLU·모캡 구성 기록입니다. 현재 NED/FRD 실행은 [DEAD_RECKONING.md](../DEAD_RECKONING.md)를 따릅니다. 아래 좌표 설정과 명령을 현재 구성에 혼용하지 마세요.

# Historical documentation — superseded by README.md

# 드론 통합 워크스페이스 — ROS 2 Humble / Ubuntu 22.04 / PX4 1.14

센서 입력, 항법, 라이다 제약, MPC, PX4 속도 명령을 분리한 Python 기반 초기 구현입니다.
홈의 `drone_avoidance_mpc.zip`에 포함된 CasADi/IPOPT NMPC를 통합했습니다. 실기 충돌회피 비행 검증은 별도로 필요합니다.

## 1. 노드와 입출력

Python 패키지는 역할에 따라 `sensor/`, `navigation/`, `control/`로 나눕니다.
실행되는 ROS 노드는 파일명과 실행 이름에 `_node`, 클래스명에 `Node`를 붙입니다.
공통 ROS 유틸리티와 좌표 변환 함수는 패키지 루트에 둡니다.

```text
src/drone_integration/drone_integration/
├── __init__.py
├── common.py
├── math_utils.py
├── sensor/
│   ├── __init__.py
│   ├── mocap_receiver_node.py
│   ├── px4_imu_receiver_node.py
│   ├── optical_flow_receiver_node.py
│   └── lidar_receiver_node.py
├── navigation/
│   ├── __init__.py
│   ├── navigation_node.py
│   └── estimator.py
└── control/
    ├── __init__.py
    ├── collision_constraints_node.py
    ├── halfplanes.py
    ├── mpc_node.py
    └── px4_command_node.py
```

| 노드 / Python 파일 | 입력 | 출력 / 역할 |
|---|---|---|
| `sensor/mocap_receiver_node.py` | `/mocap/rigid_bodies` (`RigidBodies`) | `sensors/mocap_pose`, 선택적 PX4 위치 보조 |
| `sensor/px4_imu_receiver_node.py` | PX4 `SensorCombined`, `VehicleAttitude` | `sensors/imu` (`Imu`), `sensors/attitude` (`QuaternionStamped`) |
| `sensor/optical_flow_receiver_node.py` | PX4 `VehicleOpticalFlow`, `DistanceSensor` | `sensors/flow` (`FlowMeasurement`), `sensors/range` (`Range`) |
| `sensor/lidar_receiver_node.py` | `/scan` (`LaserScan`) | `lidar/processed` (`ProcessedScan`): 수신+전처리 |
| `navigation/navigation_node.py` | 모캡, IMU, 자세, 거리, 플로우 | `navigation/state` (`NavigationState`) |
| `control/collision_constraints_node.py` | `lidar/processed` | `collision/halfplanes` (`Halfplanes`) |
| `control/mpc_node.py` | `navigation/state`, `lidar/processed` | `control/velocity_cmd` (`TwistStamped`) |
| `control/px4_command_node.py` | `control/velocity_cmd`, 항법/제약 유효성, PX4 local velocity validity | PX4 `OffboardControlMode`, `TrajectorySetpoint`, 모드 요청 `VehicleCommand` |

모든 내부 토픽은 상대 이름입니다. 표의 이름 앞에 `/`를 붙이면 기본 실행 시 전체 이름입니다.
PX4 `/fmu/...` 토픽은 절대 이름입니다. 다중 기체는 ROS remapping을 추가해야 합니다.

### 첨부 코드 재사용

- 기존 `receiver.py`에서 LaserScan 수신, 유효성/시간 검사, 타임아웃 처리를 가져왔습니다.
- 기존 `preprocessing.py`의 함수/설정 코드를 `sensor/lidar_receiver_node.py` 안에 합쳤습니다.
- 기존 `halfplanes.py`는 **파일 내용을 그대로 보존**하고 `control/halfplanes.py`에 둡니다.
- `sllidar_ros2` 하드웨어 드라이버 소스를 함께 넣었습니다. 장치 프로토콜은 이 드라이버가 담당합니다.
- 기존 한 노드의 JSON 문자열 출력은 노드 분리를 위해 명시적 ROS 메시지로 교체했습니다.

## 2. 좌표와 센서 의미

- 내부 세계 좌표: `map`, ENU (x=동, y=북, z=위), 단위 m, m/s, rad.
- 내부 기체 좌표: `base_link`, FLU (x=앞, y=왼쪽, z=위).
- PX4 세계 좌표: NED, PX4 기체 좌표: FRD.
- 쿼터니언: 내부 ROS 메시지는 xyzw, PX4 입력은 wxyz.
- 속도 명령: `TwistStamped.header.frame_id=map`, linear는 **세계좌표 속도**, angular.z는 **ENU yaw rate**.
- 변환: `(v_N,v_E,v_D)=(v_y,v_x,-v_z)`, PX4 yawspeed = -ENU yaw rate.

**모캡 좌표축은 실제 PX4 NED 축과 일치하는 ENU로 보정**해야 합니다.
Qualisys 어댑터는 `world_rotation_xyzw`, `world_translation`, `body_rotation_xyzw`,
`body_origin_in_rigid`로 세계축·강체축·기체 기준점 오프셋을 적용합니다.
기본 변환은 identity이며 실제 장착·캘리브레이션을 자동 추정하지 않습니다.
실센서 항법 실행은 [REAL_NAVIGATION.md](REAL_NAVIGATION.md)를 참고하세요.

홀리브로 모델은 아직 특정되지 않았습니다. 이 코드는 센서를 **Pixhawk에 연결한 뒤 PX4가 제공하는 정규화된 메시지**를 받습니다.
H-Flow라면 플로우와 거리 센서가 결합되어 있지만, PMW3901 등 다른 모델은 별도 거리 센서가 필요할 수 있습니다.
보유 센서가 PX4 1.14에서 실제로 지원/출력되는지는 모델·보드·드라이버를 확인해야 합니다.
H-Flow 최신 안내의 파라미터가 PX4 1.14에 모두 존재한다고 가정하지 않습니다.

옵티컬 플로우는 절대 yaw 측정기가 아닙니다.
기본 자세/yaw와 고도는 **보정된 모캡 pose**를 사용합니다. `attitude_source=px4`로
PX4 EKF 자세를 선택할 수 있고, 거리 고도 보정은 `use_range_height=true`로 선택합니다.

## 3. 항법 구현

`navigation/estimator.py`는 바이어스 추정 EKF가 아닌, 최소 상보 필터입니다.
각 관측을 콜백에서 한 번만 사용합니다.

1. 기본적으로 보정된 모캡 자세로 회전행렬 R을 구성합니다. PX4 자세도 선택 가능합니다.
2. Pixhawk IMU specific force를 `a_map = R*f_body + [0,0,-9.80665]`로 변환하고 위치/속도를 예측합니다.
3. 모캡으로 위치를 갱신하고, 연속 두 위치의 차분 속도로 속도를 보정합니다.
4. `use_range_height=true`일 때만 하향 거리로 `z = ground_z + range*R[2,2] - (R*range_offset_flu)[2]`를 적용합니다.
5. 플로우에서 회전 성분을 제거한 뒤 근사 수평 속도를 계산해 보정합니다.

플로우 기본 입력은 `SensorOpticalFlow`이며 센서→기체 yaw 차이를
`optical_flow_receiver_node.sensor_yaw_offset`으로 설정합니다. 기본 0은 축이
일치한다는 가정입니다. `flow_source: vehicle`로 선택하면 기체 축으로 보정된
`VehicleOpticalFlow`를 사용합니다.
`f = pixel_flow - delta_angle[:2]`에 대해 기체 FLU 수평 속도는
`[v_forward, v_left] = [f_y, f_x] * distance / integration_dt`입니다.
플로우의 자체 거리 값 대신 항상 `/fmu/out/distance_sensor`의 하향 거리를 사용합니다.
NaN gyro 보정값을 0으로 간주하지 않습니다.

고도는 수평 바닥을 가정한 지면 기준 높이입니다. 바닥 높이가 바뀌는 곳에서 절대고도처럼 사용할 수 없습니다.
거리 센서는 기체 아래 방향으로 장착되어야 하며, 위치 오프셋을 YAML에 설정합니다.
기본적으로 모캡 위치·자세와 IMU가 최신이고 유효해야 `state.valid=true`입니다.
`require_flow=false`, `require_range=false`가 기본이며, 플로우는 유효한 경우 보정에 사용합니다.
거리·플로우를 필수로 요구하려면 각각 `require_range=true`, `require_flow=true`를 설정합니다.

플로우 근사는 Rzz>=0.96에서만 사용하고, 항법 유효 상태는 기울기 15도 이내로 제한합니다.
라이다는 원본과 동일한 수평 2D 모델이며, 자세 보상/스캔 deskew가 없습니다. 기울기 제한이 이를 보상하는 것은 아닙니다.

PX4 자체 EKF와 ROS 항법은 역할이 다릅니다.
ROS 항법은 MPC용 상태를 구성하고, PX4 EKF는 실제 내부 속도 제어를 위한 상태를 추정합니다.
모캡 수신기는 `publish_to_px4=true`일 때 **보정된 모캡 위치만** PX4 external vision 입력으로 전달합니다. 기본값은 false입니다.
ROS에서 융합한 상태를 다시 PX4로 보내 IMU 정보를 중복 융합하지 않습니다.
PX4 EKF에서 external position/flow/range aiding을 별도로 구성해야 합니다.
모캡 브리지는 위치만 전송하며 yaw/velocity는 NaN으로 둡니다. EV yaw 융합은 켜지 마세요.

### 타임스탬프와 초기 구현의 한계

- 모캡과 LaserScan은 원래 ROS 헤더를 보존하고 오래된 값/미래 값/역순 값을 거부합니다.
- PX4 원시 센서 어댑터는 메시지의 증가하는 PX4 timestamp를 검사하고 **ROS 수신 시각**을 내부 헤더로 사용합니다.
- 내부 노드도 헤더 나이와 자세-관측 시간 차이를 검사합니다. 다시 발행한다고 측정 시각을 새로 만들지 않습니다.
- DDS 센서 헤더는 수신 시각이므로 정확한 하드웨어 동기화나 지연 보정은 아닙니다. 심하게 지연된 DDS 패킷을 완벽히 판별하지 못합니다.
- 초기 상태/비동기 관측을 단순히 보정하는 구조입니다. 센서 바이어스, 지연 상태 갱신, 공분산, innovation gate는 구현하지 않았습니다.
- PX4 재부팅으로 timestamp가 초기화되면 어댑터 노드도 재시작하세요.
- `map` 축 정렬, PX4 yaw reset, 클럭 동기화와 센서 지연은 실제 연결 후 검증해야 합니다.

## 4. 라이다 충돌 제약

`Halfplanes.a`는 (M,2) 행렬 A를 행 우선으로 펼친 배열입니다. `b`의 길이는 M입니다.
제약은 `A * p_scan_body_xy <= b`이며, 기준점과 방향은 **그 스캔을 취득한 순간의 기체 FLU**입니다.
단순히 A를 세계좌표 위치에 곱하면 안 됩니다.

MPC가 수평 yaw 모델을 사용할 경우 스캔 시점 기체 위치 p0, 수평 회전 Rz를 정렬하고
`A_map = A_body * Rz.T`, `b_map = b_body + A_map * p0_xy`로 변환할 수 있습니다.
통합 MPC는 별도로 `lidar/processed` 점들을 원형 장애물로 묶고, 스캔 시각에 가장 가까운 항법 상태(최대 0.08초 차이)로 map 좌표에 정렬합니다. 매 예측 단계의 원 접평면 제약은 ZIP 제어기 내부에서 계산합니다. 기존 Halfplanes는 PX4 command 노드의 독립적인 입력 상태 검사에 사용합니다.
`Halfplanes.header.stamp`는 원본 스캔 시각을 유지합니다.

빈 섹터는 제약 행을 만들지 않습니다. 범위 밖 점만 있으면 valid=true이면서 M=0일 수도 있습니다.
이는 관측하지 못한 공간의 안전을 보증하지 않습니다.
`origin_feasible=false`는 현재 위치가 안전 마진 안에 있음을 뜻하며 command 노드는 스트림을 차단합니다.
`valid=false`나 오래된 메시지를 빈 안전 제약으로 취급하지 않습니다.

## 5. 설치 / 빌드

Ubuntu 22.04에 ROS 2 Humble이 설치되어 있다고 가정합니다.
압축을 풀고 아래 워크스페이스 루트에서 실행합니다.

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash
sudo apt update
sudo apt install python3-colcon-common-extensions python3-rosdep python3-numpy
# rosdep init은 해당 PC에서 아직 한 적이 없을 때 한 번만 실행
# sudo rosdep init
rosdep update
# src/px4_msgs는 PX4 v1.14.4의 메시지 정의로 이미 포함되어 있습니다.
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

`src/px4_msgs`에는 **PX4 v1.14.4 태그와 동일한 메시지 정의 184개**를 포함했습니다.
출처와 SHA256은 `src/px4_msgs/PX4_SOURCE.json`에 기록했습니다.
다른 워크스페이스의 px4_msgs를 따로 source할 필요가 없습니다.
`px4_msgs`는 main/latest 대신 **사용 중인 펌웨어와 같은 정의**를 사용하세요.
커스텀 메시지나 정확한 패치 릴리스 차이가 있으면 해당 펌웨어의 msg 정의에 맞춰야 합니다.

## 6. PX4 1.14 DDS / 센서 연결

v1.14.0 기본 `dds_topics.yaml`에는 `sensor_combined`, `vehicle_attitude`, `vehicle_local_position`은 있지만,
이 코드가 구독하는 `vehicle_optical_flow`, `distance_sensor`, `vehicle_command_ack` 출력은 없습니다.

`config/px4_dds_additions.yaml`의 항목을 PX4 소스의
`src/modules/uxrce_dds_client/dds_topics.yaml`의 **기존 publications 목록에 병합**하고
해당 Pixhawk 보드용 펌웨어를 다시 빌드/업로드해야 합니다. 조각 파일로 원본 전체를 교체하지 마세요.
보드 모델이 지정되지 않아 보드별 make/flash 명령은 포함하지 않았습니다.

거리 센서가 여러 개라면 올바른 uORB instance가 노출되는지 확인하고 `range_device_id`를 지정하세요.
현재 어댑터는 `ROTATION_DOWNWARD_FACING=25`인 거리만 받으며 custom mounting quaternion은 처리하지 않습니다.

H-Flow를 사용한다면 CAN/DroneCAN 센서 연결과 실제 PX4 버전에 존재하는 flow/range subscription,
`SENS_FLOW_ROT`, `EKF2_OF_CTRL`, 외부 위치 융합(`EKF2_EV_CTRL`), range aiding 설정을 점검합니다.
실제 센서 출력은 PX4 콘솔의 `listener vehicle_optical_flow`, `listener distance_sensor`로 확인합니다.

Micro XRCE-DDS Agent를 설치/기동하고 Pixhawk uxrce_dds_client와 연결하세요.
UDP SITL의 agent 실행 예:

```bash
MicroXRCEAgent udp4 -p 8888
```

실물은 연결한 TELEM 포트/보드의 시리얼 설정에 맞게 Agent와 PX4 client를 설정합니다.
이 패키지는 Agent 설치나 펌웨어 설정을 자동 변경하지 않습니다.

PX4 내부 속도 제어는 유효한 EKF 속도가 필요합니다.
ROS state만 valid여도 PX4 `/fmu/out/vehicle_local_position`의 `v_xy_valid`, `v_z_valid`가 false면 명령을 차단합니다.

## 터미널별 실시간 실험

`ros2 run drone_integration 실행이름`으로 노드마다 터미널을 하나씩 사용합니다.
`drone_integration`의 launch 파일은 삭제했습니다.
각 노드는 기본 2 Hz로 최근 값과 입력 상태를 계속 출력합니다. `WAITING`은 아직 수신/처리한 값이
없음을, `STALE`은 마지막 상태 갱신 후 0.5초 이상 경과했음을 뜻합니다. `LIVE`는 상태 갱신이
최근이라는 뜻이며, 데이터 유효성은 별도 `valid`, `reason`, `REJECTED`, `BLOCKED`를 확인하세요.
값의 좌표계와 단위도 함께 표시합니다. 로그 출력 주기는 발행/계산 주기를 바꾸지 않습니다.

한 번 빌드한 뒤 각 터미널에서 환경을 불러옵니다:

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select drone_integration
source install/setup.bash
```

각 터미널에서는 `source /opt/ros/humble/setup.bash`와 `source ~/drone_integration_ws/install/setup.bash`를 수행하세요.
아래 표의 각 행은 별도 터미널에서 실행합니다:

| 터미널 | 명령 | 계속 출력되는 내용 |
| --- | --- | --- |
| C1 드라이버 | `ros2 run sllidar_ros2 sllidar_node --ros-args -p channel_type:=serial -p serial_port:=/dev/ttyUSB1 -p serial_baudrate:=460800 -p frame_id:=laser -p inverted:=false -p angle_compensate:=true -p scan_mode:=Standard` | 장치 연결 상태 (`/scan` 발행) |
| 라이다 수신기 | `ros2 run drone_integration lidar_receiver_node` | 원본/전처리 점 수, 유효성, 기체 원점 기준 최근접 거리 |
| 옵티컬/거리 센서 | `ros2 run drone_integration optical_flow_receiver_node` | quality, flow/gyro 적분, 적분 시간, 하향 거리 |
| PX4 IMU | `ros2 run drone_integration px4_imu_receiver_node` | FLU 가속도·각속도, ENU 자세 quaternion |
| 모캡 수신기 (실센서 항법 시) | `ros2 run drone_integration mocap_receiver_node --ros-args -p rigid_body_name:=실제강체이름` | 보정된 ENU 위치·FLU 자세 |
| 항법 | `ros2 run drone_integration navigation_node` | ENU 위치·속도·yaw, valid/reason, 센서별 age |
| 장애물 제약 | `ros2 run drone_integration collision_constraints_node` | 제약 수, origin_feasible, valid/reason |
| MPC | `ros2 run drone_integration mpc_node` | 목표점, ENU 속도 명령·yaw rate, 장애물 수, solver 시간 또는 차단 사유 |
| PX4 command 관찰 | `ros2 run drone_integration px4_command_node` | 수신 명령, 스트림 enable 상태·준비 조건, 실제 전송 시 제한 적용된 NED setpoint |

PX4 DDS 연결/Qualisys 드라이버는 별도로 필요합니다. 모캡 수신기는 기존 설정대로 유효한
모캡 위치를 PX4에 전달할 수 있습니다(`publish_to_px4` 설정 참고).
같은 노드를 여러 터미널에서 중복 실행하지 마세요.
옵티컬·IMU는 입력 PX4 uORB 토픽이 펌웨어 DDS 설정에 포함돼 있어야 값이 나옵니다.

로그를 더 자주 보거나 끄려면 `--ros-args -p monitor_rate:=5.0` 또는 `--ros-args -p monitor_rate:=0.0`을 추가합니다.

### 더미 항법으로 MPC 실험

실제 센서 항법 대신 아래 명령을 **항법 터미널 하나에서만** 실행하세요:

```bash
ros2 run drone_integration navigation_node --ros-args -p dummy_mode:=true -p dummy_position:="[0.0, 0.0, 1.0]" -p dummy_yaw:=0.0
```

센서 입력 없이 현재 시각의 `navigation/state`를 50 Hz로 발행합니다. 상태는 고정 ENU 위치,
지정 yaw(rad), 속도·가속도 0, `valid=true`, `reason=dummy_experiment`입니다.
센서를 받은 것처럼 보이지 않도록 sensor age는 1e9로 표시합니다. 센서 융합 콜백은 설치하지 않습니다.
이 모드는 명령에 따라 위치가 움직이는 시뮬레이터가 아닙니다. 위치 변경은 인자를 바꿔 재시작합니다.
실센서 항법으로 돌아갈 때는 종료 후 `dummy_mode` 없이 재실행하세요(기본 false).

MPC를 켜면 코드에 고정한 목표 `(2, 0, 1) m`와 직선 참조 궤적을 사용합니다.
별도의 목표 토픽 발행은 필요 없습니다.

MPC 터미널에서 명령과 solver 상태를, PX4 command 터미널에서 수신된 명령을 확인합니다.
더미 항법만으로 라이다를 대체하지는 않습니다. 유효한 라이다 입력이 필요합니다.
더미 상태는 MPC 계산 관찰용으로, PX4 command 노드는 `dummy_experiment` 상태에서
Offboard enable/출력을 차단합니다. 자동 arm/이륙은 수행하지 않습니다.

## 7. 실행

Qualisys QTM 토픽 수신용 설정과 별도 launch를 추가했습니다. 설치 및 실행은
[QUALISYS.md](QUALISYS.md)를 참고하세요. 드라이버·SDK·메시지 설치와 Humble 빌드를 완료했고,
실제 QTM PC 연결 및 수신 검증은 아직 필요합니다.
원본 `/mocap/rigid_bodies`에서 `mocap_receiver_node`가 강체를 선택·좌표 보정해
`sensors/mocap_pose`로 전달합니다. 실행 및 보정 방법은 [REAL_NAVIGATION.md](REAL_NAVIGATION.md)를 참고하세요.

현재 라이다는 C1입니다. 기본 포트 `/dev/ttyUSB1`, 통신 속도 `460800`, 스캔 모드 `Standard`로 별도 실행합니다:

```bash
source /opt/ros/humble/setup.bash
cd ~/drone_integration_ws
source install/setup.bash
ros2 run sllidar_ros2 sllidar_node --ros-args -p channel_type:=serial -p serial_port:=/dev/ttyUSB1 -p serial_baudrate:=460800 -p frame_id:=laser -p inverted:=false -p angle_compensate:=true -p scan_mode:=Standard
```

센서·항법·제어 노드는 위의 터미널별 표에 따라 `ros2 run`으로 각각 실행합니다.
노드의 기본값으로 바로 실행할 수 있습니다. YAML 설정을 적용하려면 `--params-file`을 추가하세요:

```bash
ros2 run drone_integration lidar_receiver_node --ros-args --params-file ~/drone_integration_ws/src/drone_integration/config/integration.yaml
```

C1 드라이버, Qualisys 드라이버, PX4 DDS 연결은 별도로 실행합니다.
PX4 command 노드는 기본적으로 armed Hold 상태에서 자동 Offboard 전환을 준비합니다. 더미 항법에서는 실제 출력을 차단합니다.

YAML의 노드별 설정 키도 `lidar_receiver_node`, `navigation_node`처럼 실행 이름과 일치시킵니다.
기존 설치가 있다면 구조 변경 후 `colcon build --packages-select drone_integration`과 `source install/setup.bash`를 다시 실행하세요.

기본 라이다 yaw_offset=pi는 첨부 코드의 180도 장착값입니다. 실제 장착에 맞게 조정하세요.

```bash
ros2 topic echo /navigation/state
ros2 topic echo /collision/halfplanes
ros2 topic info /fmu/out/vehicle_optical_flow --verbose
ros2 topic info /fmu/out/distance_sensor --verbose
```

## 8. PX4 속도 명령 동작

자동 arm/자동 이륙은 수행하지 않습니다. RC로 수동 이륙한 뒤 시작 위치
`(-3.012, -0.919)` 부근, 모캡 z=1 m에서 Hold시킨 다음 **마지막으로** 실행하세요:

```bash
ros2 run drone_integration px4_command_node
```

기본 `auto_offboard=true`입니다. `/fmu/out/vehicle_status`에서 armed Hold
(`AUTO_LOITER`)를 확인하고, MPC 명령·항법·라이다 제약·PX4 EKF 속도가
모두 유효하면 20 Hz setpoint/heartbeat를 자동으로 시작합니다.
1.1초 연속 스트림 준비 후 Offboard를 요청하고, PX4 상태로 전환 완료를 확인합니다.
Hold가 유지되는 동안 미확인 요청은 1초 간격으로 재전송합니다.
수동 enable/request_offboard 서비스 호출은 필요 없습니다.
실제 전환 시간은 입력 준비 및 PX4 승인에 따라 달라집니다.
전환 즉시 MPC 수평 이동과 모캡 z=1 m 높이 제어를 함께 수행합니다.
시작 위치와 높이는 노드가 확인하지 않으므로 RC로 맞춘 뒤 실행하세요.

초기 입력 미수신 시에는 자동으로 기다립니다. 스트림 시작 후 입력이 무효가 되거나,
PX4 상태가 2초 넘게 수신되지 않거나, disarm/다른 모드로 변경되면 스트림을 차단합니다.
Offboard 진입 후 RC로 Hold로 돌아오면 자동으로 Offboard에 재진입하지 않습니다.
자동 전환을 다시 시작하려면 노드를 재시작합니다.
`VehicleStatus` 토픽이 수신되지 않으면 `AUTO WAIT` 상태로 남습니다.

기존 수동 서비스 방식은 아래 옵션으로 사용할 수 있습니다:

```bash
ros2 run drone_integration px4_command_node --ros-args -p auto_offboard:=false
ros2 service call /control/enable std_srvs/srv/SetBool '{data: true}'
# 유효한 스트림을 1.1초 이상 유지한 뒤
ros2 service call /control/request_offboard std_srvs/srv/Trigger '{}'
```

서비스 응답 success는 모드 요청 전송을 뜻하며 실제 모드는 PX4 VehicleStatus/QGC에서 확인합니다.

- position, acceleration, jerk, yaw는 NaN, velocity만 활성화하고 yawspeed를 전송합니다.
- 수평/수직 속도 및 yaw rate 상한을 설정합니다.
- 명령/항법/라이다/PX4 속도 상태가 무효 또는 stale이면 heartbeat와 setpoint를 중단하고 비활성 상태로 고정합니다.
- 입력이 다시 와도 자동 재개하지 않습니다. 명시적으로 enable을 다시 호출해야 합니다.
- 중단 시 정지/호버를 보장하지 않습니다. PX4 `COM_OF_LOSS_T` 및 Offboard-loss 동작 설정이 적용됩니다.
- 최신 제약과 origin feasibility는 확인하지만 **속도 명령이 미래 장애물 제약을 만족하는지는 검사하지 않습니다**.
  미래 장애물 최적화는 통합 MPC가 수행합니다. 실기 안전성은 아직 검증하지 않았습니다.

스트림 중단:

```bash
ros2 service call /control/enable std_srvs/srv/SetBool '{data: false}'
```

## 9. 검증 범위

현재 MPC 통합 환경에서 ROS 2 Humble `colcon build --packages-select drone_integration`,
Python 구문 검사, 기존 오프라인 테스트 20개, MPC 검사 8개, 센서 모니터·더미 항법 검사 4개를 통과했습니다.
추가 검사는 실제 생성된 ROS 메시지와 노드를 사용해 solver/콜백을 검증하지만,
실행 환경의 네트워크 제한으로 DDS 송수신은 검증하지 못했습니다. SITL/실기 비행도 수행하지 않았습니다.

```bash
python3 -m compileall -q src/drone_integration
PYTHONPATH=src/drone_integration python3 -m unittest discover -s tests -v
```

실제 Ubuntu 대상에서 다음 단계는 colcon 빌드 → 센서 토픽 연결 → 정지 상태 축/중력/거리 확인 →
SITL Offboard 속도 추종 확인 → 통합 MPC의 실시간 성능과 제약 검증입니다.
실물 연결 전에는 프로펠러를 분리한 상태에서 명령/모드 동작을 확인하세요.

## 10. 참고한 공식 소스

- PX4 1.14 Offboard: https://docs.px4.io/v1.14/en/flight_modes/offboard
- PX4 1.14 ROS2/DDS: https://docs.px4.io/v1.14/en/middleware/uxrce_dds
- PX4 1.14 외부 위치: https://docs.px4.io/v1.14/en/ros/external_position_estimation
- PX4 v1.14.0 DDS 원본: https://github.com/PX4/PX4-Autopilot/blob/v1.14.0/src/modules/uxrce_dds_client/dds_topics.yaml
- PX4 release/1.14 메시지: https://github.com/PX4/px4_msgs/tree/release/1.14/msg
- 플로우 부호/회전 보정: https://github.com/PX4/PX4-Autopilot/blob/v1.14.0/src/modules/sensors/vehicle_optical_flow/VehicleOpticalFlow.cpp
- Holybro H-Flow: https://docs.holybro.com/peripherals/h-flow-dronecan/overview
- Holybro H-Flow 연결 안내(최신 기준): https://docs.holybro.com/peripherals/h-flow-dronecan/setup-guide

## 통합 MPC 실행

ROS Python 환경에 CasADi가 필요합니다(현재 환경: 3.8.2). 새 환경에서는
`python3 -m pip install 'casadi>=3.6,<4'`로 설치한 뒤 빌드합니다.

```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select drone_integration
source install/setup.bash
# 각각 다른 터미널에서 실행
ros2 run drone_integration lidar_receiver_node
ros2 run drone_integration navigation_node
ros2 run drone_integration collision_constraints_node
ros2 run drone_integration mpc_node
ros2 run drone_integration px4_command_node
```

목표점과 참조 궤적은 `src/drone_integration/drone_integration/control/mpc_node.py` 상단에서 수정합니다:

```python
REFERENCE_START_ENU = (-3.012, -0.919, 1.0)
GOAL_ENU = (2.063, 0.835, 1.0)
REFERENCE_SPEED = 0.5
```

수평 참조는 고정 시작점에서 목표점까지의 직선입니다. 현재 위치를 이 선분에 투영한 뒤
예측 구간의 참조 점을 생성하므로, 회피 중에도 기준선이 기체를 따라 옆으로 이동하지 않습니다.
참조 속도 상한은 코드 값을 사용하고, 목표 접근 시 감속합니다. z는 `GOAL_ENU[2]`를 유지합니다.
`/control/goal` 구독은 제거했습니다. 수정 후 빌드하고 MPC 노드를 재시작하세요.

```bash
colcon build --packages-select drone_integration
source install/setup.bash
ros2 run drone_integration mpc_node
```

2D 모델의 전진 속도/yaw rate를 map ENU 속도로 변환합니다. 수평 목표 0.15 m 이내에서는
수평 명령을 0으로 하고, 높이는 별도의 비례 제어(최대 0.5 m/s)로 목표 z를 유지합니다.
목표 yaw는 사용하지 않습니다. 목표점은 실행 중 고정됩니다.
기본 참조 속도는 0.5 m/s입니다. 기존 yaw 제한에서 ZIP의 1 m/s 참조는 근접 장애물 문제를 infeasible로 만드는 경우가 있어 낮췄습니다.
기본 주기는 0.15초이며 속도/yaw 제한은 기존 PX4 command 제한(1 m/s, 0.6 rad/s)에 맞췄습니다.

전처리된 점은 거리 간격으로 클러스터링하며 고립점도 장애물로 유지합니다. 원래 ZIP의
raw LaserScan 검출과 달리 전처리 메시지에는 beam index가 없어 누락 beam을 판별하지 못합니다.
장애물이 `max_obstacles`를 넘으면 일부를 버리지 않고 명령을 중단합니다.
센서 무효/지연, 스캔 상태 정렬 실패, solver 실패 시 명령 발행을 중단하고 기존 command
watchdog가 스트림을 차단합니다. 이것은 즉시 정지 명령이 아니며 기존 Offboard-loss 정책을 따릅니다.
출력 timestamp는 가장 오래된 입력 시각을 유지하므로 긴 solver 지연도 watchdog에 반영됩니다.
SITL/실기 비행 및 실제 센서 부하에서의 시간 제한 검증은 별도입니다.

통합 검증 명령(실제 ROS 메시지/노드를 사용하며 PX4 명령은 발행하지 않음):

```bash
ROS_LOG_DIR=/tmp/mpc_ros_logs OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 tests/check_mpc_ros.py
```

센서 모니터와 더미 항법 검사(ROS/워크스페이스 source 후):

```bash
ROS_LOG_DIR=/tmp/drone_experiment_logs OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 tests/check_experiment_ros.py
```

### IMU는 들어오지만 라이다/옵티컬이 WAITING인 경우

라이다 수신기는 C1 하드웨어 드라이버를 실행하지 않습니다. 별도 터미널에서 실행합니다:

```bash
ros2 run sllidar_ros2 sllidar_node --ros-args -p channel_type:=serial -p serial_port:=/dev/ttyUSB1 -p serial_baudrate:=460800 -p frame_id:=laser -p inverted:=false -p angle_compensate:=true -p scan_mode:=Standard
```

`ros2 topic info /scan -v`에서 Publisher count가 있어야 합니다.
옵티컬 수신기는 두 타입을 구분합니다:

- `raw_flow`: `/fmu/out/sensor_optical_flow` (`SensorOpticalFlow`), 기본 항법 입력(`flow_source: sensor`).
- `flow_source: vehicle` 선택 시 `/fmu/out/vehicle_optical_flow` (`VehicleOpticalFlow`)를 대신 사용합니다.
- `range`: `/fmu/out/distance_sensor` (`DistanceSensor`), 하향 거리 입력.

기본 sensor 모드에서는 raw_flow와 별도 하향 거리가 들어오면 `/sensors/flow`를 발행합니다.
원시 플로우의 거리 필드는 사용하지 않으며, 최근 정상 거리 미수신 시 flow는 invalid입니다.
각 토픽은 `ros2 topic info 토픽이름 -v`로 타입과 발행자를 확인합니다.
`Publisher count: 0`이면 펌웨어의 DDS publications 설정 및 PX4 내부 센서 출력을 확인해야 합니다.

### 통합 데이터 로깅 노드

각 노드와 별도 터미널에서 실행합니다. 실행마다 새로운 JSONL 파일을 생성합니다.

```bash
source install/setup.bash
ros2 run drone_integration data_logger_node --ros-args -p log_dir:=/home/jetson1/drone_integration_ws/results
# 수신 값을 터미널에도 출력하려면 -p print_values:=true 추가
```

기본 저장 경로는 `/home/jetson1/drone_integration_ws/results`이며 시작 로그에 실제 파일 경로를 표시합니다.
센서 수신기 5개 출력(모캡/IMU/자세/플로우/거리), 전처리 라이다, 항법 상태,
반평면, MPC 장애물/속도 명령, PX4 입력 4종 및 ACK/local position을 구독합니다.
각 줄에는 수신 ROS 시각 `received_ns`, 토픽, 메시지 타입, 모든 메시지 필드를 담습니다.
원본 헤더 시각도 그대로 보존합니다. NaN/Inf는 JSON 문자열 `"nan"`/`"inf"`/`"-inf"`로 저장합니다.
기본은 파일만 기록하며 1초마다 flush하고 정상 종료 시 닫습니다.

MPC는 `control/obstacles` (`ObstacleCircles`)에 스캔 시각, map ENU 중심 xy(m),
관측/안전 반지름(m), 용량 초과 여부를 발행합니다. 배열 번호는 추적 ID가 아닙니다.
유효한 스캔과 항법 시간 정렬에 성공하면 solver/용량 검사 전에 발행하므로 실패 상황의
장애물도 기록됩니다. 무효/오래된/빈 스캔에서는 발행하지 않으며, 무수신은 빈 공간을 뜻하지 않습니다.
MPC는 파일을 쓰지 않습니다.

일부 토픽만 저장하려면 목록을 지정합니다(위 기본 토픽 중 선택):

```bash
ros2 run drone_integration data_logger_node --ros-args \
  -p log_dir:=/home/jetson1/drone_integration_ws/results \
  -p 'topics:=[navigation/state, control/obstacles, control/velocity_cmd]'
```

로거는 best-effort 구독으로 센서/PX4 QoS와 호환됩니다. 높은 부하에서는 샘플이 누락될 수 있으며
다른 노드의 콘솔 로그, 서비스 호출, 내부 변수는 수집하지 않습니다.
메시지 인터페이스 추가 후 `colcon build --packages-select drone_interfaces drone_integration`으로 빌드하세요.

### 저장 로그 그래프 생성

ROS 환경을 source하지 않아도 실행됩니다. NumPy와 Matplotlib이 필요합니다.

```bash
python3 results/plot_logs.py                         # results의 최신 JSONL
python3 results/plot_logs.py results/drone_....jsonl  # 특정 로그
python3 results/plot_logs.py --at 10                 # 시작 후 10초에 가장 가까운 장애물/스캔
```

원본 로그 옆 `<파일명>_plots/`에 `overview.png`(궤적/고도/추정·명령 속도/yaw rate/상태),
`obstacles.png`(map 장애물 원과 body 라이다 점을 별도 좌표계로 표시)를 생성합니다.
IMU/거리/플로우가 있으면 `sensors.png`도 생성합니다. 출력 폴더는 `--output 경로`로 지정합니다.
장애물 주황 실선은 관측 반지름, 빨강 점선은 안전 반지름입니다.
스냅샷의 실제 시각과 요청 시각 차이를 표시하며, 수신되지 않은 토픽은 그래프에 `No data received`로 표시합니다.
기본 스냅샷은 마지막 장애물 시각에 맞추며, 장애물이 없으면 로그 마지막 시각을 사용합니다. 원본 헤더 시각이 있으면 사용하고,
없는 PX4 메시지는 수신 시각을 사용합니다. 기록 중 끊긴 JSON 줄은 경고 후 건너뜁니다.

### 미수신 값 및 장애물 거리 제한

로거는 1초마다 토픽 수신 여부를 검사합니다. 아직 수신하지 않았거나 마지막 수신 후
`missing_timeout`(기본 0.5초)이 지나면 해당 토픽을 `"missing": true, "data": {"value": "nan"}`으로
기록합니다. 정상 메시지는 `missing=false`이며 원래 필드를 그대로 저장합니다. 수신 재개 시
자동으로 정상 기록으로 돌아갑니다. 미수신 값은 plot에서 NaN으로 처리하며 장애물 0개로 취급하지 않습니다.
이 처리는 저장에만 적용하고 제어 노드의 센서 유효성/타임아웃 검사는 변경하지 않습니다.

MPC의 `obstacle_range`와 반평면의 `constraint_range` 기본값은 모두 2.0m입니다.
라이다 기체 기준점에서 2m 이내(경계 포함)의 점만 장애물 생성에 사용합니다.
전처리 라이다 원본 로그에는 기존 범위의 점을 계속 저장합니다.
스캔이 유효하지만 2m 이내 점이 없으면 장애물은 0개입니다. 무효/빈 스캔과 구분합니다.
원 피팅과 안전 반지름 확장 결과는 2m 밖으로 나갈 수 있습니다.
