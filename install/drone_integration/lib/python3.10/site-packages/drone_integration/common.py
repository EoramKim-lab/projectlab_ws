"""Common ROS conventions. Source headers are never refreshed downstream."""
import math
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
SENSOR_QOS = QoSProfile(history=HistoryPolicy.KEEP_LAST, depth=1,
 reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE)

def seconds(stamp):
    return stamp.sec + stamp.nanosec * 1e-9

class Base(Node):
    def watch_px4_clock(self):
        from std_msgs.msg import Empty
        from .px4_clock import Px4ClockGuard
        self._px4_clock = Px4ClockGuard()
        self._px4_sample_timeout = self.param('px4_sample_timeout', 0.25)
        if not math.isfinite(self._px4_sample_timeout) or self._px4_sample_timeout <= 0:
            raise ValueError('px4_sample_timeout must be positive')
        self._px4_reset_pub = self.create_publisher(Empty, 'sensors/px4_reset', 10)
        self.create_subscription(Empty, 'sensors/px4_reset', self.receive_px4_reset, 10)

    def px4_sample_stamp(self, sample_us):
        """Preserve XRCE-DDS synchronized measurement time; never re-stamp on RX."""
        from builtin_interfaces.msg import Time
        from .px4_clock import sample_time_parts
        try:
            sec, nanosec = sample_time_parts(
                sample_us, self.get_clock().now().nanoseconds,
                self._px4_sample_timeout)
        except ValueError:
            self.get_logger().warning(
                'PX4 measurement time is stale/future/invalid; check XRCE-DDS time sync',
                throttle_duration_sec=2.0)
            return None
        return Time(sec=sec, nanosec=nanosec)

    def receive_px4_reset(self, msg):
        # Keep per-stream clock guards: each stream must independently confirm
        # its new epoch, rather than accepting a delayed pre-reboot packet.
        self.on_px4_reset()

    def on_px4_reset(self):
        pass

    def px4_increasing(self, key, stamp):
        from .px4_clock import Px4ClockGuard
        if not hasattr(self, '_px4_clock'):
            self._px4_clock = Px4ClockGuard()
        accepted, reboot = self._px4_clock.accept(key, stamp)
        if reboot:
            self.get_logger().error('PX4 clock rollback confirmed: resetting sensor epoch; control must be re-enabled explicitly')
            self.on_px4_reset()
            if hasattr(self, '_px4_reset_pub'):
                from std_msgs.msg import Empty
                self._px4_reset_pub.publish(Empty())
        return accepted

    def start_monitor(self, *channels):
        rate = self.param('monitor_rate', 2.0)
        self._monitor_timeout = self.param('monitor_timeout', 0.5)
        if not math.isfinite(rate) or rate < 0 or not math.isfinite(self._monitor_timeout) or self._monitor_timeout <= 0:
            raise ValueError('monitor_rate must be nonnegative and monitor_timeout positive')
        self._monitor_values = {name: None for name in channels}
        if rate > 0:
            self.create_timer(1.0 / rate, self.print_monitor)

    def observe(self, channel, detail):
        if hasattr(self, '_monitor_values'):
            self._monitor_values[channel] = (time.monotonic(), detail)

    def print_monitor(self):
        now = time.monotonic()
        lines = []
        for channel, value in self._monitor_values.items():
            if value is None:
                lines.append(channel + ': WAITING (no accepted sample/status)')
            else:
                stamp, detail = value
                age = now - stamp
                status = 'STALE' if age > self._monitor_timeout else 'LIVE'
                lines.append(f'{channel}: {status} age={age:.2f}s {detail}')
        self.get_logger().info(' | '.join(lines))

    def param(self, name, default):
        self.declare_parameter(name, default)
        return self.get_parameter(name).value

    def age(self, stamp):
        return self.get_clock().now().nanoseconds*1e-9 - seconds(stamp)

    def fresh(self, stamp, timeout):
        return seconds(stamp) > 0 and -0.05 <= self.age(stamp) <= timeout

    def increasing(self, key, value):
        if not hasattr(self, '_source_stamps'):
            self._source_stamps = {}
        old = self._source_stamps.get(key, 0)
        if value <= old:
            return False
        self._source_stamps[key] = value
        return True

def run(cls, args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = cls()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
