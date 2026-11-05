# PX4 NED / FRD 전환 검증 (2026-11-02)

운용 명령과 좌표 규약은 [DEAD_RECKONING.md](../DEAD_RECKONING.md)에 정리했습니다.

## 변경 범위

- IMU specific force와 각속도는 PX4 FRD 값을 유지합니다. 자세는 FRD→NED 회전을 유지하고 wxyz→xyzw 순서만 바꿉니다.
- 항법은 NED 중력 +9.80665, 지면 위 음수 z, FRD optical-flow 속도를 사용합니다.
- MPC와 장애물 월드 좌표는 NED입니다. 평면 회전행렬의 수식은 유지되며 양의 yaw는 북→동, 오른쪽 회전입니다.
- 충돌 제약과 라이다 점은 FRD입니다. 기본 장착은 뒤집힘, 드라이버 inverted=false, yaw_offset=0입니다.
- PX4 velocity/yawspeed 출력의 ENU 변환을 제거했습니다.
- 기본 프레임은 map_ned / base_link_frd입니다. 메시지 설명, 설정, 모니터 출력, 기존 테스트를 갱신했습니다.
- 고정 목표는 기존 물리 방향을 보존하도록 ENU (6,0,1) → NED (0,6,-1)로 바꿨습니다. 기본 전방 목표는 초기 기수 방향 6m로 유지합니다.

## 테스트 결과

| 검사 | 통과 수 |
|---|---:|
| unittest discover: test_*.py (수치·명령 mock·시계) | 40 |
| check_dead_reckoning_ros.py | 13 |
| check_optical_distance_ros.py | 7 |
| check_px4_reset_ros.py | 3 |
| check_logger_ros.py | 3 |
| check_mpc_ros.py | 13 |
| check_experiment_ros.py | 1 |
| 합계 | 80 |

방향 회귀 검증에는 임의 자세 보존, 기울어진 정지 기체의 중력 제거,
동쪽 기수에서 오른쪽 flow/장애물의 남쪽 변환, 라이다 우측 반평면,
상승·하강·고도 유지, NED 속도와 양/음 yaw-rate의 PX4 전달,
기존 map/base_link 명령·스캔 거부가 포함됩니다.

ROS 노드 생성 테스트는 ROS_DOMAIN_ID=173, ROS_LOCALHOST_ONLY=1로 격리했습니다.
센서/항법 테스트는 실제 생성된 메시지로 콜백을 호출하고, MPC 테스트는 실제 CasADi/Ipopt를 실행합니다.
PX4 출력 검증은 캡처 또는 mock이며 실제 기체에 ARM/Offboard/비행 명령을 보내지 않았습니다.
실제 센서→DDS→제어의 전체 전달, 라이다 0° 장착 정렬, 비행 성능은 이 테스트로 검증하지 않았습니다.

재현 시 ROS 및 workspace 환경을 source하고 OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1을 사용합니다.
ROS 노드 생성 테스트는 실제 운용과 다른 ROS 도메인에서 실행합니다.
