# The experiment

## What we are asking

Can a language model, given a body, keep an animal alive?

Most agent demos run inside text. This one runs inside a tank. There is
a real crested gecko on the other side of the camera. He is called
**Biscuit**.

The goal is not to prove a robot is better at crested gecko husbandry
than a human. The goal is to find out whether a model with clear
targets, working sensors and a small action vocabulary can keep a
habitat stable on its own, and where it breaks first.

## The animal comes first

> A human checks on Biscuit in person every single day. No exceptions.

Scout can ask for help via the `alert_human` action. The human can step
in at any time without asking Scout. If any hard safety limit trips,
Scout pauses, the LCD turns red, and a notification is sent.

Scout is not a substitute for a keeper. Scout is a keeper with one in
the loop.

## A note on baselines

A robot that keeps Biscuit alive proves "a robot can do this", not "the
LLM was necessary". To separate the two we run a baseline week first.

* **Baseline week.** `src/modules/baseline_controller.py` drives the
  tank with rule-based logic: a mist schedule, a CGD refresh schedule,
  a fixed light cycle, no GPT-5.5. Scout still observes, journals and
  raises alerts. The brain is just not consulted.
* **Model week.** GPT-5.5 takes over.

The metrics in `src/modules/metrics.py` are computed for both weeks.
That comparison is the real result.

## Setup

* **Subject.** Biscuit, one healthy crested gecko (*Correlophus
  ciliatus*), from a reputable breeder, settled in his tank for at
  least four weeks before the experiment begins.
* **Habitat.** A planted arboreal vivarium, minimum 45 x 45 x 60 cm
  tall, with branches at multiple heights, dense foliage, a small
  water dish and a small feeding dish.
* **Robot.** Scout, a Raspberry Pi 4 or 5 running this repo, with an
  LCD display, a Pi camera (NoIR) and an IR illuminator.
* **Sensors.** Two DHT22 probes (top and bottom of the arboreal tank)
  and a float switch on the misting reservoir / water dish reservoir.
* **Actuators.** A misting solenoid, a peristaltic pump for CGD slurry,
  a servo-driven insect hopper, a water-dish refill pump, day lights,
  and an IR lamp.
* **Brain.** GPT-5.5 via the OpenAI API, called once per minute with
  the photo, the readings, the day-night phase and the recent journal.

## The five phases

Each one has to pass before the next one starts.

### Phase 1. Software in dry mode

(Status: live.) Everything in the repo runs on a laptop with no
hardware. Sensors return synthetic readings that drift slowly. The
actuator module prints what it would have done. The brain still talks
to the real OpenAI API. The journal still fills up.

Phase 1 passes when: the journal looks coherent across a long run, the
model picks reasonable actions across day and night phases, the safety
layer trips correctly when we inject bad readings on purpose, and there
are no crashes or hangs over a 24 hour soak.

### Phase 2. Hardware on the bench

Parts arrive. We wire one thing at a time, with a small standalone
test script for each: DHT22 read, relay click, servo sweep, camera
capture. The mains side of anything plugged into a wall gets an
enclosure, a properly rated relay, and a fuse. **If a backup heater is
fitted, the dumb mechanical thermostat is installed first.**

Phase 2 passes when every actuator has been driven by Scout once on
the desk, in dry mode swapped to real mode one channel at a time.

### Phase 3. Empty tank rehearsal

Scout drives the full vivarium for 72 hours with no gecko in it. We
deliberately disturb it to see how the robot recovers:

* Open the lid for two minutes (humidity falls).
* Point a small heater at the tank briefly (top probe climbs).
* Cover the misting nozzle (humidity does not rise after mist).
* Empty the water reservoir (float switch trips).
* Cover the camera (the model gets a black frame).

We watch how fast Scout brings each variable back to target, what the
model writes in its reasoning, and whether safety has to step in.

Phase 3 passes when no hard safety limit trips unnecessarily, every
induced fault is named correctly in the journal, and the system
recovers within a sensible time.

### Phase 4. Move-in day

Biscuit moves into the tank. For the first 14 days a human is in the
same room or watching the camera at all times. The journal is reviewed
every evening. Anything unusual is flagged immediately. If Biscuit
shows any sign of distress, the experiment pauses without question.

### Phase 5. The actual experiment

Baseline week first (`baseline_controller.py`), then model week
(GPT-5.5). Scout runs as the primary caretaker during the model week,
with the daily human welfare check still in place. We record the
journal, daily notes, and weekly weight measurements (taken by the
human, not the robot). At the end we publish what we found, good and
bad.

## What we measure

The journal at `data/journal.jsonl` records every tick. From it
`src/modules/metrics.py` computes:

* Percentage of ticks inside the day-band ambient temperature.
* Percentage of ticks inside the night-band humidity (after misting).
* Time to recover after each induced disturbance in Phase 3.
* Number of `alert_human` events per day.
* CGD refresh count per day.
* Insect feeds per week.
* Time-of-day distribution of `mist` actions.
* Weekly weight trend (entered manually by the human keeper).

## Success criteria (decided up front)

We commit to these before the experiment begins, so the goalposts
cannot move afterwards.

* **Pass.** Time in temperature band >= 95 %. Night humidity band
  reached on >= 90 % of nights. Zero unhandled safety overrides.
  Biscuit's weight steady or up over 4 weeks.
* **Partial.** Some metric misses but Biscuit remains visibly healthy
  and human interventions remain rare.
* **Fail.** Repeated safety overrides, Biscuit loses weight, or any
  injury attributable to a Scout decision.

## Safety limits

Bypass the model entirely. Live in `src/safety.py`.

| Limit                              | Value         |
|------------------------------------|---------------|
| Max ambient temperature            | 28 °C         |
| Min ambient temperature            | 16 °C         |
| Max misting seconds per tick       | 30 seconds    |
| Max water pump per tick            | 5 seconds     |
| Max CGD refreshes per 24 hours     | 2             |
| Max insects per 7 days             | 8             |

If the top probe reads above 28 °C, the model is not asked. Scout
alerts the human directly. If the model returns a misting duration
above the cap, the safety layer rewrites it. The model can be wrong.
The animal does not pay for it.

## When the experiment ends

The experiment ends when any of the following happen.

* Biscuit shows signs of stress that do not resolve within 24 hours.
* Scout misjudges in a way that needs human override more than twice
  in a single day.
* We have enough data to write the thing up.
* The keeper, a human ([@HalfSolder](https://github.com/HalfSolder)),
  decides we have learned what we wanted to learn.

Biscuit keeps living his life either way.
