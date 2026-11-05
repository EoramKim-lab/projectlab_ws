"""Runs the supplied halfplanes.py without changing its geometry."""
from dataclasses import fields
import numpy as np
from drone_interfaces.msg import ProcessedScan, Halfplanes
from .halfplanes import HalfplaneConfig, build_halfplanes
from ..common import Base, run

class CollisionConstraintsNode(Base):
    def __init__(self):
        super().__init__('collision_constraints_node')
        defaults = HalfplaneConfig()
        self.cfg = HalfplaneConfig(**{f.name:self.param(f.name,getattr(defaults,f.name)) for f in fields(defaults)})
        self.timeout = self.param('scan_timeout',.3)
        self.body = self.param('body_frame','base_link_frd')
        self.start_monitor('halfplanes')
        self.pub = self.create_publisher(Halfplanes,'collision/halfplanes',10)
        self.create_subscription(ProcessedScan,'lidar/processed',self.receive,10)

    def receive(self,msg):
        out = Halfplanes()
        out.header = msg.header
        out.reason = msg.reason
        if msg.valid and msg.header.frame_id == self.body and self.fresh(msg.header.stamp,self.timeout):
            try:
                result = build_halfplanes(np.asarray(msg.xy).reshape(-1,2),self.cfg)
                out.a,out.b = result.A.reshape(-1).tolist(),result.b.tolist()
                out.sector_ids = result.sector_ids.tolist()
                out.nearest_range = result.nearest_range.tolist()
                out.origin_feasible = result.origin_feasible
                out.valid = True
                out.reason = 'ok' if out.origin_feasible else 'inside_safety_margin'
            except ValueError as exc:
                out.reason = str(exc)
        self.observe('halfplanes', f'valid={out.valid} origin_feasible={out.origin_feasible} count={len(out.b)} reason={out.reason}')
        self.pub.publish(out)

def main(args=None): run(CollisionConstraintsNode,args)
