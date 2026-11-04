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

### Three-wire assembly — owner-reported complete

With battery, USB, and all motors disconnected, connect ESP32 GND to RC B−; GPIO4 to the loose 1 kΩ end leading to U3 pad 14; GPIO5 to the loose 1 kΩ end leading to U3 pad 13. This adds only ground and the two resistor-limited signal paths. Do not connect ESP32 3.3 V/5 V to RC B+. This wiring step does not authorize applying power or a motor test. The owner subsequently reported these three wires connected.

The subsequent operator-guided no-motor-load input experiment is recorded below. The existing GPIO waveform was reused as a test signal; motor-control firmware has not been implemented or flashed.


## Connected first-pair input experiment — 2026-11-02

The owner confirmed the three wires connected: ESP32 GND→B−, GPIO4→1 kΩ→U3 pad 14/U1-2, GPIO5→1 kΩ→U3 pad 13/U1-3. Both 10 kΩ driver-side pulldowns remain to B−. No ESP32 3.3 V/5 V-to-RC-supply connection was instructed. All motors remained instructed disconnected throughout.

### Firmware scope and power sequence

The already-flashed standalone GPIO program was reused as a manually commanded test signal generator; no firmware code or device flash changed for this experiment. Its source/banner still describe its original standalone use. This section records the separately guided resistor-interface experiment, not general approval to attach arbitrary RC inputs or operate motors with that program.

1. Assemble unpowered and check the passive network as recorded above.
2. With RC battery and all motors disconnected, power only the ESP32 from USB. Wait for the monitor banner and send `0`; do not send a HIGH command into the unpowered RC board. Check both input pads to B−.
3. Keep USB on and motors disconnected; attach the previously checked single nominal 3.7 V RC cell with correct polarity. Check U1-1 and both input-pad idle voltages before commands.
4. Command `1` while measuring pad 14 to B−, then confirm its return to LOW. Command `2` while measuring pad 13 to B− and confirm its return to LOW. No simultaneous-HIGH state or motor load was tested.
5. For shutdown, request `0`, disconnect RC battery, then disconnect USB before wiring or resistance changes.

### Owner-reported results

| Condition / probe setup | Reported result |
| --- | --- |
| USB-only, command `0`, red on pads 14/13 in turn, black B− | Owner replied 0 to the two-pad check; interpreted as both approximately 0 V |
| USB plus RC single cell, red U1-1, black B− | 3.3 V |
| Both powered, before HIGH commands, pads 14/13 to B− | Owner replied 0 to the two-pad check; interpreted as both approximately 0 V |
| Command `1`, pad 14/U1-2 to B− | 2.94 V |
| Pad 14 after approximately ten seconds | Returned to approximately 0 V, explicitly confirmed |
| Command `2`, pad 13/U1-3 to B− | Owner replied “same” to approximately 2.9 V and return to 0 V; recorded as matching the prior approximately 2.94 V pulse/return without a separate displayed number |

These are owner-reported physical measurements, not mocked or independently repeated by the agent. They establish the observed input-node voltages only. The resistor divider is consistent with roughly 2.9 V from the ESP32 HIGH level; acceptable driver input thresholds and motor behavior are not yet demonstrated. Reset transients, loaded behavior, inactive-input voltage during the other command, and loaded driver behavior remain unmeasured.

The subsequent differential driver-output check is recorded below; its black probe was on U1-13 rather than B−.


## First-channel differential output check — 2026-11-02

With motors instructed disconnected and both boards powered as above, the owner measured DC voltage with **red on U1-16 and black on U1-13**, keeping the probes unchanged between commands. Vout below means V(U1-16) − V(U1-13), not an individual pin voltage relative to ground.

| Serial command | Requested GPIO4 / GPIO5 state | Owner-reported differential Vout |
| --- | --- | --- |
| `1` | HIGH / LOW | **+3.89 V** |
| `2` | LOW / HIGH | **−3.89 V** |
| `0` | LOW / LOW | **0 V** |

**Sign correction:** the first reply appeared to report −3.89 V for command `1`; the owner explicitly corrected that first result to positive. The subsequent command `2` result was explicitly −3.89 V. The final table incorporates that correction; the earlier sign interpretation is superseded.

