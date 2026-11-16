"""Offline tests that do not require Streamlit or physical hardware."""

import unittest

from simulator.control import ControlSettings, simulate_step
from simulator.run_demo import replay_scenario
from pathlib import Path


class TestControlSimulation(unittest.TestCase):
    def setUp(self):
        self.settings = ControlSettings()

    def test_high_force_inflates_once(self):
        result = simulate_step(320, 30, 0, self.settings)
        self.assertEqual((result.pump_action, result.inflation_ticks), ("INFLATE", 1))

    def test_low_force_deflates_once(self):
        result = simulate_step(280, 30, 4, self.settings)
        self.assertEqual((result.pump_action, result.inflation_ticks), ("DEFLATE", 3))

    def test_deadband_leaves_inflation_unchanged(self):
        result = simulate_step(300, 18, 4, self.settings)
        self.assertEqual((result.pump_action, result.inflation_ticks), ("IDLE", 4))

    def test_never_exceeds_cap(self):
        result = simulate_step(1000, 8, self.settings.max_inflation_ticks, self.settings)
        self.assertEqual((result.pump_action, result.inflation_ticks),
                         ("IDLE", self.settings.max_inflation_ticks))

    def test_never_deflates_below_zero(self):
        result = simulate_step(0, 30, 0, self.settings)
        self.assertEqual((result.pump_action, result.inflation_ticks), ("IDLE", 0))

    def test_water_distance_bands(self):
        self.assertEqual(simulate_step(300, 10.0, 0).louver_angle_deg, 90)
        self.assertEqual(simulate_step(300, 20.0, 0).louver_angle_deg, 45)
        self.assertEqual(simulate_step(300, 20.01, 0).louver_angle_deg, 0)

    def test_missing_or_invalid_distance_emits_no_angle(self):
        for value in [None, 0, -4, float("nan"), float("inf")]:
            with self.subTest(value=value):
                self.assertIsNone(simulate_step(300, value, 0).louver_angle_deg)

    def test_invalid_force_rejected(self):
        for value in [-1, 1024, 300.5, True]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    simulate_step(value, 10, 0)

    def test_invalid_settings_rejected(self):
        with self.assertRaises(ValueError):
            ControlSettings(force_low=400, force_high=320)

    def test_sample_sequence_is_reproducible(self):
        scenario = Path(__file__).resolve().parents[1] / "samples" / "scenario.csv"
        results = list(replay_scenario(scenario))
        self.assertEqual(len(results), 11)
        self.assertEqual(results[0].pump_action, "IDLE")
        self.assertEqual(results[1].pump_action, "INFLATE")
        self.assertEqual(results[3].louver_angle_deg, 90)
        self.assertIsNone(results[7].louver_angle_deg)
        self.assertEqual(results[-1].inflation_ticks, 0)


if __name__ == "__main__":
    unittest.main()
