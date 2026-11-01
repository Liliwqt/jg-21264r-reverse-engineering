# Owner-reported bench observations

Recorded on **2026-11-02** from the conversation. These measurements were performed and reported by the owner. The agent did not operate the meter, inspect a post-removal photograph, or independently reproduce the electrical readings. Dates of individual earlier readings are not all established. The working IC numbering remains the owner's convention.

## Unpowered supply tracing

| Probe points / observation | Reported result | Scope |
| --- | --- | --- |
| U1-1 to B+, probes in each direction | OL both directions | No measurable resistance path in those tests; not a voltage measurement |
| B+ to U1-4 | 0.4 Ω | Reference low-resistance path |
| U1-1 to B− | OL | One reported probe orientation |
| U1-1 to U1-5 | Steady 0.3 Ω after 10 seconds | Supports the direct connection within red Group A |
| Small three-lead component marking | Something like 662K | Candidate XC6206-family 3.3 V regulator; manufacturer not independently identified |
| Lower-right leg to U1-1 | 0.4 Ω | View from above, single lead at top |
| Lower-left leg to B− | 0.4 Ω | Same physical orientation |
| Single top leg to B+ | 3.6 Ω | Unit explicitly confirmed as Ω; not the same as the 0.4 Ω reference; cause of added resistance unresolved |

A manufacturer's XC6206P332MR marking table supports the 662K identification as a candidate. Physical pin associations and output voltage evidence are recorded separately rather than assigning a manufacturer pinout from the top mark alone.

## Powered observations before U3 removal

| Point | Reported voltage / behavior |
| --- | --- |
| One PKCELL cell, separate from board | 3.88 V; nominal label 3.7 V |
| U1-1 relative to B− | Around 3.3 V |
| U1-2 (to U3-14) | Around 0.05 V |
| U1-3 (to U3-13) | 0.003 V |
| U1-6 (to U3-12) | Very low; no numeric voltage supplied |
| U1-7 (to U3-11) | −0.005 V |
| U2-2 (to U3-10) | Settles to 0 V; conversation interpreted this as the latest U2-2 test |
| U2-3 (to U3-9) | 0 V |
| U2-6 (to U3-6) | Settles to 0 V |
| U2-7 (to U3-7) | 0 V |

The motors and ESP32 were to remain disconnected for these tests. Idle near-zero voltages do not prove that U3 outputs were high-impedance. They do not establish the motor-driver truth table, PWM behavior, or input current capability.

## Rework and post-removal state

| Observation | Reported result |
| --- | --- |
| U3-14 to U1-2, before lifting | 0.4 Ω |
| Raised U3-14 lead to U1-2 | OL |
| Exposed PCB pad 14 to U1-2 | 0.4 Ω |
| U3-13 to U1-3, before lifting | 0.4 Ω; no separate after-lift result recorded |
| Final physical state | Owner reports all leads lifted and U3 completely removed |
| B+ to B−, after removal | OL, with the instructed resistance setup |
| U1-1 to B−, after removal | OL |
| U1-1 relative to B−, powered after removal | Owner explicitly confirmed approximately 3.3 V; exact displayed number not provided |
| Empty-footprint inspection | Owner says it is clear; no post-removal image reviewed by agent |

The original map is retained as a historical wiring/footprint reference. U3 numbers now identify its empty PCB pads. Removal is not evidence that every pad is undamaged, every original group still has the same connectivity, or every input is free of bridges. Only pad 14's listed continuity was separately checked during the earlier one-lead isolation step.

## Tentative LED path

The owner reports that **U3-8 appears to connect through a resistor to the LED**. This is a tentative path, not a verified direct net. It is not merged into a continuity group.

## Current integration boundary

The owner has an iron, flux, tweezers, and a multimeter, but does not have the proposed 1 kΩ/10 kΩ interface resistors. ESP-IDF with the VS Code extension is already installed. The standalone ESP32 GPIO test has now been flashed and exercised by the owner, with the salvaged board instructed to remain physically disconnected; results follow. No direct ESP32-to-driver connection, motor operation, or Wi-Fi control has been tested.


## Standalone ESP32 GPIO test — 2026-11-02

The owner selected UART as the extension flashing method, reported completion, and confirmed that the serial monitor displayed `STANDALONE GPIO BENCH: A=GPIO 4, B=GPIO 5`. The exact port name and physical USB connector were not recorded. Flashing method and firmware console configuration are separate settings.

| Check | Owner-reported result |
| --- | --- |
| GPIO4 after application startup, before a command | 0 V |
| GPIO4 after command `1`, meter referenced to ESP32 GND | 3.18 V |
| GPIO4 after approximately ten seconds without another command | Returned to approximately 0 V, explicitly confirmed |
| GPIO5 after command `2`, meter referenced to ESP32 GND | 3.18 V |
| GPIO5 after the pulse | Returned to 0 V |

These are owner-reported physical meter observations, not simulated readings or measurements independently performed by the agent. No separate startup reading for GPIO5, simultaneous check of the inactive output, reset/boot waveform, loaded-output test, or RC-driver connection was recorded. The test establishes the observed standalone commanded levels and return to LOW; it does not establish compatibility with the salvaged driver.

## Powered candidate-input readings after U3 removal — 2026-11-02

Setup instructed: RC board powered from the previously checked single 3.7 V nominal cell, ESP32 and motors disconnected, multimeter on DC volts, black probe on B−, red probe on each listed lead. The owner confirmed U1-2 was 0 V with the board powered; subsequent reports used that setup.

