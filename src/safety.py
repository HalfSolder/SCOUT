"""Hard safety limits.

The brain is Grok, but if the model misjudges, Biscuit gets hurt. So
some rules do not go through the model at all.

Crested geckos die from heat much faster than they die from cold. The
safety layer reflects that: the maximum ambient temperature is the most
important limit in this file.

`check()` runs BEFORE the model. It can short-circuit the tick with an
override action. `gate()` runs AFTER the model. It sanitises whatever
the model asked for.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta, timezone


class Safety:
    def __init__(self, safety_cfg: dict, actuators):
        self.cfg = safety_cfg
        self.actuators = actuators
        self.cgd_log: deque[datetime] = deque()
        self.insect_log: deque[datetime] = deque()

    def check(self, readings: dict) -> dict | None:
        ambient = self._max_temp(readings)

        if ambient is not None and ambient > self.cfg["max_ambient_c"]:
            return {
                "name": "alert_human",
                "params": {"reason": f"ambient {ambient}C above max {self.cfg['max_ambient_c']}C"},
                "reason": f"ambient {ambient}C > max {self.cfg['max_ambient_c']}C",
            }

        if ambient is not None and ambient < self.cfg["min_ambient_c"]:
            return {
                "name": "alert_human",
                "params": {"reason": f"ambient {ambient}C below min {self.cfg['min_ambient_c']}C"},
                "reason": f"ambient {ambient}C < min {self.cfg['min_ambient_c']}C",
            }

        return None

    def gate(self, action: dict, readings: dict) -> dict:
        name = action.get("name", "noop")
        params = dict(action.get("params") or {})

        if name == "mist":
            seconds = float(params.get("seconds", 0))
            params["seconds"] = min(seconds, self.cfg["max_mist_seconds_per_tick"])

        if name == "refill_water":
            seconds = float(params.get("seconds", 0))
            params["seconds"] = min(seconds, 5.0)

        if name == "refresh_cgd":
            self._prune_log(self.cgd_log, hours=24)
            if len(self.cgd_log) >= self.cfg["max_cgd_refreshes_per_day"]:
                return {"name": "noop", "params": {}}
            self.cgd_log.append(datetime.now(timezone.utc))

        if name == "offer_insect":
            self._prune_log(self.insect_log, hours=24 * 7)
            if len(self.insect_log) >= self.cfg["max_insects_per_week"]:
                return {"name": "noop", "params": {}}
            self.insect_log.append(datetime.now(timezone.utc))

        return {"name": name, "params": params}

    @staticmethod
    def _max_temp(readings: dict) -> float | None:
        candidates = [readings.get(k) for k in ("top_c", "bottom_c", "ambient_c")]
        candidates = [c for c in candidates if isinstance(c, (int, float))]
        return max(candidates) if candidates else None

    @staticmethod
    def _prune_log(log: deque, hours: int) -> None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        while log and log[0] < cutoff:
            log.popleft()
