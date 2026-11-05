"""Show the MPC mission segment using Gazebo Harmonic GUI-only markers."""
import math
import time

from geometry_msgs.msg import PoseArray
from gz.msgs10.boolean_pb2 import Boolean
from gz.msgs10.marker_pb2 import Marker
from gz.msgs10.marker_v_pb2 import Marker_V
from gz.transport13 import Node as TransportNode

from .common import Base, run


def reference_markers(poses, origin):
    """NED local coordinates -> Gazebo ENU, with a configurable local origin."""
    result = Marker_V()
    if not poses:
        result.marker.add(ns='mpc_reference', action=Marker.DELETE_ALL)
        return result
    if len(poses) != 2:
        raise ValueError('reference must have exactly two endpoints')
    points = [(p.position.y + origin[0], p.position.x + origin[1],
               -p.position.z + origin[2]) for p in poses]
    if not all(math.isfinite(v) for point in points for v in point):
        raise ValueError('nonfinite reference')
    for index, color in enumerate(((0.0, 0.8, 1.0), (0.1, 1.0, 0.2), (1.0, 0.2, 0.6))):
        marker = result.marker.add(ns='mpc_reference', id=index + 1,
                                   type=Marker.LINE_STRIP if index == 0 else Marker.SPHERE,
                                   action=Marker.ADD_MODIFY, visibility=Marker.GUI)
        marker.lifetime.sec = 3
        marker.pose.orientation.w = 1.0
        marker.scale.x = marker.scale.y = marker.scale.z = 1.0 if index == 0 else 0.16
        for field in (marker.material.ambient, marker.material.diffuse,
                      marker.material.emissive):
            field.r, field.g, field.b = color
            field.a = 1.0
        if index == 0:
            for x, y, z in points:
                marker.point.add(x=x, y=y, z=z)
        else:
            p = marker.pose.position
            p.x, p.y, p.z = points[index - 1]
    return result


class GzReferenceNode(Base):
    def __init__(self):
        super().__init__('gz_reference_node')
        self.frame = self.param('map_frame', 'map_ned')
        self.origin = self.param('ned_origin_enu', [0.0, 0.0, 0.0])
        if len(self.origin) != 3 or not all(math.isfinite(x) for x in self.origin):
            raise ValueError('ned_origin_enu must be three finite meters')
        self.transport = TransportNode()
        self.reference = None
        self.received = 0.0
        self.create_subscription(PoseArray, 'control/reference', self.on_reference, 1)
        self.create_timer(1.0, self.render)

    def on_reference(self, msg):
        if msg.header.frame_id != self.frame:
            self.reference = None
            return
        self.reference = msg
        self.received = time.monotonic()

    def render(self):
        poses = (self.reference.poses if self.reference is not None and
                 time.monotonic() - self.received < 2.5 else [])
        try:
            markers = reference_markers(poses, self.origin)
            ok, reply = self.transport.request('/marker_array', markers, Marker_V, Boolean, 200)
            if not ok or not reply.data:
                self.get_logger().warning('Gazebo /marker_array unavailable; retrying',
                                          throttle_duration_sec=10.0)
        except ValueError as exc:
            self.reference = None
            self.get_logger().warning(str(exc), throttle_duration_sec=10.0)


def main(args=None):
    run(GzReferenceNode, args)
