"""Tests for src/safety.py.

The safety layer is the only code in this repo whose job is to be wrong
about the model. Test it on its own.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.safety import Safety


SAFETY_CFG = {
    "max_warm_c": 35,
    "min_warm_c": 22,
    "max_humidity_pct": 80,
    "max_mealworms_per_day": 6,
    "max_water_pump_seconds_per_tick": 5,
}


@pytest.fixture
def safety():
    return Safety(SAFETY_CFG, actuators=None)


# check() runs BEFORE the model. It returns an override action when the
# environment is unsafe enough to skip asking the model.

def test_check_returns_none_when_in_range(safety):
    readings = {"warm_c": 31.0, "cool_c": 22.5, "humidity_pct": 35.0, "water_ok": True}
    assert safety.check(readings) is None


def test_check_forces_heat_off_when_warm_side_too_hot(safety):
    readings = {"warm_c": 36.0, "cool_c": 23.0, "humidity_pct": 40.0, "water_ok": True}
    override = safety.check(readings)
    assert override is not None
    assert override["name"] == "heat_off"
    assert "36" in override["reason"]


def test_check_alerts_human_when_warm_side_too_cold(safety):
    readings = {"warm_c": 18.0, "cool_c": 17.0, "humidity_pct": 30.0, "water_ok": True}
    override = safety.check(readings)
    assert override is not None
    assert override["name"] == "alert_human"


def test_check_ignores_missing_warm_reading(safety):
    readings = {"warm_c": None, "cool_c": 22.0, "humidity_pct": 35.0, "water_ok": True}
    assert safety.check(readings) is None


# gate() runs AFTER the model. It sanitises the action the model returned.

def test_gate_caps_water_pump_seconds(safety):
    action = {"name": "refill_water", "params": {"seconds": 30}}
    gated = safety.gate(action, readings={})
    assert gated["name"] == "refill_water"
    assert gated["params"]["seconds"] == SAFETY_CFG["max_water_pump_seconds_per_tick"]


def test_gate_allows_water_below_cap(safety):
    action = {"name": "refill_water", "params": {"seconds": 2}}
    gated = safety.gate(action, readings={})
    assert gated["params"]["seconds"] == 2


def test_gate_allows_feed_up_to_daily_limit(safety):
    for _ in range(SAFETY_CFG["max_mealworms_per_day"]):
        gated = safety.gate({"name": "dispense_food", "params": {}}, readings={})
        assert gated["name"] == "dispense_food"


def test_gate_blocks_feed_after_daily_limit(safety):
    for _ in range(SAFETY_CFG["max_mealworms_per_day"]):
        safety.gate({"name": "dispense_food", "params": {}}, readings={})

    blocked = safety.gate({"name": "dispense_food", "params": {}}, readings={})
    assert blocked["name"] == "noop"


def test_gate_prunes_feed_log_after_24_hours(safety):
    # backdate every entry so the prune wipes the day
    long_ago = datetime.now(timezone.utc) - timedelta(hours=25)
    for _ in range(SAFETY_CFG["max_mealworms_per_day"]):
        safety.feed_log.append(long_ago)

    gated = safety.gate({"name": "dispense_food", "params": {}}, readings={})
    assert gated["name"] == "dispense_food"


def test_gate_passes_noop_through_unchanged(safety):
    gated = safety.gate({"name": "noop", "params": {}}, readings={})
    assert gated == {"name": "noop", "params": {}}