These owner-reported physical measurements demonstrate opposite differential output polarities for the two single-HIGH commands on the observed U1-16/13 pair. They do not establish output current capability, chassis direction, other channels, reset behavior, PWM, or an operating motor. A 0 V differential reading with both inputs LOW does not distinguish coast/high-impedance from active braking, nor prove that both output pins are individually at ground. Both-HIGH behavior remains untested.

Next proposed step: request `0`, disconnect RC battery first and USB second, leave motors disconnected, confirm the logic rail has discharged, then trace the two contacts of the appropriate motor socket to U1-16 and U1-13 using unpowered continuity/resistance. Physical socket identity was not yet recorded at that step; the owner subsequently identified it below. A short-pulse motor-test procedure/firmware remains to be prepared before motor connection; the current approximately ten-second GPIO test is still a measurement generator.


## M1 socket identification and short-pulse firmware preparation — 2026-11-02

The owner identifies **Motor 1 at the very top left**, in response to the request to identify the U1-16/13 socket with the connector-side photo upright. Recorded as the first of four left motor sockets in that photo. No separate per-contact resistance values or new photograph were supplied.

An opt-in M1 bench mode is now prepared in the existing ESP-IDF project. It uses GPIO4/5 and the measured 1 kΩ/10 kΩ network, requires lowercase `a` followed by `1`/`2` within five seconds, requests LOW after an approximately 500 ms pulse, ignores pulse-extension/reversal attempts during a pulse, and enforces a two-second software cooldown plus a fresh arm. Console logging is isolated from the output task; stop requests have a separate notification. Original ten-second meter mode remains the default for fresh configurations and must not be used for a motor test.

Local SDK configuration selects the new mode and its build passed. Pure-C host tests passed startup, no unarmed output, arm expiry, fixed deadline, repeated/reverse commands, cooldown, rearming, early/unknown stop, delayed tick, and reset scenarios. These simulate time/commands and are not hardware evidence. The standalone branch was additionally cross-compiled with real ESP32-S3 SDK/compiler flags. No new flash, motor connection, motor motion, or physical pulse-timing test has occurred. The existing device image is still the prior meter-test firmware until the owner flashes and confirms the new banner.

Next step is **flash only**, RC battery and every motor unplugged, USB powering ESP32, then confirm `MOTOR BENCH: 500 ms` and `DISARMED` in the monitor. The [motor-bench procedure](motor-bench.md) separates this step from subsequent no-motor startup checks and an eventual single original unloaded motor pulse. This follow-up remains local and uncommitted; no push was made.


## First M1 motor pulses — owner-reported physical results, 2026-11-02

The owner confirmed uploading and seeing the **MOTOR BENCH: 500 ms** banner. With the new image, the owner reported 0 V for the USB-only pad-14/13 check and matching expected powered no-motor checks (U1-1 approximately 3.3 V, U1-16 relative to U1-13 approximately 0 V). Separate numeric readings were not supplied for the matching reply.

The owner then confirmed connecting one original motor to top-left M1 after the instructed shutdown (RC battery first, USB second). Other motors remained instructed unplugged; wheel-raised/free-running setup was instructed, not photographed or inspected by the agent. ESP32 USB was applied before the RC single cell, with the new mode DISARMED and command `0` requested.

| Observation | Owner report |
| --- | --- |
| Both powered, M1 attached, before arming | Motor stayed still |
| Lowercase `a`, wait for ARMED, then `1` | Motor moved and stopped |
| Wait for DISARMED/complete stop; `a`, wait for ARMED, then `2` | Yes to opposite direction and then stopping |

This establishes owner-observed bidirectional motion and automatic stopping for the first M1 experiment. The configured pulse is 500 ms; actual physical pulse duration, stop time, current, temperature, reset transients, and loaded/stall behavior were not measured. No physical manual-midpulse-stop, stop-on-wire-loss, multi-motor, Wi-Fi, or PWM claim is made. Coast versus active brake remains unresolved.

### Chassis role remains partly unknown

