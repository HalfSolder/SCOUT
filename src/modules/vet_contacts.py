"""Vet directory.

Reads `data/vets.json`. If the file does not exist, a template is
written so the keeper can fill it in. There is no reason to wait until
3 am to look up an exotics vet.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


VETS_FILE = Path("data/vets.json")


TEMPLATE = {
    "primary_exotics_vet": {
        "name": "<fill in>",
        "phone": "<fill in>",
        "address": "<fill in>",
        "hours": "Mon-Fri 09:00-17:00",
        "notes": "Email an exotic-experienced vet before opening hours."
    },
    "out_of_hours_vet": {
        "name": "<fill in>",
        "phone": "<fill in>",
        "address": "<fill in>",
        "hours": "24/7",
        "notes": "Call ahead before driving."
    },
    "reptile_rescue": {
        "name": "Pet Reptile Rescue (example)",
        "phone": "<fill in>",
        "url": "https://prc.org.uk",
        "notes": "Advice only, not emergency care."
    },
}


@dataclass
class Vet:
    key: str
    name: str
    phone: str
    address: str = ""
    hours: str = ""
    url: str = ""
    notes: str = ""


def load() -> list[Vet]:
    if not VETS_FILE.exists():
        write_template()
        return load()
    data = json.loads(VETS_FILE.read_text(encoding="utf-8"))
    return [Vet(key=k, **v) for k, v in data.items()]


def write_template() -> None:
    VETS_FILE.parent.mkdir(parents=True, exist_ok=True)
    VETS_FILE.write_text(json.dumps(TEMPLATE, indent=2) + "\n", encoding="utf-8")


def print_directory() -> None:
    for vet in load():
        print(f"=== {vet.key} ===")
        print(f"  name:    {vet.name}")
        print(f"  phone:   {vet.phone}")
        if vet.address:
            print(f"  address: {vet.address}")
        if vet.hours:
            print(f"  hours:   {vet.hours}")
        if vet.url:
            print(f"  url:     {vet.url}")
        if vet.notes:
            print(f"  notes:   {vet.notes}")
        print()


if __name__ == "__main__":
    print_directory()
