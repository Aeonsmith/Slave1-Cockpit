# Contributing to Firespray-31 (*Slave I*) Cockpit Avionics

Thank you for your interest in expanding the *Slave I* cockpit avionics and diagnostics suite. This project is built around the **"one-click starship cockpit"** philosophy—seamless tactile flight control, minimal cognitive friction, and robust diagnostic triage.

---

## 1. Development Principles & Philosophy

- **High Leverage, Low Friction**: Keep primary interactions (such as flight transit or alert mitigation) single-click/single-touch. Complex subsystems should exist under clean dials rather than cluttered interfaces.
- **Sub-Layer Seed (`Lone Ranger`)**: All new features should respect frontier resilience—fault tolerance, offline telemetry preservation, multi-hop evasion, and zero external runtime dependencies.
- **Modular Architecture**: Retain strict separation of concerns:
  - `cockpit/models.py`: Immutable schemas & dataclasses.
  - `cockpit/diagnostics.py`: Pure rule evaluation & triage functions.
  - `cockpit/blackbox.py`: Telemetry persistence and state serialization.
  - `cockpit/renderer.py`: Terminal presentation & ANSI HUD pipelines.
  - `cockpit/core.py`: State coordination & flight state machine.

---

## 2. Workflow & Pull Requests

1. **Fork & Branch**:
   - Create a feature branch off `master`:
     ```powershell
     git checkout -b feature/your-feature-name
     ```
2. **Coding Standards**:
   - Python 3.8+ compatibility.
   - Standard library only—do not introduce external package dependencies.
   - Type hints and docstrings for all new methods and classes.
3. **Testing**:
   - Every new feature, telemetry parameter, or diagnostic alert must include unit tests in `test_slave1_cockpit.py`.
   - Ensure all tests pass prior to submitting a PR:
     ```powershell
     python -m unittest test_slave1_cockpit.py -v
     ```
4. **Commit Conventions**:
   - Write clear, declarative commit messages.
   - When using AI assistance or paired development, include co-authorship attribution:
     ```
     Co-Authored-By: Warp <agent@warp.dev>
     ```

---

## 3. Ideas for Future Expansion

- **Audio Subsystem**: Cross-platform terminal audio cues (e.g. seismic charge vacuum pulse sweep, gimbal lock click).
- **Custom Galactic Sector Presets**: Sector-specific transponder spoof profiles (Core Worlds vs. Outer Rim).
- **Interactive TUI**: Rich/Curses-based HUD with interactive dial sliders and real-time attitude artificial horizon indicators.
- **Decentralized Escrow Integration**: Tor/onion network ledger hooks for autonomous contract validation.

---

## 4. Questions & Discussions

Feel free to open an Issue on GitHub for bugs, architectural questions, or feature proposals.
