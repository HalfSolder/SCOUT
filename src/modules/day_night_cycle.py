"""Day / night phase helpers.

A four-state model fits crested gecko behaviour better than just
day / night:

  dawn      transition: lights start to come up
  day       active period for the keeper, gecko hiding
  dusk      transition: lights start to come down, gecko stirs
  night     gecko active, IR camera on

The transitions are short windows around the lights-on and lights-off
times. Scout uses them to ramp behaviour, not flip it.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum


class Phase(Enum):
    DAWN = "dawn"
    DAY = "day"
    DUSK = "dusk"
    NIGHT = "night"


def current_phase(now: datetime,
                  day_starts_hour: int,
                  night_starts_hour: int,
                  transition_minutes: int = 30) -> Phase:
    day_start = now.replace(hour=day_starts_hour, minute=0, second=0, microsecond=0)
    night_start = now.replace(hour=night_starts_hour, minute=0, second=0, microsecond=0)
    window = timedelta(minutes=transition_minutes)

    if day_start - window <= now < day_start + window:
        return Phase.DAWN
    if night_start - window <= now < night_start + window:
        return Phase.DUSK
    if day_start + window <= now < night_start - window:
        return Phase.DAY
    return Phase.NIGHT


def is_active_period(phase: Phase) -> bool:
    """When the gecko is likely to be out and visible."""
    return phase in (Phase.DUSK, Phase.NIGHT, Phase.DAWN)
