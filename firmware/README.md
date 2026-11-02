# Firmware

ESP-IDF is the selected framework, matching the owner's existing VS Code extension setup.

## Bench application and modes

[Open the GPIO bench project](gpio_bench/README.md). It measures bare ESP32-S3 GPIO outputs using USB power and a multimeter. Default test GPIOs are 4 and 5, subject to checking the actual development-board header labels and onboard usage. The proposed and owner-measured M1 interface is documented separately in the bench record.

The application starts both test outputs LOW. Default standalone mode requests one output for about ten seconds; opt-in `CONFIG_GPIO_BENCH_MOTOR_TEST=y` mode requires fresh arming for each 500 ms M1 pulse and a two-second software cooldown. The local motor-mode build and pure-C host guard tests passed; the owner has since flashed it and observed M1 staying still before arming, moving in opposite directions on `1`/`2`, and stopping after both pulses. Follow the [motor-bench procedure](../docs/motor-bench.md), including battery/motors unplugged during every upload. It provides only these bench experiments, with no full vehicle-control stack, PWM, Wi-Fi, or Bluetooth. For the standalone measurements, keep the salvaged board and motors physically disconnected. The later, separately guided no-motor-load RC input experiment and its resistor network are documented in the bench record; that experiment reused the same GPIO waveform without adding motor-control firmware.

## Future RC-board integration

The owner reports successful standalone command pulses: each GPIO reached 3.18 V and returned to 0 V. GPIO4 also measured 0 V at application startup. These are physical owner measurements, not agent-operated hardware tests.

U3 removal and the post-removal 3.3 V reading are owner-reported in the [bench record](../docs/bench-record.md). A first-pair passive resistor network is assembled and measured; the owner has confirmed GPIO4/5-to-U3-pad-14/13 wiring and approximately 2.94 V input-node pulses returning to 0 V, with all motors disconnected. A validated electrical interface, input truth table, reset behavior, final GPIO-to-driver map, motor/socket/chassis mapping, and PWM behavior remain open. The measured input experiment does not expand this GPIO generator into motor-control firmware; the first U1-16/13 output pair has measured +3.89/−3.89/0 V for commands `1`/`2`/`0`, but loaded behavior and stop mode remain to be established.

Future motor firmware should separate transport, command ownership/timeouts, motion logic, the measured JG-21264R adapter, and platform GPIO/PWM. The standalone bench program does not implement these motor-control boundaries or establish a safe direct connection without series resistors or external pulldowns.
