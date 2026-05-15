"""Sensor read-out.

In dry mode (no Pi) all sensors return plausible synthetic values that
drift over time so the model has something to react to. In real mode
they read GPIO via adafruit_dht and a float switch.

For a crested gecko we track top and bottom of the arboreal enclosure
separately (Biscuit climbs) and a humidity cycle (day, night).
"""

from __future__ import annotations

import os
import random


_dry_state = {
    "top_c": 23.5,
    "bottom_c": 22.0,
    "humidity_pct": 60.0,
    "water_ok": True,
}


def read_all(pins: dict) -> dict:
    if os.getenv("HARDWARE", "dry").lower() == "real":
        return _read_real(pins)
    return _read_dry()


def _read_dry() -> dict:
    # small random walk so the model sees movement
    _dry_state["top_c"] += random.uniform(-0.2, 0.2)
    _dry_state["bottom_c"] += random.uniform(-0.2, 0.2)
    _dry_state["humidity_pct"] += random.uniform(-1.5, 1.5)
    _dry_state["top_c"] = round(max(18.0, min(_dry_state["top_c"], 27.0)), 2)
    _dry_state["bottom_c"] = round(max(17.0, min(_dry_state["bottom_c"], 26.0)), 2)
    _dry_state["humidity_pct"] = round(max(35.0, min(_dry_state["humidity_pct"], 95.0)), 1)
    return dict(_dry_state)


def _read_real(pins: dict) -> dict:
    import adafruit_dht  # type: ignore
    import board  # type: ignore
    import RPi.GPIO as GPIO  # type: ignore

    top = adafruit_dht.DHT22(_pin(board, pins["dht22_top_data"]))
    bottom = adafruit_dht.DHT22(_pin(board, pins["dht22_bottom_data"]))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pins["water_level_switch"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    return {
        "top_c": float(top.temperature),
        "bottom_c": float(bottom.temperature),
        "humidity_pct": float(top.humidity),
        "water_ok": GPIO.input(pins["water_level_switch"]) == 0,
    }


def _pin(board_mod, bcm_number: int):
    return getattr(board_mod, f"D{bcm_number}")
