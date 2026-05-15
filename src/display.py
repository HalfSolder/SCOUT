"""LCD output.

The real LCD on the Pi is driven via HDMI to a small touchscreen. The display
module just writes the current state to a file (`data/display.txt`) and prints
to stdout for now. A small GUI process can render that file in fullscreen.

This keeps the brain decoupled from any specific display library so we can
swap renderers (pygame, tkinter, framebuffer) without changing the loop.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


class Display:
    def __init__(self, state_path: Path = Path("data/display.txt")):
        self.state_path = state_path
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

    def show_boot(self, message: str) -> None:
        self._write(f"[boot] {message}")

    def show_alert(self, reason: str) -> None:
        self._write(f"[!! safety override] {reason}")

    def show_tick(self, frame_path: Path, readings: dict, action: dict, reasoning: str) -> None:
        warm = readings.get("warm_c", "?")
        cool = readings.get("cool_c", "?")
        hum = readings.get("humidity_pct", "?")
        water = "ok" if readings.get("water_ok") else "LOW"
        body = (
            f"frame:  {frame_path}\n"
            f"warm:   {warm} °C\n"
            f"cool:   {cool} °C\n"
            f"humid:  {hum} %\n"
            f"water:  {water}\n"
            f"action: {action.get('name')}  {action.get('params', {})}\n"
            f"why:    {reasoning}"
        )
        self._write(body)

    def _write(self, body: str) -> None:
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"{stamp}\n{body}\n"
        self.state_path.write_text(text, encoding="utf-8")
        print(f"\n=== Scout @ {stamp} ===\n{body}")
