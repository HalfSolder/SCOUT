"""Fast-forward a simulated day of Scout, with no hardware and no API calls.

Runs the dry-mode sensors and the safety layer against a deterministic
stub brain that drives the crested gecko day-night cycle.

    python scripts/simulate_day.py
    python scripts/simulate_day.py --ticks 60          # one simulated hour
    python scripts/simulate_day.py --ticks 1440        # one simulated day
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from src.actuators import Actuators
from src.journal import Journal
from src.safety import Safety
from src.sensors import read_all


def stub_brain(readings: dict, targets: dict, tick_index: int, ticks_per_day: int) -> dict:
    """A boring, rule-based stand-in for GPT-5.5, on crested gecko schedule."""
    hour = (tick_index % ticks_per_day) * 24 / ticks_per_day
    is_night = hour < 8 or hour >= 20

    hum = readings.get("humidity_pct", 60)
    top = readings.get("top_c", 22)

    if hour == 8:
        return {"action": {"name": "set_lights", "params": {"state": "day"}},
                "reasoning": "day begins"}
    if hour == 20:
        return {"action": {"name": "set_lights", "params": {"state": "night"}},
                "reasoning": "night begins"}

    if not is_night and hour == 9:
        return {"action": {"name": "refresh_cgd", "params": {}},
                "reasoning": "morning CGD refresh"}

    if is_night and hour == 20.5 and hum < 80:
        return {"action": {"name": "mist", "params": {"seconds": 20}},
                "reasoning": "evening humidity spike"}

    if is_night and hum < 70:
        return {"action": {"name": "mist", "params": {"seconds": 8}},
                "reasoning": "night humidity top up"}

    if not readings.get("water_ok", True):
        return {"action": {"name": "refill_water", "params": {"seconds": 3}},
                "reasoning": "reservoir low"}

    return {"action": {"name": "noop", "params": {}}, "reasoning": "stable"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticks", type=int, default=1440, help="ticks to simulate")
    args = ap.parse_args()

    cfg = yaml.safe_load((Path(__file__).resolve().parent.parent / "config.yaml").read_text())

    actuators = Actuators(cfg["pins"])
    journal = Journal(Path("data/simulated_journal.jsonl"))
    safety = Safety(cfg["safety"], actuators)

    counts: dict[str, int] = {}
    overrides = 0

    for i in range(args.ticks):
        readings = read_all(cfg["pins"])

        override = safety.check(readings)
        if override is not None:
            actuators.execute(override)
            journal.append(kind="sim_override", readings=readings, action=override)
            counts[override["name"]] = counts.get(override["name"], 0) + 1
            overrides += 1
            continue

        decision = stub_brain(readings, cfg["targets"], tick_index=i, ticks_per_day=1440)
        action = safety.gate(decision["action"], readings)
        actuators.execute(action)
        journal.append(kind="sim_tick", readings=readings, action=action,
                       reasoning=decision["reasoning"])
        counts[action["name"]] = counts.get(action["name"], 0) + 1

    print("\nsimulated", args.ticks, "ticks.")
    print("action breakdown:")
    for name in sorted(counts):
        print(f"  {name:<22} {counts[name]:>5}")
    print(f"safety overrides: {overrides}")
    print(f"journal: data/simulated_journal.jsonl")


if __name__ == "__main__":
    main()
