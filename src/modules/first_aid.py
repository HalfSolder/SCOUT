"""Crested gecko first aid quick reference.

This is for the keeper. The model does not call this. Print it.
"""

from __future__ import annotations


FIRST_AID = {
    "heat_stress": (
        "Open-mouth breathing or panting, lying flat in the open, "
        "unresponsive. Top probe above 28 C.\n"
        " - Move the tank to a cooler room (16-20 C).\n"
        " - Mist lightly.\n"
        " - No ice. No fan blowing directly on him.\n"
        " - If not recovered within 30 minutes, vet."
    ),
    "dropped_tail": (
        " - Move to a small hospital tub with paper towel.\n"
        " - Humidity 80 % plus for a day.\n"
        " - Wound seals within ~24 h.\n"
        " - Watch for swelling or discharge.\n"
        " - Tail will not grow back. He is fine."
    ),
    "stuck_shed": (
        "Especially toes, tail tip, around eyes.\n"
        " - Bump night humidity to 90 % plus for a day.\n"
        " - Damp paper-towel hide on the floor.\n"
        " - Do not pull shed off with fingers.\n"
        " - Damp cotton bud after 48 h, gentle.\n"
        " - Retained shed on toes for >72 h: vet."
    ),
    "not_eating": (
        "Adults can fast a week or so. Investigate when it goes past 7 days.\n"
        " - Check temperature: cold cresties stop eating.\n"
        " - Check humidity: dehydrated cresties stop eating.\n"
        " - Offer fresh CGD, different flavour.\n"
        " - One small dusted insect in the evening.\n"
        " - Weigh. Down >5 % of body weight is vet territory."
    ),
    "injury_or_blood": (
        " - Photograph the injury.\n"
        " - Do not improvise treatment.\n"
        " - Vet."
    ),
    "MBD_signs": (
        "Metabolic Bone Disease. Rubbery legs, jaw weakness, kinks in the spine.\n"
        " - Cause is low calcium / D3 in the long term.\n"
        " - Improve dusting schedule immediately.\n"
        " - Vet for confirmation and supportive care."
    ),
}


def show(topic: str | None = None) -> None:
    if topic is None:
        for k in FIRST_AID:
            print(f"  {k}")
        return
    body = FIRST_AID.get(topic)
    if body is None:
        print(f"unknown topic: {topic!r}. known topics:")
        for k in FIRST_AID:
            print(f"  {k}")
        return
    print(f"=== {topic} ===")
    print(body)


if __name__ == "__main__":
    import sys
    show(sys.argv[1] if len(sys.argv) > 1 else None)
