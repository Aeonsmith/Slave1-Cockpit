# Firespray-31 (*Slave I*) Cockpit Architecture
### Sub-Layer Seed: `Lone Ranger` // Manufacturer: `Kuat Systems Engineering`

---

## 1. System Overview & Design Philosophy

The *Slave I* Cockpit Avionics suite is structured as a **One-Click Galactic Cockpit**: a high-leverage flight environment that eliminates micro-friction while retaining critical manual tactical dials.

The architecture emphasizes:
- **Instant Flight Kinematics**: Single-touch departure executing automatic 90-degree gyroscopic rotation from horizontal landing posture to vertical attack posture.
- **Mastermind Alert & Triage Bus**: Continuous diagnostic rule evaluation with single-key resolution of containment breaches and interdictor traps.
- **Blackbox Flight Recorder**: Immutable snapshot logging capturing telemetry, alert hierarchies, and event logs for post-flight analysis.
- **Visual Playback Engine**: Frame-by-frame and automated telemetry playback rendered in Kuat Systems Engineering ANSI HUD styling.

---

## 2. Directory & Modular Structure

```
.
├── ARCHITECTURE.md             # System documentation and design blueprints
├── slave1_cockpit.py           # Thin CLI entry point and interactive loop
├── test_slave1_cockpit.py      # Automated unit test suite
├── slave1_blackbox_log.json    # Serialized blackbox telemetry log
└── cockpit/                    # Core avionics package
    ├── __init__.py             # Public API exports
    ├── models.py               # Strongly typed dataclasses & telemetry schemas
    ├── core.py                 # SlaveOneCockpit state machine & coordinator
    ├── diagnostics.py          # Diagnostic evaluation & triage mitigation engine
    ├── blackbox.py             # Flight recording & JSON persistence engine
    └── renderer.py             # ANSI visual HUD & playback rendering pipeline
```

---

## 3. Subsystem Architecture

### 3.1 State Models (`cockpit/models.py`)
- **`FlightState`**: Manages attitude (horizontal vs. vertical), gimbal lock flags, sublight thrust percentage, core temperature ($K$), and hyperdrive coil states.
- **`StealthSensorState`**: Tracks transponder IFF ghost signatures, thermal baffle saturation percentage, stealth profiles (`SILENT_RUNNING`, `CRUISE`, `HOT_COMBAT`), and mass-shadow warnings.
- **`WeaponsState`**: Houses status for twin rotary blasters, concussion missile racks, seismic charges, and chute jam flags.
- **`CockpitAlert`**: Represents diagnostic faults tagged by severity (`ADVISORY`, `CAUTION`, `CRITICAL`, `EMERGENCY`).

### 3.2 Diagnostic Rules Engine (`cockpit/diagnostics.py`)
Evaluates telemetry inputs against critical thresholds:
1. **Reactor Thermal Runaway** ($>650\text{ K}$): Triggers emergency containment alert $\rightarrow$ One-touch coolant vent mitigation.
2. **Stealth Baffle Saturation** ($\ge 90\%$): Triggers thermal bloom unmasking alert $\rightarrow$ Wake dump mitigation.
3. **Imperial Mass-Shadow Lock**: Gravimetric anomaly interlock $\rightarrow$ Fast-draw Silver-Bullet micro-jump override.
4. **Seismic Chute Jam**: Warhead release blocked $\rightarrow$ Ventral pneumatic purge mitigation.

### 3.3 Blackbox Flight Recorder (`cockpit/blackbox.py`)
- Automatically captures full telemetry snapshots on every state change, maneuver, or event trigger.
- Persists data to `slave1_blackbox_log.json` in a standardized format consumable by downstream tools or the visual replay engine.

### 3.4 ANSI Renderer (`cockpit/renderer.py`)
- **Active HUD**: Renders real-time annunciators, attitude indicators, weapons matrix, active alerts, and event log.
- **Replay HUD**: Dedicated playback interface supporting step-by-step navigation (`[N]`/`[P]`) and real-time auto-play (`[A]`).

---

## 4. Sub-Layer Seed: `Lone Ranger` Integration

- **Silver-Bullet Micro-Jump**: Dedicated hyperdrive override allowing emergency blind jumps through mass-shadow fields when cornered.
- **IFF Masking Matrix**: Multi-hop transponder spoofing for navigating high-security sectors under civilian or dark rig guises.
- **Autonomous Escrow & Ledger Telemetry**: Background readiness integration for bounty settlement and cargo containment security.

---

## 5. Verification & Testing

Run the automated test suite covering state transitions, alert evaluation, and blackbox serialization:
```powershell
python test_slave1_cockpit.py
```

Launch the interactive cockpit console:
```powershell
python slave1_cockpit.py
```

Launch visual blackbox playback directly:
```powershell
python slave1_cockpit.py --replay
```
