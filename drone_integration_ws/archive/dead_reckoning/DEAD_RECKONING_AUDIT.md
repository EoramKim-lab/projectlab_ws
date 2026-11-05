# 데드레코닝 실행 차단 및 호환성 점검

점검일: 2026-11-01. 대상은 현재 소스, integration.yaml, 설치된 Python 코드, 저장 로그다. 비행/ARM/Offboard 명령은 보내지 않았다. 아래의 코드 경로와 로그 증거는 실제 하드웨어 원인 확정과 구분한다.

## 점검 후 반영한 수정

후속 요청으로 DR 기본값을 `strict_sensor_checks: false`로 변경했다. 이 모드에서는 프레임/입력 나이/자세 및 flow-range 시간차 게이트와 IMU 100ms 적분 상한을 해제하고 실제 양의 dt 전체를 적분한다. 아래의 100ms 누락 오류 설명은 엄격 모드에 해당한다. 입력 순서/유한값, 센서 freshness에 따른 출력 valid와 제어 watchdog은 유지한다. 자세한 현재 동작은 DEAD_RECKONING.md를 따른다.

아래 본문은 수정 전 점검 기록이다. 이후 IMU 예측 누락의 유효성 반영, 중복/역순 flow의 정상 상태 보존, PX4 시간 역행 후 수신 복구와 reset 이벤트를 구현했다. 시간 초기화 이벤트는 DR 원점/MPC 이력을 초기화하고 command를 OFF에 고정한다. 100ms 초과 IMU 누락은 DR에서 재시작 전까지 `imu_prediction_gap`으로 남는다. 센서 수신률 조건 자체를 완화하지 않았다.

진단 스크립트에는 자세/항법/PX4 local/status/충돌 제약/명령을, 로거에는 raw PX4 센서와 VehicleStatus/reset 이벤트를 추가했다. 실제 하드웨어 미수신과 펌웨어 일치 여부, 호버 시점의 목표 확정 방식, 측정 시각 동기화는 여전히 별도 검증/설계 항목이다. 사용 방법은 DEAD_RECKONING.md의 입력 오류와 재시작 절을 따른다.

수정 후 `colcon build --packages-select drone_integration` 통과. 오프라인 30개, DR 실제 메시지 7개, PX4 초기화 실제 메시지 3개, logger 3개, MPC 10개, experiment 4개로 총 57개 검사가 통과했다. ROS 노드 검사에서는 UDP 권한 오류가 계속 발생했으므로 이 결과는 DDS 전달 검증을 포함하지 않는다.

## 저장 로그에서 확인된 현재 차단

최신 파일 `results/drone_20261101T094804Z_2hf2wlk3.jsonl`:

- 항법 2,647개 중 2,408개가 `range,flow,flow_invalid,uninitialized`, 239개가 `imu,range,flow,flow_invalid,uninitialized`다. 정상 항법은 없다.
- `/sensors/flow`, `/sensors/range`, `/lidar/processed`, `/collision/halfplanes`, `/control/velocity_cmd`는 정상 메시지 없이 각각 missing 레코드 55개다. missing 레코드 개수는 센서 패킷 개수가 아니다.
- IMU 478개, 자세 10,767개가 기록되었다. IMU 헤더 간격 477개 중 216개가 100ms 초과, 중앙값 약 85.9ms, 최댓값 약 630ms다. 로거 샘플 누락 가능성이 있어 실제 추정기에 전달된 간격과 동일하다고 단정하지 않는다.
- PX4 local position은 기록되며 마지막 샘플의 `v_xy_valid`, `v_z_valid`는 모두 true다. 전체 구간의 유효성을 뜻하지 않는다.
- 이 로그는 raw flow/range를 저장하지 않아 미수신이 DDS 미출력, receiver 미실행, receiver 거부 중 어느 원인인지는 구분할 수 없다.

## 재현한 코드 문제

