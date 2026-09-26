"""
Core data models and type definitions for the Firespray-31 cockpit.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class FlightState:
    orientation: str = "HORIZONTAL (Landing)"  # "HORIZONTAL (Landing)" | "VERTICAL (Flight)"
    gyro_locked: bool = True
    transit_engaged: bool = False
    thrust_percent: int = 0
    hyperdrive_status: str = "READY"  # READY, CHARGING, DISCHARGING, INTERLOCKED
    core_temp_k: float = 418.0
    boost_armed: bool = True


@dataclass
class StealthSensorState:
    iff_ident: str = "CIVILIAN_HAULER_489"
    baffle_saturation_percent: float = 12.0
    stealth_mode: str = "SILENT_RUNNING"  # SILENT_RUNNING, CRUISE, HOT_COMBAT
    mass_shadow_detected: bool = False
    contacts_in_range: int = 2
    sensor_mode: str = "PASSIVE_GRAVIMETRIC"


@dataclass
class WeaponsState:
    blasters_armed: bool = True
    concussion_missiles: int = 6
    seismic_charges: int = 4
    seismic_chute_status: str = "LOCKED"  # LOCKED, PRIMED, MISFIRE_JAM
    tractor_beam: bool = False


@dataclass
class CockpitAlert:
    id: str
    severity: str  # ADVISORY, CAUTION, CRITICAL, EMERGENCY
    subsystem: str
    headline: str
    action: str
    label: str

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TelemetrySnapshot:
    timestamp: str
    trigger_event: str
    flight_telemetry: Dict[str, Any]
    stealth_and_sensors: Dict[str, Any]
    weapons_and_ordnance: Dict[str, Any]
    active_alerts: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BlackboxLogPayload:
    vessel: str = "Firespray-31 (Slave I)"
    sub_layer_seed: str = "Lone Ranger"
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    total_snapshots: int = 0
    snapshots: List[Dict[str, Any]] = field(default_factory=list)
    recent_event_log: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
