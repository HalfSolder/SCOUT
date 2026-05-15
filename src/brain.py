"""GPT-5.5 brain.

Each tick the brain receives:
  - The current sensor readings.
  - A photo of the habitat (base64).
  - A short history of recent ticks (so it knows what it just did).

It must return a structured decision: an action and a one-line reasoning.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI


VALID_ACTIONS = {
    "noop",            # do nothing, keep watching
    "heat_on",         # enable heat lamp
    "heat_off",        # disable heat lamp
    "dispense_food",   # drop one mealworm
    "refill_water",    # run water pump (seconds in params)
    "alert_human",     # ask a person to check
}


class Brain:
    def __init__(self, model: str, system_prompt_path: Path, config: dict):
        self.model = model
        self.config = config
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.system_prompt = system_prompt_path.read_text(encoding="utf-8")

    def decide(self, readings: dict, frame_b64: str, history: list[dict]) -> dict:
        """Ask GPT-5.5 what to do this tick."""

        user_payload = {
            "readings": readings,
            "targets": self.config["targets"],
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
