# Daily welfare checklist

The rule above every rule in this project: **a human checks on Biscuits
in person every single day.** This is what to look at.

Print this page. Tick the boxes with a pen. Keep the printed sheet next
to the tank.

## Visual check on Biscuits

* [ ] He is visible somewhere in the tank (a hide counts).
* [ ] No open wounds, scrapes or bleeding.
* [ ] Eyes are clear, not crusted or sunken.
* [ ] No retained shed on toes, tail tip or eyes.
* [ ] Mouth is closed (not held open / gaping for long periods).
* [ ] Tail is fat, not pencil thin.
* [ ] He moves normally when prompted (no limping, no tilting, no
  flipping over).
* [ ] Vent is clean (no smearing, no impaction signs).

## The tank itself

* [ ] Warm side reading matches what a stick thermometer says
  (within 2 °C).
* [ ] Cool side reading matches what a stick thermometer says
  (within 2 °C).
* [ ] Humid hide is damp, not dry, not soaking.
* [ ] Water dish is full and clean.
* [ ] No uneaten dead crickets / mealworms in the tank.
* [ ] No droppings older than a couple of days have been left.
* [ ] No exposed wires inside the tank.
* [ ] Heat lamp guard is in place and the bulb is not touching anything
  flammable.

## What Scout did today

* [ ] The journal at `data/journal.jsonl` has new entries from the last
  few hours.
* [ ] No `safety_override` entries in the last 24 hours (or, if there
  are, the reason is understood).
* [ ] No `alert_human` actions that have been ignored.
* [ ] Mealworm count for the last 24 hours is sensible (0 to 4 for an
  adult, never 6).

## Weekly extras (every Sunday)

* [ ] Weigh Biscuits. Record grams in the weight log.
* [ ] Clean the water dish properly with hot water (no soap).
* [ ] Spot clean the substrate.
* [ ] Check the float switch in the reservoir actually moves.
* [ ] Pull a couple of frames from `data/frames/` at random and look at
  them. Anything that looks wrong, save it.

## If anything is off

Pause Scout (`Ctrl-C` on the Pi or unplug). Take Biscuits' weight. Write
down what you saw. Decide whether this is a vet call. The robot can wait.
The gecko cannot.
