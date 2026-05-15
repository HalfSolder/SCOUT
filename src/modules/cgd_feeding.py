"""CGD (crested gecko diet) feeding helper.

Crested geckos eat a complete fruit / insect powder called CGD, mixed
2 parts water to 1 part powder by weight. The slurry goes off after
24 to 36 hours and starts to smell yeasty when it does.

This module tracks freshness, recipe, and gives the model a clear
signal when it is time to refresh.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


CGD_LOG = Path("data/cgd_log.jsonl")
MAX_AGE_HOURS = 36
WARN_AGE_HOURS = 24


@dataclass
class Recipe:
    powder_grams: float
    water_grams: float

    @property
    def total_grams(self) -> float:
        return self.powder_grams + self.water_grams

    def __str__(self) -> str:
        return (f"{self.powder_grams:.1f} g powder, "
                f"{self.water_grams:.1f} g water "
                f"({self.total_grams:.1f} g total)")


def recipe_for_one_dish(grams: float = 6.0) -> Recipe:
    """Default dish: 6 g of finished slurry, 2:1 water:powder by weight."""
    powder = grams / 3
    water = grams - powder
    return Recipe(powder_grams=powder, water_grams=water)


def record_refresh(when: datetime | None = None) -> None:
    when = when or datetime.now(timezone.utc)
    CGD_LOG.parent.mkdir(parents=True, exist_ok=True)
    with CGD_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"refreshed_at": when.isoformat()}) + "\n")


def last_refresh() -> datetime | None:
    if not CGD_LOG.exists():
        return None
    lines = [line for line in CGD_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return None
    try:
        ts = json.loads(lines[-1])["refreshed_at"]
        return datetime.fromisoformat(ts)
    except (ValueError, KeyError):
        return None


def freshness_state() -> str:
    last = last_refresh()
    if last is None:
        return "unknown"
    age = datetime.now(timezone.utc) - last
    if age >= timedelta(hours=MAX_AGE_HOURS):
        return "stale"
    if age >= timedelta(hours=WARN_AGE_HOURS):
        return "old"
    return "fresh"


def hours_since_refresh() -> float | None:
    last = last_refresh()
    if last is None:
        return None
    return (datetime.now(timezone.utc) - last).total_seconds() / 3600


if __name__ == "__main__":
    state = freshness_state()
    hours = hours_since_refresh()
    print(f"CGD freshness: {state}")
    if hours is not None:
        print(f"  last refresh: {hours:.1f} h ago")
    print(f"  default recipe: {recipe_for_one_dish()}")
