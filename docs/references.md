# References and provenance

## Primary project evidence

1. Owner-supplied component-side photograph, preserved in [board-component-side.jpg](../assets/images/board-component-side.jpg).
2. Owner-supplied connector-side photograph, preserved in [board-connector-side.jpg](../assets/images/board-connector-side.jpg).
3. Owner-reported continuity tests and explicit corrections, transcribed in the [measurement record](measurement-log.md).

The photographs were not used to certify automatic trace extraction. No pin group in this repository was independently measured by the documentation tooling.

## ESP32-S3

[Espressif ESP32-S3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf), checked 2026-11-01. It documents 2.4 GHz Wi-Fi, Bluetooth LE, and PWM peripherals. It does not establish which pins are exposed or reserved on the owner's specific N16R8 development board. Check that board's module and schematic before selecting GPIOs.

## Possible U3 identification

[RC-car transmitter technical description, FCC ID 2AWSR-F51555B](https://fcc.report/FCC-ID/2AWSR-F51555B/5841853.pdf) identifies a related **XC2455B TX** device as an RF MCU. This filing was referenced during the earlier discussion; the document could not be re-fetched during repository preparation. It is background support for a possible part-family reading, not a datasheet, receiver pinout, or proof of this PCB's identity.

## Unresolved documentation

No reliable manufacturer pinout for the exact **1818BM** devices has been established in this project. Seller descriptions and similar-looking motor-driver parts are insufficient grounds for assigning supply pins, current limits, logic thresholds, or a truth table. The `21006` marking is not interpreted as a specification.

## Two-lead crystal polarity

[Abracon application guidance, Appendix A](https://abracon.com/Support/appendix-a.pdf) states that quartz-crystal leads are interchangeable. This supports the non-polarized interpretation of a two-lead crystal; it does not verify the manufacturer, complete specifications, or U3 pinout on this board. The X1/16.000 markings and the U3-3/4 lead mapping are owner reports.

## Regulator and software references

- [UMW XC6206 manufacturer datasheet](https://www.umw-ic.com/static/pdf/a7f417dcdaa605ae97c2ae679a143c9f.pdf) lists the XC6206P332MR top marking 662K. This supports a candidate identification, not proof of the actual board manufacturer.
- [ESP-IDF GPIO documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/gpio.html) documents the GPIO API and reserved/strapping/USB pins.
- [ESP-IDF console documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/stdio.html) explains primary-console input and secondary output-only behavior.

The local standalone application is prepared for the installed ESP-IDF 6.0.2 SDK. Build verification and physical flashing/measurement are separate claims.
