#!/usr/bin/env python3
"""
===============================================================================
FIRESPRAY-31 (SLAVE I) COCKPIT AVIONICS & DIAGNOSTICS CONSOLE
Sub-Layer Seed: Lone Ranger | Architecture: Kuat Systems Engineering
===============================================================================
"""

import sys
import time
from cockpit import SlaveOneCockpit, CockpitRenderer, BlackboxFlightRecorder

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"


def run_playback_mode(logfile_path="slave1_blackbox_log.json"):
    """Interactive visual playback engine for the blackbox log."""
    data = BlackboxFlightRecorder.load_from_disk(logfile_path)
    if not data:
        print(f"{RED}No valid blackbox log found at '{logfile_path}'. Run flight operations first.{RESET}")
        time.sleep(2)
        return

    snapshots = data.get("snapshots", [])
    if not snapshots:
        print(f"{YELLOW}Blackbox log contains no telemetry snapshots.{RESET}")
        time.sleep(2)
        return

    idx = 0
    total = len(snapshots)

    while True:
        CockpitRenderer.render_snapshot_hud(snapshots[idx], idx, total)
        print(f"\n{BOLD}PLAYBACK CONTROLS:{RESET}")
        print(f" {CYAN}[N]{RESET} Next Frame   {CYAN}[P]{RESET} Prev Frame   {CYAN}[A]{RESET} Auto-Play All   {CYAN}[R]{RESET} Restart (Frame 1)   {CYAN}[Q]{RESET} Exit Replay")

        choice = input(f"\n{BOLD}Playback Action > {RESET}").strip().upper()

        if choice == "N":
            if idx < total - 1:
                idx += 1
            else:
                print(f"{YELLOW}End of recorded telemetry reached.{RESET}")
                time.sleep(1)
        elif choice == "P":
            if idx > 0:
                idx -= 1
        elif choice == "A":
            speed = 0.8
            for auto_i in range(idx, total):
                CockpitRenderer.render_snapshot_hud(snapshots[auto_i], auto_i, total)
                print(f"\n{MAGENTA}{BOLD}>>> AUTO-PLAYING FLIGHT TELEMETRY ({auto_i + 1}/{total}) - Press Ctrl+C to pause <<<{RESET}")
                time.sleep(speed)
            idx = total - 1
            print(f"\n{GREEN}Playback sequence complete.{RESET}")
            time.sleep(1.5)
        elif choice == "R":
            idx = 0
        elif choice == "Q":
            break


def interactive_loop():
    cockpit = SlaveOneCockpit()

    while True:
        cockpit.render()
        print(f"\n{BOLD}TACTICAL COCKPIT DIALS & COMMANDS:{RESET}")
        print(f" {CYAN}[T]{RESET} {BOLD}IGNITE & ENGAGE TRANSIT (One-Click Launch & 90° Pivot){RESET}")
        print(f" {CYAN}[M]{RESET} Execute Top-Priority Alert Mitigation")
        print(f" {CYAN}[1]{RESET} Trigger Fault: Reactor Thermal Spike (680 K)")
        print(f" {CYAN}[2]{RESET} Trigger Fault: Stealth Baffle Saturation (96%)")
        print(f" {CYAN}[3]{RESET} Trigger Fault: Interdictor Mass-Shadow Field")
        print(f" {CYAN}[4]{RESET} Trigger Fault: Seismic Ordnance Chute Jam")
        print(f" {CYAN}[P]{RESET} {BOLD}VISUAL PLAYBACK MODE (Replay Blackbox Flight Log){RESET}")
        print(f" {CYAN}[S]{RESET} Force Export / Flush Blackbox Telemetry Log")
        print(f" {CYAN}[C]{RESET} Clear & Normalize All System Telemetry")
        print(f" {CYAN}[Q]{RESET} Disembark Cockpit")

        choice = input(f"\n{BOLD}Select Command > {RESET}").strip().upper()

        if choice == "T":
            cockpit.trigger_one_click_transit()
        elif choice == "M":
            if cockpit.alerts:
                top_alert = cockpit.alerts[0]
                cockpit.execute_mitigation(top_alert.id)
            else:
                cockpit.add_log("No active alerts to mitigate.")
        elif choice == "P":
            cockpit.save_blackbox_log()
            run_playback_mode(cockpit.flight_recorder_file)
        elif choice == "1":
            cockpit.core_temp_k = 685.0
            cockpit.add_log("FAULT INJECTED: Reactor coolant valve failure.")
        elif choice == "2":
            cockpit.baffle_saturation = 96.5
            cockpit.add_log("FAULT INJECTED: Thermal sink baffles reached threshold.")
        elif choice == "3":
            cockpit.mass_shadow_detected = True
            cockpit.hyperdrive_status = "INTERLOCKED"
            cockpit.add_log("FAULT INJECTED: Imperial Interdictor mass-shadow detected.")
        elif choice == "4":
            cockpit.seismic_chute_status = "MISFIRE_JAM"
            cockpit.add_log("FAULT INJECTED: Seismic charge 2 lodged in chute.")
        elif choice == "S":
            cockpit.save_blackbox_log()
            cockpit.add_log(f"Blackbox log saved -> {cockpit.flight_recorder_file}")
        elif choice == "C":
            cockpit.core_temp_k = 418.0
            cockpit.baffle_saturation = 12.0
            cockpit.mass_shadow_detected = False
            cockpit.hyperdrive_status = "READY"
            cockpit.seismic_chute_status = "LOCKED"
            cockpit.orientation = "HORIZONTAL (Landing)"
            cockpit.thrust_percent = 0
            cockpit.add_log("Telemetry reset to cold-dock parameters.")
        elif choice == "Q":
            cockpit.save_blackbox_log()
            print(f"\n{GREEN}Flight telemetry successfully logged to '{cockpit.flight_recorder_file}'.{RESET}")
            print(f"{GREEN}Disembarking Slave I cockpit. Powering down HUD.{RESET}\n")
            break
        else:
            cockpit.add_log(f"Invalid input [{choice}]. Dial unmapped.")


if __name__ == "__main__":
    try:
        if "--replay" in sys.argv:
            run_playback_mode()
        else:
            interactive_loop()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Emergency Cockpit Override Disengaged.{RESET}")
        sys.exit(0)
