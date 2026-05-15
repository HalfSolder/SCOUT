"""Fast-forward a simulated day of Scout, with no hardware and no API calls.

Runs the dry-mode sensors and the safety layer against a deterministic
stub brain that picks reasonable actions. Useful for sanity-checking the
pipeline (synthetic sensors -> safety -> action -> journal) at speed,
without burning OpenAI tokens.

    python scripts/simulate_day.py
    python scripts/simulate_day.py --ticks 60          # one simulated hour
    python scripts/simulate_day.py --ticks 1440        # one simulated day
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# allow running from repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

from src.actuators import Actuators
from src.journal import Journal
from src.safety import Safety
from src.sensors import read_all


def stub_brain(readings: dict, targets: dict) -> dict:
    """A boring, rule-based stand-in for GPT-5.5."""
    warm_lo, warm_hi = targets["warm_side_c"]
    warm = readings.get("warm_c", warm_lo)

    if warm < warm_lo:
        return {"action": {"name": "heat_on", "params": {}},
                "reasoning": "warm side below target"}
    if warm > warm_hi:
        return {"action": {"name": "heat_off", "params": {}},
                "reasoning": "warm side above target"}
    if not readings.get("water_ok", True):
        return {"action": {"name": "refill_water", "params": {"seconds": 3}},
                "reasoning": "reservoir low"}
    return {"action": {"name": "noop", "params": {}},
            "reasoning": "stable"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticks", type=int, default=1440, help="how many ticks to simulate")
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

        decision = stub_brain(readings, cfg["targets"])
        action = safety.gate(decision["action"], readings)
        actuators.execute(action)
        journal.append(kind="sim_tick", readings=readings, action=action,
                       reasoning=decision["reasoning"])
        counts[action["name"]] = counts.get(action["name"], 0) + 1

    print("\nsimulated", args.ticks, "ticks.")
    print("action breakdown:")
    for name in sorted(counts):
        print(f"  {name:<16} {counts[name]:>5}")
    print(f"safety overrides: {overrides}")
    print(f"journal: data/simulated_journal.jsonl")


if __name__ == "__main__":
    main()
