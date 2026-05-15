# Scout

> Can a robot, on its own, look after a living creature?

This repo is the brain and body of **Scout**, a small Raspberry Pi robot
that takes care of one leopard gecko. The gecko is real. His name is
**Biscuits**. Scout chose the name on day one.

Scout watches Biscuits through a camera, reads the air with a couple of
sensors, and asks **GPT-5.5** what to do every minute. The model decides.
Scout executes. Biscuits lives his life. We write everything down.

## The story

I wanted to know if a language model could keep something alive.

Most AI demos run inside a text box. The agent picks a winning move, books
a flight, writes a function. Nothing in the world actually changes. If the
model is wrong, you close the tab. There is no animal on the other side.

So we built one with an animal on the other side.

Scout is a Raspberry Pi with a camera and three or four cheap parts: a
temperature probe, a humidity probe, a relay for the heat lamp, a tiny
servo that drops a single mealworm into a dish. The brain is GPT-5.5,
which we call once a minute. We hand it a photo of the tank, the current
readings, and a short log of what Scout just did. The model writes back
one of six actions. Scout runs the action. A second later, the journal has
a new line.

The first time Scout came online, before any hardware was wired up, the
prompt asked it to name the gecko. It chose **Biscuits**. So that is what
the gecko is called now.

This is not a chatbot pretending to care. The thermostat is the model. The
feeding schedule is the model. The watcher is the model. Scout has hands;
GPT-5.5 has the plan. If the plan is wrong, real heat goes into a real
tank with a real animal in it. That is the whole point. We want to know
where it breaks.

A human checks on Biscuits in person every single day. The robot can ask
for help. Hard safety limits (max temperature, max feed per day, max water
pump runtime) are enforced in code and never reach the model. The
experiment is meant to test the model, not to risk the gecko.

## The plan

The build runs in five phases. Each one has to work before the next one
starts.

**Phase 1. Software in dry mode.** (Status: live.) Everything in this repo
runs on a laptop with no hardware attached. The sensors return synthetic
readings that drift over time, the actuators just print what they would
have done, and the brain still gets called for real. This lets us tune
the system prompt and watch the journal fill up before any wires touch a
gecko.

**Phase 2. Hardware on the bench.** Parts arrive. We wire up each piece in
isolation: the DHT22 probes on their own, then the relays on their own,
then the servo, then the camera. Each one gets a small test script. The
relays get a mains fuse and an enclosure. Nothing goes near the vivarium
until every part has been driven by Scout once on the desk.

**Phase 3. Empty tank rehearsal.** Scout runs against the actual vivarium,
fully wired, for seventy two hours straight, with no gecko in it. We
deliberately mess with it: open the lid, hit the heat lamp with cold air,
empty the water reservoir. We watch how fast Scout corrects, what the
model says about it in the journal, and whether the safety layer ever has
to step in.

**Phase 4. Move-in day.** Biscuits moves into the tank. For the first
fourteen days Scout runs under close supervision. A human is in the same
room or on a live camera feed at all times. The journal is reviewed every
evening. Anything weird gets flagged.

**Phase 5. The actual experiment.** Scout runs as the primary caretaker.
A human still checks in person every day. We record everything for as
long as the experiment runs. At the end we publish what we found, good
and bad.

## How Scout works

Every minute, Scout runs the same loop.

```
 ┌────────────────────┐
 │      Biscuits      │
 │  (leopard gecko)   │
 └──────────┬─────────┘
            │
   look, read, think, act
            │
 ┌──────────▼─────────┐
 │       Scout        │
 │   (Pi, Python)     │
 └──────────┬─────────┘
            │
            │  photo + readings + history
            │
 ┌──────────▼─────────┐
 │      GPT-5.5       │
 │    (the brain)     │
 └──────────┬─────────┘
            │
            │  one structured action
            │
 ┌──────────▼─────────┐
 │  actuators + log   │
 │  + LCD display     │
 └────────────────────┘
```

The action vocabulary is deliberately tiny:

* `noop`. Do nothing. Used most of the time.
* `heat_on` / `heat_off`. Toggle the warm side heat lamp.
* `refill_water`. Run the pump for a few seconds, capped by safety.
* `dispense_food`. Drop one mealworm, capped to a daily limit.
* `alert_human`. Ask a person to come look.

That is the entire interface between the model and the world. There is
nothing else it can do.

## Care for Biscuits

The system prompt tells the model what a leopard gecko is and what it
needs. Targets are configured in `config.yaml`, not hardcoded:

