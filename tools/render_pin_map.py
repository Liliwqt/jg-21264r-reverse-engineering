#!/usr/bin/env python3
"""Render owner-reported connectivity. No hardware access or pinout inference."""

import argparse
import html
import json
from pathlib import Path
import sys
import textwrap

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "hardware/data/pin-map.json"


def read_map():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    chips = {chip["id"]: chip for chip in data["chips"]}
    if set(chips) != {"U1", "U2", "U3"}:
        raise ValueError("Expected the three documented chip aliases")
    membership = {}
    ids = set()
    for group in data["groups"]:
        if group["id"] in ids:
            raise ValueError("Duplicate group: " + group["id"])
        ids.add(group["id"])
        for member in group["members"]:
            chip, pin_text = member.split("-")
            pin = int(pin_text)
            if chip not in chips or not 1 <= pin <= chips[chip]["pins"]:
                raise ValueError("Invalid chip pin: " + member)
            if member in membership:
                raise ValueError("Pin belongs to multiple groups: " + member)
            membership[member] = group
    motor_ids = set()
    for motor in data.get("motors", []):
        chip = motor["chip"]
        if motor["id"] in motor_ids or motor["id"] in ids:
            raise ValueError("Duplicate motor/channel ID: " + motor["id"])
        motor_ids.add(motor["id"])
        if chip not in chips or len(motor["pins"]) != 2 or len(set(motor["pins"])) != 2:
            raise ValueError("Each motor requires two distinct physical pins")
        for terminal, pin in zip(("A", "B"), motor["pins"]):
            member = f"{chip}-{pin}"
            if not isinstance(pin, int) or not 1 <= pin <= chips[chip]["pins"] or member in membership:
                raise ValueError("Invalid or conflicting motor terminal: " + member)
            membership[member] = {"id": motor["id"][1:] + terminal,
                                  "symbol": motor["symbol"], "color": motor["color"],
                                  "kind": "motor_terminal"}
    crystal_ids = set()
    for crystal in data.get("crystals", []):
        if crystal["id"] in crystal_ids or crystal["id"] in ids or crystal["id"] in motor_ids:
            raise ValueError("Duplicate crystal ID: " + crystal["id"])
        crystal_ids.add(crystal["id"])
        if len(crystal["connections"]) != 2:
            raise ValueError("Expected two separate crystal leads")
        terminals = set()
        for connection in crystal["connections"]:
            chip, pin, terminal = connection["chip"], connection["pin"], connection["terminal"]
            member = f"{chip}-{pin}"
            if chip not in chips or not isinstance(pin, int) or not 1 <= pin <= chips[chip]["pins"] or member in membership:
                raise ValueError("Invalid or conflicting crystal connection: " + member)
            if terminal not in {"A", "B"} or terminal in terminals:
                raise ValueError("Crystal terminals must be distinct A/B references")
            terminals.add(terminal)
            membership[member] = {"id": crystal["id"] + terminal,
                                  "symbol": crystal["symbol"], "color": crystal["color"],
                                  "kind": "crystal_terminal"}
    return data, membership


def ascii_layout(membership, colored, u3_removed=False):
    def cells(chip, pins):
        result = []
        for pin in pins:
            group = membership.get(f"{chip}-{pin}")
            if colored:
                symbol = group["symbol"] if group else "⬜"
                # The ground glyph occupies one cell; common emoji occupy two.
                result.append(f"{pin:02}{symbol}" + (" " if symbol == "⏚" else ""))
            else:
                result.append(f"{pin:02}:{group['id'] if group else '.':<3}")
        return " ".join(result)

    def chip_lines(chip):
        if colored:
            return [
                f"                  {chip}",
                " " + cells(chip, range(16, 8, -1)),
                " ┌───────────────────────────────────────┐",
                " │" + ("1818BM" if chip != "U3" else ("U3 footprint" if u3_removed else "Controller")).center(39) + "│",
                " └───────────────────────────────────────┘",
                " " + cells(chip, range(1, 9)),
            ]
        return [
            f"                     {chip}",
            " " + cells(chip, range(16, 8, -1)),
            " +" + "-" * 55 + "+",
            " |" + ("1818BM" if chip != "U3" else ("U3 footprint" if u3_removed else "Controller")).center(55) + "|",
            " +" + "-" * 55 + "+",
            " " + cells(chip, range(1, 9)),
        ]

    left, right, bottom = (chip_lines(c) for c in ("U1", "U2", "U3"))
    # Widths are display columns. Python len counts emoji as one code point.
    left_width = 42 if colored else 58
    lines = []
    for a, b in zip(left, right):
        display_width = sum(2 if ord(c) > 0xFFFF or c in "⬜⬛" else 1 for c in a)
        lines.append(a + " " * max(5, left_width - display_width + 5) + b)
    return "\n".join(line.rstrip() for line in lines + ["", ""] + bottom)


