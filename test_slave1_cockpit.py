#!/usr/bin/env python3
"""
Unit test suite for Firespray-31 (Slave I) Cockpit Diagnostics,
Telemetry Blackbox Logging, and Playback subsystems.
"""

import os
import json
import unittest
from slave1_cockpit import SlaveOneCockpit


class TestSlaveOneCockpit(unittest.TestCase):
    def setUp(self):
        self.test_log_file = "test_slave1_blackbox.json"
        self.cockpit = SlaveOneCockpit()
        self.cockpit.flight_recorder_file = self.test_log_file

    def tearDown(self):
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def test_initial_state(self):
        """Verify baseline cockpit state and default orientation."""
        self.assertEqual(self.cockpit.orientation, "HORIZONTAL (Landing)")
        self.assertTrue(self.cockpit.gyro_locked)
        self.assertFalse(self.cockpit.transit_engaged)
        self.assertEqual(self.cockpit.thrust_percent, 0)
        self.assertEqual(self.cockpit.hyperdrive_status, "READY")
        self.assertGreater(len(self.cockpit.telemetry_history), 0)

    def test_one_click_transit(self):
        """Verify 90-degree gyroscopic pivot and full propulsion engagement."""
        self.cockpit.trigger_one_click_transit()
        self.assertEqual(self.cockpit.orientation, "VERTICAL (Flight)")
        self.assertEqual(self.cockpit.thrust_percent, 100)
        self.assertTrue(self.cockpit.transit_engaged)
        self.assertGreater(self.cockpit.core_temp_k, 418.0)

        # Check recorded snapshot
        latest = self.cockpit.telemetry_history[-1]
        self.assertEqual(latest["trigger_event"], "KSE F-31 sublight engines firing at full vector.")
        self.assertEqual(latest["flight_telemetry"]["orientation"], "VERTICAL (Flight)")
        self.assertEqual(latest["flight_telemetry"]["thrust_percent"], 100)

    def test_diagnostics_reactor_overheat_and_mitigation(self):
        """Verify EMERGENCY alert triggering and coolant vent mitigation."""
        self.cockpit.core_temp_k = 680.0
        self.cockpit.run_diagnostics()

        self.assertEqual(len(self.cockpit.alerts), 1)
        alert = self.cockpit.alerts[0]
        self.assertEqual(alert.id, "FLT-RCT-01")
        self.assertEqual(alert.severity, "EMERGENCY")

        # Execute Mitigation
        self.cockpit.execute_mitigation("FLT-RCT-01")
        self.assertLessEqual(self.cockpit.core_temp_k, 420.0)
        self.assertEqual(len(self.cockpit.alerts), 0)

    def test_diagnostics_baffle_saturation_and_mitigation(self):
        """Verify CRITICAL baffle saturation alert and heat dump mitigation."""
        self.cockpit.baffle_saturation = 95.0
        self.cockpit.run_diagnostics()

        self.assertEqual(len(self.cockpit.alerts), 1)
        self.assertEqual(self.cockpit.alerts[0].id, "FLT-STL-03")

        # Mitigate
        self.cockpit.execute_mitigation("FLT-STL-03")
        self.assertEqual(self.cockpit.baffle_saturation, 10.0)
        self.assertEqual(len(self.cockpit.alerts), 0)

    def test_diagnostics_mass_shadow_interlock_and_mitigation(self):
        """Verify Imperial Interdictor mass-shadow detection and blind jump override."""
        self.cockpit.mass_shadow_detected = True
        self.cockpit.hyperdrive_status = "INTERLOCKED"
        self.cockpit.run_diagnostics()

        self.assertEqual(len(self.cockpit.alerts), 1)
        self.assertEqual(self.cockpit.alerts[0].id, "FLT-NAV-04")

        # Mitigate
        self.cockpit.execute_mitigation("FLT-NAV-04")
        self.assertFalse(self.cockpit.mass_shadow_detected)
        self.assertEqual(self.cockpit.hyperdrive_status, "DISCHARGED")
        self.assertEqual(len(self.cockpit.alerts), 0)

    def test_blackbox_log_persistence_and_replay_data(self):
        """Verify structured JSON serialization and deserialization for visual replay."""
        # Perform flight maneuvers
        self.cockpit.trigger_one_click_transit()
        self.cockpit.baffle_saturation = 92.0
        self.cockpit.add_log("Approaching asteroid field stealth vector.")
        self.cockpit.save_blackbox_log()

        self.assertTrue(os.path.exists(self.test_log_file))

        with open(self.test_log_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["vessel"], "Firespray-31 (Slave I)")
        self.assertEqual(data["sub_layer_seed"], "Lone Ranger")
        self.assertIn("snapshots", data)
        self.assertGreaterEqual(len(data["snapshots"]), 2)

        # Verify snapshot schema structure
        first_frame = data["snapshots"][0]
        self.assertIn("timestamp", first_frame)
        self.assertIn("flight_telemetry", first_frame)
        self.assertIn("stealth_and_sensors", first_frame)
        self.assertIn("weapons_and_ordnance", first_frame)
        self.assertIn("active_alerts", first_frame)


if __name__ == "__main__":
    unittest.main()
