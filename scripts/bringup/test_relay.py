"""Phase 2 bring-up: click a relay channel on and off.

Run on the Pi only. Connect NOTHING to the relay's switched side for the
first run. Listen for the click. Then connect a low-voltage test load
(e.g. a 5 V LED through a resistor) and run again.

    python scripts/bringup/test_relay.py 18
"""

from __future__ import annotations

import sys
import time


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: test_relay.py <BCM_PIN>")
        sys.exit(1)
    pin = int(sys.argv[1])

    import RPi.GPIO as GPIO  # type: ignore

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

    print(f"toggling relay on BCM pin {pin} every 2 seconds. Ctrl-C to stop.")
    state = False
    try:
        while True:
            state = not state
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
            print(f"  relay -> {'ON' if state else 'OFF'}")
            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup(pin)
        print("\nrelay left OFF. done.")


if __name__ == "__main__":
    main()
