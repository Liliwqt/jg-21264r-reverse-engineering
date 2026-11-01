# Measurement record and corrections

Recorded into this repository on **2026-11-01** from the owner's conversation. Individual test dates, meter model, resistance values, probe polarity, and beep duration were not supplied. This is a transcription of observations, not an independently repeated electrical test.

## Current accepted reports

| Record | Owner-reported observation | Current group |
| --- | --- | --- |
| M01 | U1-1, U1-5, U2-1, U2-5, U3-2, U3-5 have continuity together | A |
| M02 | U1-1 did not indicate continuity to either contact of a suspected battery connector | Historical unresolved test; connector identity/setup unclear |
| M03 | U1-2 ↔ U3-14 | C |
| M04 | U1-3 ↔ U3-13, after the U3 numbering correction | D |
| M05 | U1-4, U1-8, U2-4, U2-8 have continuity together | B |
| M06 | U1-6 ↔ U3-12, after the final correction | H |
| M07 | U1-7 ↔ U3-11, after the U3 numbering correction | E |
| M08 | U2-2 ↔ U3-10 | F |
| M09 | U2-3 ↔ U3-9 | G |
| M10 | U2-6 ↔ U3-6 | I |
| M11 | U2-7 ↔ U3-7 | J |
| M12 | ANT ↔ U3-16 | ANT |
| M13 | U3-15, U3-1, U1-15, U1-14, U2-15, U2-14 beep to the negative terminal | NEG; duration/resistance not recorded |
| M14 | U1-10, U1-11, U2-10, U2-11 are also connected to the negative terminal | NEG; owner report, resistance/duration not supplied |
| M15 | The blue mapped group (U1-4, U1-8, U2-4, U2-8) connects to battery positive | B; owner report, voltage/resistance not supplied |
| M16 | U1 pins 16 and 13 are the two outputs for Motor 1 | M1; distinct terminals |
| M17 | U1 pins 12 and 9 are the two outputs for Motor 2 | M2; distinct terminals |
| M18 | U2 has the same 16/13 output pairing | M3; project alias for U2 channel 1 |
| M19 | U2 has the same 12/9 output pairing | M4; project alias for U2 channel 2 |
| M20 | Silver oval crystal case reads 16.000; PCB marking is X1 | X1; nominal 16 MHz interpretation |
| M21 | Crystal lead nearest the X1 PCB marking connects to U3-3; other lead connects to U3-4 | X1A / X1B; separate leads, no polarity implied |

Motor pairs describe two separate outputs across a motor, not direct continuity between those outputs. M3/M4 are project aliases; physical socket order, chassis positions, and polarity are not established.

The owner also reported that some pin pairs appeared to beep while a capacitor charged. No specific pairs were identified. Preserve all current groups as **reported**, and do not promote any to verified direct copper until the stable-resistance check is recorded.

## Later bench measurements and U3 removal

The [bench record](bench-record.md) captures the later resistance/voltage readings, regulator candidate, tentative LED path, one-lead isolation checks, and owner-reported complete U3 removal. Original records above remain historical; U3 references now identify footprint pads.

## Corrections applied

1. The original U1-3 ↔ U3-4 observation was renumbered to **U1-3 ↔ U3-13**.
2. The original U1-7 ↔ U3-6 observation was renumbered to **U1-7 ↔ U3-11**. This is distinct from the later U2-6 ↔ U3-6 observation.
3. U3-2 and U3-5 were temporarily changed to U3-15 and U3-12, then explicitly reverted. Group A therefore retains **U3-2 and U3-5**.
4. The earlier U1-6 ↔ U3-5 entry was explicitly corrected to **U1-6 ↔ U3-12**. U1-6 was removed from Group A and placed in separate **Group H**. Do not re-merge H into A from the superseded entry.
5. U1/U2 numbering was not changed by the U3 corrections. All numbering remains the owner's working convention until physical orientation is verified.
6. Earlier connector guesses were superseded by the owner's LED, SPK, and battery-positive/negative identifications. The right LED socket and bottom SPK footprint are not recorded as battery inputs.

## Adding a measurement

Record one pair at a time, with power disconnected for resistance or continuity checks. Record the numeric value rather than a beep alone.

| Date | From | To | Mode | Initial reading | Reading after 5–10 s | Reversed probes | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | Ux-pin / labeled terminal | Ux-pin / terminal | Ω / continuity | Value or OL | Value or OL | Value or OL | Direct candidate / transient / component path / unresolved |

A persistent value near the probes-touching baseline in both directions supports a direct connection. A rising value or temporary beep may be capacitive; asymmetric readings may involve a semiconductor. In-circuit readings still need interpretation.
