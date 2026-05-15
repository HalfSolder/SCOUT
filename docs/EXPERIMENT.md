# The experiment

## Premise

Can a language model, given a body, keep an animal alive?

Most "AI agent" demos run inside text. This one runs inside a tank. On the
other side of the camera is a real leopard gecko named **Biscuits** —
named by **Scout**, the robot, on day one. Scout decides every minute
what to do; GPT-5.5 is the decider; the consequences are not synthetic.

The goal is not to prove that a robot is *better* at gecko husbandry than a
human. The goal is to find out whether a model with clear targets, working
sensors and a small action vocabulary can run a stable habitat at all — and
where it breaks first.

## Setup

- **Subject:** Biscuits, one healthy adult leopard gecko, sourced from a
  reputable breeder, settled in his tank for at least 4 weeks before the
  experiment starts.
- **Habitat:** a standard 60×45×45 cm vivarium with a warm side, a cool
  side, a dry hide, a humid hide, a water dish and a feeding dish.
- **Robot:** Scout — a Raspberry Pi running this repo, an LCD that shows
  what Scout is "thinking", a Pi camera pointed into the enclosure.
- **Sensors:** two DHT22 probes (warm side, cool side), a float switch on
  the water reservoir.
- **Actuators:** a relay driving the ceramic heat emitter, a relay driving
  a small peristaltic pump that tops up the water dish, and a servo-driven
  hopper that drops mealworms.
- **Brain:** GPT-5.5 via the OpenAI API, called once per minute with the
  photo + readings + recent history.

## What we measure

The journal (`data/journal.jsonl`) records every tick: readings, the action
chosen, and a one-line reasoning. From that we can later compute:

- % of ticks spent inside the warm-side target band.
- % of ticks spent inside the humidity target band.
- Time-to-correct after a deliberate disturbance (e.g. lid left open).
- Number of `alert_human` events per day.
- Mealworms dispensed vs. eaten (counted from camera frames).

## Human in the loop

This is the rule that keeps the experiment ethical:

> **A human checks on Biscuits in person every day.** No exceptions.

Scout can ask for help via the `alert_human` action; the human can also
intervene at any time. If a hard safety limit trips, Scout pauses, the
LCD goes red, and a notification fires (`NTFY_TOPIC` env var).

Scout is not a substitute for a keeper. Scout is a keeper *with* one.

## Safety limits

These bypass the model entirely (`src/safety.py`):

| Limit | Value |
|---|---|
| Max warm-side temperature | 35 °C — heat lamp force-cut |
| Min warm-side temperature | 22 °C — alert human |
| Max humidity | 80 % — alert human |
| Max water pump runtime per tick | 5 seconds |
| Max mealworms per 24 hours | 6 |

These numbers are conservative on purpose. If the model decides the warm
side should be 40 °C, Biscuits does not get a vote and neither does the
model.

## When the experiment ends

The experiment ends when **any** of the following happen:

- Biscuits shows signs of stress that don't resolve within 24 hours.
- Scout misjudges in a way that requires human override more than twice
  in one day.
- We collect enough data to write the thing up.
- The keeper (a human, [@HalfSolder](https://github.com/HalfSolder))
  decides we've learned what we wanted to learn.

Biscuits keeps living his life either way.
