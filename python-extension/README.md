# Python Extension — Responsive Systems Lab (2026)

This is a **new, software-only, AI-assisted learning extension** inspired by the original 2025 Arduino + Grasshopper architecture prototype. It is intentionally **not** described as the original firmware, or as a physical digital twin.

The app is designed to communicate programming and product-thinking skills: translate sensor readings into explainable decisions, handle invalid inputs and boundary conditions, and test behavior without access to the original hardware.

## Try without installing extra libraries

Requires **Python 3.10+**. Open a terminal in the `python-extension` folder:

```bash
python -m simulator.run_demo
python -m unittest discover -s tests -v
```

The demo reads the illustrative inputs from [`samples/scenario.csv`](samples/scenario.csv); tests rely only on Python's standard library.

## Run the interactive dashboard

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Use the sliders to choose a simulated force reading and water distance. Click **Apply reading** to advance the system one step; choose **Run sample sequence** to replay a fixed scenario. No hardware is needed.

## Model — deliberately simplified

| Variable | Illustrative rule | Limitation |
|---|---|---|
| Force reading (raw Arduino-like units) | `>=320` → request one inflation tick; `<=280` → one deflation tick; otherwise idle | No calibrated force units; deadband added as a new improvement |
| Inflation ticks | Capped from `0` to `12` | A command counter, **not** air pressure, volume, or buoyancy |
| Water distance in cm | `<=10` → 90°; `<=20` → 45°; otherwise 0° | New example thresholds, **not verified original hardware settings** |
| Missing/bad water reading | No angle command (`None`) | Real safety strategy depends on physical mechanism |

The original Grasshopper file has a different three-state conditional using `range()` over integer inputs. It should **not** be presented as this same distance-band algorithm. These rules are educational choices for the 2026 simulator.

## File guide

- [`simulator/control.py`](simulator/control.py) — pure, testable Python control rules.
- [`simulator/run_demo.py`](simulator/run_demo.py) — deterministic sample data replay.
- [`app.py`](app.py) — interactive Streamlit UI.
- [`tests/test_control.py`](tests/test_control.py) — automated tests for thresholds, limits, invalid readings and sample replay.
- [`samples/scenario.csv`](samples/scenario.csv) — example readings (fabricated for demonstration, **not recorded field measurements**).

## Suggested learning and ownership checklist

This extension was initially prepared with ChatGPT assistance. Before describing it as *your independently developed software*, run and review the code yourself, be prepared to explain each function, and make a personally understood improvement. A few useful next steps are in [the extension notes](../docs/PYTHON_EXTENSION.md).
