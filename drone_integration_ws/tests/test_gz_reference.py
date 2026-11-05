"""Offline checks; source ROS and the workspace before running."""
import unittest
from geometry_msgs.msg import Pose
from gz.msgs10.marker_pb2 import Marker
from drone_integration.gz_reference_node import reference_markers


class ReferenceTests(unittest.TestCase):
    def test_ned_segment_and_origin(self):
        start, goal = Pose(), Pose()
        start.position.z = goal.position.z = -1.0
        goal.position.y = 6.0
        markers = reference_markers([start, goal], [10., 20., .2]).marker
        self.assertEqual(len(markers), 3)
        points = markers[0].point
        self.assertEqual((points[0].x, points[0].y, points[0].z), (10., 20., 1.2))
        self.assertEqual((points[1].x, points[1].y, points[1].z), (16., 20., 1.2))
        self.assertEqual(markers[2].pose.position, points[1])
        self.assertTrue(all(m.visibility == Marker.GUI and m.lifetime.sec > 0 for m in markers))

    def test_reset_clears_only_reference_namespace(self):
        marker = reference_markers([], [0., 0., 0.]).marker[0]
        self.assertEqual(marker.action, Marker.DELETE_ALL)
        self.assertEqual(marker.ns, 'mpc_reference')

    def test_invalid_reference_rejected(self):
        with self.assertRaises(ValueError):
            reference_markers([Pose()], [0., 0., 0.])
        pose = Pose()
        pose.position.x = float('nan')
        with self.assertRaises(ValueError):
            reference_markers([pose, Pose()], [0., 0., 0.])


if __name__ == '__main__':
    unittest.main()
