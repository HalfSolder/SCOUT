# Hardware

Fill this in as parts arrive. Treat it as the bill of materials and the
wiring reference.

## Bill of materials

| Part | Purpose | Notes |
|---|---|---|
| Raspberry Pi 4 (4GB+) | The whole brain runs here | Pi 5 works too |
| Pi Camera Module 3 | Watches the gecko | Wide angle preferred |
| 7" HDMI LCD | "What the robot is thinking" display | Any HDMI panel |
| 2× DHT22 | Temperature + humidity (warm + cool) | 4.7kΩ pull-up each |
| Float switch | Water reservoir level | Normally-open recommended |
| 2-channel 5V relay module | Drives heat lamp + water pump | Opto-isolated |
| Ceramic heat emitter | Warm side heat | 50–75W typical |
| 12V peristaltic pump | Refills water dish | Food-safe tubing |
| MG90S servo | Mealworm hopper | Or any small servo |
| 12V PSU + buck converter | Pump + Pi power | Don't share grounds carelessly |

## Pin map

GPIO assignments are in `config.yaml`. Defaults (BCM numbering):

| BCM pin | Role |
|---|---|
| 4 | DHT22 warm-side data |
| 17 | DHT22 cool-side data |
| 18 | Heat lamp relay (active HIGH) |
| 22 | Water pump relay (active HIGH) |
| 23 | Feeder servo PWM |
| 24 | Water level float switch (pull-up, switch to GND) |
| 25 | LCD backlight enable (optional) |

Change them in `config.yaml`, not in the code.

## Safety notes

- The heat lamp is mains-powered. Use a relay rated for the load, mounted
  in a proper enclosure, with a fuse on the heat-lamp side. **Do not
  freestyle this.**
- The CHE has no light — make sure the gecko has a separate day-light cycle
  driven outside the robot's control loop.
- Test every actuator in dry mode first (`HARDWARE=dry`), then individually
  on the bench, **then** in the enclosure. Don't connect everything at once.
- If you are unsure about any wiring, stop and ask a person who has built
  vivarium electronics before. The gecko trusts you.