| Setting          | Target band |
|------------------|-------------|
| Warm side        | 30 to 33 °C |
| Cool side        | 21 to 24 °C |
| Ambient humidity | 30 to 40 %  |
| Humid hide       | 60 to 80 %  |

Leopard geckos are crepuscular, so Biscuits should be hiding during the
day and active around dawn and dusk. The model is told this. If Biscuits
is out in the open under bright light at noon, that is a warning sign,
not a happy gecko.

## Safety

Even with GPT-5.5 driving, there are limits the model is not allowed to
break. These live in `src/safety.py` and run *before* and *after* the
model on every tick.

| Hard limit                       | Value      |
|----------------------------------|------------|
| Max warm side temperature        | 35 °C      |
| Min warm side temperature        | 22 °C      |
| Max humidity                     | 80 %       |
| Max water pump run, per tick     | 5 seconds  |
| Max mealworms in any 24 hours    | 6          |

If the warm side crosses 35 °C, the heat lamp is forced off and the model
is not even called for that tick. If the model returns `refill_water` for
30 seconds, the safety layer rewrites it to 5. The model can want what it
wants. It cannot cook the gecko.

## Repo layout

```
SCOUT/
├── src/
│   ├── main.py              tick loop: look, read, think, act, log
│   ├── brain.py             GPT-5.5 client and JSON action parser
│   ├── vision.py            Pi camera capture (real and dry)
│   ├── display.py           LCD output
│   ├── journal.py           append-only diary in JSON lines
│   ├── safety.py            hard limits that bypass the model
│   ├── sensors/             DHT22 plus water level switch
│   └── actuators/           heat lamp, water pump, mealworm feeder
├── prompts/system.md        Scout's caretaker prompt
├── config.yaml              care targets, GPIO pins, model name
├── tests/
│   └── test_safety.py       proves the safety layer behaves
├── scripts/
│   ├── simulate_day.py      fast-forward dry mode, no API calls
│   └── bringup/             Phase 2 hardware test scripts
├── docs/
│   ├── EXPERIMENT.md        protocol, welfare rules, five phases
│   ├── HARDWARE.md          wiring, parts list, BOM, build order
│   ├── WELFARE_CHECKLIST.md printable daily human check
│   └── SAMPLE_JOURNAL.md    what the diary is supposed to read like
├── data/                    journal and captured frames (gitignored)
└── assets/                  diagrams, photos for the README
```

## Setup

Scout runs on a Raspberry Pi 4 or 5 with Raspberry Pi OS. The software
also runs from a Windows or Mac laptop in dry mode, which is how Phase 1
is being developed.

```bash
git clone https://github.com/HalfSolder/SCOUT.git
cd SCOUT
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# put your OPENAI_API_KEY in .env, leave HARDWARE=dry for now
```

Then start the loop:

```bash
python -m src.main
```

You should see Scout boot, take a synthetic photo, sample fake sensor
values, ask the model for a decision, and append the first line to
`data/journal.jsonl`. After a few minutes the journal reads like a small
diary of what Scout chose and why.

On the Pi, switch `HARDWARE=dry` to `HARDWARE=real` in `.env` to drive
GPIO. Do not do this until Phase 2 is complete.

## Tests

The safety layer is the only code whose job is to be wrong about the
model. There are unit tests for it.

```bash
pytest -q
```

## The simulator

The simulator runs Scout in dry mode at full speed, without calling the
OpenAI API. It uses a deterministic stub brain that picks reasonable
actions, so the dry-mode pipeline (sensors, safety, journal) can be
exercised free of charge.

```bash
python scripts/simulate_day.py --ticks 1440      # one simulated day
```

It writes to `data/simulated_journal.jsonl` and prints an action
breakdown at the end.

## Bring-up scripts (Phase 2)

Each piece of hardware gets its own small test script in
`scripts/bringup/`. Run them on the Pi, one at a time, before letting
Scout drive anything.

```bash
python scripts/bringup/test_dht22.py 4       # warm side probe
python scripts/bringup/test_relay.py 18      # heat lamp relay
python scripts/bringup/test_servo.py 23      # mealworm feeder
python scripts/bringup/test_camera.py        # capture one frame
```

See [`docs/HARDWARE.md`](docs/HARDWARE.md) for the build order.

## Status

Phase 1 is live. The code in this repo runs end to end against fake
sensors and a placeholder camera frame. The journal fills up. The brain
behaves itself. Tests are green. The hardware is on order.

Phase 2 starts when the parts arrive.

## Credits

Private repo, owned by [@HalfSolder](https://github.com/HalfSolder).
Shared with collaborators who are following the experiment.

Follow along on X: [**@halfsoldered**](https://x.com/halfsoldered).
