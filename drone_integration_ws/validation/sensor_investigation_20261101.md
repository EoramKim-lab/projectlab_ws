> Historical investigation for the earlier PX4 v1.14 optical-flow / dead-reckoning profile. Current active configuration is PX4 v1.16 GPS/EKF2; see `../README.md`.

# 2026-11-01 센서 수신 조사

장애물 원 추출 범위는 MPC 기본값·YAML 모두 4m로 변경했다.
LiDAR 전처리 최대 범위는 기존 8m여서 4m 점들을 제공할 수 있다.

## 확인된 사실

저장 JSONL에서 변환 토픽의 실수신 레코드를 집계했다.
시각은 파일명 UTC를 KST로 변환한 값이다.

| 시작 KST | sensors/imu | sensors/attitude | sensors/flow | sensors/range | lidar/processed |
|---|---:|---:|---:|---:|---:|
| 18:03:36 | 45 | 1234 | 0 | 0 | 63 |
| 18:10:08 | 3974 | 89992 | 0 | 0 | 4593 |
| 18:48:04 | 478 | 10767 | 0 | 0 | 0 |

파일은 results/drone_20261101T090336Z_8qq5zikg.jsonl,
results/drone_20261101T091008Z_jbwk8y0t.jsonl,
results/drone_20261101T094804Z_2hf2wlk3.jsonl 이다.
이 로거는 raw PX4 센서 토픽을 기록하지 않았으므로 이 표만으로
미발행·DDS 미수신·수신기 거부를 구분할 수 없다.

Downloads/image.png의 optical_flow_receiver_node 모니터에서는 flow/raw_flow/range가
모두 WAITING이며, IMU에는 REJECTED gyro_clipping=176이 보인다.
flow 및 range 구독/품질 필터/QoS는 데드레코닝 전환 작업에서 변경하지 않았다.
기존 모캡 항법은 require_flow=false, require_range=false여서 이 입력 없이도
유효할 수 있었고, 새 항법은 두 입력을 모두 필수로 요구한다.

SensorCombined.msg의 clipping 축 비트는 1,2,4이므로 176은 정상 비트 조합이 아니다.
현재 src/px4_msgs는 PX4 v1.14.4 태그 기반이다. 주석을 제외한 필드 정의를 비교하면
현재 워크스페이스와 qendy_slam_ws, px4_verify_ws, 로컬 PX4-Autopilot,
PX4-v1.15.4의 SensorCombined/VehicleOpticalFlow/DistanceSensor는 일치한다.
따라서 단순히 로컬 px4_msgs 브랜치가 다르다고 단정할 수 없다.
실제 탑재 펌웨어의 정의와 DDS 직렬화 코드는 아직 확인되지 않았다.
잘못된 clipping 값을 무시하지 않고, invalid clipping bitmask로 구분해 출력하도록 했다.

로컬 펌웨어 소스의 DDS publication 목록도 서로 다르다:

- ~/PX4-Autopilot: sensor_combined, distance_sensor 출력 존재; vehicle_optical_flow 출력 없음.
- ~/PX4-v1.15.4: sensor_combined, sensor_optical_flow 출력 존재; vehicle_optical_flow와 distance_sensor 출력 없음.
- ~/PX4-v1.17: 세 필요한 출력 모두 존재하나 DistanceSensor 정의는 현재와 다름.

이는 로컬 파일에 대한 확인이며 실제 보드에 어떤 빌드가 탑재됐는지는 미확인이다.
현재 펌웨어에 vehicle_optical_flow/distance_sensor DDS 출력이 빠졌을 가능성이 있다.
config/px4_dds_additions.yaml은 참고용 조각이며 ROS YAML 로딩만으로 PX4 출력이 추가되지는 않는다.

## 남은 실기 확인

scripts/check_sensor_inputs.py는 raw 입력·변환 결과의 publisher 수, 수신률, 주요 값을
읽기 전용으로 출력한다. 작업 환경에서 실행하자 UDP socket 생성이 Operation not permitted로
거부되어 실제 ROS graph와 수신률은 조사할 수 없었다. 센서 고장으로 판정한 것은 아니다.
호스트 터미널에서 ROS와 현재 workspace를 source한 뒤 이 스크립트를 실행해야 한다.

PX4 콘솔에서 ver all, listener sensor_combined 1, listener vehicle_optical_flow 1,
listener distance_sensor 1, uxrce_dds_client status도 확인한다.
보드 uORB에는 값이 있고 ROS publisher가 없으면 탑재 빌드의 DDS export부터 확인한다.
ROS raw는 수신되는데 변환 값이 없으면 clipping/시간/quality/orientation 거부 조건을 확인한다.
IMU의 176이 raw에도 있으면 탑재 펌웨어·생성된 CDR·실제 로딩된 ROS 메시지 경로를 비교한다.
LiDAR는 /scan과 /lidar/processed를 비교해 드라이버와 전처리 노드 구간을 구분한다.
