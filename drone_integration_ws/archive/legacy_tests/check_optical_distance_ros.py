"""External 1-D range plus raw flow regression checks; no DDS or flight commands."""
import math
import unittest
from types import SimpleNamespace as NS
import numpy as np
from builtin_interfaces.msg import Time
from px4_msgs.msg import SensorOpticalFlow, DistanceSensor
from drone_integration.sensor.optical_flow_receiver_node import OpticalFlowReceiverNode
from drone_integration.math_utils import flow_velocity


class OpticalDistanceTests(unittest.TestCase):
    def make(self):
        n=OpticalFlowReceiverNode.__new__(OpticalFlowReceiverNode)
        n.body='base_link_frd';n.quality=100;n.device=-1
        n._px4_sample_timeout=.25
        n.flow_source='sensor';n.sensor_yaw=0.;n.range_timeout=.5
        n.last_distance=None;n.now=10.
        n.get_clock=lambda: NS(now=lambda: NS(nanoseconds=int(n.now*1e9),
            to_msg=lambda: Time(sec=int(n.now),nanosec=round((n.now-int(n.now))*1e9))))
        n.flow_pub=NS(messages=[]);n.flow_pub.publish=n.flow_pub.messages.append
        n.range_pub=NS(messages=[]);n.range_pub.publish=n.range_pub.messages.append
        return n

    def distance(self,n,stamp=1000,value=2.):
        r=DistanceSensor();r.timestamp=int(n.now*1e6)+stamp;r.orientation=25;r.signal_quality=100
        r.min_distance=.1;r.max_distance=10.;r.current_distance=value
        n.distance(r)

    def flow(self,n,stamp=1000):
        f=SensorOpticalFlow();f.timestamp_sample=int(n.now*1e6)+stamp;f.quality=200
        f.integration_timespan_us=20000;f.pixel_flow=[0.,.01]
        f.delta_angle=[0.,0.,0.];f.delta_angle_available=True
        # Deliberately unavailable optical distance; only distance_sensor counts.
        f.distance_m=0.;f.distance_available=False
        n.raw_flow(f)
        return n.flow_pub.messages[-1]

    def test_raw_flow_uses_external_distance_for_body_velocity(self):
        n=self.make();self.distance(n);out=self.flow(n)
        self.assertTrue(out.valid);self.assertEqual(out.distance_m,2.)
        np.testing.assert_allclose(flow_velocity(out.pixel_flow,out.delta_angle,
                                                out.integration_dt,out.distance_m),[1.,0.])
        self.assertEqual(n.range_pub.messages[-1].range,2.)

    def test_missing_or_stale_distance_is_invalid_and_recovers(self):
        n=self.make();self.assertFalse(self.flow(n).valid)
        self.distance(n);self.assertTrue(self.flow(n,2000).valid)
        n.now+=.6;out=self.flow(n,3000)
        self.assertFalse(out.valid);self.assertTrue(math.isnan(out.distance_m))
        self.distance(n,2000,3.);out=self.flow(n,4000)
        self.assertTrue(out.valid);self.assertEqual(out.distance_m,3.)

    def test_bad_range_preserves_last_good_range(self):
        n=self.make();self.distance(n);self.distance(n,2000,float('nan'))
        self.assertEqual(self.flow(n).distance_m,2.)

    def test_reset_discards_cached_distance(self):
        n=self.make();self.distance(n);n.on_px4_reset()
        self.assertFalse(self.flow(n).valid)

    def test_sensor_yaw_rotates_pixel_and_gyro_together(self):
        n=self.make();self.distance(n);n.sensor_yaw=math.pi/2
        out=self.flow(n)
        np.testing.assert_allclose(out.pixel_flow,[-.01,0.],atol=1e-12)

    def test_missing_gyro_flag_invalidates_even_finite_zero_values(self):
        n=self.make();self.distance(n)
        f=SensorOpticalFlow();f.timestamp_sample=int(n.now*1e6)+1000;f.quality=200
        f.integration_timespan_us=20000;f.delta_angle=[0.,0.,0.]
        f.delta_angle_available=False;n.raw_flow(f)
        self.assertFalse(n.flow_pub.messages[-1].valid)

    def test_external_range_and_raw_flow_drive_dead_reckoning_position(self):
        from check_dead_reckoning_ros import DeadReckoningTests
        from geometry_msgs.msg import QuaternionStamped
        from sensor_msgs.msg import Imu
        fixture=DeadReckoningTests();nav=fixture.make();receiver=self.make()
        self.distance(receiver)
        attitude=QuaternionStamped();attitude.quaternion.w=1.
        attitude.header=fixture.header(nav);nav.attitude(attitude)
        nav.distance(receiver.range_pub.messages[-1])
        for k in range(11):
            nav.now=receiver.now=10.+k*.02
            attitude.header=fixture.header(nav);nav.attitude(attitude)
            nav.flow(self.flow(receiver,1000))
            imu=Imu();imu.header=fixture.header(nav,True)
            imu.linear_acceleration.z=-9.80665;nav.imu(imu)
        nav.publish()
        self.assertTrue(nav.pub.messages[-1].valid)
        np.testing.assert_allclose(nav.core.p,[.2,0.,-2.],atol=1e-8)


if __name__ == '__main__':
    unittest.main()
