# JG-21264R Reverse Engineering

**Reusing an RC car control board with an ESP32-S3.**

This project documents the reverse engineering of a salvaged **JG-21264R** RC car PCB. The goal is to retain its existing motor-driving circuitry and replace the lost remote-control interface with an **ESP32-S3 N16R8** and smartphone controls.

**Status: hardware investigation.** The original wiring map and owner-reported motor-output pairs are recorded. The owner has removed U3 and reports that the approximately 3.3 V rail remains present. The standalone ESP-IDF GPIO bench application has been built locally and physically tested by the owner; it is not motor-control firmware. The driver truth table, complete interface, load capability, and powered motor behavior remain unverified.

## Current checkpoint — 2026-11-02

| Completed work | Recorded result |
| --- | --- |
| Original board map | 12 groups, four separate motor-output pairs, 16 MHz X1 crystal, 47 recorded IC pins |
| U3 removal | Controller removed; approximately 3.3 V remains at U1-1 |
| Standalone ESP32 GPIO test | GPIO4 startup 0 V; GPIO4/5 each reached 3.18 V and returned to 0 V after the command pulse |
| Post-removal control checks | All eight candidate pins read 0 V powered and OL to B− unpowered; all eight mapped control paths gave steady continuity |
| First-pair resistor interface | Two 1 kΩ series resistors and two 10 kΩ pulldowns assembled; approximately 10/11/20 kΩ checks matched |

Physical results are owner-reported. The [bench record](docs/bench-record.md) preserves probe setups, individual readings, the resistor diagram, and measurement limits.

**Next step remains unconfirmed:** connect GND→B−, GPIO4 through 1 kΩ to empty U3 pad 14, and GPIO5 through 1 kΩ to pad 13, with USB, battery, and motors disconnected. A powered interconnected test has not occurred. Driver truth table, motor operation, PWM, and phone controls remain future work.

![Current reported pin map, arranged like the component-side photo](assets/diagrams/pin-map.svg)

## Start here

| Document | Purpose |
| --- | --- |
| [Board identification and photos](docs/hardware.md) | Components, connectors, and remaining uncertainties |
| [Current pin map](docs/pin-map.md) | Colored monospace layout, ASCII fallback, and continuity groups |
| [Measurement history](docs/measurement-log.md) | Owner observations and corrected pin references |
| [Bench record](docs/bench-record.md) | Regulator tracing, idle voltages, U3 removal, and post-removal checks |
| [ESP-IDF GPIO bench](firmware/gpio_bench/README.md) | Standalone USB-powered output checks, with the RC board disconnected |
| [System architecture](docs/architecture.md) | Existing board evidence and proposed control/power boundaries |
| [Verification plan](docs/verification-plan.md) | Checks required before powering or connecting the ESP32 |
| [References](docs/references.md) | Source provenance and limits of component identification |
| [Project log](PROJECT_LOG.md) | Current checkpoint and verification evidence |

## Intended behavior

- Smartphone control over a local Wi-Fi connection.
- Forward, reverse, stop, and turning, subject to the verified motor wiring.
- PWM speed control after the existing driver's input behavior is established.
- A configurable stop-on-disconnect behavior and safe startup state.
- Reuse of the original board where measurements establish that it is suitable.

Bluetooth LE is an optional future interface. The ESP32-S3 supports Bluetooth LE; a Bluetooth Classic serial controller is not assumed. See the [official platform reference](docs/references.md#esp32-s3).

## Proposed architecture

![Proposed architecture with unresolved hardware boundaries](assets/diagrams/architecture.svg)

U3 is now removed according to the owner. References to U3 in the original wiring map identify its remaining PCB footprint pads. The final design still needs a verified truth table, input compatibility, appropriate power/reference wiring, and startup behavior. GPIO4/5 are a proposed first-pair bench wiring selection, not a validated motor-control configuration.

## Board photographs

Original files are preserved without alteration. “Component side” refers to the side with the three visible ICs; the other side also has components.

| Component side | Connector side |
| --- | --- |
| ![Three ICs and visible copper traces](assets/images/board-component-side.jpg) | ![Motor, LED, and speaker connections](assets/images/board-connector-side.jpg) |

## Repository layout

```text
.
├── README.md
├── PROJECT_LOG.md
├── assets/
│   ├── diagrams/              # Generated pin diagram and architecture drawing
│   └── images/                # Original board photographs and provenance
├── docs/                     # Hardware evidence, architecture, and verification
├── firmware/                 # ESP-IDF standalone bench test; motor integration pending
├── hardware/
│   └── data/pin-map.json      # Canonical reported connectivity
└── tools/render_pin_map.py    # Standard-library diagram/document generator
```

## Maintaining the pin map

Update `hardware/data/pin-map.json`, append the measurement/correction to `docs/measurement-log.md`, then regenerate the views:

```bash
python3 tools/render_pin_map.py
python3 tools/render_pin_map.py --check
```

`--check` validates pin ranges and group membership, and checks that generated documents match the data. It checks documentation consistency, not electrical continuity. No hardware is accessed.

## Electrical constraints

Keep the ESP32 disconnected during identification. Use continuity/resistance mode only on an unpowered board. A temporary beep is not evidence of a direct copper connection. The printed **3.7 V / 7.4 V** options do not establish the operating voltage of this board configuration, and reported terminal connections do not establish the operating voltage or verified IC supply-pin functions.
