# Individual motor-channel bench experiments

**Current status: the owner flashed the 500 ms mode and confirmed that M1 moved in both directions and stopped after each pulse.** Powered startup stayed still. Exact pulse duration and current were not measured. The owner later reported M2 working after a connection repair on 2026-11-05. As of 2026-11-07 all four channels have owner-reported working tests; M2/M3 explicitly work on both commands and M4 has a general working report. The procedure below retains the M1 pin references; the [completed map](completed-motor-map.md) gives each channel. Rated load, reset behavior, PWM, and phone control remain unverified or unimplemented. See the latest [bench record](bench-record.md) for the physical reports.

## Recorded prerequisites

- Owner identifies M1 as the **top-left motor socket**, first of the four left sockets when the connector-side photo's JG-21264R text is upright. This is an owner identification, not an agent-inspected new photo or independently repeated contact measurement.
- M1 output pair is U1-16/13. With red U1-16 and black U1-13, owner reports `1` **+3.89 V**, `2` **−3.89 V**, `0` **0 V**, without a motor.
- GPIO4→1 kΩ→U3 pad 14/U1-2; GPIO5→1 kΩ→U3 pad 13/U1-3. Each driver-side node has 10 kΩ to B−; ESP32 GND connects to B−.
- Passive resistance checks matched approximately 10/11/20 kΩ; connected input pulses reached approximately 2.94 V and returned to 0 V; U1-1 was 3.3 V.

See the [bench record](bench-record.md) for exact reporting limits, the corrected polarity, and probe setups. The owner has now run the first M1 bidirectional jog test under ESP32 control. A differential 0 V does not establish coast versus brake.

## Select and flash the short-pulse mode

Keep RC battery and all motors unplugged. Keep the verified resistor interface in place. Power only the ESP32 through USB.

Open `firmware/gpio_bench` in VS Code. The current local ignored `sdkconfig` has `CONFIG_GPIO_BENCH_MOTOR_TEST=y` selected. For a fresh checkout, use **ESP-IDF: Open ESP-IDF Terminal**, run `idf.py menuconfig`, and select **JG-21264R bench test → Enable manually armed 500 ms M1 motor test**. Save and exit; GPIO A/B must remain 4/5. This mode is opt-in: a fresh configuration otherwise builds the original ten-second meter-test mode.

Run **ESP-IDF: Build, Flash and Start a Monitor on Your Device**, choosing **UART** as used for the earlier upload. Verify the new banner:

```text
MOTOR BENCH: 500 ms | A=GPIO 4, B=GPIO 5
DISARMED: both LOW. Send a, wait for ARMED, then 1 or 2.
```

Do not attach a motor or RC battery if the monitor still says `STANDALONE GPIO BENCH`, or if mode/configuration is uncertain. The publication/build step does not flash the device. Report the banner before proceeding to the following stages.

## No-motor startup check after the new flash

The owner reported this stage matched the expected startup readings; it is retained below for repeat tests.

1. With all motors still unplugged, keep USB on, wait for `DISARMED`, and send `0`.
2. In DC-voltage mode, black on B−, check U3 pads 14/13 are near 0 V with RC battery absent. Do not send a HIGH command into the unpowered RC board.
3. Attach the same single nominal 3.7 V RC cell with correct polarity. Check U1-1 remains approximately 3.3 V.
4. With no motor connected, red U1-16/black U1-13 should read approximately 0 V for `0`. This does not distinguish coasting from braking.
5. Send `0`, disconnect RC battery first, then USB, before plugging any motor or changing wires.

## First motor pulse

The owner reported the first forward/reverse command pulses moved M1 in opposite directions and stopped. This procedure follows the new-mode startup checks; it is retained for repeat tests.

1. With all power off, connect only the original Motor 1 to the identified top-left socket. Leave the other three motors unplugged. Raise the car so the connected drivetrain can move freely, or use the original motor unloaded; do not hold or stall its shaft/wheel.
2. Power ESP32 by USB first. Confirm the **500 ms** banner and `DISARMED`; send `0`.
3. Attach the same single-cell RC battery. Keep its connector accessible for immediate disconnection if motion continues unexpectedly.
4. Send lowercase **`a`**, wait for **`ARMED`**, then send **`1`** within five seconds. Expect a brief jog followed by both control GPIOs returning LOW. Report whether the motor moved and stopped; do not assume a physical forward direction.
5. Wait for `DISARMED` and for the motor to stop completely. A reverse pulse (`a`, wait for `ARMED`, then `2`) is a subsequent observation, not an automatic sequence.
6. For shutdown, send `0`, remove RC battery first, then USB. Use resistance/continuity mode only after all power is removed and stored rail voltage has fallen near zero.

## M2 single-channel follow-up

For M2, the instructed bench pair is GPIO4→1 kΩ→U1-6 (originally U3 pad 12) and GPIO5→1 kΩ→U1-7 (originally U3 pad 11), with driver-side 10 kΩ pulldowns and shared B−. The recorded M2 output pair is U1-12/9. The owner confirms a direct wire at U1-6 and approximately 1 kΩ through its series path, then reports M2 working after fixing a connection issue. No separate final per-command stop readings were supplied. See the [M2 bench record](bench-record.md#m2-follow-up-and-connection-repair--owner-report-2026-11-05).

The current program still drives only GPIO4/5. Change channel wiring only with battery and USB disconnected; do not wire M1 and M2 together to the same outputs. A firmware/menu label mentioning M1 does not implement additional channels.

## M3/M4 follow-up and permanent-board handoff

The owner identified M3 as socket three using U2-16/13, then reported commands `1` and `2` working with the instructed U2-2/3 input pair. The M4 U2-12/9 socket check was acknowledged without a number; after the U2-6/7 input wiring instruction, the owner reported M4 working. M2 also has a later explicit both-command working report. Detailed pulse/stop/current results were not supplied for these later tests.

Basic individual channel testing is complete. Build the separate resistor interface with all power disconnected. The owner will choose all eight final GPIOs for physical routing; check them against the exact board and update firmware before independent four-channel operation. Current GPIO4/5 firmware is unchanged.

## Commands and limits

| Input | Effect in motor-test mode |
| --- | --- |
| `a` | Arms for five seconds when idle; does not energize either output |
| `1` / `2` after `ARMED` | One approximately 500 ms pulse; repeated direction/arm characters during it are ignored |
| `0`, `s`, or unknown character | Requests both LOW and cancels arming; a stopped pulse enters cooldown |
| No input | Pulse and arm deadlines still expire |
| After a pulse | A two-second software cooldown at LOW, then a fresh `a` required |

The output task checks time on a 20 ms queue wait and does not print or wait for console output. Logging is a separate lower-priority task with a nonblocking notice queue. Stop requests use a separate task notification so later arm/direction characters cannot overwrite a queued stop. These are software measures, not a hardware interlock or a physically verified maximum pulse time. The owner has observed the first M1 motion/stop experiment; these observations do not verify a physical maximum pulse time or rated-load operation. Reset transients, load current, driver ratings, simultaneous four-channel operation, PWM, Wi-Fi, and phone controls remain unverified or unimplemented.

## Local verification

From `firmware/gpio_bench`, the pure-C state-machine checks can be run without ESP-IDF:

```bash
cc -std=c11 -Wall -Wextra -Werror -pedantic -Imain main/motor_bench_state.c tests/test_motor_bench_state.c -o /tmp/jg21264r-motor-state-test
/tmp/jg21264r-motor-state-test
```

These host tests simulate command/time sequences. They do not exercise the ESP32 GPIO hardware, RTOS scheduling, serial transport, or actual motor.
