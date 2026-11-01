# System architecture

**Architecture status:** proposed integration, dated 2026-11-02. This is a design boundary document, not a wiring schematic or a completed circuit.

## Objective and scope

Use the original JG-21264R board as the motor-power stage, with an ESP32-S3 providing local smartphone control. Preserve the existing board while determining whether its driver inputs can be accessed and safely controlled. The first deliverable is a measured interface specification; firmware follows that specification.

## Original wiring and current rework state

U3 is now removed according to the owner. This graph preserves the original wiring reference; U3 labels now denote its PCB footprint pads. The owner reports the 3.3 V rail remains present, but the agent has not inspected a post-removal image or repeated those measurements. See the [bench record](bench-record.md).

## Existing board: evidence model

```mermaid
flowchart TB
    U1["U1 · 1818BM marking\nMotor-driver candidate"]
    U2["U2 · 1818BM marking\nMotor-driver candidate"]
    U3["U3 footprint · controller removed\nOriginal wiring reference"]
    ANT["ANT connection"]
    X1["X1 · 16.000 MHz crystal\nTwo non-polarized leads"]
    POS["Battery positive\nOwner-identified terminal"]
    NEG["Battery negative\nOwner-identified terminal"]
    M1["M1 · U1 channel 1"]
    M2["M2 · U1 channel 2"]
    M3["M3 · U2 channel 1"]
    M4["M4 · U2 channel 2"]
    U1 ---|"C, D, H, E · reported continuity"| U3
    U2 ---|"F, G, I, J · reported continuity"| U3
    U1 ---|"A and B · shared reported groups"| U2
    U3 ---|"A · shared reported group"| U1
    ANT ---|"Reported to U3-16"| U3
    X1 ---|"Near-X1 lead to U3-3; other lead to U3-4"| U3
    POS ---|"B · reported continuity"| U1
    POS ---|"B · reported continuity"| U2
    NEG ---|"NEG · reported beeps"| U1
    NEG ---|"NEG · reported beeps"| U2
    NEG ---|"NEG · reported beeps"| U3
    U1 ---|"Pins 16 / 13 · separate terminals"| M1
    U1 ---|"Pins 12 / 9 · separate terminals"| M2
    U2 ---|"Pins 16 / 13 · separate terminals"| M3
    U2 ---|"Pins 12 / 9 · separate terminals"| M4
```

Undirected lines summarize owner-reported connections; they do not imply signal direction or verified direct copper. Each motor edge labels two distinct output terminals, not a short between those pins. M3/M4 are project aliases for the U2 channels; physical socket order remains open. Group names correspond to the [canonical map](../hardware/data/pin-map.json).

## Target control path

![Proposed system boundaries](../assets/diagrams/architecture.svg)

```mermaid
flowchart LR
    PHONE["Smartphone\nLocal browser controls"]
    NET["ESP32-S3\nWi-Fi command transport"]
    GUARD["Command arbiter\nValidation · arming · timeout"]
    MOTION["Motion controller\nDesired motor states"]
    HAL["Board-specific adapter\nVerified truth table and PWM"]
    IFACE["Electrical interface · TBD\nVoltage compatibility + input ownership"]
    DRV["JG-21264R power stage\nU1/U2 suitability unverified"]
    MOT["Existing motors"]
    PHONE --> NET --> GUARD --> MOTION --> HAL
    HAL -.-> IFACE -.-> DRV -.-> MOT
```

All blocks in the target path are planned. Dashed links cross hardware boundaries that must be validated before connection.

## Responsibilities and contracts

| Boundary | Responsibility | Required evidence / acceptance condition |
| --- | --- | --- |
| Phone → transport | Deliver deliberate local commands and a stop action | Single active controller; reject malformed/out-of-range commands |
| Transport → command arbiter | Provide commands plus freshness/ownership information | Stale packets and abandoned sessions cannot keep motion enabled |
| Arbiter → motion controller | Admit commands only while deliberately armed | Startup, disconnect, timeout, and fault request the verified stop state |
| Motion → board adapter | Request individual motor direction and bounded speed | Physical motor/socket assignments established before steering or tank mixing |
| Board adapter → interface | Translate abstract states to measured input combinations | Driver truth table, PWM capability, input levels, and transition behavior verified |
| Interface → existing driver stage | Deliver valid signals with one electrical driver per control input | U3 removal reported; verify pad integrity, input compatibility, and biasing |
| Supply → board and ESP32 | Provide appropriate motor and regulated logic power | Fitted board voltage, motor load, dev-board power input, and reference ground verified |