def markdown(data, membership):
    lines = [
        "# Current reported pin map", "",
        "Generated from [pin-map.json](../hardware/data/pin-map.json). Update that file and run `python3 tools/render_pin_map.py`; do not edit this generated document by hand.", "",
        "**Evidence:** owner-reported continuity, including some beeps whose duration was not recorded. This is not a verified schematic or driver pinout. Group and motor colors organize owner reports; they do not verify pin functions.", "",
        "## Arrangement matching the component-side photo", "",
        "U1 is upper left, U2 upper right, and the U3 footprint is below U1. **U3 is removed, according to the owner.** Groups preserve original-board observations; U3 numbers now refer to remaining PCB pads. They do not certify all post-removal connections. Numbering follows the owner's working convention; physical pin-1 orientation remains unverified. The NEG symbol records reported continuity to battery negative, not a certified ground assignment.", "",
        "```text", ascii_layout(membership, True, data.get("board_state", {}).get("u3_removed", False)), "```", "",
        "**A–J/ANT/NEG symbols identify reported continuity groups. Motor and crystal symbols identify components with two distinct terminals, not a shared electrical net. ⬜ means unrecorded.** Emoji appearance and alignment depend on the viewer's font; use the SVG or ASCII fallback when needed.", "",
        "![Reported pin map with group labels](../assets/diagrams/pin-map.svg)", "",
        "## Connection groups", "",
        "| Symbol | Group | Recorded IC pins | External point | Interpretation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for group in data["groups"]:
        lines.append(f"| {group['symbol']} | {group['id']} | {', '.join(group['members'])} | {', '.join(group['external']) or '—'} | {group['function']} |")
    lines.extend([
        "", "## Reported motor-output pairs", "",
        "M1/M2 follow the owner's U1 names; M3/M4 are project aliases for the corresponding U2 channels. These names do not identify a physical socket order, chassis side, or rotation direction. A/B are neutral terminal labels, not fixed positive/negative polarity.", "",
        "**Each motor connects between its A and B output terminals. A motor pair is not recorded as two pins shorted together.**", "",
        "| Symbol | Motor | IC | Terminal A | Terminal B | Source record |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for motor in data.get("motors", []):
        lines.append(f"| {motor['symbol']} | {motor['id']} | {motor['chip']} | {motor['pins'][0]} | {motor['pins'][1]} | {motor['record']} |")
    lines.extend(["", "## Crystal marking and physical lead reference", ""])
    for crystal in data.get("crystals", []):
        lines.extend([
            f"**{crystal['id']}** is the owner-read PCB marking beside the two-lead crystal; the case reads **{crystal['marking']}**, interpreted as **{crystal['frequency_hz'] / 1_000_000:g} MHz**. The PCB label is not a polarity mark or a manufacturer lead number.", "",
            "| Physical lead | Recorded IC connection | Map label |", "| --- | --- | --- |",
        ])
        for connection in crystal["connections"]:
            lines.append(f"| {connection['lead_reference']} | {connection['chip']}-{connection['pin']} | {crystal['id']}{connection['terminal']} |")
        lines.extend(["", "```text",
                      f"U3-3 ---[ {crystal['id']} : {crystal['marking']} MHz ]--- U3-4",
                      " near X1 marking                  other lead", "```", "",
                      "The crystal is non-polarized. A/B label its observed physical leads only. Its two U3 connections remain distinct; no direct copper connection between them is inferred. Oscillator input/output roles remain unverified.", ""])
    lines.extend([
        "", "## ASCII fallback", "",
        "Each pin is followed by its group ID or motor-terminal ID (`1A`/`1B` through `4A`/`4B`) or crystal-terminal ID (`X1A`/`X1B`); `.` means unrecorded. The file [pin-map.ascii.txt](pin-map.ascii.txt) is plain ASCII.", "",
        "```text", ascii_layout(membership, False, data.get("board_state", {}).get("u3_removed", False)), "```", "",
        "## Important corrections", "",
        "- U1-6 is connected to U3-12 in **H**, replacing the earlier U3-5 entry. It is not part of A.",
        "- A retains U3-2 and U3-5 after the owner's explicit reversion.",
        "- U1-3 uses U3-13, and U1-7 uses U3-11.",
        "- U2-6 to U3-6 is a separate later observation, preserved in I.", "",
        "See the [measurement history](measurement-log.md) for provenance and the [verification plan](verification-plan.md) before using any group as an electrical interface.", "",
    ])
    return "\n".join(lines)


def svg(data, membership):
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="1080" viewBox="0 0 1280 1080" role="img" aria-labelledby="title desc">',
        '<title id="title">JG-21264R owner-reported continuity map</title>',
        '<desc id="desc">U1 upper left, U2 upper right, removed U3 footprint lower left. Group IDs mark reported continuity. Numbered A/B labels mark separate motor-output terminals; matching motor colors identify a channel, not a shared net. Physical pin numbering and electrical functions are unverified.</desc>',
        '<rect width="1280" height="1080" rx="20" fill="#0b1220"/>',
        '<g font-family="Arial, Helvetica, sans-serif">',
        '<text x="48" y="57" fill="#f8fafc" font-size="30" font-weight="700">JG-21264R · Current pin map</text>',
        '<text x="48" y="88" fill="#94a3b8" font-size="16">Owner-reported continuity · Working pin numbering · Electrical functions unverified</text>',
    ]
    positions = {"U1": (70, 240), "U2": (710, 240), "U3": (70, 580)}
    for chip in data["chips"]:
        cid = chip["id"]
        x, y = positions[cid]
        out.append(f'<text x="{x}" y="{y-105}" fill="#f8fafc" font-size="22" font-weight="700">{cid} · {html.escape(chip["position"])}</text>')
        removed = cid == 'U3' and data.get('board_state', {}).get('u3_removed', False)
        dash = ' stroke-dasharray="8 5"' if removed else ''
        out.append(f'<rect x="{x}" y="{y}" width="500" height="120" rx="12" fill="#172033" stroke="#475569" stroke-width="2"{dash}/>')
        out.append(f'<text x="{x+250}" y="{y+57}" text-anchor="middle" fill="#f8fafc" font-size="22" font-weight="700">{cid}</text>')
        out.append(f'<text x="{x+250}" y="{y+87}" text-anchor="middle" fill="#cbd5e1" font-size="14">{html.escape('Removed controller · PCB pad reference' if removed else chip['label'])}</text>')
        for upper, pins in ((True, range(16, 8, -1)), (False, range(1, 9))):
            for index, pin in enumerate(pins):
                px = x + 12 + index * 62
                py = y - 38 if upper else y + 128
                group = membership.get(f"{cid}-{pin}")
                color = group["color"] if group else "#475569"
                label = group["id"] if group else "·"
                out.append(f'<rect x="{px}" y="{py}" width="42" height="30" rx="5" fill="#0b1220" stroke="{color}" stroke-width="2"/>')
                out.append(f'<text x="{px+21}" y="{py+21}" text-anchor="middle" fill="{color if group else "#94a3b8"}" font-size="13" font-weight="700">{label}</text>')
                ny = py - 9 if upper else py + 50
                out.append(f'<text x="{px+21}" y="{ny}" text-anchor="middle" fill="#e2e8f0" font-size="15">{pin}</text>')
    out.append('<rect x="690" y="435" width="540" height="432" rx="12" fill="#111c2e" stroke="#334155"/>')
    out.append('<text x="714" y="469" fill="#f8fafc" font-size="19" font-weight="700">Reported connection groups</text>')
    legend_y = 498
    for group in data["groups"]:
        y = legend_y
        out.append(f'<rect x="714" y="{y-12}" width="12" height="12" rx="3" fill="{group["color"]}"/>')
        out.append(f'<text x="738" y="{y}" fill="#f8fafc" font-size="13" font-weight="700">{group["id"]}</text>')
        pins = ", ".join(group["members"])
        if group["external"]:
            pins += " → " + ", ".join(group["external"])
        legend_lines = textwrap.wrap(pins, width=62, break_long_words=False, break_on_hyphens=False)
        for line_index, line in enumerate(legend_lines):
            out.append(f'<text x="783" y="{y + line_index * 16}" fill="#cbd5e1" font-size="12">{html.escape(line)}</text>')
        legend_y += max(28, len(legend_lines) * 16 + 10)
    out.append('<text x="70" y="800" fill="#f8fafc" font-size="18" font-weight="700">Reported motor pairs · separate A/B terminals</text>')
    for index, motor in enumerate(data.get("motors", [])):
        y = 832 + index * 26
        pins = f"{motor['chip']}-{motor['pins'][0]} / {motor['chip']}-{motor['pins'][1]}"
        out.append(f'<rect x="70" y="{y-12}" width="12" height="12" rx="6" fill="{motor["color"]}"/>')
        out.append(f'<text x="96" y="{y}" fill="#e2e8f0" font-size="15">{motor["id"]} · {pins} · terminal A / B</text>')
    for crystal in data.get("crystals", []):
        out.append('<rect x="690" y="880" width="540" height="82" rx="10" fill="#111c2e" stroke="#334155"/>')
        label = f"{crystal['id']} · {crystal['marking']} MHz · non-polarized crystal"
        out.append(f'<text x="714" y="906" fill="{crystal["color"]}" font-size="16" font-weight="700">{html.escape(label)}</text>')
        leads = "; ".join(f"{c['lead_reference']} → {c['chip']}-{c['pin']}" for c in crystal["connections"])
        out.append(f'<text x="714" y="930" fill="#cbd5e1" font-size="12">{html.escape(leads)}</text>')
        out.append('<text x="714" y="950" fill="#94a3b8" font-size="12">X1A / X1B label separate leads, not positive / negative.</text>')
    out.extend([
        '<text x="70" y="947" fill="#94a3b8" font-size="14">Gray dot = unrecorded. Motor numbers do not specify socket order.</text>',
        '<path d="M48 975H1232" stroke="#334155"/>',
        '<text x="48" y="1003" fill="#cbd5e1" font-size="14">Original-board group references retained. U3 is removed; its numbers identify footprint pads. Paired component terminals are separate.</text>',
        '<text x="48" y="1029" fill="#fbbf24" font-size="14">Rail readings are owner-reported. Package numbering and driver pin functions remain unverified.</text>',
        '<text x="48" y="1055" fill="#94a3b8" font-size="14">Source: hardware/data/pin-map.json · Photo arrangement preserved · No ESP32 GPIO assignments implied</text>',
        '</g></svg>',
    ])
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate data and compare generated files without writing")
    args = parser.parse_args()
    data, membership = read_map()
    plain = "JG-21264R - owner-reported continuity, working numbering\n\n" + ascii_layout(membership, False, data.get("board_state", {}).get("u3_removed", False)) + "\n\nMatching group IDs = reported continuity; . = unrecorded. Motor IDs 1A/1B through 4A/4B mark distinct terminals, not a shared net.\nNEG = reported battery-negative beeps; ANT = reported antenna connection.\nTemporary beeps and physical numbering remain unverified.\n"
    for crystal in data.get("crystals", []):
        plain += f"\n{crystal['id']} marking: {crystal['marking']} MHz; non-polarized.\n"
        for connection in crystal["connections"]:
            plain += f"{connection['lead_reference']} -> {connection['chip']}-{connection['pin']} ({crystal['id']}{connection['terminal']})\n"
    plain.encode("ascii")
    files = {
        ROOT / "docs/pin-map.md": markdown(data, membership),
        ROOT / "docs/pin-map.ascii.txt": plain,
        ROOT / "assets/diagrams/pin-map.svg": svg(data, membership),
    }
    stale = []
    for path, content in files.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        print("Generated files differ: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(f"{'Checked' if args.check else 'Generated'} {len(files)} views; {len(data['groups'])} reported groups; {len(data.get('motors', []))} motor channels; {len(data.get('crystals', []))} crystal; {len(membership)} recorded IC pins.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
