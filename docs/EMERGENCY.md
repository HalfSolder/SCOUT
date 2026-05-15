# Emergency

If you are reading this in a panic, slow down. Read the first section.
Then look at the section that matches what is happening.

## First, stabilise

1. **Get Biscuit out of the heat.** If the top probe reads above 28 °C
   or he is panting / open mouth breathing, move him to a cooler room.
   Carry the tank, do not lift Biscuit.
2. **Unplug Scout if you need to.** Pulling power on the Pi is fine.
   The dumb thermostat on the heater (if fitted) will keep working.
3. **Take a photo.** Even if you call a vet, they will ask.

## Fill in your local vet numbers

This page exists in the repo. Fill the numbers in. Print it.

| Contact                            | Number / link             |
|------------------------------------|---------------------------|
| Local exotics vet (primary)        | <fill in>                 |
| 24h exotics vet                    | <fill in>                 |
| Reptile-experienced friend         | <fill in>                 |
| Pet shop you bought Biscuit from   | <fill in>                 |
| Reptile rescue (UK)                | https://prc.org.uk        |

`src/modules/vet_contacts.py` reads `data/vets.json` for the structured
version of this. The repo ships an example.

## Heat stress (the most urgent)

Open mouth breathing, lying flat in the open, eyes half closed,
unresponsive. Top probe above 28 °C.

* Move tank to a cooler room (16 to 20 °C is fine).
* Mist the tank lightly to drop humidity-adjusted temperature.
* Do **not** put ice in the tank or run a fan directly on him.
* If he does not recover within 30 minutes, call a vet.

## Dropped tail

Treat as an injury that needs no surgery but does need cleanliness.

* Move Biscuit to a smaller hospital tub with paper towel.
* Keep humidity high (80 %+).
* The wound seals within a day. Watch for discharge or swelling.
* The tail will not grow back. He is fine without it. Many cresties
  live tail-free.

## Not eating for over a week

Adults can fast briefly. A week is when you start watching closely.

* Check temperature first. Cold cresties stop eating.
* Check humidity. Dehydrated cresties stop eating.
* Offer a fresh batch of CGD (different flavour if you have one).
* Offer one small dusted insect in the evening.
* Weigh him. If he has lost more than 5 % of his body weight, vet.

## Stuck shed

Especially toes, tail tip, around eyes.

* Bump night humidity to 90 %+ for a day.
* Place a damp paper towel hide on the floor.
* Do not pull shed off with your fingers. If it is on toes after 48
  hours of high humidity, dab gently with a damp cotton bud.
* Toes left in retained shed lose blood supply and the gecko loses
  toes. Vet if you cannot clear it.

## Visible injury or blood

Photo. Vet. Do not improvise.

## Power cut while you are away

* Cresties survive a power cut for many hours, even a day, as long as
  the room is between 16 and 26 °C.
* The misting reservoir is silent during a cut. Humidity will drift
  down. Not an emergency for a day.
* Lights off for a day is fine.
* The bigger risk is the misting system **stuck on** during a cut
  (mechanical solenoid failure). Inspect when power returns.

## When Scout is the problem

If Scout is misting every minute, calling for help on a loop, or doing
something visibly wrong:

1. `Ctrl-C` on the Pi terminal.
2. Or unplug the Pi power supply.
3. The relays will all open (default low). The tank is now static.
4. Open the journal at `data/journal.jsonl` and read the last twenty
   lines. The reason is usually in there.
5. Open an issue on the repo or message the keeper before restarting.

Biscuit can live without Scout. He cannot live without a human noticing.
