"""Top and bottom temperature monitoring for an arboreal tank.

Crested geckos pick where they want to be by height. A healthy
arboreal tank has a small vertical gradient: the top a degree or two
warmer than the bottom during the day, narrowing at night.

A gradient that inverts (bottom warmer than top) usually means
something is heating from below, which is wrong for a crestie.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ZoneReading:
    top_c: float
    bottom_c: float

    @property
    def gradient(self) -> float:
        return self.top_c - self.bottom_c

    @property
    def inverted(self) -> bool:
        return self.gradient < -0.5

    @property
    def hot(self) -> bool:
        return max(self.top_c, self.bottom_c) > 27.0

    @property
    def cold(self) -> bool:
        return min(self.top_c, self.bottom_c) < 18.0


def from_readings(readings: dict) -> ZoneReading | None:
    top = readings.get("top_c")
    bot = readings.get("bottom_c")
    if isinstance(top, (int, float)) and isinstance(bot, (int, float)):
        return ZoneReading(top_c=float(top), bottom_c=float(bot))
    return None


def diagnose(zone: ZoneReading) -> list[str]:
    notes: list[str] = []
    if zone.hot:
        notes.append(f"hot: max {max(zone.top_c, zone.bottom_c):.1f} C")
    if zone.cold:
        notes.append(f"cold: min {min(zone.top_c, zone.bottom_c):.1f} C")
    if zone.inverted:
        notes.append(f"inverted gradient: top {zone.top_c:.1f} < bottom {zone.bottom_c:.1f}")
    if abs(zone.gradient) > 4:
        notes.append(f"large gradient: {zone.gradient:+.1f} C")
    return notes
