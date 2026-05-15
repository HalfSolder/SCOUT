"""Hard safety limits.

The brain is GPT-5.5, but if the model misjudges, the gecko gets hurt. So
some rules don't go through the model at all:

  - If the warm side is too hot, the heat lamp is forced off.
  - The water pump cannot run longer than N seconds per tick.
  - The feeder cannot drop more than N mealworms per 24 hours.

`check()` runs BEFORE the model — it can short-circuit the tick with an
override action. `gate()` runs AFTER the model — it sanitises whatever the
model asked for.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta, timezone


class Safety:
    def __init__(self, safety_cfg: dict, actuators):
        self.cfg = safety_cfg
        self.actuators = actuators
        self.feed_log: deque[datetime] = deque()

    def check(self, readings: dict) -> dict | None:
        warm = readings.get("warm_c")
        if warm is not None and warm > self.cfg["max_warm_c"]:
            return {
                "name": "heat_off",
                "params": {},
                "reason": f"warm side {warm}°C > max {self.cfg['max_warm_c']}°C",
            }

        if warm is not None and warm < self.cfg["min_warm_c"]:
            return {
                "name": "alert_human",
                "params": {"reason": f"warm side {warm}°C below minimum"},
                "reason": f"warm side {warm}°C < min {self.cfg['min_warm_c']}°C",
            }

        return None

    def gate(self, action: dict, readings: dict) -> dict:
        name = action.get("name", "noop")
        params = dict(action.get("params") or {})

        if name == "refill_water":
            seconds = float(params.get("seconds", 0))
            params["seconds"] = min(seconds, self.cfg["max_water_pump_seconds_per_tick"])

        if name == "dispense_food":
            self._prune_feed_log()
            if len(self.feed_log) >= self.cfg["max_mealworms_per_day"]:
                return {"name": "noop", "params": {}}
            self.feed_log.append(datetime.now(timezone.utc))

        return {"name": name, "params": params}

    def _prune_feed_log(self) -> None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        while self.feed_log and self.feed_log[0] < cutoff:
            self.feed_log.popleft()
