"""PX4 reboot/reordering regression checks without ROS or hardware."""
import unittest
from drone_integration.px4_clock import Px4ClockGuard


class Px4ClockTests(unittest.TestCase):
    def test_duplicate_and_short_reordering_do_not_reset(self):
        g = Px4ClockGuard()
        self.assertEqual(g.accept('imu', 10_000_000), (True, False))
        for t in (10_000_000, 9_999_999, 9_500_000, 0):
            self.assertEqual(g.accept('imu', t), (False, False))
        self.assertEqual(g.accept('imu', 10_000_001), (True, False))

    def test_reboot_quarantines_then_accepts_new_epoch(self):
        g = Px4ClockGuard()
        g.accept('imu', 10_000_000)
        g.accept('attitude', 10_000_000)
        self.assertEqual(g.accept('imu', 1000), (False, False))
        self.assertEqual(g.accept('imu', 1000), (False, False))
        self.assertEqual(g.accept('imu', 2000), (False, False))
        self.assertEqual(g.accept('imu', 3000), (True, True))
        self.assertEqual(g.accept('imu', 4000), (True, False))
        self.assertEqual(g.accept('attitude', 4000), (True, False))

    def test_one_old_packet_cannot_change_epoch(self):
        g = Px4ClockGuard()
        g.accept('imu', 10_000_000)
        g.accept('imu', 1000)
        self.assertEqual(g.accept('imu', 10_000_001), (True, False))
        self.assertEqual(g.accept('imu', 2000), (False, False))



class MeasurementTimeTests(unittest.TestCase):
    def test_transport_jitter_does_not_change_sample_interval(self):
        from drone_integration.px4_clock import sample_time_parts
        epoch = 1_800_000_000_000_000
        stamps = [sample_time_parts(epoch + i * 10000,
                  (epoch + i * 10000 + delay) * 1000)
                  for i, delay in enumerate((1000, 30000, 2000))]
        ns = [sec * 10**9 + nano for sec, nano in stamps]
        self.assertEqual([ns[i+1]-ns[i] for i in range(2)], [10000000]*2)

    def test_unsynchronized_stale_future_and_zero_rejected(self):
        from drone_integration.px4_clock import sample_time_parts
        now = 1_800_000_000_000_000_000
        for stamp in (0, 123456, now//1000-250001, now//1000+50001):
            with self.assertRaises(ValueError):
                sample_time_parts(stamp, now)

    def test_microsecond_precision(self):
        from drone_integration.px4_clock import sample_time_parts
        self.assertEqual(sample_time_parts(1800000000123456, 1800000000123456000),
                         (1800000000, 123456000))


if __name__ == '__main__':
    unittest.main()
