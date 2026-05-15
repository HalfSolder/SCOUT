"""Tail health monitoring.

Crested geckos drop their tails under stress and do not regrow them.
A dropped tail is permanent. A thinning tail base means he is losing
weight or stressed.

This module logs tail observations from camera frames so the keeper
(and the model) can compare today against last week, and so that any
thinning is caught early.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


TAIL_LOG = Path("data/tail_log.jsonl")


@dataclass
class TailObservation:
    ts: str
    frame: str
    state: str            # "intact", "thinning", "dropped"
    notes: str = ""


def log(state: str, frame_path: str | Path, notes: str = "") -> None:
    if state not in ("intact", "thinning", "dropped"):
        raise ValueError(f"unknown tail state: {state!r}")
    obs = TailObservation(
        ts=datetime.now(timezone.utc).isoformat(),
        frame=str(frame_path),
        state=state,
        notes=notes,
    )
    TAIL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with TAIL_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(obs)) + "\n")


def history(n: int = 20) -> list[TailObservation]:
    if not TAIL_LOG.exists():
        return []
    lines = TAIL_LOG.read_text(encoding="utf-8").splitlines()[-n:]
    out: list[TailObservation] = []
    for line in lines:
        if not line.strip():
            continue
        data = json.loads(line)
        out.append(TailObservation(**data))
    return out


def latest_state() -> str | None:
    h = history(1)
    return h[0].state if h else None


def has_dropped(observations: Iterable[TailObservation]) -> bool:
    return any(o.state == "dropped" for o in observations)


if __name__ == "__main__":
    state = latest_state() or "no observations yet"
    print(f"latest tail state: {state}")
    for obs in history(5):
        print(f"  {obs.ts}  {obs.state:<9}  {obs.notes}")
