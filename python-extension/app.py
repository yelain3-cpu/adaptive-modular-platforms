"""Streamlit user interface for a software-only responsive system simulator."""

from pathlib import Path

import streamlit as st

from simulator.control import ControlSettings, simulate_step
from simulator.run_demo import replay_scenario

SETTINGS = ControlSettings()
SCENARIO = Path(__file__).parent / "samples" / "scenario.csv"

st.set_page_config(page_title="Responsive Systems Lab", page_icon="🌊", layout="wide")
st.title("Responsive Systems Lab")
st.caption("A new Python learning exercise inspired by a 2025 Arduino + Grasshopper prototype")
st.info(
    "Software simulation only. Values are illustrative; no hardware is connected. "
    "An inflation tick is not a physical measure of air volume or buoyancy."
)

if "history" not in st.session_state:
    st.session_state.history = []
if "ticks" not in st.session_state:
    st.session_state.ticks = 0

with st.sidebar:
    st.header("Simulated sensor inputs")
    force = st.slider("Force reading (raw, 0–1023)", 0, 1023, 300, 1)
    distance = st.slider("Distance to water (cm)", 1, 100, 25, 1)
    failed = st.checkbox("Simulate missing distance reading", value=False)
    st.caption(
        "Design exercise: inflate at force ≥320, deflate at ≤280, idle between. "
        "Illustrative louver angles use ≤10 cm →90°, ≤20 cm →45°, otherwise 0°."
    )
    apply = st.button("Apply reading", type="primary", use_container_width=True)
    sample = st.button("Run sample sequence", use_container_width=True)
    reset = st.button("Reset simulation", use_container_width=True)

if reset:
    st.session_state.ticks = 0
    st.session_state.history = []

if apply:
    reading = None if failed else float(distance)
    output = simulate_step(force, reading, st.session_state.ticks, SETTINGS)
    st.session_state.ticks = output.inflation_ticks
    st.session_state.history.append(
        {
            "step": len(st.session_state.history) + 1,
            "force_raw": output.force,
            "water_distance_cm": output.distance_cm,
            "pump_action": output.pump_action,
            "inflation_ticks": output.inflation_ticks,
            "louver_angle_deg": output.louver_angle_deg,
        }
    )

if sample:
    st.session_state.ticks = 0
    st.session_state.history = []
    for i, output in enumerate(replay_scenario(SCENARIO), start=1):
        st.session_state.ticks = output.inflation_ticks
        st.session_state.history.append(
            {
                "step": i,
                "force_raw": output.force,
                "water_distance_cm": output.distance_cm,
                "pump_action": output.pump_action,
                "inflation_ticks": output.inflation_ticks,
                "louver_angle_deg": output.louver_angle_deg,
            }
        )

st.subheader("Current simulation state")
last = st.session_state.history[-1] if st.session_state.history else None
left, middle, right = st.columns(3)
left.metric("Pump action", last["pump_action"] if last else "Not started")
middle.metric("Inflation counter", st.session_state.ticks)
right.metric(
    "Louver target", "No valid reading"
    if last and last["louver_angle_deg"] is None
    else f'{last["louver_angle_deg"]}°' if last else "Not started"
)

st.subheader("Scenario history")
if not st.session_state.history:
    st.write("Move the sliders and select **Apply reading**, or select **Run sample sequence**.")
else:
    rows = st.session_state.history
    st.line_chart(rows, x="step", y="inflation_ticks")
    st.dataframe(rows, hide_index=True, use_container_width=True)

with st.expander("How is this different from the original physical prototype?"):
    st.markdown(
        """
        - **Original, 2025:** Physical Arduino/Grasshopper setup with sensor and actuator integration.
        - **This extension, 2026:** Offline Python control logic and a simple interactive UI.
        - The force deadband, software command cap and distance thresholds are **new example choices**.
        - The original `Grasshopper` three-state rule and the distance-to-water mapping are **not**
          asserted to be identical to this simulator.
        - This demo does **not** validate stability, safety, floatation, pressure or wiring.
        """
    )
