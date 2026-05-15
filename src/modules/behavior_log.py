"""Behaviour observations from camera frames or human notes.

Each observation is a short tag plus optional notes plus the frame at
that moment. Over time these build up a picture of what "normal" looks
like for Biscuit so anomalies stand out.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


BEHAVIOR_LOG = Path("data/behavior_log.jsonl")


KNOWN_TAGS = {
    "hidden_top", "hidden_low", "on_glass", "on_branch_high",
    "on_branch_low", "on_ground", "drinking", "eating_cgd",
    "eating_insect", "sleeping", "alert", "panting", "shedding",
    "exploring", "out_of_view",
}


@dataclass
class Observation:
    ts: str
    tag: str
    notes: str = ""
    frame: str = ""


def log(tag: str, notes: str = "", frame: str = "") -> None:
    if tag not in KNOWN_TAGS:
        # not an error, just a free-form tag
        pass
    obs = Observation(
        ts=datetime.now(timezone.utc).isoformat(),
        tag=tag,
        notes=notes,
        frame=frame,
    )
    BEHAVIOR_LOG.parent.mkdir(parents=True, exist_ok=True)
    with BEHAVIOR_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(obs)) + "\n")


def history(n: int = 50) -> list[Observation]:
    if not BEHAVIOR_LOG.exists():
        return []
    out: list[Observation] = []
    for line in BEHAVIOR_LOG.read_text(encoding="utf-8").splitlines()[-n:]:
        if not line.strip():
            continue
        out.append(Observation(**json.loads(line)))
    return out


def tag_counts(n: int = 500) -> dict[str, int]:
    counts: dict[str, int] = {}
    for obs in history(n):
        counts[obs.tag] = counts.get(obs.tag, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: -kv[1]))


if __name__ == "__main__":
    counts = tag_counts()
    if not counts:
        print("no behaviour observations yet")
    else:
        for tag, n in counts.items():
            print(f"  {tag:<18} {n:>4}")