1. **IMU 예측 중단을 항법 valid에 반영하지 않음** — `navigation/estimator.py:38`, `navigation/navigation_node.py:135`. IMU를 accept한 뒤 predict의 dt가 100ms 초과이면 위치/속도 적분을 건너뛴다. 센서 freshness는 250ms라서 100~250ms 간격은 정상으로 표시될 수 있다. 150ms마다 센서를 주입한 재현에서 valid=true, v=[0.5,0,0]인데 열 번 동안 위치는 [0,0,1]에 머물렀다. 예측 성공/지연 상태를 별도 관리하고 샘플링 요구조건을 일치시켜야 한다.
2. **중복/역순 flow가 직전 정상 상태를 무효화** — `navigation/navigation_node.py:147`. accept 전에 flow_good=False로 바꾸므로 중복 한 개만 받아도 flow_invalid가 된다. 정상 feed 후 동일 타임스탬프 flow를 주입해 true→false를 재현했다. 중복은 상태 변경 없이 무시하고 실제 새 관측의 품질 실패와 분리해야 한다.
3. **PX4 재부팅/시간 되감기 후 수신 회복 경로 없음** — `common.py:50`. increasing은 이전 최댓값을 계속 유지한다. 10000000→1000→2000→3000을 입력하면 True,False,False,False다. 이전 uptime을 추월하거나 노드를 재시작하기 전까지 센서/status/local 입력이 막힐 수 있다. 재부팅을 검출한 안전한 상태 초기화가 필요하다.

## 항법 및 센서 조건 전체

4. **거리와 flow가 무조건 필수** — `navigation/dead_reckoning_node.py:30,48,52`. require_flow/require_range/use_range_height는 true로 고정이고 ground_z=0, attitude_source=px4다. YAML로 require_flow=false를 줘도 IMU 단독 모드가 되지 않는다. 첫 정상 거리 입력 전에는 initialized=false다. 모캡은 의도적으로 무시한다.
5. **정확한 frame, freshness, 자세 시간차 필수** — `navigation/navigation_node.py:87,97,169`, `common.py:47`. attitude는 map, 나머지는 base_link와 정확히 같아야 하고 stamp>0, age는 -50~250ms, 같은 센서 stamp는 증가해야 한다. IMU/range/flow와 가장 최근 attitude의 차이는 80ms 이하여야 한다. namespace가 다르면 내부 상대 토픽도 연결되지 않는다. 버퍼에서 맞는 자세를 찾거나 뒤늦은 자세로 재처리하지 않는다.
6. **기울기 제한 두 개가 다름** — `navigation/dead_reckoning_node.py:53`, `navigation/estimator.py:84`, `navigation/navigation_node.py:182`. range/flow 적용은 Rzz>=0.96(합성 기울기 약 16.26도), 항법 valid는 15도 이내다. 15~16.26도에서는 관측은 적용되어도 항법이 무효다. 제한은 파라미터화되지 않았다.
7. **IMU receiver의 조기 거부** — `sensor/px4_imu_receiver_node.py:20`. clipping 비트가 0이 아니거나 accel 상대시간이 INVALID이면 전체 IMU를 거부한다. 허용 마스크 밖 비트, 비유한 값, 중복/역순 timestamp도 거부한다. clipping 비정상 값만으로 메시지 불일치라고 확정할 수는 없다.
8. **flow 품질/회전 보정 필수** — `sensor/optical_flow_receiver_node.py:32`. quality>=100, 적분시간 0.1~200ms, pixel_flow와 delta_angle 전 성분이 finite여야 한다. delta_angle의 z만 NaN이어도 현재는 invalid다. raw SensorOpticalFlow는 모니터 전용이고 자동 대체하지 않는다.
9. **별도 하향 거리 필수** — `sensor/optical_flow_receiver_node.py:50`. orientation은 정확히 25, signal_quality!=0, 유한 거리와 min/max 범위를 요구한다. quality=-1(unknown)은 허용한다. CUSTOM 회전은 실제 하향이어도 거부한다. device_id를 설정하면 일치해야 한다. flow.distance_m만 있어도 range 토픽이 없으면 항법 초기화/유효화는 안 된다.
10. **flow 거리 대체 제한** — `navigation/navigation_node.py:150`. flow.distance_m이 비유한 값 또는 0 이하이면 최근 range가 필요하고 range/flow 시간차도 80ms 이하여야 한다. 별도 range는 250ms보다 자주 와야 항법 valid가 유지된다. flow의 유효 고도 범위/min_ground_distance/max_ground_distance는 검사하지 않는다.
11. **수신 시각을 측정 시각으로 사용** — PX4 IMU/attitude/flow/range receiver가 ROS now로 헤더를 만든다. raw PX4 시각은 순서 검사 등에만 쓰므로 지연된 새 샘플도 신선하게 보이고 실제 측정 시각 차이를 가릴 수 있다. IMU accel_relative_timestamp도 INVALID 여부 외에는 시간 정렬에 사용하지 않는다. 반면 LiDAR는 원본 stamp를 유지한다.

