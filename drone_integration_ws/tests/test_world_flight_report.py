import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from drone_integration.world_scene import ned_to_enu,snapshot_world
from drone_integration.flight_recording import FlightRecording
from drone_integration.flight_report import render

SDF='''<sdf version="1.9"><world name="test"><model name="obstacle"><static>true</static><pose>10 20 0 0 0 1.5707963267948966</pose><link name="wall"><pose>1 0 0 0 0 0</pose><collision name="box"><pose>0 2 1 0 0 0</pose><geometry><box><size>2 4 2</size></box></geometry></collision></link></model></world></sdf>'''
class WorldFlightReportTests(unittest.TestCase):
    def test_ned_enu_translation_and_height(self):
        np.testing.assert_allclose(ned_to_enu([[1,2,-3]],[10,20,30]),[[12,21,33]])
        np.testing.assert_allclose(ned_to_enu([[1,2]],[10,20,30]),[[12,21]])
        with self.assertRaises(ValueError):ned_to_enu([[0,0]],[float('nan'),0,0])

    def test_rotated_model_link_collision_composition(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'world.sdf';p.write_text(SDF);scene=snapshot_world(p)
            points=np.array(scene['shapes'][0]['points'])
            np.testing.assert_allclose(points.min(axis=0),[6,20])
            np.testing.assert_allclose(points.max(axis=0),[10,22])
            self.assertEqual(scene['shapes'][0]['z_min'],0)
            self.assertEqual(scene['shapes'][0]['z_max'],2)

    def test_flight_copies_snapshot_before_world_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'world.sdf';p.write_text(SDF);scene=snapshot_world(p)
            writer=FlightRecording(Path(directory)/'session.jsonl',lambda path:None,scene)
            writer.record(dict(topic='/fmu/out/vehicle_status_v1',data={'arming_state':2},received_ns=1))
            path=writer.path;writer.close();p.write_text(SDF.replace('10 20','100 200'))
            self.assertEqual(json.loads(path.with_suffix('.scene.json').read_text()),scene)
            self.assertNotEqual(snapshot_world(p)['source_sha256'],scene['source_sha256'])

    def test_report_converts_reference_scan_and_detection_and_writes_html(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);world=root/'world.sdf';world.write_text(SDF)
            path=root/'flight.jsonl';scene=snapshot_world(world,[10,20,3]);path.with_suffix('.scene.json').write_text(json.dumps(scene))
            header=dict(stamp=dict(sec=1,nanosec=0),frame_id='map_ned')
            nav=dict(header=header,valid=True,pose=dict(position=dict(x=1,y=2,z=-1),orientation=dict(x=0,y=0,z=0,w=1)),twist=dict(linear=dict(x=0,y=0,z=0)))
            reference=dict(header=header,poses=[dict(position=dict(x=0,y=0,z=-1)),dict(position=dict(x=0,y=24,z=-1))])
            scan=dict(header=dict(stamp=dict(sec=1,nanosec=0),frame_id='base_link_frd'),valid=True,xy=[1,0])
            obstacle=dict(header=header,xy=[3,4],radius=[.3],safe_radius=[.8])
            records=[dict(topic=topic,received_ns=1000000000,data=data) for topic,data in [('/navigation/state',nav),('/control/reference',reference),('/lidar/processed',scan),('/control/obstacles',obstacle)]]
            path.write_text('\n'.join(map(json.dumps,records)))
            output=render(path,max_frames=2)
            html=(output/'lidar_obstacles.html').read_text();payload=json.loads(html.split('const data=',1)[1].split(';\nconst seek=',1)[0])
            np.testing.assert_allclose(payload['references'][0],[[10,20],[34,20]])
            np.testing.assert_allclose(payload['frames'][0]['drone'],[12,21])
            np.testing.assert_allclose(payload['frames'][0]['world'],[[12,22]])
            np.testing.assert_allclose(payload['frames'][0]['obstacles'][0]['center'],[14,23])
            self.assertEqual(len(payload['shapes']),1)
            self.assertTrue((output/'trajectory_world.png').exists())
            self.assertFalse((output/'lidar_obstacles.gif').exists())
            self.assertIn('seek.oninput',html);self.assertIn('play.onclick',html)
            # Legacy logs never silently borrow today's world geometry.
            path.with_suffix('.scene.json').unlink()
            legacy=render(path,root/'legacy',max_frames=2)
            summary=json.loads((legacy/'summary.json').read_text())
            self.assertIsNone(summary['world_scene'])

if __name__=='__main__':unittest.main()
