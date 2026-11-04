# Permanent motor-signal interface board

**Plan: eight separate U3 signal wires plus one B−/ground wire, not all sixteen U3 pads.** This is a perfboard/wired-interface plan, not fabrication-ready PCB artwork. M1 has a detailed owner-reported motor test; M2 was later reported working after a connection repair. M3/M4 remain to be exercised.

The car is disassembled according to the owner. Wheel/chassis mapping can wait until assembly. The earlier cleanup plan superseded a pending temporary M2 move. On 2026-11-05 the owner reported M2 ready and subsequently working, with its A-signal wire directly on U1-6. Full separate-board/harness completion and simultaneous channel wiring remain unconfirmed. Keep power and motors disconnected during construction.

## RC-board connections

Use the owner's existing pad-number convention and the continuity map. Each A/B entry is a distinct signal: never join the two pads together.

| Proposed channel | Signal A: U3 pad → driver lead | Signal B: U3 pad → driver lead | Functional evidence |
| --- | --- | --- | --- |
| M1 | 14 → U1-2 | 13 → U1-3 | Owner reports both motion directions and stopping |
| M2 | 12 → U1-6 | 11 → U1-7 | Owner reports working after connection repair; A wire directly on U1-6; 1 kΩ series path confirmed |
| M3 | 10 → U2-2 | 9 → U2-3 | Continuity mapped; powered function pending |
| M4 | 6 → U2-6 | 7 → U2-7 | Continuity mapped; powered function pending |

Add one ground wire from the **larger B− connection** to the interface-board ground bus and ESP32 GND. U3 pads 1/15 are not needed for this design because ground is taken from B−. Leave U3 pads **1, 2, 3, 4, 5, 8, 15, 16** unused by the motor interface. These include the original supply, oscillator, antenna, and tentative LED-related nodes; no ESP32 3.3 V/5 V or B+ feed is part of this signal board.

Eight U3 wires + one B− wire = **nine RC-side connections**. The ESP32 side similarly has eight signal connections plus common GND. Motor power remains on the original RC board and battery wiring, not through this resistor board.

## Unused pads remain available

The eight remaining U3 pads are **not declared unusable**. Preserve them as separate copper pads; leave them disconnected from this motor-only interface and do not bridge them together.

| U3 pads | Recorded association | Scope |
| --- | --- | --- |
| 1, 15 | Battery-negative group | Original owner-reported continuity; use the larger B− connection for this interface ground |
| 2, 5 | Shared Group A | Original map joins the group containing U1-1, where approximately 3.3 V was reported; not an ESP32 power source |
| 3, 4 | Two separate X1 crystal leads | Original oscillator connections, unused by the replacement ESP32 motor interface |
| 8 | Appears to lead through a resistor to the LED | Tentative owner observation; investigate before any future LED connection |
| 16 | Antenna | Original reported radio connection, unused by ESP32 control |

The permanent breakout therefore needs only P14/P13/P12/P11/P10/P9/P6/P7 and GND for the planned motor function. Each signal stays independent. Additional functions, such as LED control, would be a separate investigated extension. No completion of the permanent wiring or new board has been reported.

## One lane, repeated eight times

```text
ESP32 GPIO ----[ 1 kOhm ]----+---- RC signal wire / selected U3 pad
                            |
                         [10 kOhm]
                            |
                   common GND bus ---- RC B- and ESP32 GND
```

The pulldown belongs on the **driver/U3-pad side** of the series resistor. The lane has no polarity-sensitive components. Keeping the interface board connected to RC signals and B− while unplugging the ESP32-side signal connector leaves the installed pulldowns connected to the driver-side nodes. It does not establish any untested reset or motor stop behavior.

## Suggested labels and construction

Use two labeled nine-position connectors, one facing the RC harness and the other the ESP32 harness. These are custom harness labels, not U3 pin numbers:

```text
RC-side labels:     P14  P13  P12  P11  P10  P9   P6   P7   GND
                    |    |    |    |    |    |    |    |     |
                  eight independent resistor lanes       ground bus
                    |    |    |    |    |    |    |    |     |
ESP-side labels:   M1A  M1B  M2A  M2B  M3A  M3B  M4A  M4B  GND
```

M1A/M1B correspond to the original GPIO4/GPIO5 bench pair. For the M2-only follow-up the same GPIO4/5 pair was instructed to M2A/M2B, and the owner reported working operation after a connection repair. This is one-channel-at-a-time reuse, not simultaneous independent control. GPIOs for the other six ESP-side signals are **not assigned yet**; confirm the actual ESP32-S3 board headers and update firmware before connecting or driving them. Do not connect several channel signals to the same GPIO to compensate for unassigned pins.

The original plan uses the eight selected U3 pads; a corresponding mapped driver lead is an alternative attachment point, as with the owner-confirmed M2 A wire at U1-6. Preserve separate signals and the series/pulldown network whichever attachment point is used. Solder flexible signal leads once, route them to the connector, and secure the harness so movement does not pull on the small pads. Put the resistors and ground bus on the separate board. Provide readable labels so later tests change connector wiring rather than repeatedly heating the U3 pads. Perfboard with isolated copper pads or stripboard can implement the circuit; inspect any shared copper and isolate signal lanes as required by the actual board type.

## Parts

| Part | Full four-channel quantity | Already available | Additional needed |
| --- | --- | --- | --- |
| 1 kΩ series resistor, ¼ W | 8 | 2 | 6 |
| 10 kΩ pulldown resistor, ¼ W | 8 | 2 | 6 |
| Labeled nine-position connection, RC side | 1 | Not established | As needed |
| Labeled nine-position connection, ESP32 side | 1 | Not established | As needed |
| Perfboard, insulated wire, and strain relief | To fit the enclosure | Not established | As needed |

The available-parts column records the 2026-11-02 inventory; later M2 wiring does not establish a new total count or whether parts were reused. The full board uses **sixteen resistors**, which is different from soldering all sixteen U3 pads. It can be laid out now with positions for all eight lanes and initially populated only for M1 using the existing four resistors. Leave unpopulated series positions open; keep untested/unpopulated motors and corresponding ESP32 signal wires unplugged.

## Checks before power

With battery/USB/motors removed and ESP32 signal wires disconnected, check each populated lane against the intended pad and ground. Based on the previously measured M1 network, expect approximately 10 kΩ from the driver-side node to B− and 11 kΩ from the ESP-side node to B−; between two isolated 10 kΩ-pulled-down nodes expect approximately 20 kΩ. These are in-circuit checks, so investigate unexpected readings rather than assuming a new driver specification. Confirm no direct shorts between separate lanes, and check connector labels against physical wires.

Complete the per-channel no-motor input/output checks before attaching a motor to a newly populated channel. Use a fresh, deliberately armed short-pulse experiment for each motor. The current program controls only GPIO4/5; an eight-GPIO/four-channel controller is not implemented. No custom PCB footprint or board dimensions have been measured for a direct U3 replacement. A custom printed board would require those mechanical measurements and a reviewed schematic/layout separately.
