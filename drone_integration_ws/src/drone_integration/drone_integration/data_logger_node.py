"""Subscribe to pipeline outputs and write one complete message per JSONL record."""
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import tempfile
import time
import subprocess
import sys
from rosidl_runtime_py.convert import message_to_ordereddict
from rosidl_runtime_py.utilities import get_message
from rclpy.qos import QoSProfile, ReliabilityPolicy
from .common import Base, run
from .flight_recording import FlightRecording
from .world_scene import snapshot_world


TOPICS = {
    '/scan': 'sensor_msgs/msg/LaserScan',
    'sensors/imu': 'sensor_msgs/msg/Imu',
    'sensors/attitude': 'geometry_msgs/msg/QuaternionStamped',
    'sensors/flow': 'drone_interfaces/msg/FlowMeasurement',
    'sensors/range': 'sensor_msgs/msg/Range',
    'sensors/px4_reset': 'std_msgs/msg/Empty',
    'navigation/reset': 'std_msgs/msg/Empty',
    'lidar/processed': 'drone_interfaces/msg/ProcessedScan',
    'navigation/state': 'drone_interfaces/msg/NavigationState',
    'collision/halfplanes': 'drone_interfaces/msg/Halfplanes',
    'control/obstacles': 'drone_interfaces/msg/ObstacleCircles',
    'control/velocity_cmd': 'geometry_msgs/msg/TwistStamped',
    'control/reference': 'geometry_msgs/msg/PoseArray',
    '/fmu/in/vehicle_visual_odometry': 'px4_msgs/msg/VehicleOdometry',
    '/fmu/in/offboard_control_mode': 'px4_msgs/msg/OffboardControlMode',
    '/fmu/in/trajectory_setpoint': 'px4_msgs/msg/TrajectorySetpoint',
    '/fmu/in/vehicle_command': 'px4_msgs/msg/VehicleCommand',
    '/fmu/out/vehicle_command_ack': 'px4_msgs/msg/VehicleCommandAck',
    '/fmu/out/vehicle_local_position': 'px4_msgs/msg/VehicleLocalPosition',
    '/fmu/out/vehicle_gps_position': 'px4_msgs/msg/SensorGps',
    '/fmu/out/estimator_status_flags': 'px4_msgs/msg/EstimatorStatusFlags',
    '/fmu/out/vehicle_global_position': 'px4_msgs/msg/VehicleGlobalPosition',
    '/fmu/out/vehicle_status_v1': 'px4_msgs/msg/VehicleStatus',
    '/fmu/out/sensor_combined': 'px4_msgs/msg/SensorCombined',
    '/fmu/out/vehicle_attitude': 'px4_msgs/msg/VehicleAttitude',
    '/fmu/out/vehicle_optical_flow': 'px4_msgs/msg/VehicleOpticalFlow',
    '/fmu/out/sensor_optical_flow': 'px4_msgs/msg/SensorOpticalFlow',
    '/fmu/out/distance_sensor': 'px4_msgs/msg/DistanceSensor',
}


