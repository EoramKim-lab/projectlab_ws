import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from drone_integration.flight_recording import FlightRecording
from drone_integration.flight_report import recent, to_world, load_records, reference_segments


class FlightReportTests(unittest.TestCase):
    def test_reference_uses_recorded_segment_and_deduplicates(self):
        data = {'header': {'frame_id': 'map_ned'}, 'poses': [
            {'position': dict(x=1., y=2., z=-1.)},
            {'position': dict(x=1., y=8., z=-1.)}]}
        records = [(1., data), (2., data),
                   (3., {'header': {'frame_id': 'map_ned'}, 'poses': []})]
        result = reference_segments(records, [[0,0,-1], [0,6,-1]])
        self.assertEqual(len(result), 1)
        np.testing.assert_allclose(result[0], [[1,2,-1], [1,8,-1]])

    def test_legacy_reference_requires_explicit_fallback(self):
        self.assertEqual(reference_segments([]), [])
        result = reference_segments([], [[0,0,-1], [0,6,-1]])
        np.testing.assert_allclose(result[0], [[0,0,-1], [0,6,-1]])
        with self.assertRaises(ValueError):
            reference_segments([], [[0,0,float('nan')], [0,6,-1]])

    def status(self, state, missing=False):
        return dict(topic='/fmu/out/vehicle_status_v1', data={'arming_state': state},
                    missing=missing, received_ns=1000000000)

    def test_two_flights_and_shutdown(self):
        with tempfile.TemporaryDirectory() as directory:
            completed = []
            writer = FlightRecording(Path(directory)/'session.jsonl', completed.append)
            writer.record(self.status(1))
            self.assertIsNone(writer.file)
            writer.record(self.status(2))
            writer.record(self.status(2))
            writer.record(self.status(1, missing=True))
            self.assertFalse(completed)
            writer.record(self.status(1))
            self.assertEqual(len(completed), 1)
            self.assertEqual(len(completed[0].read_text().splitlines()), 4)
            self.assertTrue(json.loads((completed[0].parent/'flight_metadata.json').read_text())['complete'])
            writer.record(self.status(1))
            writer.record(self.status(2))
            writer.close()
            writer.close()
            self.assertEqual(len(completed), 2)
            self.assertNotEqual(completed[0], completed[1])
            self.assertFalse(json.loads((completed[1].parent/'flight_metadata.json').read_text())['complete'])

    def test_alignment_never_uses_future_or_stale_data(self):
        items = [(1., 'a'), (2., 'b')]
        self.assertIsNone(recent(items, [1.,2.], .9))
        self.assertIsNone(recent(items, [1.,2.], 1.5))
        self.assertEqual(recent(items, [1.,2.], 2.1), 'b')

    def test_rotation_translation(self):
        nav = {'pose': {'orientation': dict(x=0.,y=0.,z=2**-.5,w=2**-.5),
                        'position': dict(x=10.,y=20.,z=0.)}}
        np.testing.assert_allclose(to_world(np.array([[1.,0.]]), nav), [[10.,21.]])

    def test_truncated_json_and_source_timestamp(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'log.jsonl'
            record = {'topic':'/lidar/processed', 'received_ns':9000000000,
                      'data': {'header': {'stamp': {'sec': 5, 'nanosec':0}}, 'xy': []}}
            path.write_text(json.dumps(record)+'\n{"truncated":')
            series, malformed = load_records(path)
            self.assertEqual(malformed, 1)
            self.assertEqual(series['/lidar/processed'][0][0], 5.)


if __name__ == '__main__':
    unittest.main()
