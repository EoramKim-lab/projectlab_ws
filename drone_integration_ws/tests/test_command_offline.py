"""ROS-free callback checks using message doubles; does not claim DDS/runtime validation."""
import sys
import types
import unittest
import time
from types import SimpleNamespace as NS
import numpy as np

def module(name,**attrs):
    m=types.ModuleType(name);m.__dict__.update(attrs);sys.modules[name]=m
    return m
class Message:
    VEHICLE_CMD_DO_SET_MODE=176
    ARMING_STATE_ARMED=2
    NAVIGATION_STATE_POSCTL=2
    NAVIGATION_STATE_ALTCTL=1
    NAVIGATION_STATE_AUTO_LOITER=4
    NAVIGATION_STATE_OFFBOARD=14
    def __init__(self):
        self.position=self.velocity=self.acceleration=self.jerk=[]
        self.velocity=False
class QoS:
    def __init__(self,**kwargs):pass
module('rclpy');module('rclpy.node',Node=object)
module('rclpy.qos',QoSProfile=QoS,ReliabilityPolicy=NS(BEST_EFFORT=1),DurabilityPolicy=NS(VOLATILE=1),HistoryPolicy=NS(KEEP_LAST=1))
module('geometry_msgs');module('geometry_msgs.msg',TwistStamped=Message)
module('std_srvs');module('std_srvs.srv',SetBool=Message,Trigger=Message)
module('std_msgs');module('std_msgs.msg',Empty=Message)
module('drone_interfaces');module('drone_interfaces.msg',NavigationState=Message,Halfplanes=Message)
module('px4_msgs');module('px4_msgs.msg',**{n:Message for n in ['OffboardControlMode','TrajectorySetpoint','VehicleCommand','VehicleCommandAck','VehicleLocalPosition','VehicleStatus']})
from drone_integration.control.px4_command_node import Px4CommandNode

def vec(x=0,y=0,z=0):return NS(x=x,y=y,z=z)
def stamp(t=10):return NS(sec=int(t),nanosec=int((t-int(t))*1e9))
def header(frame='map_ned',t=10):return NS(frame_id=frame,stamp=stamp(t))
class Pub:
    def __init__(self):self.messages=[]
    def publish(self,msg):self.messages.append(msg)

