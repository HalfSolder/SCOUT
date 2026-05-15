# The experiment

## What we are asking

Can a language model, given a body, keep an animal alive?

Most agent demos run inside text. This one runs inside a tank. There is a
real leopard gecko on the other side of the camera. He is called
**Biscuits**, a name **Scout**, the robot, chose itself on day one.

The goal is not to prove a robot is better at gecko husbandry than a
human. The goal is to find out whether a model with clear targets,
working sensors and a small action vocabulary can keep a habitat stable
on its own, and where it breaks first.

## The animal comes first

This rule sits above every other rule in this document.

> A human checks on Biscuits in person every single day. No exceptions.

Scout can ask for help via the `alert_human` action. The human can step
in at any time without asking Scout. If any hard safety limit trips,
Scout pauses, the LCD turns red, and a notification is sent.

Scout is not a substitute for a keeper. Scout is a keeper with one in the
loop.

## Setup

* **Subject.** Biscuits, one healthy adult leopard gecko (*Eublepharis
  macularius*), from a reputable breeder, settled in his tank for at
  least four weeks before the experiment begins.
* **Habitat.** A 60 x 45 x 45 cm vivarium with a warm side, a cool side,
  a dry hide, a humid hide, a water dish and a feeding dish.
* **Robot.** Scout, a Raspberry Pi 4 or 5 running this repo, with an LCD
  display and a Pi camera pointed into the enclosure.
* **Sensors.** Two DHT22 probes (warm side, cool side) and a float switch
  on the water reservoir.
* **Actuators.** One relay driving the ceramic heat emitter, one relay
  driving a small peristaltic pump that tops up the water dish, and a
  servo driven hopper that drops mealworms into the feeding dish.
* **Brain.** GPT-5.5 via the OpenAI API, called once per minute with the
  photo, the readings and the recent journal.

## The five phases

The build runs in five phases. Each one has to pass before the next one
starts.

### Phase 1. Software in dry mode

(Status: live.) Everything in the repo runs on a laptop with no hardware.
The sensor module returns synthetic readings that drift slowly so the
model has something to react to. The actuator module just prints what it
would have done. The brain still talks to the real OpenAI API. The
journal still fills up.

Phase 1 passes when: the journal looks coherent across a long run, the
model picks reasonable actions, the safety layer trips correctly when we
inject bad readings on purpose, and there are no crashes or hangs over a
24 hour soak.

### Phase 2. Hardware on the bench

Parts arrive. We wire one thing at a time, with a small standalone test
script for each: DHT22 read, relay click, servo sweep, camera capture.
The mains side of the heat lamp gets an enclosure, a properly rated
relay, and a fuse.

Phase 2 passes when every actuator has been driven by Scout once on the
desk, in dry mode swapped to real mode one channel at a time.

### Phase 3. Empty tank rehearsal

Scout drives the full vivarium for 72 hours with no gecko in it. We
deliberately disturb the system to see how the robot recovers:

* Open the lid for two minutes (humidity falls).
* Cold soda can on top of the warm side hide (warm side drops).
* Empty the water reservoir (float switch trips).
* Cover the camera (the model gets a black frame).

We watch how fast Scout brings each variable back to target, what the
model writes in its reasoning, and whether safety has to step in.

Phase 3 passes when no hard safety limit trips unnecessarily, and the
system recovers from every induced fault within a sensible time.

### Phase 4. Move-in day

Biscuits moves into the tank. For the first 14 days a human is in the
same room or watching the camera at all times. The journal is reviewed
every evening. Anything unusual is flagged immediately. If Biscuits
shows any sign of distress, the experiment pauses without question.

### Phase 5. The actual experiment

Scout runs as the primary caretaker, with the daily human welfare check
still in place. We record the journal, daily notes, and weekly weight
measurements (taken by the human, not the robot). At the end we publish
what we found, good and bad.

## What we measure

The journal at `data/journal.jsonl` records every tick. From it we can
later compute:

* Percentage of ticks spent inside the warm side target band.
* Percentage of ticks spent inside the humidity target band.
* Time to recover after each induced disturbance in Phase 3.
* Number of `alert_human` events per day.
* Mealworms dispensed versus eaten (counted from camera frames).
* Weekly weight trend (entered manually by the human keeper).

## Safety limits

These bypass the model entirely. They live in `src/safety.py`.

| Limit                          | Value      |
|--------------------------------|------------|
| Max warm side temperature      | 35 °C      |
| Min warm side temperature      | 22 °C      |
| Max ambient humidity           | 80 %       |
| Max water pump run per tick    | 5 seconds  |
| Max mealworms per 24 hours     | 6          |

If the warm side reads above 35 °C, the heat lamp is forced off for that
tick and the model is not asked. If the model returns `refill_water` with
a larger duration than allowed, the safety layer rewrites it. The model
can be wrong. The animal does not pay for it.

## When the experiment ends

The experiment ends when any of the following happen.

* Biscuits shows signs of stress that do not resolve within 24 hours.
* Scout misjudges in a way that needs human override more than twice in
  a single day.
* We have enough data to write the thing up.
* The keeper, a human ([@HalfSolder](https://github.com/HalfSolder)),
  decides we have learned what we wanted to learn.

Biscuits keeps living his life either way.
