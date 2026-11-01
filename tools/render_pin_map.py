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
    return data, membership


def ascii_layout(membership, colored):
    def cells(chip, pins):
        result = []
        for pin in pins:
            group = membership.get(f"{chip}-{pin}")
            if colored:
                symbol = group["symbol"] if group else "⬜"
                # The ground glyph occupies one cell; common emoji occupy two.
                result.append(f"{pin:02}{symbol}" + (" " if symbol == "⏚" else ""))
            else:
                result.append(f"{pin:02}{group['id'] if group else '.':<3}")
        return " ".join(result)

    def chip_lines(chip):
        if colored:
            return [
                f"                  {chip}",
                " " + cells(chip, range(16, 8, -1)),
                " ┌───────────────────────────────────────┐",
                " │" + ("1818BM" if chip != "U3" else "Controller").center(39) + "│",
                " └───────────────────────────────────────┘",
                " " + cells(chip, range(1, 9)),
            ]
        return [
            f"                     {chip}",
            " " + cells(chip, range(16, 8, -1)),
            " +" + "-" * 47 + "+",
            " |" + ("1818BM" if chip != "U3" else "Controller").center(47) + "|",
            " +" + "-" * 47 + "+",
            " " + cells(chip, range(1, 9)),
        ]

    left, right, bottom = (chip_lines(c) for c in ("U1", "U2", "U3"))
    # Widths are display columns. Python len counts emoji as one code point.
    left_width = 42 if colored else 50
    lines = []
    for a, b in zip(left, right):
        display_width = sum(2 if ord(c) > 0xFFFF or c in "⬜⬛" else 1 for c in a)
        lines.append(a + " " * max(5, left_width - display_width + 5) + b)
    return "\n".join(line.rstrip() for line in lines + ["", ""] + bottom)


def markdown(data, membership):
    lines = [
        "# Current reported pin map", "",
        "Generated from [pin-map.json](../hardware/data/pin-map.json). Update that file and run `python3 tools/render_pin_map.py`; do not edit this generated document by hand.", "",
        "**Evidence:** owner-reported continuity, including some beeps whose duration was not recorded. This is not a verified schematic or driver pinout. Colors identify reported groups, not signal functions.", "",
        "## Arrangement matching the component-side photo", "",
        "U1 is upper left, U2 upper right, and U3 below U1. Numbering follows the owner's working convention; physical pin-1 orientation remains unverified. The NEG symbol records reported continuity to battery negative, not a certified ground assignment.", "",
        "```text", ascii_layout(membership, True), "```", "",
        "**Matching symbols = reported continuity. ⬜ = no connection recorded, not a measured open circuit.** Emoji appearance and alignment depend on the viewer's font; use the SVG or ASCII fallback when needed.", "",
        "![Reported pin map with group labels](../assets/diagrams/pin-map.svg)", "",
        "## Connection groups", "",
        "| Symbol | Group | Recorded IC pins | External point | Interpretation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for group in data["groups"]:
        lines.append(f"| {group['symbol']} | {group['id']} | {', '.join(group['members'])} | {', '.join(group['external']) or '—'} | {group['function']} |")
    lines.extend([
        "", "## ASCII fallback", "",
        "Each pin is followed by its group ID; `.` means unrecorded. The file [pin-map.ascii.txt](pin-map.ascii.txt) is plain ASCII.", "",
        "```text", ascii_layout(membership, False), "```", "",
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
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="980" viewBox="0 0 1280 980" role="img" aria-labelledby="title desc">',
        '<title id="title">JG-21264R owner-reported continuity map</title>',
        '<desc id="desc">U1 upper left, U2 upper right, U3 lower left. Colored pins share a reported group. Group letters accompany colors. Physical pin numbering and electrical functions are unverified.</desc>',
        '<rect width="1280" height="980" rx="20" fill="#0b1220"/>',
        '<g font-family="Arial, Helvetica, sans-serif">',
        '<text x="48" y="57" fill="#f8fafc" font-size="30" font-weight="700">JG-21264R · Current pin map</text>',
        '<text x="48" y="88" fill="#94a3b8" font-size="16">Owner-reported continuity · Working pin numbering · Electrical functions unverified</text>',
    ]
    positions = {"U1": (70, 240), "U2": (710, 240), "U3": (70, 580)}
    for chip in data["chips"]:
        cid = chip["id"]
        x, y = positions[cid]
        out.append(f'<text x="{x}" y="{y-105}" fill="#f8fafc" font-size="22" font-weight="700">{cid} · {html.escape(chip["position"])}</text>')
        out.append(f'<rect x="{x}" y="{y}" width="500" height="120" rx="12" fill="#172033" stroke="#475569" stroke-width="2"/>')
        out.append(f'<text x="{x+250}" y="{y+57}" text-anchor="middle" fill="#f8fafc" font-size="22" font-weight="700">{cid}</text>')
        out.append(f'<text x="{x+250}" y="{y+87}" text-anchor="middle" fill="#cbd5e1" font-size="14">{html.escape(chip["label"])}</text>')
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
    out.extend([
        '<text x="70" y="820" fill="#cbd5e1" font-size="15">Same group label / color = reported continuity.</text>',
        '<text x="70" y="846" fill="#94a3b8" font-size="15">Gray dot = no connection recorded.</text>',
        '<path d="M48 895H1232" stroke="#334155"/>',
        '<text x="48" y="926" fill="#fbbf24" font-size="15">NEG records a reported beep to battery negative. Transient beeps do not establish direct copper.</text>',
        '<text x="48" y="952" fill="#94a3b8" font-size="14">Source: hardware/data/pin-map.json · Photo arrangement preserved · No GPIO or supply assignments implied</text>',
        '</g></svg>',
    ])
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate data and compare generated files without writing")
    args = parser.parse_args()
    data, membership = read_map()
    plain = "JG-21264R - owner-reported continuity, working numbering\n\n" + ascii_layout(membership, False) + "\n\nMatching IDs = reported continuity; . = unrecorded.\nNEG = reported battery-negative beeps; ANT = reported antenna connection.\nTemporary beeps and physical numbering remain unverified.\n"
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
    print(f"{'Checked' if args.check else 'Generated'} {len(files)} views; {len(data['groups'])} reported groups; {len(membership)} recorded IC pins.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
