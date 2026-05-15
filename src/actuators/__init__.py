"""Actuators. Heat lamp relay, water pump, mealworm feeder.

In dry mode the actuators just print what they would do. In real mode they
toggle GPIO pins.
"""

from __future__ import annotations

import os
import time


class Actuators:
    def __init__(self, pins: dict):
        self.pins = pins
        self._real = os.getenv("HARDWARE", "dry").lower() == "real"
        self._heat_on = False
        if self._real:
            self._init_gpio()

    def _init_gpio(self) -> None:
        import RPi.GPIO as GPIO  # type: ignore

        GPIO.setmode(GPIO.BCM)
        for pin in (self.pins["heat_lamp_relay"],
                    self.pins["water_pump_relay"],
                    self.pins["feeder_servo"]):
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        self._gpio = GPIO

    def execute(self, action: dict) -> None:
        name = action.get("name", "noop")
        params = action.get("params", {}) or {}

        if name == "noop":
            return
        if name == "heat_on":
            self._set_heat(True)
        elif name == "heat_off":
            self._set_heat(False)
        elif name == "refill_water":
            self._pump_water(float(params.get("seconds", 0)))
        elif name == "dispense_food":
            self._dispense_one_mealworm()
        elif name == "alert_human":
            self._alert(str(params.get("reason", "robot asked for help")))

    def _set_heat(self, on: bool) -> None:
        if self._heat_on == on:
            return
        self._heat_on = on
        print(f"[actuator] heat lamp -> {'ON' if on else 'OFF'}")
        if self._real:
            self._gpio.output(self.pins["heat_lamp_relay"],
                              self._gpio.HIGH if on else self._gpio.LOW)

    def _pump_water(self, seconds: float) -> None:
        seconds = max(0.0, min(seconds, 10.0))  # belt and braces
        if seconds <= 0:
            return
        print(f"[actuator] water pump -> ON for {seconds:.1f}s")
        if self._real:
            self._gpio.output(self.pins["water_pump_relay"], self._gpio.HIGH)
            time.sleep(seconds)
            self._gpio.output(self.pins["water_pump_relay"], self._gpio.LOW)

    def _dispense_one_mealworm(self) -> None:
        print("[actuator] feeder -> drop 1 mealworm")
        if self._real:
            import RPi.GPIO as GPIO  # type: ignore
            servo = GPIO.PWM(self.pins["feeder_servo"], 50)
            servo.start(0)
            servo.ChangeDutyCycle(7.5)
            time.sleep(0.4)
            servo.ChangeDutyCycle(2.5)
            time.sleep(0.4)
            servo.stop()

    def _alert(self, reason: str) -> None:
        print(f"[actuator] ALERT HUMAN: {reason}")
        topic = os.getenv("NTFY_TOPIC", "").strip()
        if not topic:
            return
        try:
            import requests
            requests.post(f"https://ntfy.sh/{topic}", data=reason.encode("utf-8"), timeout=5)
        except Exception as exc:
            print(f"[actuator] ntfy failed: {exc}")