## MPC/Offboard 단계의 추가 차단

12. **데드레코닝으로 PX4 자체 EKF를 대체하지 않음** — `control/px4_command_node.py:106`. 내부 항법이 정상이어도 PX4 local position이 300ms 이내로 수신되고 v_xy_valid/v_z_valid가 true여야 명령 스트림을 시작한다. DR 결과를 PX4 vehicle_visual_odometry로 보내는 경로는 없다.
13. **LiDAR가 제어의 필수 입력** — `sensor/lidar_receiver_node.py:114`, `control/collision_constraints_node.py:27`, `control/mpc_node.py:151`. 드라이버를 별도로 실행해야 한다. 전처리 후 최소 3점, 유효하고 신선한 scan, body frame이 필요하다. 장애물이 없는 넓은 공간이라도 전처리 결과가 빈 스캔이면 막힌다. 반경 0.35+여유 0.20=0.55m 안쪽 점으로 origin_feasible=false가 되면 command가 막힌다.
14. **MPC 시간/용량/solver 조건** — `control/mpc_node.py:151`. scan/state 시간차<=80ms, 입력<=250ms, 계산 후에도 오래된 입력<=250ms여야 한다. 장애물 원이 8개 초과, solver 실패/비유한 출력이면 명령을 발행하지 않는다. 150ms MPC 주기와 scan 나이, 계산 시간을 합치면 250ms command timeout 여유가 줄어든다.
15. **짧은 오류도 스트림 OFF에 고정 가능** — `control/px4_command_node.py:63,156`. 스트림 중 readiness가 한 번이라도 실패하면 enabled=false/auto_phase=off로 고정된다. 센서 회복만으로 자동 재개하지 않는다. flow 중복 문제도 항법 invalid→MPC 중단→스트림 OFF로 전파될 수 있다.
16. **자동 전환 진입 조건** — `control/px4_command_node.py:69`. VehicleStatus가 2초 이내이고 armed이며 Hold/Position/Altitude 중 하나여야 한다. 다른 모드, 미시동, status 미수신이면 대기한다. 1.1초 stream 준비 후 요청하며 PX4 승인이 별도로 필요하다. 목표 시스템/컴포넌트 기본값은 1/1이고 PX4 토픽은 절대 경로라 다중 기체에는 remap/설정이 필요하다.
17. **전방 목표는 이륙/Offboard 시점이 아닌 첫 valid 항법 시점에 고정** — `control/mpc_node.py:128`. 지상에서 정상 range/flow가 들어오면 지상 위치/기수로 전방 6m 목표가 미리 확정된다. 그 후 수동 이륙하며 이동/회전해도 목표를 다시 잡지 않는다. 의도한 호버 위치에서 출발하려면 기준 확정 시점을 바꿔야 한다.

