# Local Qualisys sources

Imported from user-provided GitHub ZIPs on 2026-10-31:

| Archive | SHA256 | Destination |
|---|---|---|
| mocap4ros2_qualisys-rolling.zip | 69d975c9f15ea84bb880054d120879c82379ea176ac20e21c9a662135dee61c0 | src/mocap4ros2_qualisys |
| qualisys_cpp_sdk-master.zip | 93d98ed021eb074412502a046c4981aadba2b6380368c10f7c1218ae993509ba | vendor/qualisys_cpp_sdk |
| mocap4r2_msgs-rolling.zip | 1785cb2ebd10f2d4b971c6da2d4b460c449459cfa9a086dd124e754ee19c396b | src/mocap_msgs |

Local driver changes: prefer the workspace SDK via FetchContent's source override;
correct upstream YAML's `host_port` key to `port`.
SDK master is used as supplied rather than upstream's recommended rt_protocol_1.23 tag.
The master SDK and driver build together on ROS 2 Humble; real QTM reception remains unverified.
The SDK is built inside the driver; vendor/COLCON_IGNORE prevents duplicate colcon discovery.
