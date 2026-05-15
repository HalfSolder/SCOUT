"""Grok brain.

Each tick the brain receives:
  - The current sensor readings.
  - A photo of the tank (base64).
  - A short history of recent ticks (so it knows what it just did).
  - Whether it is currently day or night.

It must return a structured decision: an action and a one-line reasoning.

Uses xAI's OpenAI-compatible API. The `openai` Python SDK is pointed at
`https://api.x.ai/v1` and supplied an `XAI_API_KEY`.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI


VALID_ACTIONS = {
    "noop",                 # do nothing, keep watching
    "mist",                 # run the misting nozzle, params.seconds
    "refresh_cgd",          # signal CGD should be replaced
    "offer_insect",         # drop one dusted insect
    "refill_water",         # top up fresh-water dish, params.seconds
    "set_lights",           # params.state: "day" | "night" | "off"
    "record_observation",   # log a behaviour note, params.note
    "alert_human",          # ask a person to come check
}


XAI_BASE_URL = "https://api.x.ai/v1"


class Brain:
    def __init__(self, model: str, system_prompt_path: Path, config: dict):
        self.model = model
        self.config = config
        self.client = OpenAI(
            api_key=os.environ["XAI_API_KEY"],
            base_url=XAI_BASE_URL,
        )
        self.system_prompt = system_prompt_path.read_text(encoding="utf-8")

    def decide(self, readings: dict, frame_b64: str, history: list[dict],
               is_night: bool) -> dict:
        """Ask Grok what to do this tick."""

        user_payload = {
            "readings": readings,
            "targets": self.config["targets"],
            "phase": "night" if is_night else "day",
            "recent_ticks": history,
        }

        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": json.dumps(user_payload, indent=2)},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{frame_b64}"},
                    },
                ],
            },
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content or "{}"
        return self._parse(raw)

    def _parse(self, raw: str) -> dict:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {"action": {"name": "noop", "params": {}}, "reasoning": "parse error"}

        action = data.get("action") or {}
        name = action.get("name", "noop")
        if name not in VALID_ACTIONS:
            name = "noop"

        return {
            "action": {"name": name, "params": action.get("params", {}) or {}},
            "reasoning": (data.get("reasoning") or "").strip()[:240],
        }
