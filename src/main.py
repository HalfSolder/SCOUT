"""The tick loop: observe, think, act, log.

Run with:  python -m src.main
"""

from __future__ import annotations

import signal
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

from .brain import Brain
from .display import Display
from .journal import Journal
from .safety import Safety
from .sensors import read_all
from .actuators import Actuators
from .vision import Camera


def load_config() -> dict:
    cfg_path = Path(__file__).resolve().parent.parent / "config.yaml"
    with cfg_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_night(cfg: dict) -> bool:
    hour = datetime.now().hour
    day_start = cfg.get("day_starts_hour", 8)
    night_start = cfg.get("night_starts_hour", 20)
    return not (day_start <= hour < night_start)


def main() -> None:
    load_dotenv()
    cfg = load_config()

    camera = Camera(cfg["camera"])
    actuators = Actuators(cfg["pins"])
    journal = Journal(Path("data/journal.jsonl"))
    display = Display()
    safety = Safety(cfg["safety"], actuators)
    brain = Brain(model=cfg["model"], system_prompt_path=Path("prompts/system.md"), config=cfg)

    running = True

    def _stop(*_):
        nonlocal running
        running = False
        print("\n[scout] shutting down...")

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    print(f"[scout] tick = {cfg['tick_seconds']}s, model = {cfg['model']}, "
          f"animal = {cfg.get('animal_name', 'Biscuit')} ({cfg.get('species', 'crested_gecko')})")
    display.show_boot("Scout online. Watching Biscuit.")

    while running:
        tick_started = time.time()

        frame_path, frame_b64 = camera.snapshot()
        readings = read_all(cfg["pins"])
        night = is_night(cfg)

        override = safety.check(readings)
        if override is not None:
            journal.append(kind="safety_override", readings=readings, action=override, night=night)
            display.show_alert(override["reason"])
            actuators.execute(override)
            _sleep_until(tick_started + cfg["tick_seconds"])
            continue

        recent = journal.recent(n=8)
        decision = brain.decide(readings=readings, frame_b64=frame_b64, history=recent,
                                is_night=night)

        action = safety.gate(decision["action"], readings)
        actuators.execute(action)

        journal.append(
            kind="tick",
            readings=readings,
            frame=str(frame_path),
            action=action,
            reasoning=decision.get("reasoning", ""),
            night=night,
        )

        display.show_tick(frame_path=frame_path, readings=readings, action=action,
                          reasoning=decision.get("reasoning", ""))

        _sleep_until(tick_started + cfg["tick_seconds"])

    display.show_boot("Scout offline")
    print("[scout] stopped cleanly.")


def _sleep_until(target_ts: float) -> None:
    remaining = target_ts - time.time()
    if remaining > 0:
        time.sleep(remaining)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[scout] fatal: {exc}", file=sys.stderr)
        raise
