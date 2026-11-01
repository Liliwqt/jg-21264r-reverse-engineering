# Board identification

## Photographs and orientation

![Component side](../assets/images/board-component-side.jpg)

The drawing and map use this photo's arrangement: **U1 upper left, U2 upper right, U3 below U1**. These U-labels are project aliases, not verified factory reference designators.

![Connector side](../assets/images/board-connector-side.jpg)

The connector-side photo is a separate view. It must be mirrored/aligned before comparing positions across the two sides. Do not transfer a left/right position directly between photographs.

## Inventory and evidence

| Item | Record | Evidence / remaining uncertainty |
| --- | --- | --- |
| PCB | JG-21264R; printed date 2021/07/21 | Board photograph |
| U1 | Reported YX 1818BM, second line 21006 | Candidate motor driver; manufacturer pinout unverified |
| U2 | Reported YX 1818BM, second line 21006 | Candidate motor driver; manufacturer pinout unverified |
| U3 | Reported XHGC XC24558; XC2455B is a possible reading | Candidate radio/controller; exact marking unresolved |
| Four left sockets | Motor connections | Owner identification; socket-to-IC output map not yet supplied |
| Right socket | LED | Owner read the LED label; earlier battery-socket guess superseded |
| Bottom two-pin footprint | SPK | Owner read the SPK label; earlier SW interpretation superseded |
| Battery connections | Positive and negative wiring identified by owner, including B+ marking | Exact annotated photo/pad references and B+ circuit tracing still needed |
| ANT | Reported continuity to U3-16 | Does not independently establish U3's full identity or pinout |
| Unpopulated square pads | Exposed solder pads within component outlines | Exact fitted-component options and circuit functions unverified |
| ESP32-S3 | N16R8 development board | Exact module/dev-board pin availability must be checked before GPIO selection |
| Instruments | Soldering equipment and continuity-capable multimeter | Original remote is unavailable |

The text `21006` is retained as a marking. Its meaning has not been verified; it is not used as an electrical specification.

## Pin numbering

All recorded pin references use the owner's current numbering. The diagrams show positions **16 through 9 across the upper edge** and **1 through 8 across the lower edge**. The drawing records that convention; it does not certify the manufacturer's pin-1 orientation.

Before a pin is used electrically, correlate the physical lead, package indicator, photograph, and a verified package/pinout reference. If a numbering correction is required, explicitly migrate affected records rather than silently rotating the diagram.

## Power status

The board includes printed 3.7 V and 7.4 V configuration options. The earlier project context described a 3.7 V toy battery, but its actual pack, condition, and this board's fitted supply configuration have not been electrically established here. Battery polarity identification alone does not authorize applying an arbitrary voltage.

U1-14/15, U2-14/15, and U3-1/15 were reported to beep to battery negative. They form the **NEG** candidate group in the map. Beep duration and resistance values were not recorded. Ground role, low resistance, and direct copper routing remain to be confirmed.
