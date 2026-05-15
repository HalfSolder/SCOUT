"""Journal analyser.

Reads `data/journal.jsonl` (or any path) and computes the metrics named
in `docs/EXPERIMENT.md`. Outputs a small textual report.

CLI:
    python -m src.modules.metrics
    python -m src.modules.metrics data/simulated_journal.jsonl
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def percent_in_temperature_band(rows: list[dict], band: tuple[float, float]) -> float:
    lo, hi = band
    relevant = [r for r in rows if (r.get("readings") or {}).get("top_c") is not None]
    if not relevant:
        return 0.0
    inside = sum(1 for r in relevant
                 if lo <= r["readings"]["top_c"] <= hi)
    return 100 * inside / len(relevant)


def percent_in_humidity_band(rows: list[dict], band: tuple[float, float]) -> float:
    lo, hi = band
    relevant = [r for r in rows if (r.get("readings") or {}).get("humidity_pct") is not None]
    if not relevant:
        return 0.0
    inside = sum(1 for r in relevant
                 if lo <= r["readings"]["humidity_pct"] <= hi)
    return 100 * inside / len(relevant)


def action_breakdown(rows: list[dict]) -> Counter:
    c: Counter = Counter()
    for r in rows:
        name = ((r.get("action") or {}).get("name")) or "<no action>"
        c[name] += 1
    return c


def safety_override_count(rows: list[dict]) -> int:
    return sum(1 for r in rows if r.get("kind") == "safety_override")


def alert_human_count(rows: list[dict]) -> int:
    return sum(1 for r in rows
               if ((r.get("action") or {}).get("name")) == "alert_human")


def report(rows: list[dict]) -> str:
    if not rows:
        return "no rows yet."
    lines = [f"{len(rows)} ticks loaded.", ""]

    lines.append(f"% top_c in day band (22-26 C):   "
                 f"{percent_in_temperature_band(rows, (22.0, 26.0)):>5.1f} %")
    lines.append(f"% top_c in night band (18-22 C): "
                 f"{percent_in_temperature_band(rows, (18.0, 22.0)):>5.1f} %")
    lines.append(f"% humidity in day band (50-70):  "
                 f"{percent_in_humidity_band(rows, (50.0, 70.0)):>5.1f} %")
    lines.append(f"% humidity in night band (80+):  "
                 f"{percent_in_humidity_band(rows, (80.0, 100.0)):>5.1f} %")
    lines.append("")
    lines.append(f"safety overrides:   {safety_override_count(rows):>5}")
    lines.append(f"alert_human events: {alert_human_count(rows):>5}")
    lines.append("")
    lines.append("action breakdown:")
    for name, count in action_breakdown(rows).most_common():
        lines.append(f"  {name:<22} {count:>5}")
    return "\n".join(lines)


def main() -> None:
    default = Path("data/journal.jsonl")
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    rows = load(path)
    print(report(rows))


if __name__ == "__main__":
    main()
