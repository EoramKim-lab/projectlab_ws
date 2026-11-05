> Historical validation notes from the PX4 v1.14 / motion-capture / dead-reckoning iterations. They are retained for provenance and are not the active build or launch instructions. The current target is PX4 v1.16 + Gazebo Harmonic with GPS/EKF2 navigation. See `../README.md` and `../simulation/README.md`.

# 통합 초안 검증 — 2026-10-30

## 확인 결과

- ROS 2 Humble, 기존 `~/px4_verify_ws/install`의 px4_msgs를 사용했다. 실제 펌웨어와 메시지 정의 일치는 확인하지 못했다.
- `drone_interfaces`, `drone_integration`: colcon symlink 빌드 성공.
- `sllidar_ros2`: 빌드 성공. SDK의 zero-size array/unused/sign-compare 컴파일 경고 있음. 장치 실행은 미검증.
- 기존 unittest: 20/20 통과.
- integration launch: 8개 노드 기동, 제한 시간 내 시작 중 Python 예외 없음. `launch.log` 참고.
- 제한 시간 종료 시 SIGINT가 프로세스 그룹과 launch에서 중복 전달되어 일부 종료 과정에 KeyboardInterrupt가 기록됨. 정상 운영 종료 검증은 아님.
- 요청한 `~/Projectlab/qendy_slam_ws/optical_flow_test/optical_flow_test.py`를 변경 없이 실행했다. 이 코드는 PX4 토픽을 진단하는 구독기이다.
- `check_flow.py`: 원본 진단 노드를 import하여 합성 입력으로 실행. 통합 수신기의 실제 ROS 메시지 직렬화, 시간 단위 변환, 중복 거부, 저품질/NaN gyro 무효화 통과. `flow_callback.log` 참고.
- 실행 샌드박스가 DDS UDP 소켓 생성을 `Operation not permitted`로 차단했다. 실제 토픽 미수신을 센서 고장으로 판단할 수 없다. 위 콜백 검사는 DDS 전달을 검증하지 않는다.
- MPC는 빈 구현이므로 자율 주행/충돌회피/속도 추종 동작은 검증 대상 구현이 없다.
- 실기 arm, offboard 요청, 비행 명령은 수행하지 않았다.

## 재현

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash
source ~/px4_verify_ws/install/setup.bash
source install/setup.bash
PYTHONPATH=src/drone_integration python3 -m unittest discover -s tests -v
python3 validation/check_flow.py
```

## 네트워크 제한이 없는 호스트 터미널에서 남은 확인

위 환경을 source한 터미널에서 원본 진단 코드를 실행한다.

```bash
python3 ~/Projectlab/qendy_slam_ws/optical_flow_test/optical_flow_test.py
```

별도 터미널에서 같은 환경을 source하고 통합 launch를 실행한다.
기본 설정은 모캡을 PX4로 전달하므로, 모캡 발행 전 좌표 보정을 확인해야 한다.

```bash
ros2 launch drone_integration integration.launch.py
ros2 topic echo /sensors/flow
ros2 topic echo /sensors/range
ros2 topic echo /navigation/state
ros2 topic echo /collision/halfplanes
```

플로우뿐 아니라 모캡·IMU·자세·하향 거리·라이다 입력이 필요하다.
진단 출력 수신률/quality/거리와 `/sensors/flow.valid`, 항법 `valid/reason`을 함께 확인한다.
명령 enable 서비스와 offboard 요청은 센서 수신 검증에 필요하지 않다.

## PX4 v1.14.4 메시지 적용 (2026-11-01)

현재는 `src/px4_msgs`에 PX4-Autopilot v1.14.4 태그의 메시지 184개를 포함합니다.
위의 이전 검증에서 사용한 `px4_verify_ws` 메시지는 더 이상 source할 필요가 없습니다.
현재 실행은 `/opt/ros/humble/setup.bash`와 이 워크스페이스 `install/setup.bash`를 사용합니다.
출처와 파일 해시는 `src/px4_msgs/PX4_SOURCE.json`에 기록했습니다.

적용 후 `px4_msgs`·`drone_integration` 빌드를 통과했고, 다른 워크스페이스의 underlay를
제외한 환경에서 `ros2 pkg prefix px4_msgs`가 이 워크스페이스의 `install/px4_msgs`임을 확인했습니다.
새 메시지로 센서·더미 검사 4개, 모캡 항법 검사 3개, 로거 검사 3개를 통과했습니다.
VehicleCommand/ACK/LocalPosition/OffboardControlMode/TrajectorySetpoint 생성도 확인했습니다.
검사는 실제 ROS 메시지의 로딩·콜백 검사이며, 네트워크 소켓 제한으로 실기 DDS 연결은 미검증입니다.
