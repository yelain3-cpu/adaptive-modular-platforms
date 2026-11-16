# Source-code notes and review

These notes describe the historical uploaded source. **They are not evidence that all variants were compiled, tested, or simultaneously deployed**.

## Arduino files

| File | Function | Notes |
|---|---|---|
| `20250209_Force_v2.ino` | Reads `A0` and switches between pneumatic modes based on a force threshold and `timer` | A copy named `sketch_feb12a.ino` was also provided, but is byte-for-byte identical and omitted from this upload to avoid duplication |
| `20250211_Force_v4.ino` | Adds serial-byte input (`air_delay`) and `timer`/`amount` counters to the force-controlled pneumatic routine | `Serial.begin()` is called at 115200 then 9600; the latter setting takes effect |
| `VVS_1.ino` | Related force-control variant with English comments and adjusted initialization values | Kept as a distinct historical variant, not presented as the definitive final firmware |
| `sketch_feb9a.ino` | Timed pneumatic cycling experiment | No force-sensitive input shown |

### Observed technical limitations

- **Fixed threshold:** `fsr > 300` is used without visible calibration, filtering or hysteresis.
- **Equality edge case:** v4 branches address `fsr > 300` and `fsr < 300`; exact equality is not explicitly handled.
- **Timing vs measurement:** `timer` and `amount` count control actions; they do not measure elapsed milliseconds, pressure or air volume.
- **Serial protocol:** `Serial.read()` reads one raw byte; this does not automatically interoperate with text lines or the general Firefly-style serial command format.
- **Servo commands:** `Servo.write(255)` is outside the usual 0–180 degree input range and is constrained by the standard Arduino Servo library. Its physical meaning for the connected switching hardware should be checked.
- **Comments vs pins:** some comments describe pins D6/D8 whereas the sketches attach objects to pins 7/3. Wiring needs separate verification.
- **Blocking operations:** `delay(...)` blocks the control loop, limiting responsiveness.

These are worthwhile learning and refactoring opportunities; they do not invalidate the reported physical prototype.

## Grasshopper Python components

The six extracted scripts are provided for reading only and have not been rewritten. The embedded definition documents that the Open/Close Port, Uno Read and Uno Write scripts were generated with ChatGPT-4o.

| Script | Behavior |
|---|---|
| `open_close_port.py` | Opens/closes a serial port, storing it in `scriptcontext.sticky`; contains a hard-coded local `/dev/cu.usbserial-120` path |
| `uno_read.py` | Reads and returns the most recent available serial line |
| `uno_write.py` | Sends a newline-terminated command via serial |
| `pin_command_formatter.py` | Encodes per-pin values and mode choices into numerical command fields |
| `two_state_angle_mapping.py` | Maps `x < 20` to 0 and other values to 90 |
| `three_state_angle_mapping.py` | Maps selected `range()`-membership values to 0/45/90 |

The `range()` check is integer-membership logic, not a generic continuous numeric comparison: fractional input values may not behave as a user expects. The scripts rely on Grasshopper-provided variables and dependencies (`rhinoscriptsyntax`, `scriptcontext`, `pyserial`) and cannot be run as ordinary standalone Python files without their host inputs.

## Suggested transparent portfolio wording

> Designed and contributed to programming a two-part responsive architectural prototype using Arduino force sensing and pneumatic actuation alongside an ultrasonic/servo façade system. Developed project-specific control logic and Grasshopper parameter workflows using a course-provided microcontroller communication foundation. The prototype was demonstrated physically; the surviving source has been archived with clear attribution and technical limitations.
