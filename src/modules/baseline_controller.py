"""Dumb baseline controller, for comparison against GPT-5.5.

To know whether the language model actually helps, we need a non-LLM
baseline. This module is that baseline. It is intentionally boring:

  - Lights on at the configured hour.
  - Lights off at the configured hour.
  - Evening mist at dusk, light pre-dawn mist.
  - CGD refresh every 24 hours.
  - Insect drop on Wednesdays and Saturdays in the evening.
  - Refill water when the float switch trips.
  - Alert human when ambient > 27 C.

Same action vocabulary as the brain. Same journal format. Run it for
a week, then run GPT-5.5 for a week, then compare with metrics.py.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from . import humidity_cycler


INSECT_WEEKDAYS = {2, 5}    # Wednesday, Saturday
EVENING_HOUR = 20
PRE_DAWN_HOUR = 6
CGD_REFRESH_HOUR = 9


def decide(readings: dict, now: datetime, last_cgd_refresh_hour: int | None) -> dict[str, Any]:
    hour = now.hour
    is_night = hour < 8 or hour >= 20

    if hour == 8:
        return _act("set_lights", {"state": "day"}, "scheduled day start")
    if hour == 20:
        return _act("set_lights", {"state": "night"}, "scheduled night start")

    if hour == EVENING_HOUR and (readings.get("humidity_pct") or 0) < 80:
        return _act("mist", {"seconds": 20}, "scheduled evening mist")
    if hour == PRE_DAWN_HOUR:
        return _act("mist", {"seconds": 8}, "scheduled pre-dawn mist")

    if hour == CGD_REFRESH_HOUR and last_cgd_refresh_hour != CGD_REFRESH_HOUR:
        return _act("refresh_cgd", {}, "scheduled CGD refresh")

    if (not is_night and now.weekday() in INSECT_WEEKDAYS
            and hour == 20 and now.minute < 5):
        return _act("offer_insect", {}, "scheduled insect feed")

    if not readings.get("water_ok", True):
        return _act("refill_water", {"seconds": 3}, "float switch tripped")

    top = readings.get("top_c") or 0
    if top > 27:
        return _act("alert_human",
                    {"reason": f"top {top:.1f} C approaching limit"},
                    "temperature climbing")

    # opportunistic humidity correction
    verdict = humidity_cycler.verdict(readings.get("humidity_pct") or 60, is_night)
    if not verdict.in_band and verdict.suggestion == "mist" and verdict.suggested_seconds > 0:
        return _act("mist", {"seconds": verdict.suggested_seconds},
                    f"humidity {verdict.distance:.1f} below band")

    return _act("noop", {}, "stable")


def _act(name: str, params: dict, reason: str) -> dict[str, Any]:
    return {"action": {"name": name, "params": params}, "reasoning": reason}
