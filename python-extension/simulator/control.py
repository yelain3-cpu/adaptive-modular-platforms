"""A small, testable *new* control simulation inspired by the 2025 prototype.

This code does NOT run the original Arduino hardware. The readings are simulated
and the inflation counter represents command ticks, not pressure or volume.

The new demonstration uses a force deadband and illustrative distance bands.
Neither is claimed to be the exact logic used in the physical installation.
"""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class ControlSettings:
    """Settings selected for a software demonstration, not field calibration."""

    force_low: int = 280
    force_high: int = 320
    max_inflation_ticks: int = 12
    water_near_cm: float = 10.0
    water_mid_cm: float = 20.0

    def __post_init__(self) -> None:
        if not (0 <= self.force_low < self.force_high <= 1023):
            raise ValueError("Expected 0 <= force_low < force_high <= 1023")
        if self.max_inflation_ticks < 1:
            raise ValueError("max_inflation_ticks must be positive")
        if not (0 < self.water_near_cm < self.water_mid_cm):
            raise ValueError("Expected 0 < water_near_cm < water_mid_cm")


@dataclass(frozen=True)
class StepResult:
    """One simulated step, retaining state using an inflation tick count."""

    force: int
    distance_cm: float | None
    pump_action: str  # INFLATE, DEFLATE, IDLE
    inflation_ticks: int
    louver_angle_deg: int | None  # None means no valid distance data
    reason: str


def simulate_step(
    force: int,
    distance_cm: float | None,
    previous_ticks: int,
    settings: ControlSettings = ControlSettings(),
) -> StepResult:
    """Calculate one step without accessing hardware or external services.

    - High force produces one inflation command until the software cap.
    - Low force produces one deflation command until the count reaches zero.
    - Force in the deadband produces no pump command.
    - Closer water (smaller measured distance) yields a larger example angle.

    An invalid/absent distance is reported with `angle=None` rather than
    sending an invented actuator command. The calling UI can display this.
    """
    if type(force) is not int or not (0 <= force <= 1023):
        raise ValueError("force must be an integer in 0..1023")
    if type(previous_ticks) is not int or not (0 <= previous_ticks <= settings.max_inflation_ticks):
        raise ValueError("previous_ticks must be a valid software tick count")

    ticks = previous_ticks
    if force >= settings.force_high and ticks < settings.max_inflation_ticks:
        action = "INFLATE"
        ticks += 1
        reason = "High force: request one inflation command"
    elif force <= settings.force_low and ticks > 0:
        action = "DEFLATE"
        ticks -= 1
        reason = "Low force: request one deflation command"
    else:
        action = "IDLE"
        reason = "Inside deadband, already empty, or at software cap"

    if distance_cm is None:
        angle = None
    elif isinstance(distance_cm, bool) or not isinstance(distance_cm, (int, float)):
        raise ValueError("distance_cm must be a number or None")
    elif not isfinite(distance_cm) or distance_cm <= 0:
        angle = None
    elif distance_cm <= settings.water_near_cm:
        angle = 90
    elif distance_cm <= settings.water_mid_cm:
        angle = 45
    else:
        angle = 0

    return StepResult(
        force=force,
        distance_cm=distance_cm,
        pump_action=action,
        inflation_ticks=ticks,
        louver_angle_deg=angle,
        reason=reason,
    )
