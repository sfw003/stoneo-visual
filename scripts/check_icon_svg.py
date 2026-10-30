#!/usr/bin/env python3
"""Lint a stoneo icon SVG against the series rules in references/icon-mode.md.

Usage:
    python3 check_icon_svg.py icon.svg [more.svg ...] [--json]

The grid is detected from the viewBox:
    "0 0 1024 1024"  main art (48px and up)
    "0 0 32 32"      small-size frame (32px and below, see icon-mode.md section 3)

ERROR (exit 1): wrong viewBox, plate geometry / colour, plate-edge missing or
wrong, colours outside the palette, forbidden elements or attributes (text,
images, gradients, filters, masks, opacity, style=...), strokes thinner than
the minimum, axis-aligned lines in the small grid not centred on odd units.
WARN: more than two apricot elements, small-grid fills off the integer grid.
"""
from __future__ import annotations
import argparse, json, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://www.w3.org/2000/svg}"
INK, PAPER, APRICOT, LIGHT = "#2b2520", "#f7f2ea", "#ee9a55", "#fffdf8"
GRIDS = {
    "0 0 1024 1024": dict(name="large", plate=(64, 64, 896, 896, 208), edge=(70, 70, 884, 884, 202),
                          edge_color="#e3d8c8", edge_width=12, min_stroke=40),
    "0 0 32 32": dict(name="small", plate=(2, 2, 28, 28, 6.5), edge=(2.5, 2.5, 27, 27, 6),
                      edge_color="#ddd1c0", edge_width=1, min_stroke=2),
}
ALLOWED_TAGS = {"svg", "defs", "clipPath", "g", "rect", "circle", "ellipse", "line", "path", "polygon", "polyline", "title", "desc"}
DRAWABLE = {"rect", "circle", "ellipse", "line", "path", "polygon", "polyline"}
FORBIDDEN_ATTRS = {"style", "opacity", "fill-opacity", "stroke-opacity", "filter", "mask", "href",
                   "{http://www.w3.org/1999/xlink}href", "font-family", "font-size", "stroke-dasharray"}
URL_OK = re.compile(r"^url\(#[\w-]+\)$")


def num(el, k, default=0.0):
    v = el.get(k)
    if v is None:
        return default
    try:
        return float(v)
    except ValueError:
        raise ValueError(f"<{el.tag.replace(NS, '')}> {k}={v!r} is not a plain number (no units / percentages)")


