"""Weekly weight log.

Crested gecko weight is the single best long-term indicator of health.
Adults should be slowly gaining or steady. Sudden drops mean trouble.

Weights are entered by the keeper (Scout does not have a scale).

CLI:
    python -m src.modules.weight_log add 45.2
    python -m src.modules.weight_log show
    python -m src.modules.weight_log trend
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path


WEIGHTS_CSV = Path("data/weights.csv")


def add(grams: float, when: datetime | None = None) -> None:
    when = when or datetime.now()
    WEIGHTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    new_file = not WEIGHTS_CSV.exists()
    with WEIGHTS_CSV.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "grams"])
        writer.writerow([when.isoformat(timespec="seconds"), f"{grams:.2f}"])


def rows() -> list[tuple[datetime, float]]:
    if not WEIGHTS_CSV.exists():
        return []
    out: list[tuple[datetime, float]] = []
    with WEIGHTS_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ts = datetime.fromisoformat(row["timestamp"])
                grams = float(row["grams"])
                out.append((ts, grams))
            except (KeyError, ValueError):
                continue
    return out


def trend() -> str:
    data = rows()
    if not data:
        return "no weights yet"
    if len(data) == 1:
        return f"single weight: {data[0][1]:.1f} g on {data[0][0].date()}"

    first, last = data[0], data[-1]
    delta = last[1] - first[1]
    weeks = max(1, (last[0] - first[0]).days / 7)
    per_week = delta / weeks

    direction = "up" if per_week >= 0 else "down"
    return (f"latest: {last[1]:.1f} g on {last[0].date()}, "
            f"{abs(delta):.1f} g {direction} over {weeks:.1f} weeks "
            f"({per_week:+.2f} g / week)")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("grams", type=float)

    sub.add_parser("show")
    sub.add_parser("trend")

    args = ap.parse_args()

    if args.cmd == "add":
        add(args.grams)
        print(f"logged {args.grams:.2f} g")
    elif args.cmd == "show":
        for ts, grams in rows():
            print(f"  {ts.date()}  {grams:>6.1f} g")
    elif args.cmd == "trend":
        print(trend())


if __name__ == "__main__":
    sys.exit(main() or 0)
