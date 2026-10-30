#!/usr/bin/env python3
"""Export a stoneo icon SVG to every desktop (and optionally mobile) size.

Usage:
    python3 export_icon.py icon.svg outdir/ [--name app] [--mobile] [--fg-scale 0.78]

Desktop (always):
    outdir/png/<name>-{16,24,32,48,64,128,256,512,1024}.png   transparent RGBA
    outdir/<name>.ico    Windows: 16/24/32/48/64/128/256 frames, each rendered from the vector
    outdir/<name>.icns   macOS: 16/32/64/128/256/512/1024 (incl. @2x slots)

Mobile (--mobile). Needs the plate (tile) elements tagged data-role="plate" /
data-role="plate-edge" in the SVG, see references/icon-mode.md:
    outdir/mobile/<name>-fullbleed-1024.png   opaque square, plate colour edge to edge
                                              (iOS App Store / Xcode single size; AppGallery 1024)
    outdir/mobile/<name>-fullbleed-512.png    Google Play store listing
    outdir/mobile/<name>-fullbleed-216.png    AppGallery small upload option
    outdir/mobile/foreground-1024.png         transparent, content scaled by --fg-scale
    outdir/mobile/background-1024.png         solid plate colour, no alpha
                                              (Android adaptive icon / HarmonyOS layered-image)

Requires: Python 3, cairosvg (`pip install cairosvg`), Pillow >= 10.
"""
from __future__ import annotations
import argparse, io, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import cairosvg
    from PIL import Image
except ImportError as e:  # pragma: no cover
    sys.exit(f"missing dependency: {e.name}. pip install cairosvg pillow")

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
PNG_SIZES = [16, 24, 32, 48, 64, 128, 256, 512, 1024]
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]
ICNS_SIZES = [16, 32, 64, 128, 256, 512, 1024]


def render(svg: bytes, size: int) -> Image.Image:
    png = cairosvg.svg2png(bytestring=svg, output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def strip_plate(svg: bytes) -> tuple[bytes, str]:
    """Remove plate elements; return (svg without plate, plate fill colour)."""
    root = ET.fromstring(svg)
    colour = None
    for parent in root.iter():
        for child in list(parent):
            role = child.get("data-role", "")
            if role == "plate":
                colour = colour or child.get("fill")
                parent.remove(child)
            elif role == "plate-edge":
                parent.remove(child)
    if not colour:
        sys.exit('--mobile needs an element with data-role="plate" and a fill colour')
    return ET.tostring(root), colour


def scaled(svg: bytes, scale: float) -> bytes:
    root = ET.fromstring(svg)
    vb = [float(v) for v in re.split(r"[ ,]+", root.get("viewBox", "0 0 1024 1024").strip())]
    cx, cy = vb[0] + vb[2] / 2, vb[1] + vb[3] / 2
    g = ET.Element(f"{{{SVG_NS}}}g", {"transform": f"translate({cx} {cy}) scale({scale}) translate({-cx} {-cy})"})
    for child in list(root):
        if child.tag != f"{{{SVG_NS}}}defs":
            root.remove(child)
            g.append(child)
    root.append(g)
    return ET.tostring(root)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--name", default="app")
    ap.add_argument("--mobile", action="store_true", help="also export full-bleed and layered mobile assets")
    ap.add_argument("--fg-scale", type=float, default=0.78,
                    help="foreground scale for Android/HarmonyOS layers (keeps art inside the ~66%% safe circle)")
    a = ap.parse_args()
    svg = a.svg.read_bytes()
    out = a.outdir
    (out / "png").mkdir(parents=True, exist_ok=True)

    imgs = {s: render(svg, s) for s in PNG_SIZES}
    for s, im in imgs.items():
        im.save(out / "png" / f"{a.name}-{s}.png")

    ico = out / f"{a.name}.ico"
    imgs[256].save(ico, format="ICO", sizes=[(s, s) for s in ICO_SIZES],
                   append_images=[imgs[s] for s in ICO_SIZES if s != 256])
    icns = out / f"{a.name}.icns"
    imgs[1024].save(icns, format="ICNS", append_images=[imgs[s] for s in ICNS_SIZES if s != 1024])

    print(f"png  {out / 'png'}  {', '.join(map(str, PNG_SIZES))}")
    print(f"ico  {ico}  frames={sorted(Image.open(ico).info.get('sizes', []))}")
    print(f"icns {icns}  sizes={sorted(Image.open(icns).info.get('sizes', []))}")

    if a.mobile:
        m = out / "mobile"; m.mkdir(exist_ok=True)
        bare, colour = strip_plate(svg)
        bg = Image.new("RGBA", (1024, 1024), colour)
        full = Image.alpha_composite(bg, render(bare, 1024)).convert("RGB")
        for s in (1024, 512, 216):
            (full if s == 1024 else full.resize((s, s), Image.LANCZOS)).save(m / f"{a.name}-fullbleed-{s}.png")
        render(scaled(bare, a.fg_scale), 1024).save(m / "foreground-1024.png")
        bg.convert("RGB").save(m / "background-1024.png")
        print(f"mobile {m}  plate={colour}  fg-scale={a.fg_scale}")


if __name__ == "__main__":
    main()
