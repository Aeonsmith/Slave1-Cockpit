# Firespray-31 (*Slave I*) Cockpit Avionics Console
> **Sub-Layer Seed**: `Lone Ranger` | **Avionics**: `Kuat Systems Engineering`

An interactive, modular terminal cockpit simulation for the iconic *Firespray-31* class patrol craft (*Slave I*). Designed with a **"one-click starship cockpit"** philosophy—instant departure with automated 90° attitude rotation, tactile tactical dials, real-time diagnostic alerts, and blackbox telemetry playback.

---

## Features

- **One-Click Transit Ignition (`[T]`)**: Automates the 90-degree gyroscopic rotation from horizontal landing mode to vertical attack/flight posture while spooling the F-31 sublight propulsion core to 100% vector thrust.
- **Tactical Mastermind Dials**: Real-time controls for IFF multi-hop transponder spoofing, stealth heat baffles, rotary blasters, and ordnance chutes.
- **Diagnostic Alert & Triage Engine**: Priority-tiered alert hierarchy (`ADVISORY` → `CAUTION` → `CRITICAL` → `EMERGENCY`) with one-touch mitigation actions (e.g. coolant venting, Silver-Bullet blind micro-jumps, pneumatic chute purges).
- **Blackbox Flight Recorder**: Automatically logs structured telemetry snapshots and flight events to `slave1_blackbox_log.json`.
- **Visual Playback Engine (`[P]` or `--replay`)**: Step-by-step (`[N]`/`[P]`) or automated (`[A]`) visual frame playback of historical flights rendered in Kuat Systems Engineering ANSI HUD styling.

---

## Project Structure

```
.
├── ARCHITECTURE.md             # In-depth architectural specification
├── README.md                   # Project overview, installation & usage
├── slave1_cockpit.py           # CLI entrypoint and interactive flight loop
├── test_slave1_cockpit.py      # Automated unit test suite
├── cockpit/                    # Modular avionics package
│   ├── __init__.py             # Public module interface
│   ├── models.py               # Strongly typed state dataclasses
│   ├── core.py                 # State machine & SlaveOneCockpit coordinator
│   ├── diagnostics.py          # Diagnostic evaluation & triage engine
│   ├── blackbox.py             # Telemetry snapshot persistence manager
│   └── renderer.py             # ANSI HUD & visual replay rendering engine
```

---

## Installation & Requirements

### Requirements
- **Python 3.8+**
- Standard library only (no external dependencies required).
- Terminal with ANSI color support (PowerShell, Windows Terminal, bash, zsh).

### Quick Start
Clone or download the repository to your local machine:
```powershell
git clone <repository-url>
cd <repository-directory>
```

---

## Usage Examples

### 1. Launch the Interactive Cockpit
```powershell
python slave1_cockpit.py
```

### 2. Interactive Commands
Once in the cockpit, use single-key commands:
- **`[T]`**: Ignite & engage one-click transit (90° flight rotation).
- **`[M]`**: Execute top-priority alert mitigation action.
- **`[1]`**: Inject reactor thermal spike fault (680 K).
- **`[2]`**: Inject stealth baffle saturation fault (96%).
- **`[3]`**: Inject Imperial Interdictor mass-shadow trap.
- **`[4]`**: Inject seismic ordnance chute jam.
- **`[P]`**: Enter visual blackbox playback mode.
- **`[S]`**: Force flush/save telemetry log.
- **`[C]`**: Clear and normalize telemetry.
- **`[Q]`**: Disembark and save flight log.

### 3. Launch Directly in Playback Mode
```powershell
python slave1_cockpit.py --replay
```

### 4. Run the Unit Test Suite
```powershell
python -m unittest test_slave1_cockpit.py -v
```

---

## Sub-Layer Seed: `Lone Ranger`

The `Lone Ranger` seed introduces frontier independence into the cockpit avionics:
- **Silver-Bullet Micro-Jump**: An emergency hyperdrive bypass calculating micro-escape vectors through mass-shadow fields.
- **Ghost Transponder Relays**: Multi-hop IFF scrambling across Outer Rim beacons.
- **Offline Blackbox Ledger**: Durable local flight data logging independent of planetary network availability.
