"""IR night vision helpers.

Crested geckos are nocturnal. To see anything interesting we need the
camera and an 850 nm IR illuminator running through the night. 850 nm
is invisible to crested geckos and to humans.

The Pi Camera NoIR (no IR filter) is required for this to work.
"""

from __future__ import annotations

from datetime import datetime


def should_ir_be_on(now: datetime, day_starts_hour: int, night_starts_hour: int) -> bool:
    hour = now.hour
    return hour >= night_starts_hour or hour < day_starts_hour


def annotate_frame_intent(now: datetime, day_starts_hour: int, night_starts_hour: int) -> str:
    if should_ir_be_on(now, day_starts_hour, night_starts_hour):
        return "ir"
    return "visible"
