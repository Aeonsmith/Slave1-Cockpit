"""
Blackbox telemetry recording and persistence subsystem.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .models import TelemetrySnapshot, BlackboxLogPayload, FlightState, StealthSensorState, WeaponsState, CockpitAlert
from dataclasses import asdict


class BlackboxFlightRecorder:
    def __init__(self, log_filepath: str = "slave1_blackbox_log.json"):
        self.log_filepath = log_filepath
        self.snapshots: List[TelemetrySnapshot] = []

    def record_snapshot(
        self,
        trigger_event: str,
        flight: FlightState,
        stealth: StealthSensorState,
        weapons: WeaponsState,
        alerts: List[CockpitAlert],
    ) -> TelemetrySnapshot:
        snapshot = TelemetrySnapshot(
            timestamp=datetime.now().isoformat(),
            trigger_event=trigger_event,
            flight_telemetry={
                "orientation": flight.orientation,
                "gyro_locked": flight.gyro_locked,
                "transit_engaged": flight.transit_engaged,
                "thrust_percent": flight.thrust_percent,
                "hyperdrive_status": flight.hyperdrive_status,
                "core_temp_kelvin": round(flight.core_temp_k, 2),
            },
            stealth_and_sensors={
                "iff_ident": stealth.iff_ident,
                "baffle_saturation_percent": round(stealth.baffle_saturation_percent, 2),
                "stealth_mode": stealth.stealth_mode,
                "mass_shadow_detected": stealth.mass_shadow_detected,
                "contacts_in_range": stealth.contacts_in_range,
                "sensor_mode": stealth.sensor_mode,
            },
            weapons_and_ordnance={
                "blasters_armed": weapons.blasters_armed,
                "concussion_missiles": weapons.concussion_missiles,
                "seismic_charges": weapons.seismic_charges,
                "seismic_chute_status": weapons.seismic_chute_status,
                "tractor_beam": weapons.tractor_beam,
            },
            active_alerts=[a.to_dict() for a in alerts],
        )
        self.snapshots.append(snapshot)
        return snapshot

    def save_to_disk(self, event_logs: List[str]) -> bool:
        payload = BlackboxLogPayload(
            vessel="Firespray-31 (Slave I)",
            sub_layer_seed="Lone Ranger",
            last_updated=datetime.now().isoformat(),
            total_snapshots=len(self.snapshots),
            snapshots=[s.to_dict() for s in self.snapshots],
            recent_event_log=list(event_logs),
        )
        try:
            with open(self.log_filepath, "w", encoding="utf-8") as f:
                json.dump(payload.to_dict(), f, indent=2)
            return True
        except Exception:
            return False

    @staticmethod
    def load_from_disk(filepath: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
