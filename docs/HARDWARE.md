# Hardware

Bill of materials and wiring reference. Update as parts arrive.

## Bill of materials

| Part                                  | Purpose                                    | Notes                                  |
|---------------------------------------|--------------------------------------------|----------------------------------------|
| Raspberry Pi 4 (4 GB) or Pi 5         | Runs the whole brain                       | Pi 5 preferred for camera bandwidth    |
| Pi Camera Module 3                    | Watches Biscuit                            | Wide angle. Look for "NoIR" version.   |
| IR illuminator (850 nm)               | Lights the tank at night for the camera    | 850 nm is invisible to cresties        |
| 7 inch HDMI LCD                       | "What Scout is thinking" display           | Any HDMI panel                         |
| 2 x DHT22                             | Temperature and humidity (top and bottom)  | 4.7 kΩ pull up on each data line       |
| Float switch                          | Water reservoir level                      | Normally open                          |
| 4 channel 5 V relay module            | Misting, water pump, lights, IR lamp       | Opto isolated                          |
| 12 V solenoid valve                   | Misting line                               | Food-safe NSF rated                    |
| Misting nozzle                        | Inside the tank                            | Fine mist, not jet                     |
| 12 V pressurised reservoir or pump    | Drives the misting line                    | Aquarium misting kit is fine           |
| 12 V peristaltic pump                 | CGD slurry into food dish                  | Food-safe silicone tubing              |
| MG90S servo                           | Insect feeder hopper                       | Or any small hobby servo               |
| Plant grow lights or T5 fixture       | Day cycle                                  | Low intensity through foliage          |
| Ceramic heat emitter (optional)       | Cold-weather backup heat                   | On its own dumb thermostat, not Scout  |
| Dumb mechanical thermostat            | Backstop on the heater                     | **Mandatory if a heater is fitted.**   |
| 12 V PSU plus buck converter          | Pumps and Pi power                         | Do not share grounds carelessly        |

## Pin map

GPIO assignments live in `config.yaml`. Defaults (BCM numbering):

| BCM pin | Role                                          |
|---------|-----------------------------------------------|
| 4       | DHT22 top of tank, data                       |
| 17      | DHT22 bottom of tank, data                    |
| 18      | Misting solenoid relay (active HIGH)          |
| 27      | Optional fogger relay                         |
| 22      | CGD peristaltic pump relay                    |
| 23      | Insect feeder servo PWM                       |
| 5       | Water pump relay                              |
| 24      | Water level float switch (pull up, to GND)    |
| 25      | Day lights relay                              |
| 6       | IR lamp relay                                 |

Change pin numbers in `config.yaml`, never in the code.

## Build order

Follow this order, top to bottom. Do not skip ahead.

1. Pi boots, talks to the camera and the LCD, runs the loop in dry mode.
2. Wire up DHT22 number one (top). Confirm a sensible reading with
   `scripts/bringup/test_dht22.py 4`.
3. Wire up DHT22 number two (bottom). Confirm.
4. Wire up the water level float switch. Tip the reservoir to check.
5. Wire up the relay module with NO loads attached. Drive each channel
   with `scripts/bringup/test_relay.py <pin>` and listen for the click.
6. Add the misting solenoid to its relay channel. Run a 1 second pulse
   into a measuring jug. Confirm volume.
7. Add the CGD pump. Run a 2 second pulse with water in the tubing.
   Measure how much moves.
8. Add the water dish pump. Same.
9. Add the day lights and IR lamp. Confirm they switch.
10. Wire up the servo and test the insect hopper drops one insect
    reliably and does not jam.
11. **If a backup heater is fitted, install the dumb mechanical
    thermostat in series before connecting power to the heater.** This
    is non negotiable. It is the third safety layer.
12. Empty tank rehearsal (Phase 3 in the experiment doc).

## Safety notes for the keeper

* The misting line is under pressure. Route hoses where a slip cannot
  spray electronics or Biscuit.
* The lights and the optional heater are mains powered. Use a properly
  rated relay. Enclosure. Fuse. If anything feels homemade in a bad
  way, stop.
* The IR illuminator gets warm. Mount it outside the tank, pointing in
  through the glass. Never inside.
* Crested geckos die from heat. **The dumb mechanical thermostat in
  series with the heater is the most important component on this list.**
  Code-level safety does not protect Biscuit if the Pi crashes with the
  relay stuck on.
* Always run a new actuator in dry mode first, then by hand on the
  bench, then connected to its real load, then under Scout. Each step
  catches a different kind of mistake.
* Biscuit trusts the human who built this. Take that seriously.
