# Extracted Grasshopper scripts

These six files are **verbatim decoded excerpts** from embedded Python script components in `../0902_Arduino.gh` (renamed according to their observed functionality). They are intended to make project logic reviewable on GitHub.

They are **not** an executable Python package and depend on Rhino/Grasshopper-provided input variables. Do not run the file content in isolation expecting it to control an Arduino.

The original Grasshopper definition explicitly states that **Open/Close Port, Uno Read and Uno Write** scripts were generated with **ChatGPT-4o**. This attribution is preserved in the public documentation. The exact authorship of all other individual components should be confirmed with the project team.

- `open_close_port.py` — port initialization using `pyserial` and `scriptcontext.sticky`
- `uno_read.py` — serial read
- `uno_write.py` — serial write
- `pin_command_formatter.py` — per-pin output command preparation
- `two_state_angle_mapping.py` — 0 / 90 mapping
- `three_state_angle_mapping.py` — 0 / 45 / 90 mapping
