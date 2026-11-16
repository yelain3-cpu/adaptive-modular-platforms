# Reproduction notes and limitations

## What you can inspect without hardware

- `*.ino`: Arduino C++ source; readable in any text editor or the Arduino IDE.
- `0902_Arduino.gh`: requires Rhino and Grasshopper to open the visual definition.
- `extracted-scripts/*.py`: plain-text excerpts from the embedded Python components; **not standalone scripts**.
- `media/`: images of the project and GH canvas.

## Hardware/software required for a live demonstration

The original physical setup may require an Arduino board, force sensor, ultrasonic sensor, pneumatic pump and valves, servo-driven façade elements, suitable electrical power and wiring, and a Rhino/Grasshopper environment with relevant Python serial dependencies. The hardware pin mappings and electrical specifications must be verified against the actual prototype.

The GH file's opening script refers to `/dev/cu.usbserial-120`. This is a device-specific path; it is not portable to another computer. The GH screenshots show `Serial port is not open` and no captured data in their panels, consistent with the screenshots being taken without a running Arduino session.

The complete code used for the final kinetic-façade physical demonstration has not been reconstructed from the archived materials. The teaching-framework source files have been withheld from this public-ready package for attribution/licensing review, so uploading the files as-is does not recreate the original hardware environment.

## Safety

Do not power pumps/valves from Arduino pins directly. Check component ratings, wiring, transistor/driver circuits, current limits and external supply requirements before uploading any historical sketch to real hardware. The archived control logic contains blocking delays and hard-coded actuator commands.

## Useful next steps

1. Record a short video of the working prototype, if available.
2. Add a labelled electrical/connection diagram with actual Arduino pins and hardware part numbers.
3. Record original sensor values and calibration thresholds.
4. Build an independent software-only controller simulation and include unit tests. Label it explicitly as a **new post-graduation extension**.
