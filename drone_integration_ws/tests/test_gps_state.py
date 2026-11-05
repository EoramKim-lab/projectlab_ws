"""Offline validation tests for PX4 v1.16 GPS/EKF navigation gates."""
from types import SimpleNamespace as NS
import unittest
from drone_integration.navigation.gps_state import (
    gps_quality_reasons, local_position_reasons, gnss_aided)


class GpsStateTests(unittest.TestCase):
    def good_gps(self, **changes):
        values = dict(FIX_TYPE_3D=3, fix_type=3, satellites_used=10,
                      eph=1.2, epv=2.0)
        values.update(changes)
        return NS(**values)

    def good_local(self, **changes):
        values = dict(xy_valid=True, z_valid=True, v_xy_valid=True,
                      v_z_valid=True, xy_global=True, dead_reckoning=False,
                      x=1.0, y=2.0, z=-1.0, vx=0.1, vy=0.2, vz=0.0,
                      ax=0.0, ay=0.0, az=0.0)
        values.update(changes)
        return NS(**values)

    def test_healthy_3d_gps(self):
        gps = self.good_gps()
        local = self.good_local()
        flags = NS(cs_gnss_pos=True)
        self.assertEqual(gps_quality_reasons(gps), [])
        self.assertEqual(local_position_reasons(local), [])
        self.assertTrue(gnss_aided(local, gps, [], flags))

    def test_rejects_no_3d_fix_and_low_satellite_count(self):
        gps = self.good_gps(fix_type=2, satellites_used=4)
        reasons = gps_quality_reasons(gps)
        self.assertIn('gps_no_3d_fix', reasons)
        self.assertIn('gps_too_few_satellites', reasons)

    def test_rejects_poor_accuracy(self):
        gps = self.good_gps(eph=7.0, epv=float('inf'))
        reasons = gps_quality_reasons(gps)
        self.assertIn('gps_horizontal_accuracy', reasons)
        self.assertIn('gps_vertical_accuracy', reasons)

    def test_rejects_invalid_or_dead_reckoning_ekf_state(self):
        local = self.good_local(xy_valid=False, dead_reckoning=True)
        reasons = local_position_reasons(local)
        self.assertIn('local_xy_invalid', reasons)
        self.assertIn('ekf_dead_reckoning_active', reasons)
        self.assertFalse(gnss_aided(local, self.good_gps(), [], NS(cs_gnss_pos=True)))

    def test_requires_global_reference(self):
        local = self.good_local(xy_global=False)
        self.assertIn('gnss_global_reference_invalid', local_position_reasons(local))

    def test_requires_ekf_gnss_fusion_flag(self):
        local = self.good_local()
        self.assertFalse(gnss_aided(local, self.good_gps(), [], NS(cs_gnss_pos=False)))


if __name__ == '__main__':
    unittest.main()