def lint(path: Path) -> dict:
    errors, warns = [], []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return {"file": str(path), "grid": None, "errors": [f"not well-formed XML: {e} (note: '--' is not allowed inside comments)"], "warnings": []}
    if root.tag != NS + "svg":
        return {"file": str(path), "grid": None, "errors": ["root element is not an SVG in the SVG namespace"], "warnings": []}
    vb = re.sub(r"[ ,]+", " ", (root.get("viewBox") or "").strip())
    grid = GRIDS.get(vb)
    if not grid:
        return {"file": str(path), "grid": None, "errors": [f'viewBox must be "0 0 1024 1024" or "0 0 32 32", got "{vb}"'], "warnings": []}
    if root.get("width") or root.get("height"):
        warns.append("width/height on <svg> are ignored by export; remove them")

    allowed_colors = {INK, PAPER, APRICOT, LIGHT, grid["edge_color"], "none"}
    plate = edge = None
    first_drawable = None
    apricot_count = 0

    def walk(el, inherited, in_defs):
        nonlocal plate, edge, first_drawable, apricot_count
        tag = el.tag.replace(NS, "")
        if tag not in ALLOWED_TAGS:
            errors.append(f"<{tag}> is not allowed (no text, images, gradients, filters, masks, patterns, use)")
            return
        for k in el.attrib:
            if k in FORBIDDEN_ATTRS:
                errors.append(f'<{tag}> attribute "{k.split("}")[-1]}" is not allowed - use plain fill/stroke attributes, solid colours only')
        attrs = dict(inherited)
        for k in ("fill", "stroke", "stroke-width"):
            if el.get(k) is not None:
                attrs[k] = el.get(k).strip().lower()
        for k in ("fill", "stroke"):
            v = el.get(k)
            if v is None:
                continue
            v = v.strip().lower()
            if v.startswith("url("):
                errors.append(f"<{tag}> {k}={v} - gradients / patterns are not allowed")
            elif v not in allowed_colors:
                errors.append(f"<{tag}> {k}={v} is outside the palette {sorted(allowed_colors - {'none'})}")
        clip_ref = el.get("clip-path")
        if clip_ref and not URL_OK.match(clip_ref.strip()):
            errors.append(f"<{tag}> clip-path must be url(#id)")
        defs_here = in_defs or tag in ("defs", "clipPath")
        if tag in DRAWABLE and not defs_here:
            role = el.get("data-role")
            if first_drawable is None:
                first_drawable = el
            if role == "plate":
                plate = el
            elif role == "plate-edge":
                edge = el
            else:
                fill = attrs.get("fill", "#000000")
                stroke = attrs.get("stroke", "none")
                if tag != "line" and fill not in allowed_colors and el.get("fill") is None:
                    errors.append(f"<{tag}> has no fill and inherits black - set fill explicitly")
                if APRICOT in (fill, stroke):
                    apricot_count += 1
                if stroke != "none":
                    sw = float(attrs.get("stroke-width", "1"))
                    if sw < grid["min_stroke"]:
                        errors.append(f"<{tag}> stroke-width {sw:g} < minimum {grid['min_stroke']} for the {grid['name']} grid")
                    if grid["name"] == "small" and tag == "line":
                        x1, y1, x2, y2 = (num(el, k) for k in ("x1", "y1", "x2", "y2"))
                        if sw == int(sw) and int(sw) % 2 == 0:
                            for axis, a, b in (("y", y1, y2), ("x", x1, x2)):
                                if a == b and not (a == int(a) and int(a) % 2 == 1):
                                    errors.append(f"<line> {axis}={a:g}: an even-width line must sit on an odd coordinate in the 32 grid")
                if grid["name"] == "small" and tag == "rect" and stroke == "none":
                    for k in ("x", "y"):
                        v = num(el, k)
                        if v != int(v):
                            warns.append(f"<rect> {k}={v:g} is off the integer grid (blurs at 16/32px)")
                    for k, base in (("width", "x"), ("height", "y")):
                        e = num(el, base) + num(el, k)
                        if e != int(e):
                            warns.append(f"<rect> {base}+{k}={e:g} is off the integer grid (blurs at 16/32px)")
        for c in el:
            walk(c, attrs, defs_here)

    try:
        walk(root, {}, False)
    except ValueError as e:
        errors.append(str(e))

    if plate is None:
        errors.append('missing the plate: <rect data-role="plate" ...> (copy assets/templates/icon-plate.svg)')
    else:
        if plate is not first_drawable:
            errors.append("the plate must be the first drawn element")
        geom = tuple(num(plate, k) for k in ("x", "y", "width", "height", "rx"))
        if geom != tuple(float(v) for v in grid["plate"]):
            errors.append(f"plate geometry {geom} != {grid['plate']} (x, y, width, height, rx)")
        pf = (plate.get("fill") or "").lower()
        if pf not in (PAPER, INK):
            errors.append(f"plate fill {pf} must be paper {PAPER} or ink {INK}")
        if pf == PAPER:
            if edge is None:
                errors.append('paper plate needs the light edge <rect data-role="plate-edge" ...>')
            else:
                eg = tuple(num(edge, k) for k in ("x", "y", "width", "height", "rx"))
                if eg != tuple(float(v) for v in grid["edge"]):
                    errors.append(f"plate-edge geometry {eg} != {grid['edge']}")
                if (edge.get("stroke") or "").lower() != grid["edge_color"] or num(edge, "stroke-width") != grid["edge_width"] or (edge.get("fill") or "").lower() != "none":
                    errors.append(f'plate-edge must be fill="none" stroke="{grid["edge_color"].upper()}" stroke-width="{grid["edge_width"]}"')
        if pf == INK and edge is not None:
            errors.append("ink plate must not have a plate-edge")
    if apricot_count == 0:
        warns.append("no apricot element - the series uses apricot exactly once")
    elif apricot_count > 2:
        warns.append(f"apricot used on {apricot_count} elements - the rule is ONE accent place (a pair of ears counts as one)")
    return {"file": str(path), "grid": grid["name"], "errors": errors, "warnings": warns, "apricot_elements": apricot_count}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    results = []
    for p in a.svg:
        if not p.is_file():
            print(f"check_icon_svg: no such file {p}", file=sys.stderr); sys.exit(2)
        results.append(lint(p))
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for r in results:
            print(f"== {r['file']}  [{r['grid'] or '?'} grid]")
            for e in r["errors"]:
                print(f"ERROR {e}")
            for w in r["warnings"]:
                print(f"WARN  {w}")
            print("OK" if not r["errors"] else "FAIL")
    sys.exit(1 if any(r["errors"] for r in results) else 0)


if __name__ == "__main__":
    main()