## 호환성 및 실행 구성

18. **PX4 메시지와 DDS 출력 일치 필요** — `config/px4_dds_additions.yaml`, 로컬 `src/px4_msgs/msg/`. receiver는 SensorCombined의 clipping/상대시간, VehicleOpticalFlow의 timestamp_sample/delta_angle/integration_timespan_us, SensorOpticalFlow, DistanceSensor orientation/quality 필드를 직접 참조한다. 실행 중 펌웨어/메시지 정의가 일치하는지는 이 workspace만으로 확인 불가다. raw flow만 DDS에 출력되어도 항법용 vehicle flow는 생기지 않는다. DDS fragment는 원본 publications에 병합하는 파일이며 sensor_combined/attitude/local/status를 모두 추가하는 완전한 파일이 아니다.
19. **Python/라이브러리/설치 overlay** — Humble 및 생성 메시지 경로는 Python 3.10이다. 다른 Python/ROS overlay에서는 import/type support 문제가 가능하다. CasADi/IPOPT는 MPC import/초기 warmup에 필요하며 DR 자체에는 불필요하다. setup.py에는 casadi가 있지만 package.xml에는 해당 의존성이 없으므로 rosdep만으로 준비 완료라고 볼 수 없다. 현재 src와 install의 패키지 Python 파일은 모두 동일해 오래된 설치 코드 문제는 발견되지 않았다.
20. **중복 항법 노드와 QoS** — 기존 navigation_node와 dead_reckoning_node가 동시에 navigation/state를 발행하면 정상/무효/다른 위치가 섞인다. 기본 PX4 입력은 BEST_EFFORT/VOLATILE, 내부 receiver 출력은 RELIABLE이어서 현재 조합에 명백한 QoS 불일치는 없다. 외부 best-effort publisher를 내부 토픽에 직접 연결하면 기본 reliable 구독과 호환되지 않을 수 있다.
21. **모델/장착 호환성** — 프레임 문자열만 같아도 실제 축이 같다는 보장은 없다. IMU는 FRD→FLU, 자세는 NED→ENU 변환하며 flow는 PX4가 body 정렬한 값이라는 전제다. 거리 센서 보어사이트는 body -z, 바닥은 평면 z=0, LiDAR 기본 yaw 보정은 pi다. 장착/flow 회전/거리 offset이 다르면 정상 valid여도 추정과 명령 방향이 틀릴 수 있다. 바이어스 추정, yaw 절대 보정, 수평 위치 절대 보정은 없다.

## 수행한 검증과 한계

- 오프라인 unittest 25개와 check_dead_reckoning_ros.py 4개 통과.
- 실제 생성 ROS 메시지를 사용하되 DDS 노드를 생성하지 않고 위 세 코드 문제 재현.
- src/install 패키지 Python 코드 내용 일치 확인.
- 현재 환경에서 UDP socket 생성이 Operation not permitted로 실패해 live DDS 진단은 실행 불가. 펌웨어 버전, raw 센서 실측, DDS 송수신과 실제 PX4 모드 승인은 미검증.
- 실기 호스트에서 ROS/workspace source 후 `python3 scripts/check_sensor_inputs.py --seconds 10` 실행으로 raw/변환 토픽 수신을 구분할 수 있다. 해당 스크립트에는 attitude/navigation/status 진단이 빠져 있으므로 이 세 토픽은 별도로 확인해야 한다.

우선순위: flow/range/LiDAR 미수신 원인 분리 → IMU 수신 간격과 거부 사유 확인 → 100ms 예측/valid 불일치 수정 → flow 중복 처리 수정 → PX4 재부팅 복구 처리 → 기준점 확정 시점과 전체 watchdog 지연 검증. 제한값을 일괄 완화하는 것으로 해결해서는 원인과 상태 오류가 가려진다.
