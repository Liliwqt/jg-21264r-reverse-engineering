# JG-21264R motor-control reverse engineering — completed

Milestone completed **2026-11-07**, based on the owner's continuity measurements and physical bench reports. All eight motor-control inputs and all four output pairs have been mapped, the original U3 controller has been removed, and each channel has an owner-reported working test using the ESP32 bench setup. This is the completed motor-control map for building the replacement interface.

## Completed motor map

| Channel | Input A | Original U3 pad | Input B | Original U3 pad | Two separate motor outputs | Physical socket / bench report |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | U1-2 | 14 | U1-3 | 13 | U1-16 / U1-13 | First/top-left socket; both directions and automatic stopping reported |
| M2 | U1-6 | 12 | U1-7 | 11 | U1-12 / U1-9 | Both commands working after follow-up; direct A wire on U1-6 confirmed; socket number not separately supplied |
| M3 | U2-2 | 10 | U2-3 | 9 | U2-16 / U2-13 | Third socket; commands `1` and `2` reported working |
| M4 | U2-6 | 6 | U2-7 | 7 | U2-12 / U2-9 | Matching output-pair socket acknowledged; numeric socket position not supplied; owner reports working |

Socket counting uses the connector-side photograph with **JG-21264R upright**, counting the four left motor sockets from the top. U1 is upper left, U2 upper right, and the removed U3 footprint below U1 in the component-side reference. Numbering preserves the owner's convention. Output pairs are two distinct terminals across a motor, never a shorted net. A/B do not define chassis forward/reverse.

The original continuity map still includes 12 connection groups, four output pairs, the 16 MHz crystal, and 47 recorded IC pins. Its color/ASCII/SVG views are in the [pin map](pin-map.md). Unrecorded or tentative non-motor functions remain marked as such.

## Permanent interface to build

Repeat this lane for each of the eight inputs:

```text
Selected ESP GPIO ----[1 kOhm]----+---- mapped driver input
                                |
                             [10 kOhm]
                                |
                         B- / ESP32 GND
```

Use **eight 1 kΩ series resistors and eight 10 kΩ pulldowns**, with the pulldown on the driver side of each series resistor. The RC side has eight independent signal wires plus one shared B− connection. A mapped U3 pad or its corresponding driver lead accesses the same recorded signal; keep every signal separate. No B+/ESP32 3.3 V/5 V feed is part of this signal interface.

The owner will manually choose eight GPIOs for convenient routing. Final assignments remain **TBD** until the actual development board and reserved/onboard pins are checked. GPIO4/5 are only the existing reusable two-wire test pair. The firmware must be updated before independently controlling all four channels. See the [interface-board plan](interface-board.md).

## Completion evidence and next stage

M1 has the detailed startup, measured input/output, direction, and stopping record. M2 was explicitly reported working on both commands after further troubleshooting; its earlier approximately 1 kΩ reading and later 8.90 kΩ reading are separate observations, not a single stable value. M3 was explicitly reported working on commands `1` and `2`. M4 was reported working without a separate per-command stopping or timing record. The agent did not operate or independently measure the hardware; see the [bench record](bench-record.md).

The completed milestone is motor-control mapping and individual functional checks. The separate interface board has been planned and authorized for construction, not reported fabricated. Simultaneous four-motor operation, rated load/current, reset and disconnect behavior, PWM, chassis/wheel allocation, phone control, and the original radio/LED/speaker circuitry remain outside this milestone. The original board photos are preserved unchanged; no post-rework image or fabrication-ready PCB layout has been supplied.
