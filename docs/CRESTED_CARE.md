# Crested gecko, in one page

A reference sheet, not a full husbandry guide. Read a real keeper guide
before bringing Biscuit home. This page exists so anyone reading the
repo understands why the targets in `config.yaml` are what they are.

## Who he is

* **Species:** *Correlophus ciliatus* (crested gecko, "crestie").
* **Origin:** New Caledonia, an island system south west of the Pacific.
* **Climate of origin:** Temperate rainforest. Cool nights, mild days,
  high humidity. **Not** desert.
* **Habit:** Arboreal (climbs), nocturnal (active at night), insectivore
  with a strong fruit habit.
* **Lifespan:** 15 to 20 years in captivity.

## Temperature

| Phase | Target |
|-------|--------|
| Day   | 22 to 26 °C |
| Night | 18 to 22 °C |

* Cresties **do not bask**. There is no warm side and no heat lamp.
* Above 28 °C is dangerous. Above 30 °C kills them, sometimes within
  hours.
* If a normal indoor room is in the 19 to 24 °C range, no supplemental
  heat is needed at all.
* In a cold room (under 16 °C), a low-watt ceramic heater on a
  thermostat is acceptable. Scout does not control the heater. A
  separate dumb thermostat does.

## Humidity

Cresties need a **cycle**, not a constant value.

| Phase | Target |
|-------|--------|
| Day   | 50 to 70 % |
| Night (after misting) | 80 to 100 % |

* Heavy misting after dusk to spike humidity.
* Light misting before dawn to top up.
* Tank dries down through the day.
* Constant 80 %+ rots foliage and invites bacterial / fungal infections.

## Food

* **Primary:** CGD (crested gecko diet). Mix the powder 2 parts water,
  1 part powder, by weight. Stir. Offer in a small flat dish.
* **Freshness:** Replace every 24 to 36 hours. CGD goes off, smells
  yeasty when it does.
* **Supplemental:** Dusted insects 1 to 2 times per week, in the
  evening, when Biscuit is active. Crickets or dubia roaches, sized
  smaller than the gap between his eyes.
* **Calcium plus D3:** Every other insect feed. Plain calcium on the
  rest.
* **Water:** Fresh bowl daily. He drinks droplets off leaves more than
  from the bowl.

## Light

* 12 hours day, 12 hours night.
* Low-output T5 UVB is **beneficial but not strictly required** if the
  diet is complete and dusted correctly.
* Bright direct light stresses him. Plant grow lights through dense
  foliage is the right intensity.
* IR illuminator only ever lights up at night, for the camera.

## Tank

* **Size:** Minimum 45 x 45 x 60 cm tall for an adult. Bigger is better.
  Cresties use vertical space.
* **Decor:** Branches at multiple heights, dense foliage (live or fake),
  cork bark, leaf litter, a vine or two near the top.
* **Substrate:** Bioactive (drainage layer, soil mix, leaf litter,
  isopods, springtails) is ideal. Paper towel is fine for juveniles or
  if you are quarantining.

## Behaviour

* Hides during the day, often slept high up against the glass or
  flattened on a leaf. Out and about after dark.
* Drops his tail when stressed or grabbed. **Tails do not grow back.**
  Treat him gently, no grabbing the tail, no fast movements.
* Curious but easily startled. Misting normally wakes him up.
* Healthy cresties have a plump tail base, clear eyes, all toes intact
  and a strong grip.

## Things that go wrong

* **MBD (metabolic bone disease).** Comes from low calcium or low D3.
  Looks like rubbery legs, kinks in the spine, jaw weakness. Prevent it
  with proper dusting.
* **Floppy tail syndrome (FTS).** From hanging head-down on glass for
  long periods. Prevent it with plenty of climbing surfaces and
  horizontal perches up high.
* **Impaction.** From eating substrate, often loose substrate offered
  too young. Bioactive avoids this.
* **Dehydration.** From too little misting. Sunken eyes, sticky shed.
* **Heat stress.** Open-mouth breathing, panting. Cool the room
  immediately.
* **Retained shed.** Toes, tail tip, around eyes. Bump humidity for a
  day.

## What Scout pays attention to

* Top probe higher than 27 °C ever.
* Daytime humidity stuck under 45 %.
* Night humidity that never spikes above 75 %.
* Tail visibly thinner than the previous reference frame.
* Biscuit on the ground in the open during the day.
* CGD not refreshed in over 36 hours.

These map to the prompts in `prompts/system.md` and the safety limits
in `src/safety.py`. Change them in those files, not here.
