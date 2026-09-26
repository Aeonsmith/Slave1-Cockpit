# Firespray-31 (*Slave I*) Cockpit Avionics & Diagnostics Suite
> **Galactic Sub-Layer Seed**: `Lone Ranger` | **Avionics Architecture**: `Kuat Systems Engineering`

[![Firespray-31 Avionics CI](https://github.com/Aeonsmith/Slave1-Cockpit/actions/workflows/ci.yml/badge.svg)](https://github.com/Aeonsmith/Slave1-Cockpit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Modular](https://img.shields.io/badge/architecture-modular-brightgreen.svg)](ARCHITECTURE.md)

---

## 1. Project Overview & Purpose

The **Firespray-31 Cockpit Avionics Suite** is a terminal-based flight avionics, diagnostics, and telemetry management console designed for the iconic *Slave I* patrol craft.

Rooted in a **"one-click starship cockpit"** interaction model, the system removes unnecessary operational friction while providing the high-leverage tactical dials required of a galactic mastermind. You hop in, trigger departure, and the ship executes full flight kinematics—including the iconic 90-degree gyroscopic rotation from horizontal landing orientation to vertical flight posture.

### Core Philosophy
- **Frictionless Action**: Single-key flight ignition, automated gyro-attitude transitions, and instant one-touch emergency triage.
- **Bounty Hunter Flair**: Stealth thermal baffle controls, IFF multi-hop transponder spoofing, and ordnance chutes.
- **Galactic Sub-Layer Seed (`Lone Ranger`)**: Independent frontier resilience—zero external runtime dependencies, offline telemetry persistence, and emergency "Silver-Bullet" hyperdrive blind-jump overrides.

---

## 2. Key Subsystems & Features

| Subsystem | Description | Primary Controls |
| :--- | :--- | :--- |
| **Kinematic Flight Transit** | Automates the 90° cockpit rotation from landing posture to vertical attack flight, spooling the F-31 sublight engines to 100% vector thrust. | `[T]` |
| **Tactical Weapons Array** | Tracks twin rotary blasters, Dymek concussion missile tubes, and rear seismic charge chutes. | `[4]` (Simulate Jam) |
| **Stealth & Sensor Matrix** | Manages passive gravimetric sweeps, multi-hop transponder ghost IDs, and thermal baffle saturation. | `[2]` (Simulate Saturation) |
| **Diagnostic & Alert Bus** | Evaluates real-time telemetry against critical thresholds across 4 severity tiers (`ADVISORY`, `CAUTION`, `CRITICAL`, `EMERGENCY`). | `[1]`, `[3]`, `[M]` |
| **Blackbox Flight Recorder** | Serializes immutable, ISO-timestamped telemetry frames and event logs to disk (`slave1_blackbox_log.json`). | `[S]` (Flush) / `[Q]` (Auto-save) |
| **Visual Playback Engine** | Frame-by-frame (`[N]`/`[P]`) or automated (`[A]`) visual replay of recorded flights in ANSI Kuat HUD styling. | `[P]` or `--replay` |

---

## 3. Modular Architecture

```
Slave1-Cockpit/
├── ARCHITECTURE.md             # In-depth engineering specification
├── README.md                   # Comprehensive project documentation
├── CONTRIBUTING.md             # Community contribution & PR guidelines
├── LICENSE                     # MIT License
├── slave1_cockpit.py           # Interactive CLI entrypoint & flight loop
├── test_slave1_cockpit.py      # Automated unit test suite
├── slave1_blackbox_log.json    # Serialized blackbox flight log
└── cockpit/                    # Modular avionics package
    ├── __init__.py             # Public API exports
    ├── models.py               # Strongly typed dataclasses & schemas
    ├── core.py                 # SlaveOneCockpit state machine & coordinator
    ├── diagnostics.py          # Diagnostic evaluation & triage mitigation engine
    ├── blackbox.py             # Telemetry snapshot persistence manager
    └── renderer.py             # ANSI HUD & visual replay rendering engine
```

---

## 4. Installation & Requirements

### System Requirements
- **Python**: Version `3.8` or newer.
- **Dependencies**: None (Uses Python Standard Library exclusively: `os`, `sys`, `json`, `time`, `dataclasses`, `unittest`).
- **Terminal**: Any terminal supporting ANSI color sequences (PowerShell, Windows Terminal, Bash, Zsh, iTerm2).

### Clone & Setup
```powershell
# Clone the repository
git clone https://github.com/Aeonsmith/Slave1-Cockpit.git

# Enter project directory
cd Slave1-Cockpit
```

---

## 5. Usage & Operations

### 5.1 Launch Active Cockpit
```powershell
python slave1_cockpit.py
```

### 5.2 Interactive Command Reference
Once inside the cockpit HUD:
```
TACTICAL COCKPIT DIALS & COMMANDS:
 [T] IGNITE & ENGAGE TRANSIT (One-Click Launch & 90° Pivot)
 [M] Execute Top-Priority Alert Mitigation
 [1] Trigger Fault: Reactor Thermal Spike (680 K)
 [2] Trigger Fault: Stealth Baffle Saturation (96%)
 [3] Trigger Fault: Interdictor Mass-Shadow Field
 [4] Trigger Fault: Seismic Ordnance Chute Jam
 [P] VISUAL PLAYBACK MODE (Replay Blackbox Flight Log)
 [S] Force Export / Flush Blackbox Telemetry Log
 [C] Clear & Normalize All System Telemetry
 [Q] Disembark Cockpit
```

### 5.3 Launch Visual Playback Directly
To review previous flight telemetry without entering active flight mode:
```powershell
python slave1_cockpit.py --replay
```

**Playback Controls:**
- `[N]`: Advance to the next recorded frame.
- `[P]`: Step back to the previous frame.
- `[A]`: Auto-play all frames sequentially with live HUD rendering.
- `[R]`: Reset playback to frame 1.
- `[Q]`: Exit replay mode.

---

## 6. Programmatic API Integration

You can integrate the `cockpit` avionics package into external scripts or automated agents:

```python path=null start=null
from cockpit import SlaveOneCockpit

# Initialize cockpit avionics
ship = SlaveOneCockpit(blackbox_filepath="mission_log.json")

# 1. Trigger One-Click Transit (executes 90° attitude rotation & thrust burn)
ship.trigger_one_click_transit()
print(f"Attitude: {ship.orientation} | Thrust: {ship.thrust_percent}%")

# 2. Inject telemetry anomaly
ship.flight.core_temp_k = 690.0
alerts = ship.run_diagnostics()

for alert in alerts:
    print(f"[{alert.severity}] {alert.headline} -> Action: {alert.label}")

# 3. Execute Mastermind Mitigation
if alerts:
    ship.execute_mitigation(alerts[0].id)
    print(f"Normalized Core Temp: {ship.core_temp_k} K")

# 4. Save Blackbox Telemetry
ship.save_blackbox_log()
```

---

## 7. Running the Unit Test Suite

The project includes unit test coverage across state transitions, fault evaluations, and blackbox persistence:

```powershell
python -m unittest test_slave1_cockpit.py -v
```

**Test Matrix:**
- `test_initial_state`: Validates cold-dock landing parameters (0° horizontal).
- `test_one_click_transit`: Tests 90° gyroscopic orientation change and sublight thrust lock.
- `test_diagnostics_reactor_overheat_and_mitigation`: Tests emergency coolant venting.
- `test_diagnostics_baffle_saturation_and_mitigation`: Tests stealth heat wake flushing.
- `test_diagnostics_mass_shadow_interlock_and_mitigation`: Tests Silver-Bullet micro-jump bypass.
- `test_blackbox_log_persistence_and_replay_data`: Tests structured JSON serialization and replay frame integrity.

---

## 8. License & Attribution

- **License**: [MIT License](LICENSE) © 2026 Aeonsmith.
- **Lore Context**: Inspired by the *Firespray-31* class patrol vessel (*Slave I*) from *Star Wars* Canon & Legends (Kuat Systems Engineering).