| IC | Pin 2 | Pin 3 | Pin 6 | Pin 7 |
| --- | --- | --- | --- | --- |
| U1 | 0 V | 0 V | 0 V | 0 V |
| U2 | 0 V | 0 V | 0 V | 0 V |

U1 results were reported individually; U2 was reported as all zero. These physical observations were owner-reported, not independently repeated by the agent. Near-zero idle voltage does not establish a pulldown, input impedance, compatible drive voltage, or a motor stop truth table. No direct ESP32-to-RC-board connection has been reported.

## Unpowered candidate-input resistance to B− — 2026-11-02

Setup instructed: battery, USB, ESP32, and motors disconnected; confirm the logic rail discharged in DC-voltage mode before switching to resistance. U1-2 was tested with black on B−/red on the pin, then with probes reversed; the owner reported OL separately for each direction. For the remaining seven pins, the owner was asked to test both directions and reported “ol all.” Meter model and resistance range were not recorded.

| IC | Pin 2 | Pin 3 | Pin 6 | Pin 7 |
| --- | --- | --- | --- | --- |
| U1 | OL both ways | OL, batch report | OL, batch report | OL, batch report |
| U2 | OL, batch report | OL, batch report | OL, batch report | OL, batch report |

These owner-reported physical readings indicate no measurable resistance to B− under the tested conditions. They do not establish infinite resistance, a faulty/disconnected input, a guaranteed floating state, or the absence of every internal bias path. No measurable external pulldown has been demonstrated. No direct ESP32 connection or powered drive test has occurred.

## Control-trace continuity after complete U3 removal — 2026-11-02

With all power instructed disconnected and the meter in continuity mode, the owner reports a steady beep for every listed pair:

| Driver lead | Empty U3 footprint pad | Owner result |
| --- | --- | --- |
| U1-2 | 14 | Steady beep |
| U1-3 | 13 | Steady beep |
| U1-6 | 12 | Steady beep |
| U1-7 | 11 | Steady beep |
| U2-2 | 10 | Steady beep |
| U2-3 | 9 | Steady beep |
| U2-6 | 6 | Steady beep |
| U2-7 | 7 | Steady beep |

The owner reported “steady beep all” in response to the complete table. This supports that the eight mapped paths still conduct after removal; no numeric resistance, reverse-polarity check, adjacent-pad isolation, driver input function, or loaded behavior is established by this result. Observations were not independently repeated by the agent.

## Interface parts and passive assembly plan — 2026-11-02

The owner now has two 1 kΩ and two 10 kΩ resistors. Asked to check each loose resistor with the meter, the owner replied “perfect”; interpreted as confirmation of approximately the expected values, without exact readings or tolerances supplied.

Proposed first input pair: U1-2 via empty U3 pad 14, and U1-3 via empty U3 pad 13. Motor association and truth table remain to be tested. Use one 1 kΩ series resistor per signal and one 10 kΩ pulldown per driver-side node. This is a provisional bench interface, not a manufacturer-specified circuit or guaranteed voltage conversion. Resistors are nonpolarized.

**Initial passive assembly step (now owner-reported complete):** battery, ESP32 USB, motors, and ESP32 GPIO/ground wires were instructed disconnected. The two resistor branches were assembled beside the RC board with future ESP32 ends loose and insulated:

```text
Future GPIO4 end (loose) -- 1k --+-- empty U3 pad 14 --> U1-2
                                |
                               10k
                                |
                               B-

Future GPIO5 end (loose) -- 1k --+-- empty U3 pad 13 --> U1-3
                                |
                               10k
                                |
                               B-
```

Both pulldowns share the RC board B− reference. The 10 kΩ parts attach on the RC-pad side of the 1 kΩ parts. No ESP32 3.3 V/5 V connection is proposed.

### Owner-reported passive network checks

The owner reported the assembly complete, then approximately 10 kΩ for the requested pad-to-B− checks. For the following three checks the owner reported “match exaxtly”; no separate numeric readings or meter tolerances were supplied.

| Black probe | Red probe | Expected value / matched owner report |
| --- | --- | --- |
| B− | Empty U3 pad 14 | Approximately 10 kΩ |
| B− | Empty U3 pad 13 | Approximately 10 kΩ |
| B− | Loose 1 kΩ end for pad 14 | Approximately 11 kΩ |
| B− | Loose 1 kΩ end for pad 13 | Approximately 11 kΩ |
| Empty U3 pad 13 | Empty U3 pad 14 | Approximately 20 kΩ |

All checks were instructed unpowered, with ESP32 wires and motors disconnected. These are owner-reported physical measurements, not independently reproduced by the agent. They support the intended passive paths but do not certify all adjacent pads or driven input behavior.

### Next assembly step — still unpowered

With battery, USB, and all motors disconnected, connect ESP32 GND to RC B−; GPIO4 to the loose 1 kΩ end leading to U3 pad 14; GPIO5 to the loose 1 kΩ end leading to U3 pad 13. This adds only ground and the two resistor-limited signal paths. Do not connect ESP32 3.3 V/5 V to RC B+. This wiring step does not authorize applying power or a motor test. Completion of these three wires has not yet been reported.

Next: document the no-motor-load input test, firmware scope, and power sequencing before energizing the interconnected setup. The existing standalone firmware instructions remain ESP32-only at this checkpoint.
