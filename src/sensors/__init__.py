"""Sensor read-out.

In dry mode (no Pi) all sensors return plausible synthetic values that drift
over time so the model has something to react to. In real mode they read
GPIO via adafruit_dht and a float switch.
"""

from __future__ import annotations

import os
import random


_dry_state = {
    "warm_c": 30.5,
    "cool_c": 22.5,
    "humidity_pct": 35.0,
    "water_ok": True,
}


def read_all(pins: dict) -> dict:
    if os.getenv("HARDWARE", "dry").lower() == "real":
        return _read_real(pins)
    return _read_dry()


def _read_dry() -> dict:
    # tiny random walk so the model sees movement, not flat values
    _dry_state["warm_c"] += random.uniform(-0.3, 0.3)
    _dry_state["cool_c"] += random.uniform(-0.2, 0.2)
    _dry_state["humidity_pct"] += random.uniform(-0.8, 0.8)
    _dry_state["warm_c"] = round(max(20.0, min(_dry_state["warm_c"], 36.0)), 2)
    _dry_state["cool_c"] = round(max(18.0, min(_dry_state["cool_c"], 28.0)), 2)
    _dry_state["humidity_pct"] = round(max(15.0, min(_dry_state["humidity_pct"], 70.0)), 1)
    return dict(_dry_state)


def _read_real(pins: dict) -> dict:
    import adafruit_dht  # type: ignore
    import board  # type: ignore
    import RPi.GPIO as GPIO  # type: ignore

    warm = adafruit_dht.DHT22(_pin(board, pins["dht22_data"]))
    cool = adafruit_dht.DHT22(_pin(board, pins["dht22_cool_data"]))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pins["water_level_switch"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    return {
        "warm_c": float(warm.temperature),
        "cool_c": float(cool.temperature),
        "humidity_pct": float(warm.humidity),
        "water_ok": GPIO.input(pins["water_level_switch"]) == 0,
    }


def _pin(board_mod, bcm_number: int):
    return getattr(board_mod, f"D{bcm_number}")
