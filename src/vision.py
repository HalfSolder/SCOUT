"""Pi camera capture.

On the Pi (HARDWARE=real) this uses picamera2. Off-Pi (HARDWARE=dry) it
returns a placeholder image so the rest of the loop can run on a laptop.
"""

from __future__ import annotations

import base64
import io
import os
import time
from pathlib import Path

from PIL import Image, ImageDraw


class Camera:
    def __init__(self, camera_cfg: dict):
        self.width = camera_cfg["width"]
        self.height = camera_cfg["height"]
        self.frames_dir = Path("data/frames")
        self.frames_dir.mkdir(parents=True, exist_ok=True)
        self._real = os.getenv("HARDWARE", "dry").lower() == "real"
        self._picam = self._init_real() if self._real else None

    def _init_real(self):
        from picamera2 import Picamera2  # type: ignore

        cam = Picamera2()
        cfg = cam.create_still_configuration(main={"size": (self.width, self.height)})
        cam.configure(cfg)
        cam.start()
        time.sleep(2)  # let the sensor warm up
        return cam

    def snapshot(self) -> tuple[Path, str]:
        ts = int(time.time())
        frame_path = self.frames_dir / f"{ts}.jpg"

        if self._real and self._picam is not None:
            self._picam.capture_file(str(frame_path))
            img = Image.open(frame_path)
        else:
            img = _placeholder_frame(self.width, self.height, ts)
            img.save(frame_path, "JPEG", quality=80)

        buf = io.BytesIO()
        img.convert("RGB").save(buf, "JPEG", quality=70)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return frame_path, b64


def _placeholder_frame(width: int, height: int, ts: int) -> Image.Image:
    img = Image.new("RGB", (width, height), color=(30, 28, 24))
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), f"[dry-run] no camera attached  t={ts}", fill=(200, 200, 200))
    draw.rectangle([(width // 3, height // 2), (2 * width // 3, height // 2 + 40)],
                   outline=(160, 140, 90), width=2)
    draw.text((width // 3 + 8, height // 2 + 12), "gecko goes here", fill=(160, 140, 90))
    return img
