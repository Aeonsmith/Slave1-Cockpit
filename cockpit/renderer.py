"""
ANSI UI and HUD rendering routines for active flights and blackbox replay.
"""

import os
from typing import List, Dict, Any
from .models import FlightState, StealthSensorState, WeaponsState, CockpitAlert

# ANSI Palette
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
BG_RED = "\033[41m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"


class CockpitRenderer:
    @staticmethod
    def render_active_hud(
        flight: FlightState,
        stealth: StealthSensorState,
        weapons: WeaponsState,
        alerts: List[CockpitAlert],
        event_logs: List[str],
    ) -> None:
        os.system("cls" if os.name == "nt" else "clear")

        has_emergency = any(a.severity == "EMERGENCY" for a in alerts)
        has_critical = any(a.severity == "CRITICAL" for a in alerts)
        has_caution = any(a.severity == "CAUTION" for a in alerts)

        if has_emergency:
            annunciator = f"{BG_RED}{WHITE}{BOLD} [ ! ] MASTER EMERGENCY: CRITICAL CONTAINMENT THREAT {RESET}"
        elif has_critical:
            annunciator = f"{BG_RED}{WHITE}{BOLD} [ ! ] MASTER WARNING: ACTIVE SYSTEM FAULT DETECTED {RESET}"
        elif has_caution:
            annunciator = f"{BG_YELLOW}{WHITE}{BOLD} [ * ] MASTER CAUTION: ANOMALOUS TELEMETRY {RESET}"
        else:
            annunciator = f"{GREEN}{BOLD} [ OK ] ALL SYSTEMS NOMINAL - READY FOR DEPARTURE {RESET}"

        print(f"{CYAN}╔══════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{CYAN}║{RESET}  {BOLD}KUAT SYSTEMS ENGINEERING // FIRESPRAY-31 [SLAVE I]{RESET}        {MAGENTA}SEED: LONE RANGER{RESET}       {CYAN}║{RESET}")
        print(f"{CYAN}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{CYAN}║{RESET}  {annunciator:<92} {CYAN}║{RESET}")
        print(f"{CYAN}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

        # Flight & Propulsion Box
        print(f"{CYAN}║{RESET} {BOLD}FLIGHT & PROPULSION{RESET}                               {BOLD}STEALTH & SENSORS{RESET}                     {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET}   - Orientation: {YELLOW}{flight.orientation:<24}{RESET}    - IFF Ghost: {WHITE}{stealth.iff_ident:<22}{RESET} {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET}   - Thrust:      {GREEN}{flight.thrust_percent}%{RESET}                            - Baffles:   {YELLOW}{stealth.baffle_saturation_percent:.1f}% Saturation{RESET}           {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET}   - Core Temp:   {RED if flight.core_temp_k > 530 else GREEN}{flight.core_temp_k:.1f} K{RESET}                       - Mode:      {CYAN}{stealth.stealth_mode:<22}{RESET} {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET}   - Hyperdrive:  {GREEN if flight.hyperdrive_status == 'READY' else RED}{flight.hyperdrive_status:<24}{RESET}    - Contacts:  {WHITE}{stealth.contacts_in_range} targets in range{RESET}       {CYAN}║{RESET}")
        print(f"{CYAN}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

        # Weapons
        print(f"{CYAN}║{RESET} {BOLD}TACTICAL WEAPONS ARRAY{RESET}                                                                {CYAN}║{RESET}")
        blaster_str = "SYNCED & ARMED" if weapons.blasters_armed else "STANDBY"
        print(f"{CYAN}║{RESET}   - Twin Rotary Blasters: {GREEN if weapons.blasters_armed else DIM}{blaster_str:<42}{RESET}  {CYAN}║{RESET}")
        print(f"{CYAN}║{RESET}   - Concussion Tubes:     {WHITE}{weapons.concussion_missiles}/6 Missiles Ready{RESET}                                            {CYAN}║{RESET}")
        chute_col = RED if "JAM" in weapons.seismic_chute_status else GREEN
        print(f"{CYAN}║{RESET}   - Seismic Chute:        {chute_col}{weapons.seismic_charges}/4 Charges [{weapons.seismic_chute_status}]{RESET}                                  {CYAN}║{RESET}")
        print(f"{CYAN}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

        # Diagnostics Table
        print(f"{CYAN}║{RESET} {BOLD}ACTIVE DIAGNOSTIC FAULTS & TRIAGE GATES{RESET}                                                {CYAN}║{RESET}")
        if not alerts:
            print(f"{CYAN}║{RESET}   {DIM}No active alerts. Diagnostic bus clear.{RESET}                                              {CYAN}║{RESET}")
        else:
            for i, a in enumerate(alerts, 1):
                sev_color = RED if a.severity in ["EMERGENCY", "CRITICAL"] else YELLOW
                print(f"{CYAN}║{RESET}   [{i}] {sev_color}[{a.severity}]{RESET} {BOLD}{a.headline}{RESET}")
                print(f"{CYAN}║{RESET}       -> Mitigation Available: {CYAN}{BOLD}{a.label}{RESET}")

        print(f"{CYAN}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{CYAN}║{RESET} {BOLD}AVIONICS EVENT LOG{RESET}                                                                     {CYAN}║{RESET}")
        for log in event_logs[:4]:
            print(f"{CYAN}║{RESET}   {DIM}{log:<82}{RESET} {CYAN}║{RESET}")
        print(f"{CYAN}╚══════════════════════════════════════════════════════════════════════════════════════╝{RESET}")

    @staticmethod
    def render_snapshot_hud(snapshot: Dict[str, Any], current_idx: int, total_count: int) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        flight = snapshot.get("flight_telemetry", {})
        stealth = snapshot.get("stealth_and_sensors", {})
        weapons = snapshot.get("weapons_and_ordnance", {})
        alerts = snapshot.get("active_alerts", [])
        trigger = snapshot.get("trigger_event", "TELEMETRY_SAMPLE")
        timestamp = snapshot.get("timestamp", "")

        has_emergency = any(a.get("severity") == "EMERGENCY" for a in alerts)
        has_critical = any(a.get("severity") == "CRITICAL" for a in alerts)
        has_caution = any(a.get("severity") == "CAUTION" for a in alerts)

        if has_emergency:
            annunciator = f"{BG_RED}{WHITE}{BOLD} [ ! ] REPLAY EMERGENCY: CONTAINMENT THREAT {RESET}"
        elif has_critical:
            annunciator = f"{BG_RED}{WHITE}{BOLD} [ ! ] REPLAY WARNING: SYSTEM FAULT DETECTED {RESET}"
        elif has_caution:
            annunciator = f"{BG_YELLOW}{WHITE}{BOLD} [ * ] REPLAY CAUTION: ANOMALOUS TELEMETRY {RESET}"
        else:
            annunciator = f"{GREEN}{BOLD} [ OK ] REPLAY: TELEMETRY NOMINAL {RESET}"

        print(f"{MAGENTA}╔══════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{MAGENTA}║{RESET}  {BOLD}BLACKBOX VISUAL PLAYBACK // REPLAY FRAME [{current_idx + 1}/{total_count}]{RESET}           {CYAN}{timestamp}{RESET} {MAGENTA}║{RESET}")
        print(f"{MAGENTA}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{MAGENTA}║{RESET}  {annunciator:<92} {MAGENTA}║{RESET}")
        print(f"{MAGENTA}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

        print(f"{MAGENTA}║{RESET} {BOLD}FLIGHT & PROPULSION{RESET}                               {BOLD}STEALTH & SENSORS{RESET}                     {MAGENTA}║{RESET}")
        print(f"{MAGENTA}║{RESET}   - Orientation: {YELLOW}{flight.get('orientation', 'N/A'):<24}{RESET}    - IFF Ghost: {WHITE}{stealth.get('iff_ident', 'N/A'):<22}{RESET} {MAGENTA}║{RESET}")
        print(f"{MAGENTA}║{RESET}   - Thrust:      {GREEN}{flight.get('thrust_percent', 0)}%{RESET}                            - Baffles:   {YELLOW}{stealth.get('baffle_saturation_percent', 0.0):.1f}% Saturation{RESET}           {MAGENTA}║{RESET}")
        c_temp = flight.get("core_temp_kelvin", 0.0)
        print(f"{MAGENTA}║{RESET}   - Core Temp:   {RED if c_temp > 530 else GREEN}{c_temp:.1f} K{RESET}                       - Mode:      {CYAN}{stealth.get('stealth_mode', 'N/A'):<22}{RESET} {MAGENTA}║{RESET}")
        h_stat = flight.get("hyperdrive_status", "N/A")
        print(f"{MAGENTA}║{RESET}   - Hyperdrive:  {GREEN if h_stat == 'READY' else RED}{h_stat:<24}{RESET}    - Contacts:  {WHITE}{stealth.get('contacts_in_range', 0)} targets in range{RESET}       {MAGENTA}║{RESET}")
        print(f"{MAGENTA}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

        print(f"{MAGENTA}║{RESET} {BOLD}TACTICAL WEAPONS ARRAY{RESET}                                                                {MAGENTA}║{RESET}")
        blaster_str = "SYNCED & ARMED" if weapons.get("blasters_armed", False) else "STANDBY"
        print(f"{MAGENTA}║{RESET}   - Twin Rotary Blasters: {GREEN if weapons.get('blasters_armed', False) else DIM}{blaster_str:<42}{RESET}  {MAGENTA}║{RESET}")
        print(f"{MAGENTA}║{RESET}   - Concussion Tubes:     {WHITE}{weapons.get('concussion_missiles', 0)}/6 Missiles Ready{RESET}                                            {MAGENTA}║{RESET}")
        chute = weapons.get("seismic_chute_status", "N/A")
        print(f"{MAGENTA}║{RESET}   - Seismic Chute:        {RED if 'JAM' in chute else GREEN}{weapons.get('seismic_charges', 0)}/4 Charges [{chute}]{RESET}                                  {MAGENTA}║{RESET}")
        print(f"{MAGENTA}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

        print(f"{MAGENTA}║{RESET} {BOLD}RECORDED DIAGNOSTIC ALERTS AT FRAME{RESET}                                                   {MAGENTA}║{RESET}")
        if not alerts:
            print(f"{MAGENTA}║{RESET}   {DIM}No active alerts during this sample frame.{RESET}                                         {MAGENTA}║{RESET}")
        else:
            for i, a in enumerate(alerts, 1):
                sev_color = RED if a.get("severity") in ["EMERGENCY", "CRITICAL"] else YELLOW
                print(f"{MAGENTA}║{RESET}   [{i}] {sev_color}[{a.get('severity')}]{RESET} {BOLD}{a.get('headline')}{RESET}")
                print(f"{MAGENTA}║{RESET}       -> Logged Action: {CYAN}{BOLD}{a.get('label')}{RESET}")

        print(f"{MAGENTA}╠══════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{MAGENTA}║{RESET} {BOLD}TRIGGER EVENT FOR THIS FRAME:{RESET} {YELLOW}{BOLD}{trigger}{RESET}")
        print(f"{MAGENTA}╚══════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
