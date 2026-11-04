# Verification plan

## Evidence levels

| Level | Meaning | Present status |
| --- | --- | --- |
| Owner report | Photograph interpretation or a reported meter observation | Available |
| Direct connection candidate | Stable near-baseline resistance in both probe orientations, tied to an identified physical lead | Not yet recorded |
| Verified pin function | Identified physical pin plus reliable component documentation or appropriate electrical evidence | Not established for driver pins |
| Powered verification | Measured behavior at a suitable, confirmed supply | Owner reports supply/input/output measurements and first bidirectional M1 jogs with stopping, plus M2 reported working after connection repair; rated load/reset/M3/M4 untested |
| Integrated verification | Measured behavior through the intended ESP32/driver interface | Partial: M1 startup/jogs/stops observed by owner; M2 later reported working after connection repair; full vehicle/load/reset validation remains open |

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

U3 removal and post-removal approximately 3.3 V are now owner-reported in the [bench record](bench-record.md). The owner has flashed and run the standalone ESP-IDF GPIO test: GPIO4 and GPIO5 each measured 3.18 V on command and returned to 0 V after the test pulse. GPIO4 also measured 0 V at application startup. See the bench record for limits of these observations. Post-removal checks now include all eight candidate pins at 0 V while powered, OL to B− in unpowered resistance checks, and steady continuity on all eight original U1/U2-to-U3-pad paths. The first-pair 1 kΩ/10 kΩ network is now assembled and its 10/11/20 kΩ passive checks matched. The owner has now confirmed the three-wire ESP32 assembly and no-motor-load input experiment: U1-1 remained 3.3 V, both input pads were approximately 0 V idle, and each reached approximately 2.94 V on command then returned to 0 V. The bench record documents USB-first power sequencing and reuse of the existing GPIO waveform. The first U1-16/13 output pair subsequently measured +3.89 V for `1`, −3.89 V for `2`, and 0 V for `0`, with the first sign explicitly corrected by the owner. The owner now identifies M1 at the top-left socket. An opt-in manually armed 500 ms firmware mode and [motor-bench procedure](motor-bench.md) were built/host-tested locally, then flashed by the owner. New-mode startup checks matched; M1 stayed still before arming, moved and stopped for `1`, and reversed and stopped for `2`. The owner clarified the car is disassembled and requested a separate [permanent interface board](interface-board.md). On 2026-11-05 the owner reported M2 ready, initially running only on command `2`, then working after a connection repair. The A wire is directly on U1-6 and its series path measured approximately 1 kΩ. No separate M2 startup voltages or final per-command stopping results were supplied. Next: finish/check the permanent interface and test M3/M4 individually. Additional GPIO assignment, per-channel no-motor tests, and guarded motor tests remain prerequisites for four-channel operation; wheel/side mapping can wait until assembly. Reset behavior, threshold limits, coast-versus-brake behavior, and motor-load capability remain open.

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
