"""Light smoke tests for a few modules in src/modules/.

We are not aiming for full coverage. These tests catch the obvious
regressions: humidity verdict math, CGD recipe shape, temperature zone
diagnosis, baseline scheduling.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.modules import (
    baseline_controller,
    cgd_feeding,
    day_night_cycle,
    humidity_cycler,
    night_vision,
    temperature_zones,
)


# humidity_cycler ----------------------------------------------------

def test_humidity_in_day_band_is_in_band():
    v = humidity_cycler.verdict(60.0, is_night=False)
    assert v.in_band is True
    assert v.suggestion is None


def test_humidity_too_low_in_day_suggests_mist():
    v = humidity_cycler.verdict(40.0, is_night=False)
    assert v.in_band is False
    assert v.suggestion == "mist"
    assert v.suggested_seconds > 0


def test_humidity_in_night_band_is_in_band():
    v = humidity_cycler.verdict(90.0, is_night=True)
    assert v.in_band is True


def test_humidity_too_low_at_night_suggests_more_misting_than_day():
    night = humidity_cycler.verdict(50.0, is_night=True)
    day = humidity_cycler.verdict(50.0, is_night=False)
    assert night.suggested_seconds >= day.suggested_seconds


# cgd_feeding --------------------------------------------------------

def test_cgd_recipe_is_two_one_water_to_powder():
    recipe = cgd_feeding.recipe_for_one_dish(grams=6.0)
    assert recipe.water_grams == pytest.approx(2 * recipe.powder_grams)
    assert recipe.total_grams == pytest.approx(6.0)


# temperature_zones --------------------------------------------------

def test_zone_reading_detects_hot_top():
    zone = temperature_zones.from_readings({"top_c": 28.5, "bottom_c": 24.0})
    assert zone is not None
    assert zone.hot is True
    notes = temperature_zones.diagnose(zone)
    assert any("hot" in n for n in notes)


def test_zone_reading_detects_inverted_gradient():
    zone = temperature_zones.from_readings({"top_c": 22.0, "bottom_c": 24.0})
    assert zone is not None
    assert zone.inverted is True


# night_vision -------------------------------------------------------

def test_ir_should_be_on_at_night():
    midnight = datetime(2026, 5, 15, 1, 30, tzinfo=timezone.utc)
    assert night_vision.should_ir_be_on(midnight, 8, 20) is True


def test_ir_should_be_off_at_noon():
    noon = datetime(2026, 5, 15, 12, 0, tzinfo=timezone.utc)
    assert night_vision.should_ir_be_on(noon, 8, 20) is False


# day_night_cycle ----------------------------------------------------

def test_phase_is_day_in_the_middle_of_the_day():
    noon = datetime(2026, 5, 15, 12, 0)
    assert day_night_cycle.current_phase(noon, 8, 20) is day_night_cycle.Phase.DAY


def test_phase_is_dawn_near_lights_on():
    just_after_dawn = datetime(2026, 5, 15, 8, 10)
    assert day_night_cycle.current_phase(just_after_dawn, 8, 20) is day_night_cycle.Phase.DAWN


def test_phase_is_dusk_near_lights_off():
    just_before_night = datetime(2026, 5, 15, 19, 50)
    assert day_night_cycle.current_phase(just_before_night, 8, 20) is day_night_cycle.Phase.DUSK


# baseline_controller ------------------------------------------------

def test_baseline_alerts_when_too_hot():
    readings = {"top_c": 27.5, "bottom_c": 26.0, "humidity_pct": 55, "water_ok": True}
    out = baseline_controller.decide(readings, datetime(2026, 5, 15, 14, 0), None)
    assert out["action"]["name"] == "alert_human"


def test_baseline_does_evening_mist():
    readings = {"top_c": 24.0, "bottom_c": 22.5, "humidity_pct": 60, "water_ok": True}
    out = baseline_controller.decide(readings, datetime(2026, 5, 15, 20, 1), None)
    assert out["action"]["name"] in ("mist", "set_lights")


def test_baseline_idles_when_stable():
    readings = {"top_c": 24.0, "bottom_c": 22.5, "humidity_pct": 60, "water_ok": True}
    out = baseline_controller.decide(readings, datetime(2026, 5, 15, 14, 30), None)
    assert out["action"]["name"] == "noop"