“Stop” is a required behavior, not an assumed all-low pattern. Whether the driver coasts, brakes, or needs an enable signal is currently unknown. No dead-time, PWM frequency, current rating, or truth-table value has been selected. GPIO4/5 are selected only for the standalone test and proposed first-pair bench interface; the final motor-control GPIO map remains open.

## Power architecture

```mermaid
flowchart LR
    PACK["Battery / protected supply\nVoltage and capability to verify"]
    BOARD["JG-21264R motor supply\nB+ path not yet mapped"]
    REG["Suitable logic power path\nRegulation / dev-board input TBD"]
    ESP["ESP32-S3 development board"]
    REF["Verified signal reference\nGround routing TBD"]
    PACK -.-> BOARD
    PACK -.-> REG -.-> ESP
    REF -.- BOARD
    REF -.- ESP
```

Battery-positive identification is separate from logic-supply identification. Motor current must not pass through ESP32 GPIO or an unsuitable logic rail. The final schematic must show any common ground, power switching, decoupling, and back-power prevention required by the measured interface. USB and battery power must not be combined without checking the actual dev-board circuit.

## Control ownership

U3 removal is owner-reported and recorded in the bench log. The owner has rechecked all eight mapped control paths with steady continuity; the two-input passive network at U3 pads 14/13 also matched its 10/11/20 kΩ resistance checks. These checks do not establish input electrical compatibility or certify every adjacent pad. Never parallel driven controller outputs. The eight U1/U2-to-U3 pairs are **candidate control paths**, not proven input pins.

## First-pair bench interface checkpoint

The owner assembled two 1 kΩ series resistors and two 10 kΩ pulldowns at empty U3 pads 14/13. The proposed signal assignments are GPIO4→1 kΩ→pad 14 (U1-2) and GPIO5→1 kΩ→pad 13 (U1-3), with each 10 kΩ pulldown on the driver-side node to B− and ESP32 GND proposed to B−. Completion of the three ESP32 wires is not reported. The [bench record](bench-record.md) contains the assembly diagram and matched passive measurements.

This is a provisional experiment, not a validated motor-control interface. USB, battery, and motors stay disconnected during assembly. A powered test still needs documented firmware scope, supply sequencing, and measured input/output behavior. Motor connection is a later checkpoint. The planned power architecture above is a future design; standalone tests used USB for the ESP32 and separate single-cell RC-board measurements.

## Planned firmware structure

```text
transport/       Wi-Fi session and command transport; optional later BLE adapter
control/         Command validation, ownership, arming, and timeout
motion/          Motor-state requests and measured chassis mapping
board/           JG-21264R input truth table and hardware configuration
platform/        GPIO, PWM, timers, and board startup handling
```

These are module boundaries for a future implementation; the standalone bench program does not implement the future motion-control stack. ESP-IDF is selected. A separate standalone GPIO bench project exists under `firmware/gpio_bench`; motor-control firmware remains unimplemented. A future board configuration must reject incomplete pin assignments and must not ship with guessed defaults.

## Decisions and open questions

| Topic | Current decision / open question |
| --- | --- |
| Reuse | Prefer retaining the original power stage; feasibility is still being investigated |
| Wireless | Local Wi-Fi browser control first; Bluetooth LE optional later |
| Driver identity | No verified 1818BM manufacturer pinout obtained |
| Controller identity | XC24558 versus XC2455B marking unresolved |
| Supply | Owner reports a 3.88 V single cell and approximately 3.3 V logic rail; full supply routing and behavior under load remain unverified |
| Motor allocation | Four owner-reported output pairs recorded; physical socket order, chassis-side mapping, and powered behavior remain open |
| PWM | Required capability to test; no supported range assumed |
| GPIO interface | Eight control paths and first-pair passive network rechecked by owner; ESP32 wiring unconfirmed, driven levels, reset behavior, input thresholds, and stop truth table remain unverified |
| Validation | Unpowered tracing first, then bounded power/logic checks, then unloaded motor tests |

The [verification plan](verification-plan.md) defines what closes each uncertainty.
