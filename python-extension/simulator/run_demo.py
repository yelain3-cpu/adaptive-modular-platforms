"""Replay a documented CSV scenario with the same core logic as the web UI."""

import csv
from pathlib import Path

from simulator.control import ControlSettings, simulate_step


def replay_scenario(csv_path: Path):
    """Yield the result of each row in a sample input file."""
    settings = ControlSettings()
    ticks = 0
    with csv_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            force = int(row["force_raw"])
            raw_distance = row["distance_cm"].strip()
            distance = float(raw_distance) if raw_distance else None
            result = simulate_step(force, distance, ticks, settings)
            ticks = result.inflation_ticks
            yield result


def main():
    source = Path(__file__).resolve().parents[1] / "samples" / "scenario.csv"
    print("SIMULATED DATA ONLY — no Arduino or sensor connection")
    print("Step | Force | Distance | Pump    | Counter | Louver")
    for i, result in enumerate(replay_scenario(source), start=1):
        distance = "missing" if result.distance_cm is None else f"{result.distance_cm:.1f} cm"
        angle = "unknown" if result.louver_angle_deg is None else f"{result.louver_angle_deg}°"
        print(
            f"{i:>4} | {result.force:>5} | {distance:>8} | "
            f"{result.pump_action:<7} | {result.inflation_ticks:>7} | {angle}"
        )


if __name__ == "__main__":
    main()
