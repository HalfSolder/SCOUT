# Scout

> An experiment: can a robot, on its own, keep a living creature alive and well?

**Scout** is a Raspberry Pi robot that looks after a single leopard gecko —
named **Biscuits**, a name Scout gave him on day one. Scout watches Biscuits
through a camera, reads the environment through a small set of sensors, and
uses **GPT-5.5** as the deciding mind. Every minute, the model is given a
clean picture of the tank and chooses what to do next — turn on the heat,
top up the water, drop a mealworm, dim the lights, or just keep watching.

Nothing is hardcoded as a control loop. The thermostat is the model. The
feeding schedule is the model. Scout has hands; GPT-5.5 has the plan.

The whole thing is logged so we can read it back like a diary.

---

## The experiment

| | |
|---|---|
| **Subject** | One leopard gecko (*Eublepharis macularius*), named **Biscuits** by Scout |
| **Caretaker** | **Scout** — a Raspberry Pi running this repo, with GPT-5.5 as the decision-maker |
| **Question** | Can a language model, given the right tools, keep a living animal in good health without a human in the loop? |
| **Duration** | Open-ended, with daily human welfare checks |
| **Owner** | [@HalfSolder](https://github.com/HalfSolder) |

See [`docs/EXPERIMENT.md`](docs/EXPERIMENT.md) for the protocol and welfare
safeguards. **A human checks on Biscuits every day.** Scout can ask for
help, and there are hard safety overrides that don't go through the model
at all.

---

## How it works

```
       ┌────────────────────┐
       │      Biscuits      │
       │  (leopard gecko)   │
       └─────────┬──────────┘
                 │
   ┌─────────────┼──────────────┐
   │             │              │
camera        sensors        actuators
   │             │              │
   └─────────────┼──────────────┘
                 │
        ┌────────▼─────────┐
        │      Scout       │
        │   (Pi, Python)   │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │     GPT-5.5      │
        │   (the brain)    │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │   LCD display    │
        │  (what it sees,  │
        │ what it's doing) │
        └──────────────────┘
```

Every tick (default: 60 seconds) Scout:

1. **Looks** — takes a photo of the tank with the Pi camera.
2. **Reads** — samples temperature, humidity, water level.
3. **Thinks** — sends the readings, a recent history, and the photo to
   GPT-5.5 along with the care guidelines for a leopard gecko.
4. **Acts** — the model returns a structured action (heat on/off, dispense
   mealworm, refill water, nothing). Scout executes it.
5. **Writes it down** — every observation and decision is appended to
   `data/journal.jsonl`.
6. **Shows it** — the LCD shows the current photo, the chosen action, and
   a short sentence from the model about *why*.

---

## Repo layout

```
SCOUT/
├── src/
│   ├── main.py              # tick loop — observe, think, act, log
│   ├── brain.py             # GPT-5.5 client + tool calls
│   ├── vision.py            # Pi camera capture
│   ├── display.py           # LCD output
│   ├── journal.py           # append-only decision log
│   ├── safety.py            # hard limits that bypass the model
│   ├── sensors/             # DHT22 (temp/humidity), water level
│   └── actuators/           # heat lamp relay, water pump, feeder servo
├── prompts/
│   └── system.md            # Scout's caretaker prompt
├── config.yaml              # care targets, pin numbers, model name
├── docs/
│   ├── EXPERIMENT.md        # protocol, welfare rules, daily checks
│   └── HARDWARE.md          # wiring, parts list, BOM
├── data/                    # journal + captured frames (gitignored)
└── assets/                  # diagrams, photos for the README
```

---

## Setup

> Scout runs on a Raspberry Pi 4 / 5 with Raspberry Pi OS. Development from
> a Windows machine works fine — only the final `main.py` needs the Pi.

```bash
git clone https://github.com/HalfSolder/SCOUT.git
cd SCOUT
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# add your OPENAI_API_KEY to .env
```

To run the loop:

```bash
python -m src.main
```

In **dry-run mode** (no real hardware), the sensors return fake readings and
the actuators just log what they would have done. That's the default off the
Pi. On the Pi, set `HARDWARE=real` in `.env`.

---

## Safety

Even though GPT-5.5 is the brain, the model is **not allowed to cook
Biscuits**. `src/safety.py` enforces hard limits that run *before* the
model's action is executed:

- Heat lamp is force-cut if warm side > 35 °C.
- Water pump max run time per tick is capped.
- Feeder cannot dispense more than N mealworms per 24 hours.
- All actions are gated on the daily human check-in being recent.

If any hard limit trips, Scout pauses, lights up the LCD red, and
[sends a notification](docs/EXPERIMENT.md#human-in-the-loop) to a human.

---

## Status

Early build. Hardware on order. The software runs end-to-end in dry-run
against fake sensors, so the brain and the journal are exercisable from a
laptop while the parts arrive.

---

*Built by [@HalfSolder](https://github.com/HalfSolder). Private repo —
shared with collaborators to document the experiment.*
