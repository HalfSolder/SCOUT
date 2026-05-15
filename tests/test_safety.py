"""Tests for src/safety.py.

Crested gecko version. The safety layer is the only code in this repo
whose job is to be wrong about the model. Test it on its own.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.safety import Safety


SAFETY_CFG = {
    "max_ambient_c": 28,
    "min_ambient_c": 16,
    "max_humidity_pct_extended": 90,
    "min_humidity_pct_extended": 40,
    "max_mist_seconds_per_tick": 30,
    "max_cgd_refreshes_per_day": 2,
    "max_insects_per_week": 8,
}


@pytest.fixture
def safety():
    return Safety(SAFETY_CFG, actuators=None)


# check() runs BEFORE the model.

def test_check_returns_none_when_in_range(safety):
    readings = {"top_c": 24.0, "bottom_c": 22.5, "humidity_pct": 60.0, "water_ok": True}
    assert safety.check(readings) is None


def test_check_alerts_when_top_too_hot(safety):
    readings = {"top_c": 29.0, "bottom_c": 27.0, "humidity_pct": 50.0, "water_ok": True}
    override = safety.check(readings)
    assert override is not None
    assert override["name"] == "alert_human"
    assert "29" in override["reason"]


def test_check_alerts_when_too_cold(safety):
    readings = {"top_c": 14.0, "bottom_c": 13.5, "humidity_pct": 55.0, "water_ok": True}
    override = safety.check(readings)
    assert override is not None
    assert override["name"] == "alert_human"


def test_check_uses_hottest_of_top_or_bottom(safety):
    readings = {"top_c": 23.0, "bottom_c": 29.0, "humidity_pct": 60.0, "water_ok": True}
    override = safety.check(readings)
    assert override is not None
    assert override["name"] == "alert_human"


def test_check_ignores_missing_temperature(safety):
    readings = {"humidity_pct": 60.0, "water_ok": True}
    assert safety.check(readings) is None


# gate() runs AFTER the model.

def test_gate_caps_mist_seconds(safety):
    action = {"name": "mist", "params": {"seconds": 120}}
    gated = safety.gate(action, readings={})
    assert gated["name"] == "mist"
    assert gated["params"]["seconds"] == SAFETY_CFG["max_mist_seconds_per_tick"]


def test_gate_allows_mist_below_cap(safety):
    action = {"name": "mist", "params": {"seconds": 8}}
    gated = safety.gate(action, readings={})
    assert gated["params"]["seconds"] == 8


def test_gate_caps_water_pump(safety):
    action = {"name": "refill_water", "params": {"seconds": 30}}
    gated = safety.gate(action, readings={})
    assert gated["params"]["seconds"] == 5


def test_gate_allows_cgd_refresh_up_to_daily_limit(safety):
    for _ in range(SAFETY_CFG["max_cgd_refreshes_per_day"]):
        gated = safety.gate({"name": "refresh_cgd", "params": {}}, readings={})
        assert gated["name"] == "refresh_cgd"


def test_gate_blocks_cgd_refresh_after_daily_limit(safety):
    for _ in range(SAFETY_CFG["max_cgd_refreshes_per_day"]):
        safety.gate({"name": "refresh_cgd", "params": {}}, readings={})

    blocked = safety.gate({"name": "refresh_cgd", "params": {}}, readings={})
    assert blocked["name"] == "noop"


def test_gate_allows_insect_up_to_weekly_limit(safety):
    for _ in range(SAFETY_CFG["max_insects_per_week"]):
        gated = safety.gate({"name": "offer_insect", "params": {}}, readings={})
        assert gated["name"] == "offer_insect"


def test_gate_blocks_insect_after_weekly_limit(safety):
    for _ in range(SAFETY_CFG["max_insects_per_week"]):
        safety.gate({"name": "offer_insect", "params": {}}, readings={})

    blocked = safety.gate({"name": "offer_insect", "params": {}}, readings={})
    assert blocked["name"] == "noop"


def test_gate_prunes_cgd_log_after_24_hours(safety):
    long_ago = datetime.now(timezone.utc) - timedelta(hours=25)
    for _ in range(SAFETY_CFG["max_cgd_refreshes_per_day"]):
        safety.cgd_log.append(long_ago)

    gated = safety.gate({"name": "refresh_cgd", "params": {}}, readings={})
    assert gated["name"] == "refresh_cgd"


def test_gate_prunes_insect_log_after_one_week(safety):
    long_ago = datetime.now(timezone.utc) - timedelta(days=8)
    for _ in range(SAFETY_CFG["max_insects_per_week"]):
        safety.insect_log.append(long_ago)

    gated = safety.gate({"name": "offer_insect", "params": {}}, readings={})
    assert gated["name"] == "offer_insect"


def test_gate_passes_noop_through_unchanged(safety):
    gated = safety.gate({"name": "noop", "params": {}}, readings={})
    assert gated == {"name": "noop", "params": {}}


def test_gate_passes_set_lights_through_unchanged(safety):
    action = {"name": "set_lights", "params": {"state": "night"}}
    gated = safety.gate(action, readings={})
    assert gated == action


def test_gate_passes_alert_human_through_unchanged(safety):
    action = {"name": "alert_human", "params": {"reason": "test"}}
    gated = safety.gate(action, readings={})
    assert gated == action
