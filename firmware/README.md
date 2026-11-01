# Firmware

ESP-IDF is the selected framework, matching the owner's existing VS Code extension setup.

## Standalone GPIO bench application

[Open the GPIO bench project](gpio_bench/README.md). It measures bare ESP32-S3 GPIO outputs using USB power and a multimeter. Default test GPIOs are 4 and 5, subject to checking the actual development-board header labels and onboard usage. This is not an RC-board wiring assignment.

The application starts both test outputs LOW, accepts serial commands for one output at a time, and requests LOW again after about ten seconds. It has no motor-control, PWM, Wi-Fi, or Bluetooth implementation. Keep the salvaged board and motors physically disconnected while using it.

## Future RC-board integration

The owner reports successful standalone command pulses: each GPIO reached 3.18 V and returned to 0 V. GPIO4 also measured 0 V at application startup. These are physical owner measurements, not agent-operated hardware tests.

U3 removal and the post-removal 3.3 V reading are owner-reported in the [bench record](../docs/bench-record.md). A first-pair passive resistor network is assembled and measured; the GPIO4/5-to-U3-pad-14/13 wiring is proposed but unconfirmed. A validated electrical interface, input truth table, reset behavior, final GPIO-to-driver map, motor/socket/chassis mapping, and PWM behavior remain open. The unpowered assembly plan does not expand this standalone program into motor-control firmware.

Future motor firmware should separate transport, command ownership/timeouts, motion logic, the measured JG-21264R adapter, and platform GPIO/PWM. The standalone bench program does not implement these motor-control boundaries or establish a safe direct connection without series resistors or external pulldowns.
