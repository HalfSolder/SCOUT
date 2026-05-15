# What the journal reads like

This is what `data/journal.jsonl` is supposed to read like once Scout is
running. The lines below are illustrative, not real. They give a sense
of the diary the experiment is building.

Each line is one tick. Times are simulated.

```
2026-05-15 18:00:14   warm 30.4   cool 22.7   hum 36   water ok
  scout: noop. "Biscuits is hidden, all readings in band, nothing to do."

2026-05-15 18:01:14   warm 30.2   cool 22.6   hum 36   water ok
  scout: noop. "Holding steady. Light fading, no action needed."

2026-05-15 18:14:14   warm 29.8   cool 22.5   hum 35   water ok
  scout: heat_on. "Warm side drifted to 29.8 C, just below the band."

2026-05-15 18:18:14   warm 31.1   cool 22.6   hum 35   water ok
  scout: heat_off. "Back inside the band, let it coast."

2026-05-15 19:02:14   warm 30.9   cool 22.4   hum 33   water ok
  scout: dispense_food. "Evening feeding time, Biscuits is out of his
  hide, one mealworm is enough."

2026-05-15 19:03:14   warm 30.9   cool 22.5   hum 33   water ok
  scout: noop. "He found the mealworm. Watch him eat."

2026-05-16 02:14:14   warm 30.6   cool 22.0   hum 32   water LOW
  scout: refill_water. "Float switch tripped, top up for 3 seconds."

2026-05-16 02:14:18   warm 30.6   cool 22.0   hum 34   water ok
  scout: noop. "Reservoir back to ok."

2026-05-16 11:47:14   warm 35.4   cool 23.1   hum 30   water ok
  scout: SAFETY OVERRIDE -> heat_off. "warm side 35.4 C > max 35 C"
  scout: alert_human. "Hot spell, want a person to check the room
  thermostat is sane."

2026-05-16 12:08:14   warm 32.3   cool 22.9   hum 31   water ok
  scout: noop. "Cooling normally. Keeper acknowledged the alert."
```

## What good looks like

* Long runs of `noop`. Boredom is correct.
* Heat decisions come in pairs (on then off) a few minutes apart, not
  flapping every tick.
* Feeding is concentrated in the evening, not scattered through the
  day, never more than the daily cap.
* Water refills are short, triggered by a real float-switch event, not
  speculative top ups.
* Safety overrides are rare. When they happen, an `alert_human` follows
  in the same tick or the next one.
* When the keeper does the daily check, the journal explains itself.
