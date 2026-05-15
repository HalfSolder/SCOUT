"""Tiered alerts.

Three levels:

  info   journal only, no external notification
  warn   notification, but not waking anyone up
  urgent notification flagged for immediate attention

The notification backend is ntfy.sh if `NTFY_TOPIC` is set, otherwise
stdout. Topics for `warn` and `urgent` can be configured separately so
quiet messages do not vibrate a phone at 4 am.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


Level = Literal["info", "warn", "urgent"]


ALERT_LOG = Path("data/alerts.jsonl")


def send(level: Level, message: str, *, context: dict | None = None) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "message": message,
        "context": context or {},
    }
    ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ALERT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    if level == "info":
        return

    topic = os.getenv("NTFY_TOPIC", "").strip()
    if level == "urgent":
        topic = os.getenv("NTFY_TOPIC_URGENT", topic).strip()

    if not topic:
        print(f"[alert/{level}] {message}")
        return

    try:
        import requests
        priority = {"info": "low", "warn": "default", "urgent": "max"}[level]
        requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode("utf-8"),
            headers={"Priority": priority, "Title": f"Scout / {level}"},
            timeout=5,
        )
    except Exception as exc:
        print(f"[alert] ntfy failed: {exc}")
        print(f"[alert/{level}] {message}")
