"""Humidity cycler.

Crested geckos need a humidity CYCLE, not a flat number. The tank
should spike to 80 to 100 % after the evening misting and drift down
to 50 to 70 % during the day. Constant 80 %+ rots plants and invites
infections.

This module turns "is the current humidity reading where it should be
right now" into a single boolean and, if not, a suggested action.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HumidityVerdict:
    in_band: bool
    distance: float
    suggestion: str | None
    suggested_seconds: int


DAY_BAND = (50.0, 70.0)
NIGHT_BAND = (80.0, 100.0)


def verdict(humidity_pct: float, is_night: bool) -> HumidityVerdict:
    lo, hi = NIGHT_BAND if is_night else DAY_BAND

    if lo <= humidity_pct <= hi:
        return HumidityVerdict(True, 0.0, None, 0)

    if humidity_pct < lo:
        deficit = lo - humidity_pct
        seconds = _mist_seconds_for_deficit(deficit, is_night)
        return HumidityVerdict(False, deficit, "mist", seconds)

    excess = humidity_pct - hi
    return HumidityVerdict(False, excess, "ventilate", 0)


def _mist_seconds_for_deficit(deficit_pct: float, is_night: bool) -> int:
    # Empirical, tuned during Phase 3. The right curve depends on the
    # nozzle and the tank volume.
    if is_night:
        return min(20, max(5, int(deficit_pct * 0.8)))
    return min(10, max(3, int(deficit_pct * 0.4)))


def night_spike_happened(recent_ticks: list[dict]) -> bool:
    """Did humidity exceed 75 % at any point in the last few ticks?"""
    for entry in recent_ticks:
        reading = entry.get("readings", {}) or {}
        if (reading.get("humidity_pct") or 0) >= 75:
            return True
    return False
