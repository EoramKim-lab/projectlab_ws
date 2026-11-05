"""Real ROS message serialization checks; no vehicle messages are published."""
import json
from pathlib import Path
import tempfile
import unittest
import rclpy
from sensor_msgs.msg import Range
from drone_interfaces.msg import ObstacleCircles
from drone_integration.data_logger_node import DataLoggerNode, TOPICS


class LoggerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        rclpy.init(args=['--ros-args', '-p', f'log_dir:={cls.directory.name}'])

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()
        cls.directory.cleanup()

    def test_complete_records_and_close(self):
        node = DataLoggerNode()
        try:
            self.assertEqual(len(list(node.subscriptions)), len(TOPICS))
            msg = Range()
            msg.header.stamp.sec = 123
            msg.range = float('nan')
            node.record('sensors/range', msg)
            circles = ObstacleCircles()
            circles.xy = [1., 2.]
            circles.radius = [.3]
            circles.safe_radius = [.85]
            node.record('control/obstacles', circles)
            node.flush()
            records = [json.loads(line) for line in node.log_path.read_text().splitlines()]
            self.assertEqual(records[0]['data']['header']['stamp']['sec'], 123)
            self.assertEqual(records[0]['data']['range'], 'nan')
            self.assertEqual(records[0]['topic'], '/sensors/range')
            self.assertGreater(records[0]['received_ns'], 0)
            self.assertEqual(records[1]['data']['xy'], [1., 2.])
            node.record('control/obstacles', circles)
            path = node.log_path
        finally:
            node.destroy_node()
        self.assertTrue(node.log_file.closed)
        self.assertEqual(len(path.read_text().splitlines()), 3)

    def test_missing_stale_and_recovered_topics(self):
        import time
        node = DataLoggerNode()
        try:
            node.record('sensors/range', Range())
            node.last_received['sensors/imu'] = time.monotonic() - 10
            node.check_missing()
            records = [json.loads(line) for line in node.log_path.read_text().splitlines()]
            missing = {r['topic']: r for r in records if r['missing']}
            self.assertNotIn('/sensors/range', missing)
            self.assertEqual(missing['/sensors/imu']['data']['value'], 'nan')
            self.assertEqual(missing['/control/obstacles']['data']['value'], 'nan')
            node.record('sensors/imu', __import__('sensor_msgs.msg', fromlist=['Imu']).Imu())
            node.check_missing()
            records = [json.loads(line) for line in node.log_path.read_text().splitlines()]
            self.assertFalse([r for r in records if r['topic'] == '/sensors/imu'][-1]['missing'])
        finally:
            node.destroy_node()

    def test_new_session_preserves_previous_file(self):
        first = DataLoggerNode()
        first_path = first.log_path
        first.destroy_node()
        second = DataLoggerNode()
        try:
            self.assertNotEqual(first_path, second.log_path)
            self.assertTrue(Path(first_path).exists())
        finally:
            second.destroy_node()

    def test_disarm_starts_real_report_worker(self):
        import time
        from px4_msgs.msg import VehicleStatus
        node = DataLoggerNode()
        try:
            status = VehicleStatus()
            status.arming_state = 2
            node.record('/fmu/out/vehicle_status_v1', status)
            status.arming_state = 1
            node.record('/fmu/out/vehicle_status_v1', status)
            self.assertEqual(len(node.report_jobs), 1)
            job, path = node.report_jobs[0]
            self.assertEqual(job.wait(timeout=45), 0,
                             (path.parent / 'report.log').read_text())
            for filename in ('flight.jsonl', 'flight_metadata.json',
                             'flight_plots.png', 'trajectory_world.png', 'lidar_obstacles.html', 'summary.json'):
                self.assertTrue((path.parent / filename).is_file(), filename)
        finally:
            node.destroy_node()


if __name__ == '__main__':
    unittest.main()
