# Qualisys 모캡 토픽 수신

첨부 `UAM_테스트실.pdf` 3–4쪽의 MOCAP4ROS2 방식으로 구성했습니다.
테스트실 프로젝트 폴더, Crazyflie, RViz, PX4 제어 설정 없이 QTM 토픽만 수신합니다.

## 현재 적용 상태

- 이 워크스페이스에 `qualisys_mocap_bringup` 설정/launch 패키지를 추가했습니다.
- ROS 2 Humble에서 해당 패키지의 colcon 빌드와 launch 인자 로딩을 확인했습니다.
- upstream 드라이버와 메시지는 `config/qualisys.repos`에 지정했습니다.
- 사용자가 제공한 드라이버 ZIP을 `src/mocap4ros2_qualisys`에 적용했습니다.
- SDK master ZIP을 `vendor/qualisys_cpp_sdk`에 적용하고 SDK 단독 CMake 빌드를 통과했습니다.
- 드라이버는 로컬 SDK를 우선 사용하도록 수정했습니다. SDK master와의 실제 QTM 통신은 아직 미검증입니다.
- 사용자가 제공한 `mocap4r2_msgs-rolling.zip`을 `src/mocap_msgs`에 적용했습니다.
- 시스템 의존성은 `rosdep check`로 충족됨을 확인했습니다.
- ROS 2 Humble에서 메시지·드라이버·bringup 3개 패키지 빌드, launch 인자 로딩,
  메시지 인터페이스 조회와 실행 파일의 공유 라이브러리 연결을 확인했습니다.
- 실제 QTM 연결과 장비 토픽 수신은 현장에서 확인해야 합니다.
- localhost 기동 점검에서 노드의 설정 로딩과 configure 전환을 확인했습니다.
  이 작업 환경은 네트워크 소켓 권한이 제한되어 DDS 통신 오류가 발생했고,
  QTM이 없는 localhost 대상 activate는 연결 실패로 종료되었습니다.

## 다시 빌드하기 (현재 ZIP 소스 사용, 인터넷 불필요)

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select mocap4r2_msgs qualisys_driver qualisys_mocap_bringup --cmake-args -DBUILD_TESTING=OFF
```

## 새 환경에서 의존성까지 설치하기

```bash
cd ~/drone_integration_ws
bash scripts/setup_qualisys.sh
```

스크립트는 드라이버/메시지 소스를 `src`로 가져와 rosdep 의존성을 설치하고
`mocap4r2_msgs`, `qualisys_driver`, `qualisys_mocap_bringup`만 빌드합니다.
시스템 의존성 설치에 sudo 인증이 필요할 수 있습니다. rosdep 초기화가 안 된 PC라면
`sudo rosdep init`을 한 번 실행한 뒤 `rosdep update`를 실행하세요.
현재는 사용자가 제공한 로컬 SDK를 사용합니다. 로컬 SDK가 없으면
upstream CMake가 `rt_protocol_1.23` 태그를 자동으로 내려받습니다.
SDK를 `/usr/lib`에 직접 복사할 필요가 없습니다.

저장소는 upstream에서 제공하는 `rolling` 소스를 지정했습니다. 이는 ROS 배포판을
Rolling으로 바꾸는 설정이 아닙니다. 현재 적용한 ZIP 파일의 SHA256과 로컬 수정 사항은
`vendor/QUALISYS_SOURCES.md`에 기록했습니다. ZIP에는 Git 커밋 메타데이터가 없습니다.

## 실행

QTM PC와 Jetson을 같은 네트워크에 연결하고 QTM에서 캡처와 6DOF rigid body 추적을
준비합니다. QTM의 RT protocol 통신을 허용하고 방화벽도 확인하세요.
`host_name`에는 **카메라나 Jetson IP가 아닌 QTM이 실행 중인 Windows PC의 IPv4**를 넣습니다.
문서의 `192.168.253.1`을 QTM PC의 주소라고 단정하지 않았습니다.
현재 사용자 제공 주소는 QTM PC `192.168.0.34`, Jetson `192.168.0.32`이며 모두 무선 LAN입니다.
launch의 기본 QTM 주소를 `192.168.0.34`로 반영했습니다.
두 장치의 서브넷 마스크가 `255.255.255.0`이면 같은 서브넷입니다.
무선 AP의 클라이언트 격리와 Windows 방화벽이 장치 간 QTM 통신을 막지 않아야 합니다.
이 설정은 OS 네트워크 주소를 자동 변경하지 않습니다.

```bash
cd ~/drone_integration_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch qualisys_mocap_bringup qualisys.launch.py
# 주소 변경 시: host_name:=새_QTM_PC_IP
```

포트 기본값은 `22222`이며 변경 시 `port:=22222` 인자로 지정합니다.
추가 설정은 `src/qualisys_mocap_bringup/config/qualisys.yaml`을 수정한 뒤 다시 빌드하거나
`config:=/절대경로/설정.yaml`로 지정합니다. `host_port`가 아니라 `port`를 사용합니다.
기본 요청 주기는 100 Hz이며 실제 수신 속도는 QTM과 네트워크에 따라 달라집니다.

다른 터미널에서도 위 두 setup 파일을 source한 뒤 확인합니다.

```bash
ros2 lifecycle get /qualisys_driver_node
ros2 topic list -t
ros2 topic echo /mocap/rigid_bodies --qos-reliability best_effort
ros2 topic hz /mocap/rigid_bodies
```

정상 연결 시 lifecycle 상태는 `active`이고 주요 출력은 다음과 같습니다.

| 토픽 | 메시지 | 내용 |
|---|---|---|
| `/mocap/rigid_bodies` | `mocap4r2_msgs/msg/RigidBodies` | 이름별 강체 위치(m), 자세 |
| `/mocap/markers` | `mocap4r2_msgs/msg/Markers` | 마커 위치(m) |

강체 목록은 메시지의 `rigidbodies` 필드에서 확인합니다.
현재 upstream은 수신 시각을 ROS header stamp에 사용합니다.

## 기존 드론 노드와의 연결 범위

이번 launch는 원본 모캡 수신만 실행합니다. `drone_integration`의 `mocap_receiver_node`가
`/mocap/rigid_bodies`에서 강체를 선택하고 좌표를 보정하여 `sensors/mocap_pose`로 발행합니다.
항법·MPC 연결과 개별 실행 명령은 [REAL_NAVIGATION.md](REAL_NAVIGATION.md)를 참고하세요.

## 참고

- [문서에 지정된 공식 드라이버](https://github.com/MOCAP4ROS2-Project/mocap4ros2_qualisys)
- [실제 파라미터와 출력 토픽 구현](https://github.com/MOCAP4ROS2-Project/mocap4ros2_qualisys/blob/rolling/qualisys_driver/src/qualisys_driver.cpp)
- [Qualisys SDK](https://github.com/qualisys/qualisys_cpp_sdk)
