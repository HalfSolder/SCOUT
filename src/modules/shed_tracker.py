"""Shed cycle tracking.

Crested geckos shed every couple of weeks (more often when growing,
less often as adults). A shed is preceded by milky / dull colouration,
then the gecko comes out vivid and bright the next day.

Stuck shed is the main risk: toes, tail tip, around eyes. Bump
humidity for a day if any retained shed is seen.

This module stores shed events so the keeper can see the rhythm and
catch a shed cycle that is taking too long.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


SHED_LOG = Path("data/shed_log.jsonl")


@dataclass
class ShedEvent:
    ts: str
    stage: str            # "pre", "in_progress", "completed", "retained"
    notes: str = ""


def log(stage: str, notes: str = "") -> None:
    if stage not in ("pre", "in_progress", "completed", "retained"):
        raise ValueError(f"unknown shed stage: {stage!r}")
    event = ShedEvent(
        ts=datetime.now(timezone.utc).isoformat(),
        stage=stage,
        notes=notes,
    )
    SHED_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SHED_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(event)) + "\n")


def history(n: int = 30) -> list[ShedEvent]:
    if not SHED_LOG.exists():
        return []
    lines = SHED_LOG.read_text(encoding="utf-8").splitlines()[-n:]
    out: list[ShedEvent] = []
    for line in lines:
        if not line.strip():
            continue
        out.append(ShedEvent(**json.loads(line)))
    return out


def days_since_last_completed_shed() -> float | None:
    for event in reversed(history(100)):
        if event.stage == "completed":
            then = datetime.fromisoformat(event.ts)
            return (datetime.now(timezone.utc) - then).total_seconds() / 86400
    return None


if __name__ == "__main__":
    days = days_since_last_completed_shed()
    if days is None:
        print("no completed shed logged yet")
    else:
        print(f"days since last completed shed: {days:.1f}")
    for event in history(10):
        print(f"  {event.ts}  {event.stage:<12}  {event.notes}")
