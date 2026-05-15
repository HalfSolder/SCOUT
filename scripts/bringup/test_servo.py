"""Phase 2 bring-up: sweep the mealworm feeder servo.

Run on the Pi only. The servo arm should rotate to the open position,
release one mealworm, then rotate back to the closed position. Do this
with the hopper EMPTY for the first run. Then with one mealworm. Then
with five, to check it does not jam.

    python scripts/bringup/test_servo.py 23
"""

from __future__ import annotations

import sys
import time


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: test_servo.py <BCM_PIN>")
        sys.exit(1)
    pin = int(sys.argv[1])

    import RPi.GPIO as GPIO  # type: ignore

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin, 50)
    servo.start(0)

    try:
        for cycle in range(3):
            print(f"  cycle {cycle + 1}: open ...")
            servo.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            print(f"  cycle {cycle + 1}: close.")
            servo.ChangeDutyCycle(2.5)
            time.sleep(0.5)
            servo.ChangeDutyCycle(0)
            time.sleep(2)
    finally:
        servo.stop()
        GPIO.cleanup(pin)
        print("done.")


if __name__ == "__main__":
    main()
