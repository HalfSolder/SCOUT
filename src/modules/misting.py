"""Misting schedule and cooldowns.

Misting drives the humidity cycle. This module enforces sensible
cooldowns between bursts and an evening / pre-dawn schedule, on top of
whatever the model wants.

The model can always ask for `mist`, but if it asks too often the
cooldown blocks it. The safety layer also caps duration.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from dataclasses import dataclass


@dataclass
class MistDecision:
    allowed: bool
    seconds: int
    reason: str


class MistController:
    def __init__(self, min_gap_minutes: int = 8, max_per_hour: int = 4):
        self.min_gap = timedelta(minutes=min_gap_minutes)
        self.max_per_hour = max_per_hour
        self.history: list[datetime] = []

    def request(self, seconds: int, now: datetime | None = None) -> MistDecision:
        now = now or datetime.now(timezone.utc)
        self._prune(now)

        if seconds <= 0:
            return MistDecision(False, 0, "zero seconds requested")

        if self.history and (now - self.history[-1]) < self.min_gap:
            wait = (self.min_gap - (now - self.history[-1])).total_seconds()
            return MistDecision(False, 0, f"cooldown, {int(wait)}s to go")

        if len(self.history) >= self.max_per_hour:
            return MistDecision(False, 0, "hourly mist cap reached")

        self.history.append(now)
        return MistDecision(True, seconds, "ok")

    def _prune(self, now: datetime) -> None:
        cutoff = now - timedelta(hours=1)
        self.history = [t for t in self.history if t >= cutoff]


# Suggested schedule when the model has no strong opinion.
EVENING_MIST_HOUR = 20
PRE_DAWN_MIST_HOUR = 6


def scheduled_mist(now: datetime, last_mist: datetime | None) -> tuple[bool, int]:
    """Return (should_mist, seconds)."""
    if last_mist is not None and (now - last_mist) < timedelta(hours=3):
        return False, 0
    hour = now.hour
    if hour == EVENING_MIST_HOUR:
        return True, 20
    if hour == PRE_DAWN_MIST_HOUR:
        return True, 8
    return False, 0
