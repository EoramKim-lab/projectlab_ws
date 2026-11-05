"""NED velocity -> PX4 v1.16 Offboard. Automatic hover -> Offboard handover; no auto arming or takeoff."""
import math
import time
import numpy as np
from geometry_msgs.msg import TwistStamped
from std_srvs.srv import SetBool, Trigger
from std_msgs.msg import Empty
from drone_interfaces.msg import NavigationState, Halfplanes
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleCommandAck, VehicleLocalPosition, VehicleStatus
from ..common import Base, SENSOR_QOS, run
from ..math_utils import vector, limited_velocity

class Px4CommandNode(Base):
    def __init__(self):
        super().__init__('px4_command_node')
        self.frame = self.param('map_frame','map_ned')
        self.body = self.param('body_frame','base_link_frd')
        self.timeout = self.param('command_timeout',.25)
        self.sensor_timeout = self.param('sensor_timeout',.3)
        self.hmax = self.param('max_horizontal_speed',1.)
        self.vmax = self.param('max_vertical_speed',.5)
        self.yawmax = self.param('max_yaw_rate',.6)
        self.system = self.param('target_system',1)
        self.component = self.param('target_component',1)
        self.start_monitor('velocity_cmd', 'px4_stream')
        self.enabled = False
        self.auto_phase = 'waiting' if self.param('auto_offboard', True) else 'off'
        self.status = self.status_rx = None
        self.last_mode_request = None
        self.stream_start = None
        self.cmd = self.state = self.planes = self.local = None
        self.local_rx = None
        self.watch_px4_clock()
        if min(self.hmax,self.vmax,self.yawmax,self.timeout,self.sensor_timeout) <= 0:
            raise ValueError('limits and timeouts must be positive')
        self.heartbeat = self.create_publisher(OffboardControlMode,'/fmu/in/offboard_control_mode',10)
        self.setpoint = self.create_publisher(TrajectorySetpoint,'/fmu/in/trajectory_setpoint',10)
        self.vehicle_cmd = self.create_publisher(VehicleCommand,'/fmu/in/vehicle_command',10)
        self.create_subscription(TwistStamped,'control/velocity_cmd',self.on_cmd,10)
        self.create_subscription(NavigationState,'navigation/state',self.on_state,10)
        self.create_subscription(Empty,'navigation/reset',self.on_navigation_reset,10)
        self.create_subscription(Halfplanes,'collision/halfplanes',self.on_planes,10)
        self.create_subscription(VehicleLocalPosition,'/fmu/out/vehicle_local_position',self.on_local,SENSOR_QOS)
        self.create_subscription(VehicleStatus,'/fmu/out/vehicle_status_v1',self.on_status,SENSOR_QOS)
        self.create_subscription(VehicleCommandAck,'/fmu/out/vehicle_command_ack',self.on_ack,SENSOR_QOS)
        self.create_service(SetBool,'control/enable',self.enable)
        self.create_service(Trigger,'control/request_offboard',self.offboard)
        rate = self.param('publish_rate',20.)
        if rate < 5.:
            raise ValueError('Offboard publish_rate must be >= 5 Hz')
        self.create_timer(1./rate,self.tick)

    def on_navigation_reset(self, msg):
        self.cmd = self.state = self.planes = None
        self.local = self.local_rx = None
        self.stop_auto('PX4 EKF local-position reset; wait for valid GNSS navigation and re-enable')

    def on_cmd(self,msg):
        self.cmd = msg
        v = msg.twist.linear
        self.observe('velocity_cmd', f'frame={msg.header.frame_id} v_NED=({v.x:.3f},{v.y:.3f},{v.z:.3f})m/s yaw_rate={msg.twist.angular.z:.3f}rad/s')
    def on_state(self,msg): self.state = msg
    def on_planes(self,msg): self.planes = msg
    def on_local(self,msg):
        if self.px4_increasing('local',msg.timestamp):
            self.local,self.local_rx = msg,time.monotonic()
    def on_status(self,msg):
        if self.px4_increasing('status', msg.timestamp):
            self.status, self.status_rx = msg, time.monotonic()

    def on_px4_reset(self):
        self.local = self.local_rx = self.status = self.status_rx = None
        self.cmd = self.state = self.planes = None
        self.last_mode_request = None
        self.stop_auto('PX4 clock reset; navigation origin may have changed')

    def stop_auto(self, reason):
        self.enabled = False
        self.stream_start = None
        self.auto_phase = 'off'
        self.get_logger().error('Offboard stream latched OFF: '+reason+'; restart node or explicitly re-enable')

    def automatic_handover(self):
        if self.auto_phase == 'off':
            return
        now = time.monotonic()
        status_fresh = self.status_rx is not None and now - self.status_rx <= 2.0
        armed = status_fresh and self.status.arming_state == VehicleStatus.ARMING_STATE_ARMED
        hover_modes = (VehicleStatus.NAVIGATION_STATE_AUTO_LOITER,
                       VehicleStatus.NAVIGATION_STATE_POSCTL, VehicleStatus.NAVIGATION_STATE_ALTCTL)
        hold = armed and self.status.nav_state in hover_modes
        offboard = armed and self.status.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD
        if self.auto_phase == 'waiting':
            reason = self.readiness()
            if not hold or reason:
                self.observe('px4_stream', 'AUTO WAIT: '+(reason or 'waiting for armed Hold/Position/Altitude and fresh VehicleStatus'))
                return
            self.enabled = True
            self.stream_start = None
            self.auto_phase = 'streaming'
            self.get_logger().info('Armed hover mode detected; preparing Offboard stream automatically')
        elif not armed or not (hold or offboard) or (self.auto_phase == 'active' and not offboard):
            self.stop_auto('PX4 status lost, disarmed, or pilot/mode takeover')
            return
        if offboard:
            if self.auto_phase != 'active':
                self.get_logger().info('Offboard confirmed; MPC control active')
            self.auto_phase = 'active'
        elif self.stream_start is not None and now - self.stream_start >= 1.1:
            if self.last_mode_request is None or now - self.last_mode_request >= 1.0:
                if not self.readiness():
                    self.send_offboard_request()
                    self.last_mode_request = now
                    self.get_logger().info('Automatic Offboard request sent; waiting for VehicleStatus confirmation')

    def on_ack(self,msg):
        if msg.command == VehicleCommand.VEHICLE_CMD_DO_SET_MODE:
            self.get_logger().info(f'PX4 mode command ACK result={msg.result} (0=accepted)')

    def command_reason(self):
        if self.cmd is None or self.cmd.header.frame_id != self.frame or not self.fresh(self.cmd.header.stamp,self.timeout):
            return 'missing/stale/wrong-frame velocity command'
        vals = np.r_[vector(self.cmd.twist.linear),vector(self.cmd.twist.angular)]
        if not np.isfinite(vals).all() or np.any(np.abs(vals[3:5]) > 1e-9):
            return 'invalid velocity/yaw-rate command'
        return ''

    def sensor_reason(self):
        if self.state is None or not self.state.valid or self.state.header.frame_id != self.frame or not self.fresh(self.state.header.stamp,self.sensor_timeout):
            return 'missing/invalid/stale navigation'
        if self.planes is None or not self.planes.valid or self.planes.header.frame_id != self.body or not self.fresh(self.planes.header.stamp,self.sensor_timeout):
            return 'missing/invalid/stale collision constraints'
        if len(self.planes.a) != 2*len(self.planes.b) or not np.isfinite(self.planes.a).all() or not np.isfinite(self.planes.b).all():
            return 'malformed collision constraints'
        if self.local_rx is None or time.monotonic()-self.local_rx > self.sensor_timeout:
            return 'PX4 EKF local position stale'
        if not (self.local.xy_valid and self.local.z_valid and self.local.v_xy_valid and self.local.v_z_valid):
            return 'PX4 EKF position/velocity invalid'
        if not self.local.xy_global or self.local.dead_reckoning:
            return 'PX4 EKF has no GNSS-aided global horizontal reference'
        return ''

    def readiness(self):
        reason = self.sensor_reason() or self.command_reason()
        if reason:
            return reason
        return '' if self.planes.origin_feasible else 'inside collision safety margin'

    def enable(self,request,response):
        reason = self.readiness() if request.data else ''
        if reason:
            response.success,response.message = False,reason
            return response
        self.auto_phase = 'off'  # Explicit service calls override startup automation.
        self.enabled = bool(request.data)
        self.stream_start = None
        response.success = True
        response.message = 'stream enabled; arming/mode unchanged' if self.enabled else 'stream disabled; PX4 Offboard-loss policy applies'
        return response

    def offboard(self,request,response):
        reason = self.readiness()
        if not self.enabled or reason or self.stream_start is None or time.monotonic()-self.stream_start < 1.1:
            response.success,response.message = False,'enable healthy stream for >=1.1s first: '+reason
            return response
        self.send_offboard_request()
        response.success,response.message = True,'request sent; confirm VehicleStatus/ACK in PX4 (not an arming command)'
        return response

    def send_offboard_request(self):
        cmd = VehicleCommand()
        cmd.timestamp = self.get_clock().now().nanoseconds//1000
        cmd.command = VehicleCommand.VEHICLE_CMD_DO_SET_MODE
        cmd.param1,cmd.param2 = 1.,6.
        cmd.target_system,cmd.target_component = self.system,self.component
        cmd.source_system,cmd.source_component = 255,191
        cmd.from_external = True
        self.vehicle_cmd.publish(cmd)

    def tick(self):
        self.automatic_handover()
        if self.auto_phase == 'waiting':
            return
        self.observe('px4_stream', f'enabled={self.enabled} readiness={self.readiness() or "ready"}')
        if not self.enabled:
            return
        reason = self.sensor_reason()
        if reason:
            self.stop_auto(reason)
            return
        # The heartbeat has its own timer/process, so a slow or infeasible MPC
        # cannot cause Offboard loss while the sensor pipeline remains healthy.
        hold_reason = self.command_reason()
        if not self.planes.origin_feasible:
            hold_reason = 'inside collision safety margin'
        ts = self.get_clock().now().nanoseconds//1000
        velocity = np.zeros(3) if hold_reason else limited_velocity(vector(self.cmd.twist.linear),self.hmax,self.vmax)
        sp = TrajectorySetpoint()
        sp.timestamp = ts
        sp.position = [float('nan')]*3
        sp.velocity = velocity.tolist()
        sp.acceleration = [float('nan')]*3
        sp.jerk = [float('nan')]*3
        sp.yaw = float('nan')
        sp.yawspeed = 0.0 if hold_reason else float(np.clip(self.cmd.twist.angular.z,-self.yawmax,self.yawmax))
        if hold_reason:
            self.observe('px4_stream', 'HOLD: '+hold_reason+'; zero velocity/yaw rate, Offboard stream maintained')
        self.observe('px4_setpoint', f'v_NED={np.round(sp.velocity, 3).tolist()}m/s yaw_rate_NED={sp.yawspeed:.3f}rad/s')
        mode = OffboardControlMode()
        mode.timestamp = ts
        mode.velocity = True
        self.setpoint.publish(sp)
        self.heartbeat.publish(mode)
        if self.stream_start is None:
            self.stream_start = time.monotonic()

def main(args=None): run(Px4CommandNode,args)
