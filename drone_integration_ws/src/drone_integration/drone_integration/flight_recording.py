"""ROS-independent armed/disarmed flight log segmentation."""
import json
from pathlib import Path


class FlightRecording:
    def __init__(self, session_path, finished, scene=None):
        self.session_path = Path(session_path)
        self.finished = finished
        self.scene = scene
        self.file = None
        self.number = 0

    def record(self, record):
        status = (record['topic'].endswith('/vehicle_status_v1')
                  and not record.get('missing'))
        armed = record['data'].get('arming_state') if status else None
        if armed == 2 and self.file is None:
            self.number += 1
            self.directory = self.session_path.with_suffix('') / f'flight_{self.number:03d}'
            self.directory.mkdir(parents=True, exist_ok=True)
            self.path = self.directory / 'flight.jsonl'
            self.file = self.path.open('w', encoding='utf-8')
            if self.scene is not None:
                self.path.with_suffix('.scene.json').write_text(json.dumps(self.scene, indent=2))
        if self.file is not None:
            self.file.write(json.dumps(record, allow_nan=False) + '\n')
            if armed == 1:
                self.close('disarmed')

    def flush(self):
        if self.file is not None:
            self.file.flush()

    def close(self, reason='logger_stopped_while_armed'):
        if self.file is None:
            return
        self.file.close()
        self.file = None
        (self.directory / 'flight_metadata.json').write_text(json.dumps({
            'end_reason': reason,
            'complete': reason == 'disarmed',
            'start': 'first observed armed status; takeoff may precede logger startup',
        }, indent=2) + '\n', encoding='utf-8')
        self.finished(self.path)
