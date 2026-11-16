# Post-graduation Python extension — rationale and learning notes

**Date:** November 2026  
**Status:** Offline prototype prepared with AI coding assistance; original author review and UI testing on their machine pending.

## Why build this?

The 2025 final-year project included a physical sensor/actuator prototype. The new software-only extension translates that experience into **explainable Python code with automated tests**. It aims to show a transition from design-led hardware prototyping into software reasoning and product development.

**Problem statement:** How can a user inspect the decisions made by a responsive system without having the original physical installation at hand?

**User:** An admissions reviewer, collaborator, or engineering/design student who wants to explore how example sensor readings can change system behavior.

**MVP design:** Two input sliders, a discrete state update, readable pump/louver decisions, a history table, a fixed scenario replay, and repeatable unit tests.

## Difference from the 2025 project

| 2025 historical evidence | 2026 extension |
|---|---|
| Working physical prototype reported by the project team; surviving Arduino / GH files | Pure Python simulator; no serial port or hardware access |
| Threshold `300` in archived force-control Arduino sketches | New force deadband `280–320` to avoid continuously switching at one boundary |
| Three-state angle script in GH uses integer `range()` membership | New numeric distance bands for a user-facing simulator |
| Pump state recorded in code using experimental counters | Simulated command count bounded from 0 to 12; not real pressure/volume |

The simulator is not evidence that the original hardware used these thresholds. It is a new design proposal inspired by the prototype, not an archaeological reconstruction of the final firmware.

## What has been tested automatically?

- Inflation when high force is applied.
- Deflation when low force is applied.
- No action in the force deadband.
- Counter never exceeds the configured bound or drops below zero.
- Boundary handling for example water distance bands.
- Missing or invalid ultrasonic reading produces no angle command.
- Sample CSV replay is reproducible.

The tests do **not** establish real-world electrical safety, pneumatic stability, actuator timing, or distance sensor accuracy.

## Good next improvement to implement yourself

Start with one achievable task (rather than adding AI just to call the project AI-related):

1. **Understand the current model.** Run the sample scenario and explain why each row outputs `INFLATE`, `DEFLATE`, or `IDLE`.
2. **Modify one rule.** Try changing the force deadband to `275–325`; update a test accordingly and compare behaviors.
3. **Investigate sensor noise.** Write a new 10-row CSV alternating around `300`. Compare the original single-threshold idea against the new deadband.
4. **Explain a tradeoff.** Document how the deadband reduces chattering but also makes the controller less sensitive.

If you do a personal modification, document it under a new dated heading in this file and take a screenshot of the working Streamlit dashboard for your portfolio. A short, meaningful, understood improvement is more credible than a feature added without testing.

## Responsible project description

> Built an interactive Arduino/Grasshopper architectural prototype as part of a team (2025). In a later Python learning extension (2026), explored an offline rule-based controller with user-adjustable inputs and automated tests. The extension was developed with AI coding assistance and is not connected to the original hardware.

Adapt this statement to reflect **what you personally reviewed, changed, tested, and can explain**.
