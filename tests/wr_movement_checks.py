"""Physics checks for the separate Step 2 review module.

Run explicitly: python -m unittest discover -s tests -p wr_movement_checks.py -v
Kept outside the submission builder's test_*.py bundle until Step 5 integration.
"""
import unittest

import numpy as np
import pandas as pd

from src.kinematics import decompose
from src.wr_movement import summarize_trace


def track(x, y):
    frame = pd.DataFrame({'x': x, 'y': y, 'time': pd.date_range('2023-01-01', periods=len(x), freq='100ms')})
    return frame.assign(**{k:v for k,v in decompose(x, y).items() if k in ['sp', 'a_lon', 'a_lat', 'curv']})


class MovementPhysicsChecks(unittest.TestCase):
    def test_straight_motion_has_speed_without_lateral_acceleration(self):
        t = np.arange(80)*.1
        d = decompose(4*t, np.zeros(len(t)))
        np.testing.assert_allclose(d['sp'][3:-3], 4., atol=1e-10)
        np.testing.assert_allclose(d['a_lat'][3:-3], 0., atol=1e-10)

    def test_known_circle_separates_speed_and_curvature(self):
        t, radius = np.arange(100)*.1, 12.
        values = []
        for speed in [2., 4.]:
            d = decompose(radius*np.cos(speed*t/radius), radius*np.sin(speed*t/radius))
            np.testing.assert_allclose(d['sp'][3:-3], speed, rtol=.01)
            np.testing.assert_allclose(np.abs(d['curv'][3:-3]), 1/radius, rtol=.01)
            np.testing.assert_allclose(np.abs(d['a_lat'][3:-3]), speed**2/radius, rtol=.01)
            values.append(np.median(np.abs(d['a_lat'][3:-3])))
        self.assertAlmostEqual(values[1]/values[0], 4., delta=.04)

    def test_rigid_coordinate_changes_preserve_local_motion(self):
        t = np.arange(90)*.1
        x, y = 7*np.cos(.35*t), 7*np.sin(.35*t)
        base = summarize_trace(track(x, y))
        theta = .73
        changed = summarize_trace(track(x*np.cos(theta)-y*np.sin(theta)+20,
                                        x*np.sin(theta)+y*np.cos(theta)-13))
        # Circular motion has near-tied peaks; assess physical values, not their arbitrary times.
        for key in ['full_attempt_turn', 'peak_speed', 'peak_absolute_lateral_acceleration', 'peak_absolute_curvature']:
            np.testing.assert_allclose(base[key], changed[key], atol=1e-10, rtol=1e-10)

    def test_irregular_cadence_cannot_produce_local_summaries(self):
        t = np.arange(30)*.1
        f = track(t*3, t*t*.1)
        f.loc[10, 'time'] += pd.Timedelta(milliseconds=20)
        with self.assertRaisesRegex(ValueError, 'cadence'):
            summarize_trace(f)


if __name__ == '__main__':
    unittest.main()
