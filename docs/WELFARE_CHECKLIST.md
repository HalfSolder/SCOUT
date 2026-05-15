# Daily welfare checklist

The rule above every rule in this project: **a human checks on Biscuit
in person every single day.** This is what to look at.

Print this page. Tick the boxes with a pen. Keep the printed sheet next
to the tank.

## Visual check on Biscuit

* [ ] He is visible somewhere in the tank.
* [ ] No open wounds, scrapes or bleeding.
* [ ] Eyes are clear, not crusted or sunken.
* [ ] No retained shed on toes, tail tip or eyes.
* [ ] Mouth is closed (not panting, not held open).
* [ ] **Tail is plump at the base and intact.** A thinner tail than
  yesterday is a red flag. A dropped tail is an immediate alert.
* [ ] Toes are all present and gripping.
* [ ] He moves normally when prompted (no limping, no twisting).
* [ ] Vent is clean.
* [ ] No rubbery legs or jaw weakness (signs of MBD).

## The tank itself

* [ ] Top temperature reading matches a stick thermometer (within 2 °C).
  **Anything above 27 °C, act now.**
* [ ] Bottom temperature reading sensible.
* [ ] Daytime humidity is in the 50 to 70 % band.
* [ ] Last night's mist actually fired (look at the journal).
* [ ] CGD dish has fresh food (replaced in the last 36 hours).
* [ ] Water dish is full and clean.
* [ ] No dead insects in the tank from a previous feeding.
* [ ] Foliage looks healthy (no rot, no mould).
* [ ] No standing water on the floor for over a day.
* [ ] No exposed wires inside the tank.

## What Scout did today

* [ ] The journal at `data/journal.jsonl` has new entries from the last
  few hours.
* [ ] No `safety_override` entries in the last 24 hours (or, if there
  are, the reason is understood).
* [ ] No `alert_human` actions that have been ignored.
* [ ] CGD refresh count for the day is 1 or 2.
* [ ] Insect count for the week is at most 2 or 3.
* [ ] Misting fired in the evening last night (or last evening, if
  this is morning).

## Weekly extras (every Sunday)

* [ ] Weigh Biscuit. Record grams in `data/weights.csv` via the weight
  log CLI.
* [ ] Clean the water dish properly with hot water (no soap).
* [ ] Wipe condensation off the front glass.
* [ ] Spot clean any visible droppings.
* [ ] Check the float switch in the reservoir actually moves.
* [ ] Pull a couple of frames from `data/frames/` at random and look at
  them. Anything that looks wrong, save it.
* [ ] Top up the misting reservoir from a known-clean source.

## If anything is off

Pause Scout (`Ctrl-C` on the Pi or unplug). Take a photo. If it is heat,
move Biscuit to a cooler room. If it is shed, raise humidity for a day.
If it is the tail, weight loss or anything you cannot name, see
`docs/EMERGENCY.md` and consider a reptile vet. The robot can wait.
Biscuit cannot.
