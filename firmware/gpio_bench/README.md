# ESP32-S3 bench firmware

**For the standalone procedure below, use USB power and a multimeter only. Keep the RC board, its battery, all motors, and all other external wiring disconnected from the ESP32.** No external resistors are needed to measure a bare GPIO with the meter in DC-voltage mode.

This ESP-IDF project starts GPIO4/5 LOW after application initialization and offers two build modes:

| Mode | Selection | Behavior |
| --- | --- | --- |
| Standalone meter test | Default, `CONFIG_GPIO_BENCH_MOTOR_TEST` off | Original ten-second GPIO pulses; no motor attached |
| First M1 experiment | Opt-in, `CONFIG_GPIO_BENCH_MOTOR_TEST=y` | Fresh `a` required for each 500 ms pulse; two-second software cooldown; GPIO4/5 only |

The local SDK configuration now selects the **motor-test mode**, built locally and subsequently flashed by the owner. For a fresh configuration use `idf.py menuconfig` → **JG-21264R bench test → Enable manually armed 500 ms M1 motor test**. The [motor-bench procedure](../../docs/motor-bench.md) starts with flashing while RC battery and motors are unplugged, then requires a **MOTOR BENCH: 500 ms** banner. Do not attach a motor to the ten-second standalone mode.

The existing physical measurements used the previous meter-test image; they are recorded in the [bench record](../../docs/bench-record.md). The new state machine has host command/time tests, plus owner-reported M1 motion in both directions and stopping after each pulse. Exact physical pulse duration, rated load, reset transients, and other channels remain unverified. No steering, PWM, Wi-Fi, Bluetooth, or full vehicle-control stack is implemented.

**The remaining instructions on this page describe standalone meter mode. For motor mode use the linked motor-bench procedure.**

## Project and toolchain

Open **this directory**, `firmware/gpio_bench`, as the VS Code folder. It contains the ESP-IDF project's root `CMakeLists.txt`.

Use the existing ESP-IDF extension. Locally available SDK: **ESP-IDF 6.0.2**. This project depends on `esp_driver_gpio` and `esp_timer`; it has no Arduino dependency and uses no PSRAM. It retains the SDK's small default flash layout rather than allocating the full N16R8 memory.

From the command palette, run **ESP-IDF: Open ESP-IDF Terminal**. In that terminal:

```bash
idf.py --version
idf.py set-target esp32s3
idf.py build
```

The standalone test defaults to **GPIO4 and GPIO5**, not physical header positions 4 and 5. Confirm the headers marked `4`/`IO4` and `5`/`IO5` on the exact development board are exposed and unused before testing. The opt-in motor experiment is restricted to the measured GPIO4/5 first-pair interface; other GPIOs are standalone choices only. If necessary, use `idf.py menuconfig` → **JG-21264R bench test** to select two distinct unused GPIOs in the allowed 4–18 range. A board can use some of these pins for its own peripherals; the range is not a guarantee of header availability.

## Console and flashing

The supplied defaults use the ESP32-S3's **native USB Serial/JTAG** console. Use the board's native USB/data port, often labeled USB or OTG. If connected through a USB-to-UART bridge instead, select **UART0** as the primary console using `idf.py menuconfig` → **Component config → ESP System Settings → Channel for console output**. Commands must be sent to the **primary** console; secondary console output does not accept input.

Select the ESP32's port in **ESP-IDF: Select Port to Use**. With the ESP32 still physically separate from the RC board, run **ESP-IDF: Build, Flash and Start a Monitor on Your Device**, or use:

```bash
idf.py -p YOUR_PORT flash monitor
```

Replace `YOUR_PORT` with the actual COM/tty device. This writes firmware to the connected ESP32; the repository preparation/build did not flash any device.

## One measurement at a time

First test the startup state:

1. Meter leads in COM and V/Ω; select **DC voltage**, not resistance/current.
2. Black probe on an ESP32 **GND** header.
3. Red probe on **GPIO4**. Expect near 0 V after the application starts.

Once that result is recorded, type a command into the primary serial monitor:

| Command | GPIO4 / A | GPIO5 / B | Meter expectation |
| --- | --- | --- | --- |
| `0` or `s` | LOW | LOW | Near 0 V |
| `1` | HIGH briefly | LOW | GPIO4 near the board's 3.3 V logic level |
| `2` | LOW | HIGH briefly | GPIO5 near the board's 3.3 V logic level |
| Any other non-newline character | LOW | LOW | Near 0 V |

Each `1` or `2` requests a fresh approximately ten-second test. Do not hold a key down: repeated commands can extend the test. A separate output task checks the deadline even if console input is waiting. The owner has reported both command pulses reaching 3.18 V and returning to 0 V, with GPIO4 at 0 V on application startup. Exact timing, reset transients, and loaded behavior have not been measured. This software timeout is not a hardware safety interlock or a motor watchdog. See the [bench record](../../docs/bench-record.md) for the physical observations and the later, separately guided no-motor-load RC input experiment.

Internal pulldowns are configured during application startup; they do not guarantee a LOW state throughout reset, flashing, or power sequencing. Neither a successful build nor these GPIO measurements establishes a safe interface to the salvaged driver. Do not infer a general-purpose driver interface from these measurements; the first output pair has no-motor voltage observations plus one owner-reported original-motor jog/stop experiment, with reset and rated-load behavior still unverified.

## Official references

- [ESP32-S3 GPIO API and restricted pins](https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32s3/api-reference/peripherals/gpio.html)
- [ESP-IDF standard I/O and primary console selection](https://docs.espressif.com/projects/esp-idf/en/v6.0.2/esp32s3/api-guides/stdio.html)
- [ESP-IDF VS Code commands](https://github.com/espressif/vscode-esp-idf-extension)
