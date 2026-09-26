"""
Core cockpit state coordinator and high-level flight state machine.
"""

from datetime import datetime
from typing import List, Optional
from .models import FlightState, StealthSensorState, WeaponsState, CockpitAlert
from .diagnostics import DiagnosticsEngine
from .blackbox import BlackboxFlightRecorder
from .renderer import CockpitRenderer


class SlaveOneCockpit:
    def __init__(self, blackbox_filepath: str = "slave1_blackbox_log.json"):
        self.flight = FlightState()
        self.stealth = StealthSensorState()
        self.weapons = WeaponsState()
        self.diagnostics_engine = DiagnosticsEngine()
        self.blackbox = BlackboxFlightRecorder(blackbox_filepath)
        self.renderer = CockpitRenderer()

        self.alerts: List[CockpitAlert] = []
        self.event_log: List[str] = [
            f"[{datetime.now().strftime('%H:%M:%S')}] Avionics cold-start complete.",
            f"[{datetime.now().strftime('%H:%M:%S')}] Gyro-gimbal ring initialized in 0° landing mode.",
            f"[{datetime.now().strftime('%H:%M:%S')}] Lone Ranger sub-layer seed active.",
            f"[{datetime.now().strftime('%H:%M:%S')}] Blackbox flight recorder online.",
        ]
        self.record_snapshot("SYSTEM_INITIALIZED")

    # Property aliases for backward compatibility & convenience
    @property
    def orientation(self) -> str:
        return self.flight.orientation

    @orientation.setter
    def orientation(self, value: str):
        self.flight.orientation = value

    @property
    def gyro_locked(self) -> bool:
        return self.flight.gyro_locked

    @gyro_locked.setter
    def gyro_locked(self, value: bool):
        self.flight.gyro_locked = value

    @property
    def transit_engaged(self) -> bool:
        return self.flight.transit_engaged

    @transit_engaged.setter
    def transit_engaged(self, value: bool):
        self.flight.transit_engaged = value

    @property
    def thrust_percent(self) -> int:
        return self.flight.thrust_percent

    @thrust_percent.setter
    def thrust_percent(self, value: int):
        self.flight.thrust_percent = value

    @property
    def hyperdrive_status(self) -> str:
        return self.flight.hyperdrive_status

    @hyperdrive_status.setter
    def hyperdrive_status(self, value: str):
        self.flight.hyperdrive_status = value

    @property
    def core_temp_k(self) -> float:
        return self.flight.core_temp_k

    @core_temp_k.setter
    def core_temp_k(self, value: float):
        self.flight.core_temp_k = value

    @property
    def baffle_saturation(self) -> float:
        return self.stealth.baffle_saturation_percent

    @baffle_saturation.setter
    def baffle_saturation(self, value: float):
        self.stealth.baffle_saturation_percent = value

    @property
    def mass_shadow_detected(self) -> bool:
        return self.stealth.mass_shadow_detected

    @mass_shadow_detected.setter
    def mass_shadow_detected(self, value: bool):
        self.stealth.mass_shadow_detected = value

    @property
    def seismic_chute_status(self) -> str:
        return self.weapons.seismic_chute_status

    @seismic_chute_status.setter
    def seismic_chute_status(self, value: str):
        self.weapons.seismic_chute_status = value

    @property
    def flight_recorder_file(self) -> str:
        return self.blackbox.log_filepath

    @flight_recorder_file.setter
    def flight_recorder_file(self, value: str):
        self.blackbox.log_filepath = value

    @property
    def telemetry_history(self):
        return [s.to_dict() for s in self.blackbox.snapshots]

    def add_log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.event_log.insert(0, f"[{timestamp}] {message}")
        if len(self.event_log) > 6:
            self.event_log.pop()
        self.record_snapshot(message)

    def run_diagnostics(self) -> List[CockpitAlert]:
        self.alerts = self.diagnostics_engine.evaluate(self.flight, self.stealth, self.weapons)
        return self.alerts

    def record_snapshot(self, trigger_event: str) -> None:
        self.blackbox.record_snapshot(
            trigger_event=trigger_event,
            flight=self.flight,
            stealth=self.stealth,
            weapons=self.weapons,
            alerts=self.alerts,
        )
        self.save_blackbox_log()

    def save_blackbox_log(self) -> bool:
        return self.blackbox.save_to_disk(self.event_log)

    def trigger_one_click_transit(self) -> None:
        """One-click instant transit with automated 90° attitude transition."""
        self.add_log("ONE-CLICK TRANSIT ENGAGED.")
        if self.flight.orientation == "HORIZONTAL (Landing)":
            self.add_log("Gimbal ring rotation: 0° -> 90° VERTICAL FLIGHT.")
            self.flight.orientation = "VERTICAL (Flight)"
            self.flight.thrust_percent = 100
            self.flight.transit_engaged = True
            self.flight.core_temp_k += 45.0
            self.add_log("KSE F-31 sublight engines firing at full vector.")
        else:
            self.add_log("Ship already in flight orientation. Spooling sublight burn.")
            self.flight.thrust_percent = 100
            self.flight.transit_engaged = True

    def execute_mitigation(self, alert_id: str) -> bool:
        target = next((a for a in self.alerts if a.id == alert_id), None)
        if not target:
            return False

        log_msg = self.diagnostics_engine.apply_mitigation(target, self.flight, self.stealth, self.weapons)
        self.add_log(log_msg)
        self.run_diagnostics()
        return True

    def render(self) -> None:
        self.run_diagnostics()
        self.renderer.render_active_hud(
            self.flight,
            self.stealth,
            self.weapons,
            self.alerts,
            self.event_log,
        )
