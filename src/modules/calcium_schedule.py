"""Calcium and D3 dusting schedule.

CGD is complete but supplemental dusted insects need calcium plus D3
on roughly every other feed and plain calcium on the rest. Missing
calcium is the fast path to metabolic bone disease (MBD), which is
permanent and visible.

This module remembers what the last insect was dusted with and tells
the keeper (or the prompt) what the next one should be.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


DUSTING_LOG = Path("data/dusting_log.jsonl")


def log(supplement: str) -> None:
    if supplement not in ("calcium", "calcium_d3", "multivitamin", "none"):
        raise ValueError(f"unknown supplement: {supplement!r}")
    DUSTING_LOG.parent.mkdir(parents=True, exist_ok=True)
    with DUSTING_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(),
            "supplement": supplement,
        }) + "\n")


def last_supplement() -> str | None:
    if not DUSTING_LOG.exists():
        return None
    for line in reversed(DUSTING_LOG.read_text(encoding="utf-8").splitlines()):
        if line.strip():
            return json.loads(line).get("supplement")
    return None


def next_supplement() -> str:
    """The plain rotation: D3 -> calcium -> D3 -> calcium ..."""
    last = last_supplement()
    if last in (None, "calcium", "none"):
        return "calcium_d3"
    if last == "calcium_d3":
        return "calcium"
    return "calcium"


if __name__ == "__main__":
    print(f"last supplement: {last_supplement() or 'none yet'}")
    print(f"next insect should be dusted with: {next_supplement()}")
