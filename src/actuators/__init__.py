"""Actuators. Misting solenoid, CGD pump, insect feeder, water pump, lights, IR lamp.

In dry mode the actuators just print what they would do. In real mode
they toggle GPIO pins.
"""

from __future__ import annotations

import os
import time


class Actuators:
    def __init__(self, pins: dict):
        self.pins = pins
        self._real = os.getenv("HARDWARE", "dry").lower() == "real"
        self._lights_state = "off"
        if self._real:
            self._init_gpio()

    def _init_gpio(self) -> None:
        import RPi.GPIO as GPIO  # type: ignore

        GPIO.setmode(GPIO.BCM)
        for pin in (self.pins.get("misting_solenoid_relay"),
                    self.pins.get("fogger_relay"),
                    self.pins.get("cgd_pump_relay"),
                    self.pins.get("water_pump_relay"),
                    self.pins.get("day_lights_relay"),
                    self.pins.get("ir_lamp_relay"),
                    self.pins.get("insect_feeder_servo")):
            if pin is None:
                continue
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        self._gpio = GPIO

    def execute(self, action: dict) -> None:
        name = action.get("name", "noop")
        params = action.get("params", {}) or {}

        if name == "noop":
            return
        if name == "mist":
            self._mist(float(params.get("seconds", 0)))
        elif name == "refresh_cgd":
            self._refresh_cgd()
        elif name == "offer_insect":
            self._offer_insect()
        elif name == "refill_water":
            self._pump_water(float(params.get("seconds", 0)))
        elif name == "set_lights":
            self._set_lights(str(params.get("state", "off")))
        elif name == "record_observation":
            self._record(str(params.get("note", "")))
        elif name == "alert_human":
            self._alert(str(params.get("reason", "Scout asked for help")))

    def _mist(self, seconds: float) -> None:
        seconds = max(0.0, min(seconds, 30.0))
        if seconds <= 0:
            return
        print(f"[actuator] misting nozzle -> ON for {seconds:.1f}s")
        if self._real:
            self._gpio.output(self.pins["misting_solenoid_relay"], self._gpio.HIGH)
            time.sleep(seconds)
            self._gpio.output(self.pins["misting_solenoid_relay"], self._gpio.LOW)

    def _refresh_cgd(self) -> None:
        print("[actuator] CGD pump -> dose")
        if self._real:
            self._gpio.output(self.pins["cgd_pump_relay"], self._gpio.HIGH)
            time.sleep(2.5)
            self._gpio.output(self.pins["cgd_pump_relay"], self._gpio.LOW)

    def _offer_insect(self) -> None:
        print("[actuator] insect feeder -> drop 1")
        if self._real:
            servo = self._gpio.PWM(self.pins["insect_feeder_servo"], 50)
            servo.start(0)
            servo.ChangeDutyCycle(7.5)
            time.sleep(0.4)
            servo.ChangeDutyCycle(2.5)
            time.sleep(0.4)
            servo.stop()

    def _pump_water(self, seconds: float) -> None:
        seconds = max(0.0, min(seconds, 5.0))
        if seconds <= 0:
            return
        print(f"[actuator] water pump -> ON for {seconds:.1f}s")
        if self._real:
            self._gpio.output(self.pins["water_pump_relay"], self._gpio.HIGH)
            time.sleep(seconds)
            self._gpio.output(self.pins["water_pump_relay"], self._gpio.LOW)

    def _set_lights(self, state: str) -> None:
        if state == self._lights_state:
            return
        self._lights_state = state
        print(f"[actuator] lights -> {state}")
        if not self._real:
            return
        day_pin = self.pins.get("day_lights_relay")
        ir_pin = self.pins.get("ir_lamp_relay")
        if state == "day":
            if day_pin is not None: self._gpio.output(day_pin, self._gpio.HIGH)
            if ir_pin is not None: self._gpio.output(ir_pin, self._gpio.LOW)
        elif state == "night":
            if day_pin is not None: self._gpio.output(day_pin, self._gpio.LOW)
            if ir_pin is not None: self._gpio.output(ir_pin, self._gpio.HIGH)
        else:
            if day_pin is not None: self._gpio.output(day_pin, self._gpio.LOW)
            if ir_pin is not None: self._gpio.output(ir_pin, self._gpio.LOW)

    def _record(self, note: str) -> None:
        print(f"[actuator] observation: {note}")

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
