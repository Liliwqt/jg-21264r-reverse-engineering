# Current reported pin map

Generated from [pin-map.json](../hardware/data/pin-map.json). Update that file and run `python3 tools/render_pin_map.py`; do not edit this generated document by hand.

**Evidence:** owner-reported continuity, including some beeps whose duration was not recorded. This is not a verified schematic or driver pinout. Colors identify reported groups, not signal functions.

## Arrangement matching the component-side photo

U1 is upper left, U2 upper right, and U3 below U1. Numbering follows the owner's working convention; physical pin-1 orientation remains unverified. The NEG symbol records reported continuity to battery negative, not a certified ground assignment.

```text
                  U1                                             U2
 16⬜ 15⏚  14⏚  13⬜ 12⬜ 11⏚  10⏚  09⬜        16⬜ 15⏚  14⏚  13⬜ 12⬜ 11⏚  10⏚  09⬜
 ┌───────────────────────────────────────┐      ┌───────────────────────────────────────┐
 │                 1818BM                │      │                 1818BM                │
 └───────────────────────────────────────┘      └───────────────────────────────────────┘
 01🟥 02🟩 03🟨 04🟦 05🟥 06⬛ 07🟪 08🟦        01🟥 02🟧 03🟫 04🟦 05🟥 06🔷 07🔶 08🟦


                  U3
 16📡 15⏚  14🟩 13🟨 12⬛ 11🟪 10🟧 09🟫
 ┌───────────────────────────────────────┐
 │               Controller              │
 └───────────────────────────────────────┘
 01⏚  02🟥 03⬜ 04⬜ 05🟥 06🔷 07🔶 08⬜
```

**Matching symbols = reported continuity. ⬜ = no connection recorded, not a measured open circuit.** Emoji appearance and alignment depend on the viewer's font; use the SVG or ASCII fallback when needed.

![Reported pin map with group labels](../assets/diagrams/pin-map.svg)

## Connection groups

| Symbol | Group | Recorded IC pins | External point | Interpretation |
| --- | --- | --- | --- | --- |
| 🟥 | A | U1-1, U1-5, U2-1, U2-5, U3-2, U3-5 | — | Unidentified shared group |
| 🟦 | B | U1-4, U1-8, U2-4, U2-8 | battery positive | Reported positive-terminal connection; voltage and direct copper unverified |
| 🟩 | C | U1-2, U3-14 | — | Unidentified connection |
| 🟨 | D | U1-3, U3-13 | — | Unidentified connection |
| 🟪 | E | U1-7, U3-11 | — | Unidentified connection |
| 🟧 | F | U2-2, U3-10 | — | Unidentified connection |
| 🟫 | G | U2-3, U3-9 | — | Unidentified connection |
| ⬛ | H | U1-6, U3-12 | — | Unidentified connection; supersedes U1-6 to U3-5 |
| 🔷 | I | U2-6, U3-6 | — | Unidentified connection |
| 🔶 | J | U2-7, U3-7 | — | Unidentified connection |
| 📡 | ANT | U3-16 | ANT | Reported antenna connection |
| ⏚ | NEG | U1-10, U1-11, U1-14, U1-15, U2-10, U2-11, U2-14, U2-15, U3-1, U3-15 | battery negative | Reported negative-terminal beeps; ground/direct copper unverified |

## ASCII fallback

Each pin is followed by its group ID; `.` means unrecorded. The file [pin-map.ascii.txt](pin-map.ascii.txt) is plain ASCII.

```text
                     U1                                                     U2
 16.   15NEG 14NEG 13.   12.   11NEG 10NEG 09.          16.   15NEG 14NEG 13.   12.   11NEG 10NEG 09.
 +-----------------------------------------------+      +-----------------------------------------------+
 |                     1818BM                    |      |                     1818BM                    |
 +-----------------------------------------------+      +-----------------------------------------------+
 01A   02C   03D   04B   05A   06H   07E   08B          01A   02F   03G   04B   05A   06I   07J   08B


                     U3
 16ANT 15NEG 14C   13D   12H   11E   10F   09G
 +-----------------------------------------------+
 |                   Controller                  |
 +-----------------------------------------------+
 01NEG 02A   03.   04.   05A   06I   07J   08.
```

## Important corrections

- U1-6 is connected to U3-12 in **H**, replacing the earlier U3-5 entry. It is not part of A.
- A retains U3-2 and U3-5 after the owner's explicit reversion.
- U1-3 uses U3-13, and U1-7 uses U3-11.
- U2-6 to U3-6 is a separate later observation, preserved in I.

See the [measurement history](measurement-log.md) for provenance and the [verification plan](verification-plan.md) before using any group as an electrical interface.
