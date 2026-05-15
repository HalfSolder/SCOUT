# Hardware

This is the bill of materials and the wiring reference. Update it as
parts arrive and as the build evolves.

## Bill of materials

| Part                          | Purpose                              | Notes                                  |
|-------------------------------|--------------------------------------|----------------------------------------|
| Raspberry Pi 4 (4 GB) or Pi 5 | Runs the whole brain                 | Pi 5 preferred for camera bandwidth    |
| Pi Camera Module 3            | Watches Biscuits                     | Wide angle if available                |
| 7 inch HDMI LCD               | "What Scout is thinking" display     | Any HDMI panel works                   |
| 2 x DHT22                     | Temperature and humidity probes      | 4.7 kΩ pull up on each data line       |
| Float switch                  | Water reservoir level                | Normally open recommended              |
| 2 channel 5 V relay module    | Drives heat lamp and water pump      | Opto isolated                          |
| Ceramic heat emitter (CHE)    | Warm side heat                       | 50 W to 75 W typical                   |
| 12 V peristaltic pump         | Refills water dish                   | Food safe tubing                       |
| MG90S servo                   | Mealworm hopper                      | Any small hobby servo will do          |
| 12 V PSU plus buck converter  | Pump and Pi power                    | Do not share grounds carelessly        |

## Pin map

GPIO assignments live in `config.yaml`. The defaults (BCM numbering):

| BCM pin | Role                                          |
|---------|-----------------------------------------------|
| 4       | DHT22 warm side data                          |
| 17      | DHT22 cool side data                          |
| 18      | Heat lamp relay (active HIGH)                 |
| 22      | Water pump relay (active HIGH)                |
| 23      | Feeder servo PWM                              |
| 24      | Water level float switch (pull up, to GND)    |
| 25      | LCD backlight enable (optional)               |

Change pin numbers in `config.yaml`, never in the code.

## Build order

Follow this order, top to bottom. Do not skip ahead.

1. Pi boots, talks to the camera and the LCD, runs the loop in dry mode.
2. Wire up DHT22 number one (warm side). Confirm a sensible reading.
3. Wire up DHT22 number two (cool side). Confirm a sensible reading.
4. Wire up the water level float switch. Tip the reservoir to check both
   states.
5. Wire up the relay module. Drive the channels from a small test
   script before connecting any load.
6. Connect the water pump to its relay channel. Run a 1 second pulse and
   measure how much water moves.
7. Connect the heat lamp to its relay channel. **Mains side stays in a
   proper enclosure, with a fuse, mounted somewhere a falling object
   cannot land on it.** If you have not done mains wiring before, ask
   someone who has.
8. Wire up the servo. Test the hopper drops one mealworm reliably and
   does not jam.
9. Empty tank rehearsal (Phase 3 in the experiment doc).

## Safety notes for the keeper

* The heat lamp is mains powered. Use a relay rated for the load. Mount
  it inside an enclosure. Put a fuse on the heat lamp side. If anything
  feels homemade in a bad way, stop.
* The CHE puts out no light. Biscuits still needs a day cycle, driven
  outside Scout (a simple plug timer is fine).
* Always run a new actuator in dry mode first, then by hand on the
  bench, then connected to its real load, then under Scout. Each step
  catches a different kind of mistake.
* The gecko trusts the human who built this. Take that seriously.