The owner reports no separate steering mechanism in the car and assumes M1 is a driving-wheel motor. This is a tentative role, not identification of which wheel, axle, or side is connected. The steering method and left/right/chassis mapping remain unconfirmed; do not choose skid-steer/tank mixing from that statement alone.

At that 2026-11-02 checkpoint, the next task was to power down and identify which wheel/mechanism M1 moved. Only M1 had been exercised and its interface used two series resistors and two pulldowns; see the later M2 record below. These follow-up results were included in the 2026-11-02 published checkpoint.


## Disassembled setup and cleanup plan — 2026-11-02

The owner clarified that the car is disassembled. After confirming power and motors disconnected, the owner was instructed to temporarily disconnect GPIO4/5 and move the resistor junctions from U3 14/13 to 12/11 for M2. The owner asked whether resoldering was necessary; **completion of that move was never reported**. The next request is to clean up the wiring and make a separate board. That plan supersedes the pending temporary retarget instruction.

The [permanent interface plan](interface-board.md) exposes eight separate control traces (U3 14, 13, 12, 11, 10, 9, 6, 7) plus a larger B− ground connection, with one 1 kΩ series and one 10 kΩ driver-side pulldown per lane. It does not connect all sixteen U3 pads, motor power, the original oscillator/antenna, or the tentative LED path. Full population needs eight of each resistor (six additional of each beyond the existing two); M1-only initial population remains possible. At that 2026-11-02 checkpoint, board construction, its continuity/isolation checks, six additional ESP32 GPIO assignments, and M2–M4 function tests remained pending. See the 2026-11-05 M2 follow-up below for the later working report. No PCB artwork or mechanical dimensions have been prepared.


## Permanent breakout clarification — 2026-11-02

The owner wants permanent extensions from the removed U3 footprint to a separate board. The clarified plan is one independent wire per signal pad (6, 7, 9, 10, 11, 12, 13, 14), plus ground from the larger B− point. “Bridge” here means extending the signals to a header, not joining pads electrically. The remaining pads are left available and unconnected for this motor-only interface; original ground/shared rail/crystal/antenna and tentative LED associations are listed in the interface-board document. No soldered breakout completion or new board construction has been reported. The owner then explicitly requested publishing this progress.


## M2 follow-up and connection repair — owner report, 2026-11-05

The owner reported M2 wiring ready. The instructed single-channel bench setup reuses GPIO4/5: GPIO4 through 1 kΩ to U3 pad 12/U1-6, GPIO5 through 1 kΩ to U3 pad 11/U1-7, with a 10 kΩ driver-side pulldown on each input and common B−. This reuses the existing 500 ms bench image; no additional GPIOs or simultaneous two-channel control were implemented.

| Observation | Owner-reported result / limit |
| --- | --- |
| Initial run | Command `2` ran the motor; command `1` did not |
| Fresh-arm retry | `0`, wait, `a`, wait for `ARMED`, then `1` still did not move the motor |
| A-signal attachment | Owner explicitly says the wire is soldered directly to U1 pin 6, rather than U3 pad 12; these are the same originally mapped signal |
| Series-path resistance | With battery and USB instructed disconnected, GPIO4-side end of the series resistor to U1-6 measured approximately **1 kΩ** (`1k yes`) |
| Resolution | Owner then reports the motor works fine and the issue was a connection; exact failed joint and repair details were not specified |

The USB-only and powered startup checks were proposed, but the owner advanced with “next” without individual readings. U1-6-to-B− was subsequently requested with approximately 10 kΩ expected; no numeric result was supplied before the owner reported the connection issue resolved. Do not copy M1's measured voltages, differential polarity, startup behavior, per-command stopping observations, or measured resistor quantities into M2's record. M2's final report is a general working result after repair, not a separate measured timing/load/stop-mode characterization.

The owner requested recording and pushing this checkpoint. M3/M4, the full permanent interface-board/harness assembly, final multi-channel GPIO assignments, and chassis/socket mapping remain open. Current power state and simultaneous M1/M2 wiring were not specified. No firmware change or new flash was reported for this follow-up.
