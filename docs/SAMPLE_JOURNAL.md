# What the journal reads like

This is what `data/journal.jsonl` is supposed to read like once Scout
is running. The lines below are illustrative, not real. They give a
sense of the diary the experiment is building.

Each line is one tick. Times are simulated.

```
2026-05-15 19:58:14   top 24.1   bot 22.7   hum 58   water ok   phase day
  scout: noop. "End of day band, humidity dropping toward dusk."

2026-05-15 20:00:14   top 24.0   bot 22.6   hum 56   water ok   phase night
  scout: set_lights {state: "night"}. "Day cycle ends, lights to IR."

2026-05-15 20:01:14   top 23.9   bot 22.5   hum 56   water ok   phase night
  scout: mist {seconds: 20}. "Evening mist to start the night cycle."

2026-05-15 20:01:34   top 23.7   bot 22.5   hum 88   water ok   phase night
  scout: noop. "Humidity at 88 %, in band for night, hold."

2026-05-15 21:14:14   top 23.4   bot 22.3   hum 81   water ok   phase night
  scout: record_observation {note: "Biscuit on the high branch, looks
  alert"}. "Active period beginning."

2026-05-15 21:30:14   top 23.4   bot 22.4   hum 80   water ok   phase night
  scout: offer_insect. "Wednesday evening, last insect feed was Sunday."

2026-05-15 21:31:14   top 23.4   bot 22.4   hum 80   water ok   phase night
  scout: noop. "He ate the cricket. Watch."

2026-05-16 04:02:14   top 23.0   bot 21.9   hum 71   water ok   phase night
  scout: mist {seconds: 10}. "Pre-dawn top-up to hold humidity."

2026-05-16 08:00:14   top 23.2   bot 22.1   hum 68   water ok   phase day
  scout: set_lights {state: "day"}. "Day cycle begins."

2026-05-16 09:05:14   top 23.6   bot 22.4   hum 62   water ok   phase day
  scout: refresh_cgd. "Last CGD batch is 28 hours old, replace it."

2026-05-16 14:47:14   top 25.1   bot 23.8   hum 54   water ok   phase day
  scout: noop. "Warmer day, still well inside band, no action."

2026-05-16 16:11:14   top 27.2   bot 25.5   hum 49   water ok   phase day
  scout: alert_human {reason: "top 27.2 C and climbing, room may be
  hot today"}. "Approaching safety limit, want a person to check."

2026-05-16 16:18:14   top 28.4   bot 26.0   hum 48   water ok   phase day
  scout: SAFETY OVERRIDE -> alert_human. "ambient 28.4C > max 28C"

2026-05-16 16:33:14   top 26.7   bot 25.1   hum 50   water ok   phase day
  scout: noop. "Keeper opened a window, cooling normally."
```

## What good looks like

* Long runs of `noop`. Boredom is correct.
* The humidity cycle is visible: drops through the day, spikes after
  the evening mist, drifts back overnight.
* Lights flip exactly once at day start and once at night start.
* CGD refresh is one or two times per day, never more.
* Insect feeds are concentrated in the evening, never more than 1 to
  2 per week.
* The mist actions cluster in the evening with a small top-up before
  dawn. Not scattered through the day.
* Safety overrides are rare and always preceded by an `alert_human`
  that Scout raised on its own.
* When the keeper does the daily check, the journal explains itself.
