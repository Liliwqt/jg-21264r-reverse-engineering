# Verification plan

## Evidence levels

| Level | Meaning | Present status |
| --- | --- | --- |
| Owner report | Photograph interpretation or a reported meter observation | Available |
| Direct connection candidate | Stable near-baseline resistance in both probe orientations, tied to an identified physical lead | Not yet recorded |
| Verified pin function | Identified physical pin plus reliable component documentation or appropriate electrical evidence | Not established for driver pins |
| Powered verification | Measured behavior at a suitable, confirmed supply | Owner reports supply/input/output measurements and M1 direction/stopping, M2/M3 both commands working, and M4 working; rated load/reset/simultaneous operation untested |
| Integrated verification | Measured behavior through the intended ESP32/driver interface | Individual channel tests complete by owner reports; permanent eight-GPIO interface, full vehicle/load/reset validation remain open |

Documentation generation, link checks, and image verification do not advance these hardware evidence levels.

## Investigation sequence

| Stage | Work | Exit evidence |
| --- | --- | --- |
| A · Identity | Read package markings, identify package orientation, resolve U3 naming | Annotated physical pin-1 references; verified component documentation where obtainable |
| B · Unpowered connectivity | Check meter baseline; revisit suspect transient reports; trace battery and sockets | Stable resistance records; physical battery-pad references; separate supply/output/control groups |
| C · Power suitability | Establish actual fitted voltage, pack condition/protection, logic rail, and a controlled power setup | Measured rails and documented power limits before ESP32 connection |
| D · Driver interface | Determine input/output direction, truth table, input thresholds, PWM suitability, and U3 ownership | Reviewed interface table and a reversible isolation/connection plan |
| E · ESP32 bench integration | Configure a verified stop state; connect compatible logic; test one unloaded motor | Correct direction/stop behavior; no contention/back-powering; stable rails |
| F · Smartphone control | Add deliberate arming, command ownership, timeouts, and steering | Stop-on-loss/reset tests; measured motor mapping; bounded movement trial |

## Immediate next checkpoint

**Motor-control mapping and basic individual tests are complete as of 2026-11-07.** Eight input paths and four output pairs are recorded; M1 has detailed direction/stop observations, M2 and M3 are explicitly reported working on both commands, and M4 is reported working. M3 is owner-identified at the third motor socket. See the [completed map](completed-motor-map.md) and [bench record](bench-record.md) for the measured values, earlier M2 connection issues, and reporting limits.

Next, build the [permanent interface board](interface-board.md). The owner will choose eight GPIOs for convenient routing; verify them against the exact development-board model before soldering the ESP32 side. Install one 1 kΩ series resistor and one driver-side 10 kΩ pulldown per input, with common B−/ESP32 ground. Complete unpowered connection/isolation checks on the assembled board, then update firmware for the chosen GPIOs. Existing firmware remains a reusable GPIO4/5 single-channel bench program.

After assembly and firmware changes, recheck startup, each channel, and stopping before any combined operation. Rated load/current, reset/disconnect behavior, coast versus brake, PWM, chassis mapping, and smartphone control remain next-stage work. No completed new board or simultaneous four-channel operation is claimed.

Correlate the owner's numbering with physical package leads and identify which earlier results were temporary beeps. Continue with **one measurement task at a time**, explaining probe positions, meter mode, expected readings, and interpretation before moving on. Do not infer a driver input solely because it has continuity to U3.

## Electrical operating rules

- Disconnect battery, USB, and all other supplies for resistance/continuity tests. Check for residual voltage before measuring resistance; never discharge a capacitor by shorting it.
- Keep ESP32 GPIO disconnected from unidentified pins. Never drive a motor directly from GPIO.
- Do not connect a meter in current mode across the battery.
- Avoid deliberately stalling a motor. Driver current capability and simultaneous motor load remain open questions.
- Do not connect cells in series or parallel until the required voltage and the cells' suitability/protection are established.
- Lift wheels or unload the drivetrain during initial motor tests. Make power easy to disconnect.
- Treat temporary beeps separately from stable low-resistance measurements. The present shared groups are not certified copper nets.
- Preserve the antenna and original controller until their role and the required interface change are understood.

## Integration acceptance criteria

Before publishing a working firmware claim, record: board supply and logic levels; exact GPIO/header mapping; electrical ownership of each input; driver truth table; stop behavior; motor/socket mapping; measured startup behavior; and loss-of-command/reset tests. Record separately whether tests were simulated, bench-powered, unloaded motor tests, or physical driving tests.
