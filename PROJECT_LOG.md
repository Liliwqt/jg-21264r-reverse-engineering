# Project log

## Current status

- 2026-11-01: Added owner reports M14/M15: U1/U2 pins 10 and 11 join NEG, and blue Group B (U1/U2 pins 4 and 8) connects to battery positive. The current map has 12 reported groups covering 37 IC pins. Updated hardware evidence, current-board architecture, generated layouts, and the measurement history; electrical functions and voltage remain unverified.

- 2026-11-01: Initial documentation is complete locally: both original board photos, 12 reported connection groups covering 33 IC pins, colored/ASCII pin layouts, SVG diagrams, architecture, correction history, and verification plan. The project is located at `~/Hardware projects/jg-21264r-reverse-engineering` and published privately at `https://github.com/Liliwqt/jg-21264r-reverse-engineering` on `main`. Initial content commit `8c05c78c0ef68991ca91d00bd5bec5cd3e00da9f` was verified through the GitHub API. No ESP32 connection, firmware, powered board test, or independently verified driver pinout is recorded.

## Active work

- None. Initial documentation and repository publication are complete; hardware investigation remains open.

## Changes

- 2026-11-01: Started the standalone JG-21264R hardware project. Work is staged separately from the unrelated AI Defense Arena repository; the requested destination is `~/Hardware projects/jg-21264r-reverse-engineering`. Verification: repository destination and image availability checked locally; hardware observations remain owner-reported.

- 2026-11-01: Completed `root-hardware-repository` documentation checkpoint. Added README, hardware/architecture/measurement/verification/reference documents, firmware entry criteria, original photographs with a SHA-256 manifest, canonical JSON connectivity, and a standard-library renderer generating colored Markdown, pure ASCII, and SVG views. Preserved the U1-6 to U3-12 correction, U3-2/5 reversion, separate U2-6/7 links, ANT-to-U3-16, and latest battery-negative reports. Verification: `python3 tools/render_pin_map.py --check` passed locally on 12 groups/33 pins; Python SHA-256 checks matched both original JPEGs; ElementTree parsed both SVGs; local Markdown link/image checks passed all 28 targets; pure ASCII encoding check passed. Both diagrams were rasterized with ImageMagick and visually inspected by the agent; this is not owner visual acceptance. These are live local file/document checks, not mocked hardware tests or electrical verification. No firmware or hardware connection was performed. GitHub publication remains pending.

- 2026-11-01: Placed the standalone repository in the requested home folder and published the 19-file initial commit `8c05c78c0ef68991ca91d00bd5bec5cd3e00da9f` to private GitHub repository `Liliwqt/jg-21264r-reverse-engineering`, default branch `main`. Updated only this project log after publication. Verification: `python3 tools/render_pin_map.py --check` and `git diff --cached --check` passed locally; live `gh repo view` confirmed private visibility and the `main` default, while `gh api .../commits/main` and `.../git/trees/main?recursive=1` confirmed the initial commit and all 19 published files, including both photos and diagrams. No mocked hardware, powered circuit test, firmware run, or owner visual review is claimed. The unrelated workspace repository was not modified.

- 2026-11-01: Recorded M14/M15 in canonical connectivity and measurement history; expanded NEG to U1/U2-10/11/14/15 and U3-1/15, and associated B with battery positive. Regenerated colored Markdown, pure ASCII, and SVG layouts; wrapped long SVG legend entries to keep the enlarged group readable. Updated hardware, README, and existing-board architecture descriptions. Verification: live local `python3 tools/render_pin_map.py --check` passed for 12 groups/37 pins; `git diff --check` passed; Python checks passed terminal membership, SVG XML/legend bounds, pure ASCII, and all 28 local link/image targets. ImageMagick rendered the updated SVG and the agent inspected it; no owner visual acceptance or independently repeated electrical measurement is claimed. Earlier numbering corrections remain preserved.