class CommandTests(unittest.TestCase):
    def make(self):
        n=Px4CommandNode.__new__(Px4CommandNode)
        n.frame,n.body='map_ned','base_link_frd';n.timeout=.25;n.sensor_timeout=.3
        n.hmax,n.vmax,n.yawmax=1.,.5,.6;n.system=n.component=1
        n.enabled=True;n.stream_start=None
        n.auto_phase='off';n.status=n.status_rx=None;n.last_mode_request=None
        n.cmd=NS(header=header(),twist=NS(linear=vec(3,4,2),angular=vec(0,0,.3)))
        n.state=NS(header=header(),valid=True)
        n.planes=NS(header=header('base_link_frd'),valid=True,origin_feasible=True,a=[1.,0.],b=[2.])
        n.local=NS(xy_valid=True,z_valid=True,v_xy_valid=True,v_z_valid=True,
                  xy_global=True,dead_reckoning=False);n.local_rx=time.monotonic()
        n.get_clock=lambda:NS(now=lambda:NS(nanoseconds=10_000_000_000))
        n.get_logger=lambda:NS(error=lambda x:None,info=lambda x:None)
        n.heartbeat,n.setpoint,n.vehicle_cmd=Pub(),Pub(),Pub()
        return n

    def hold(self, n):
        n.enabled=False;n.auto_phase='waiting'
        n.status=NS(arming_state=2,nav_state=4);n.status_rx=time.monotonic()

    def test_automatic_hold_to_offboard(self):
        n=self.make();self.hold(n)
        n.tick()
        self.assertTrue(n.enabled)
        self.assertEqual(len(n.vehicle_cmd.messages),0)
        n.stream_start=time.monotonic()-1.2
        n.tick()
        self.assertEqual(len(n.vehicle_cmd.messages),1)
        n.tick()  # Requests are rate limited while PX4 confirms the mode.
        self.assertEqual(len(n.vehicle_cmd.messages),1)
        n.status.nav_state=14;n.tick()
        self.assertEqual(n.auto_phase,'active')
        n.status.nav_state=4;n.tick()  # Pilot returns to Hold: do not re-enter.
        self.assertFalse(n.enabled)
        self.assertEqual(n.auto_phase,'off')
        n.tick();self.assertEqual(len(n.vehicle_cmd.messages),1)

    def test_start_from_position_or_altitude_hover(self):
        for mode in (1, 2):
            n=self.make();self.hold(n);n.status.nav_state=mode
            n.tick()
            self.assertTrue(n.enabled)
            n.stream_start=time.monotonic()-1.2;n.tick()
            self.assertEqual(len(n.vehicle_cmd.messages),1)
            n.status.nav_state=14;n.tick()
            self.assertEqual(n.auto_phase,'active')
            n.status.nav_state=mode;n.tick()
            self.assertFalse(n.enabled)
            self.assertEqual(n.auto_phase,'off')

    def test_auto_waits_for_hold_armed_status_and_inputs(self):
        for missing in ['disarmed','mode','status','command']:
            n=self.make();self.hold(n)
            if missing=='disarmed': n.status.arming_state=1
            if missing=='mode': n.status.nav_state=0
            if missing=='status': n.status_rx=None
            if missing=='command': n.cmd=None
            n.tick()
            self.assertFalse(n.enabled)
            self.assertFalse(n.vehicle_cmd.messages)
            self.assertFalse(n.heartbeat.messages)

    def test_auto_status_loss_stops_active_stream(self):
        n=self.make();self.hold(n);n.tick()
        n.status.nav_state=14;n.tick()
        n.status_rx=time.monotonic()-3.;n.tick()
        self.assertFalse(n.enabled)
        self.assertEqual(n.auto_phase,'off')

    def test_auto_command_gap_holds_and_explicit_disable_latches(self):
        n=self.make();self.hold(n);n.tick()
        n.cmd.header.stamp=stamp(9);n.tick()
        self.assertTrue(n.enabled)
        np.testing.assert_allclose(n.setpoint.messages[-1].velocity, [0.,0.,0.])
        n.cmd.header.stamp=stamp(10);n.tick()
        self.assertTrue(n.enabled)
        n=self.make();self.hold(n)
        n.enable(NS(data=False),NS());n.tick()
        self.assertFalse(n.enabled)
        self.assertEqual(n.auto_phase,'off')

    def test_velocity_only_mapping_and_nan_fields(self):
        n=self.make();n.tick();sp=n.setpoint.messages[-1]
        np.testing.assert_allclose(sp.velocity,[.6,.8,.5])
        self.assertTrue(np.isnan(sp.position).all());self.assertTrue(np.isnan(sp.acceleration).all())
        self.assertTrue(np.isnan(sp.yaw));self.assertAlmostEqual(sp.yawspeed,.3)
        self.assertTrue(n.heartbeat.messages[-1].velocity)

    def test_stale_command_holds_and_recovers(self):
        n=self.make();n.cmd.header.stamp=stamp(9);n.tick()
        self.assertTrue(n.enabled);self.assertEqual(len(n.heartbeat.messages),1)
        np.testing.assert_allclose(n.setpoint.messages[-1].velocity,[0.,0.,0.])
        self.assertEqual(n.setpoint.messages[-1].yawspeed,0.)
        n.cmd.header.stamp=stamp(10);n.tick()
        self.assertEqual(len(n.heartbeat.messages),2)
        np.testing.assert_allclose(n.setpoint.messages[-1].velocity,[.6,.8,.5])

    def test_missing_or_invalid_command_holds(self):
        for fault in ('missing','frame','nonfinite'):
            n=self.make()
            if fault=='missing': n.cmd=None
            if fault=='frame': n.cmd.header.frame_id='map'
            if fault=='nonfinite': n.cmd.twist.linear.x=float('nan')
            n.tick()
            self.assertTrue(n.enabled)
            self.assertEqual(len(n.heartbeat.messages),1)
            np.testing.assert_allclose(n.setpoint.messages[-1].velocity,[0.,0.,0.])

    def test_collision_margin_holds_but_stale_sensors_stop(self):
        n=self.make();n.planes.origin_feasible=False;n.tick()
        self.assertTrue(n.enabled)
        np.testing.assert_allclose(n.setpoint.messages[-1].velocity,[0.,0.,0.])
        n.planes.header.stamp=stamp(9);n.tick()
        self.assertFalse(n.enabled)
        self.assertEqual(len(n.heartbeat.messages),1)

    def test_ned_directions_and_yaw_pass_through(self):
        for v in ([.2,0.,0.], [0.,.2,0.], [0.,0.,-.2], [0.,0.,.2]):
            for yaw_rate in (-.2, .2):
                n=self.make()
                n.cmd.twist.linear=vec(*v)
                n.cmd.twist.angular.z=yaw_rate
                n.tick()
                np.testing.assert_allclose(n.setpoint.messages[-1].velocity,v)
                self.assertEqual(n.setpoint.messages[-1].yawspeed,yaw_rate)

    def test_legacy_enu_command_is_rejected(self):
        n=self.make();n.cmd.header.frame_id='map';n.tick()
        np.testing.assert_allclose(n.setpoint.messages[-1].velocity,[0.,0.,0.])

    def test_invalid_navigation_blocks_stream(self):
        n=self.make();n.state.valid=False;n.tick();self.assertFalse(n.enabled)

    def test_wrong_frame_or_nonfinite_command(self):
        n=self.make();n.cmd.header.frame_id='base_link_frd';self.assertTrue(n.readiness())
        n.cmd.header.frame_id='map_ned';n.cmd.twist.linear.x=float('nan');self.assertTrue(n.readiness())

    def test_infeasible_or_stale_planes(self):
        n=self.make();n.planes.origin_feasible=False;self.assertTrue(n.readiness())
        n.planes.origin_feasible=True;n.planes.header.stamp=stamp(9);self.assertTrue(n.readiness())

    def test_ekf_invalid_blocks(self):
        n=self.make();n.local.v_xy_valid=False;self.assertTrue(n.readiness())
        n=self.make();n.local.xy_global=False;self.assertTrue(n.readiness())
        n=self.make();n.local.dead_reckoning=True;self.assertTrue(n.readiness())

    def test_no_mode_request_before_prestream(self):
        n=self.make();response=NS();n.offboard(NS(),response)
        self.assertFalse(response.success);self.assertEqual(len(n.vehicle_cmd.messages),0)
        n.stream_start=time.monotonic()-1.2;n.offboard(NS(),response)
        self.assertTrue(response.success);self.assertEqual(n.vehicle_cmd.messages[-1].command,176)

    def test_px4_reboot_recovers_local_input_but_latches_control_off(self):
        n=self.make()
        n.on_local(NS(timestamp=10_000_000,xy_valid=True,z_valid=True,v_xy_valid=True,v_z_valid=True,xy_global=True,dead_reckoning=False))
        for t in (1000,2000):
            n.on_local(NS(timestamp=t,xy_valid=True,z_valid=True,v_xy_valid=True,v_z_valid=True,xy_global=True,dead_reckoning=False))
            self.assertTrue(n.enabled)
        n.on_local(NS(timestamp=3000,xy_valid=True,z_valid=True,v_xy_valid=True,v_z_valid=True,xy_global=True,dead_reckoning=False))
        self.assertFalse(n.enabled)
        self.assertEqual(n.auto_phase,'off')
        self.assertEqual(n.local.timestamp,3000)
        self.assertIsNone(n.cmd)
        self.assertIsNone(n.state)
        self.assertIsNone(n.status)
        n.tick()
        self.assertFalse(n.setpoint.messages)

    def test_reset_event_cancels_startup_automation(self):
        n=self.make();self.hold(n)
        n.receive_px4_reset(None)
        n.tick()
        self.assertEqual(n.auto_phase,'off')
        self.assertFalse(n.heartbeat.messages)

if __name__=='__main__':unittest.main()