def json_values(value):
    """Keep nonfinite sensor values explicit while producing standard JSON."""
    if isinstance(value, dict):
        return {key: json_values(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_values(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)  # "nan", "inf", "-inf"
    return value


class DataLoggerNode(Base):
    def __init__(self):
        super().__init__('data_logger_node')
        directory = Path(self.param('log_dir', '/home/jetson1/drone_integration_ws/results')).expanduser().resolve()
        self.print_values = self.param('print_values', False)
        self.missing_timeout = self.param('missing_timeout', 0.5)
        if not math.isfinite(self.missing_timeout) or self.missing_timeout <= 0:
            raise ValueError('missing_timeout must be finite and positive')
        selected = self.param('topics', list(TOPICS))
        self.auto_report = self.param('auto_flight_report', True)
        if self.auto_report and '/fmu/out/vehicle_status_v1' not in selected:
            selected = list(selected) + ['/fmu/out/vehicle_status_v1']
        self.report_jobs = []
        self.last_received = dict.fromkeys(selected)
        unknown = set(selected) - TOPICS.keys()
        if unknown:
            raise ValueError(f'Unknown logger topics: {sorted(unknown)}')
        # Resolve types before creating a file, so missing dependencies fail clearly.
        types = {topic: get_message(TOPICS[topic]) for topic in selected}
        directory.mkdir(parents=True, exist_ok=True)
        prefix = datetime.now(timezone.utc).strftime('drone_%Y%m%dT%H%M%SZ_')
        self.log_file = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                                  prefix=prefix, suffix='.jsonl',
                                                  dir=directory, delete=False)
        self.log_path = Path(self.log_file.name)
        scene = None
        world_sdf = self.param('report_world_sdf', '')
        origin = self.param('ned_origin_enu', [0.0, 0.0, 0.0])
        if world_sdf:
            try:
                scene = snapshot_world(world_sdf, origin)
                self.log_path.with_suffix('.scene.json').write_text(json.dumps(scene, indent=2))
            except Exception as exc:
                self.get_logger().error(f'World snapshot unavailable: {exc}; flight logging continues')
        self.flight = FlightRecording(self.log_path, self.generate_report, scene)
        qos = QoSProfile(depth=100, reliability=ReliabilityPolicy.BEST_EFFORT)
        for topic, msg_type in types.items():
            self.create_subscription(msg_type, topic,
                                     lambda msg, topic=topic: self.record(topic, msg), qos)
        self.create_timer(1.0, self.check_missing)
        self.get_logger().info(f'Recording {len(types)} topics to {self.log_path}')

    def record(self, topic, msg):
        self.last_received[topic] = time.monotonic()
        self.write_record(topic, json_values(message_to_ordereddict(msg)))

    def write_record(self, topic, data, missing=False):
        record = {'received_ns': self.get_clock().now().nanoseconds,
                  'topic': self.resolve_topic_name(topic), 'type': TOPICS[topic],
                  'missing': missing, 'data': data}
        line = json.dumps(record, ensure_ascii=False, allow_nan=False)
        try:
            self.log_file.write(line + '\n')
            if self.auto_report:
                self.flight.record(record)
        except OSError as exc:
            self.get_logger().fatal(f'Log write failed: {exc}')
            raise
        if self.print_values:
            self.get_logger().info(line)

    def check_missing(self):
        for job, path in list(self.report_jobs):
            result = job.poll()
            if result is not None:
                self.report_jobs.remove((job, path))
                if result == 0:
                    self.get_logger().info(f'Flight report saved: {path.parent}')
                else:
                    self.get_logger().error(f'Flight report failed ({result}): {path.parent / "report.log"}')
        now = time.monotonic()
        for topic, received in self.last_received.items():
            if received is None or now - received > self.missing_timeout:
                self.write_record(topic, {'value': 'nan'}, missing=True)
        self.flush()

    def flush(self):
        self.log_file.flush()
        self.flight.flush()

    def generate_report(self, path):
        # Rendering must never block the flight logger or the control loop.
        try:
            with (path.parent / 'report.log').open('w') as report_log:
                job = subprocess.Popen(
                    [sys.executable, '-m', 'drone_integration.flight_report',
                     str(path), '--output', str(path.parent)],
                    stdout=report_log, stderr=subprocess.STDOUT, start_new_session=True)
            self.report_jobs.append((job, path))
            self.get_logger().info(f'Generating flight report: {path.parent}')
        except OSError as exc:
            self.get_logger().error(f'Could not start flight report: {exc}; log saved at {path}')

    def destroy_node(self):
        if hasattr(self, 'log_file'):
            self.flight.close()
            self.log_file.close()
        return super().destroy_node()


def main(args=None):
    run(DataLoggerNode, args)
