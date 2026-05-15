"""Phase 2 bring-up: read one DHT22 probe.

Run on the Pi only. Wire the data line to the BCM pin given on the
command line, with a 4.7 kΩ pull-up to 3.3 V on the data line.

    python scripts/bringup/test_dht22.py 4
"""

from __future__ import annotations

import sys
import time


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: test_dht22.py <BCM_PIN>")
        sys.exit(1)
    pin = int(sys.argv[1])

    import adafruit_dht  # type: ignore
    import board  # type: ignore

    probe = adafruit_dht.DHT22(getattr(board, f"D{pin}"))
    print(f"reading DHT22 on BCM pin {pin}. Ctrl-C to stop.")
    try:
        while True:
            try:
                t = probe.temperature
                h = probe.humidity
                print(f"  {t:>5.1f} °C    {h:>5.1f} %")
            except RuntimeError as exc:
                print(f"  read failed: {exc}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\ndone.")


if __name__ == "__main__":
    main()
