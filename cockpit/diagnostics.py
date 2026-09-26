"""
Diagnostics and rule evaluation engine for the Firespray-31 cockpit.
"""

from typing import List, Tuple
from .models import CockpitAlert, FlightState, StealthSensorState, WeaponsState


class DiagnosticsEngine:
    """Evaluates telemetry states and computes active alerts and triage actions."""

    @staticmethod
    def evaluate(
        flight: FlightState,
        stealth: StealthSensorState,
        weapons: WeaponsState,
    ) -> List[CockpitAlert]:
        alerts: List[CockpitAlert] = []

        # 1. Reactor Core Temp
        if flight.core_temp_k > 650.0:
            alerts.append(
                CockpitAlert(
                    id="FLT-RCT-01",
                    severity="EMERGENCY",
                    subsystem="REACTOR",
                    headline="REACTOR CONTAINMENT OVERHEAT",
                    action="VENT_CORE",
                    label="VENT REACTOR COOLANT",
                )
            )
        elif flight.core_temp_k > 530.0:
            alerts.append(
                CockpitAlert(
                    id="FLT-RCT-02",
                    severity="CAUTION",
                    subsystem="REACTOR",
                    headline="ELEVATED CORE TEMPERATURE",
                    action="THROTTLE_DOWN",
                    label="REDUCE THRUST DEMAND",
                )
            )

        # 2. Stealth Baffle Saturation
        if stealth.baffle_saturation_percent >= 90.0:
            alerts.append(
                CockpitAlert(
                    id="FLT-STL-03",
                    severity="CRITICAL",
                    subsystem="STEALTH",
                    headline="HEAT BAFFLE SATURATED (BLOOM IMMINENT)",
                    action="FLUSH_BAFFLES",
                    label="DUMP HEAT INTO WAKE",
                )
            )

        # 3. Mass-Shadow Interlock
        if stealth.mass_shadow_detected:
            alerts.append(
                CockpitAlert(
                    id="FLT-NAV-04",
                    severity="CRITICAL",
                    subsystem="PROPULSION",
                    headline="MASS-SHADOW HYPERDRIVE LOCK",
                    action="OVERRIDE_JUMP",
                    label="FORCE BLIND MICRO-JUMP",
                )
            )

        # 4. Ordnance Chute Jam
        if weapons.seismic_chute_status == "MISFIRE_JAM":
            alerts.append(
                CockpitAlert(
                    id="FLT-WPN-09",
                    severity="CRITICAL",
                    subsystem="WEAPONS",
                    headline="SEISMIC CHUTE DISCHARGE FAILURE",
                    action="CLEAR_CHUTE",
                    label="PURGE VENTRAL PNEUMATICS",
                )
            )

        return alerts

    @staticmethod
    def apply_mitigation(
        alert: CockpitAlert,
        flight: FlightState,
        stealth: StealthSensorState,
        weapons: WeaponsState,
    ) -> str:
        """Applies tactical triage to alleviate the given alert."""
        action = alert.action
        if action == "VENT_CORE":
            flight.core_temp_k = 420.0
            return "MITIGATION: High-pressure coolant vented. Core temp normalized."
        elif action == "THROTTLE_DOWN":
            flight.thrust_percent = 40
            flight.core_temp_k = 440.0
            return "MITIGATION: Propulsion dialed down to 40%. Core cooled."
        elif action == "FLUSH_BAFFLES":
            stealth.baffle_saturation_percent = 10.0
            return "MITIGATION: Stealth baffles flushed into sublight exhaust stream."
        elif action == "OVERRIDE_JUMP":
            stealth.mass_shadow_detected = False
            flight.hyperdrive_status = "DISCHARGED"
            return "MITIGATION: Silver-Bullet blind micro-jump executed. Shadow cleared."
        elif action == "CLEAR_CHUTE":
            weapons.seismic_chute_status = "LOCKED"
            return "MITIGATION: Pneumatic burst cleared jammed ordnance clamps."
        return f"MITIGATION: Unhandled action {action}."
