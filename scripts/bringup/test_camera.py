"""Phase 2 bring-up: capture one frame from the Pi camera.

Run on the Pi only. Writes a single JPEG to ./bringup_frame.jpg. Open it
and confirm the field of view covers the whole tank including the warm
hide, the cool hide, the water dish and the feeding dish.

    python scripts/bringup/test_camera.py
"""

from __future__ import annotations

import time
from pathlib import Path


def main() -> None:
    from picamera2 import Picamera2  # type: ignore

    cam = Picamera2()
    cfg = cam.create_still_configuration(main={"size": (1024, 768)})
    cam.configure(cfg)
    cam.start()
    time.sleep(2)

    out = Path("bringup_frame.jpg").resolve()
    cam.capture_file(str(out))
    cam.close()

    print(f"saved {out}")


if __name__ == "__main__":
    main()
