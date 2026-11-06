# JG-21264R Reverse Engineering

**Reusing an RC car control board with an ESP32-S3.**

This project documents the reverse engineering of a salvaged **JG-21264R** RC car PCB. The goal is to retain its existing motor-driving circuitry and replace the lost remote-control interface with an **ESP32-S3 N16R8** and smartphone controls.

**Status: motor-control reverse engineering complete.** The JG-21264R's eight control-input paths and four motor-output pairs are mapped, U3 has been removed, and the owner reports all four channels working in individual ESP32 bench tests. The completed milestone covers access to the original motor-control circuitry; the permanent interface board, final GPIO assignments, independent four-channel firmware, simultaneous operation, PWM, and smartphone control are the next stage.

See the [completed motor-control map](docs/completed-motor-map.md) for the wiring table and the exact evidence for each channel. Original radio, LED/speaker functions, a manufacturer-level IC pinout, driver ratings, reset behavior, and coast-versus-brake behavior are outside this completed milestone.

## Current checkpoint — 2026-11-07

| Completed work | Recorded result |
| --- | --- |
| Original board map | 12 groups, four separate motor-output pairs, 16 MHz X1 crystal, 47 recorded IC pins |
| U3 removal | Controller removed; approximately 3.3 V remains at U1-1 |
| Standalone ESP32 GPIO test | GPIO4 startup 0 V; GPIO4/5 each reached 3.18 V and returned to 0 V after the command pulse |
| Post-removal control checks | All eight candidate pins read 0 V powered and OL to B− unpowered; all eight mapped control paths gave steady continuity |
| First-pair resistor interface | Two 1 kΩ series resistors and two 10 kΩ pulldowns assembled; approximately 10/11/20 kΩ checks matched |
| Connected input experiment, no motors | Three ESP32 wires connected; RC logic rail 3.3 V; pads 14/13 each pulsed to approximately 2.94 V and returned to 0 V |
| First output pair, no motors | Red U1-16 / black U1-13: command `1` +3.89 V, `2` −3.89 V, `0` 0 V |
| M1 socket | Owner identifies the top-left socket in the connector-side photo |
| Short-pulse firmware | 500 ms mode built/host-tested locally, then flashed by owner with banner confirmed |
| First M1 motor experiment | Stayed still before arming; commands `1` and `2` moved it in opposite directions and it stopped after each pulse |
| M2 follow-up | Both commands now reported working; prior connection issue and later 8.90 kΩ A-path reading retained in bench history |
| M3 | Third motor socket identified; commands `1` and `2` reported working |
| M4 | Owner reports working; no separate final per-command/timing readings supplied |
| Motor-control reverse engineering | Completed map of eight control inputs and four output pairs, with individual working reports for M1–M4 |

Physical results are owner-reported. The [bench record](docs/bench-record.md) preserves probe setups, individual readings, the resistor diagram, and measurement limits.

**Next step:** build the [permanent signal interface](docs/interface-board.md). The owner will choose eight ESP32 GPIOs to suit physical wire routing; the proposed GPIOs and exact development-board model must be checked before soldering the ESP32 side. Each signal uses 1 kΩ in series and 10 kΩ to B− on the driver side: eight of each resistor, plus shared ground. Then update the firmware for the final assignments and test the assembled system. Keep power disconnected during construction. No completed new interface board is claimed.

![Current reported pin map, arranged like the component-side photo](assets/diagrams/pin-map.svg)

## Start here

| Document | Purpose |
| --- | --- |
| [Board identification and photos](docs/hardware.md) | Components, connectors, and remaining uncertainties |
| [Completed motor-control map](docs/completed-motor-map.md) | Completed reverse-engineering milestone, driver/U3 signal table, channel reports, and next-stage scope |
| [Current pin map](docs/pin-map.md) | Colored monospace layout, ASCII fallback, and continuity groups |
| [Measurement history](docs/measurement-log.md) | Owner observations and corrected pin references |
| [Bench record](docs/bench-record.md) | Regulator tracing, idle voltages, U3 removal, and post-removal checks |
| [ESP-IDF bench firmware](firmware/gpio_bench/README.md) | Standalone meter mode and opt-in short-pulse M1 mode |
| [First motor-bench procedure](docs/motor-bench.md) | Flash/banner check, no-motor startup checks, then a single unloaded motor experiment |
| [Permanent interface board](docs/interface-board.md) | Eight signal lanes, common ground, connectors, and full/partial resistor population |
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

U3 is now removed according to the owner. References to U3 in the original wiring map identify its remaining PCB footprint pads. The final design still needs a verified truth table, input compatibility, appropriate power/reference wiring, and startup behavior. GPIO4/5 are the reusable single-channel bench pair used in the sequential M1–M4 procedures. The owner reports every channel working, with a direct U1-6 attachment confirmed for M2. The final eight GPIOs will be selected by the owner; the current program still operates only GPIO4/5 and does not provide independent four-channel control.

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
│   └── data/pin-map.json      # Canonical map and owner-reported bench milestones
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
