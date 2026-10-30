#!/usr/bin/env python3
"""Export a stoneo icon SVG to every desktop (and optionally mobile) size.

Usage:
    python3 export_icon.py icon.svg outdir/ [--name app] [--small small.svg [--small-max 32]]
                           [--mobile] [--fg-scale 0.78]

Small-size frames (--small): every size <= --small-max (default 32, i.e. 16/24/32)
is rendered from the simplified small SVG instead of the main one. This applies to
the png/ set, every .ico frame and the matching .icns slots (16@2x is a 32px image,
so it uses the small art; 32@2x = 64px uses the main art). Mobile assets always
use the main SVG.

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
        raise ValueError('--mobile needs an element with data-role="plate" and a fill colour')
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


def export(svg_path: Path, out: Path, name: str = "app", small_path: Path | None = None,
           small_max: int = 32, mobile: bool = False, fg_scale: float = 0.78, log=print) -> dict:
    """Export everything; returns {relative path: size} of written files."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        raise ValueError(f"--name must be lowercase letters, digits and '-', got {name!r}")
    if small_max not in PNG_SIZES or small_max > 256:
        raise ValueError(f"--small-max must be one of {[s for s in PNG_SIZES if s <= 256]}")
    if not 0.5 <= fg_scale <= 1.0:
        raise ValueError("--fg-scale must be between 0.5 and 1.0")
    svg = svg_path.read_bytes()
    small = small_path.read_bytes() if small_path else None
    (out / "png").mkdir(parents=True, exist_ok=True)
    src = lambda s: small if small is not None and s <= small_max else svg
    imgs = {s: render(src(s), s) for s in PNG_SIZES}
    for s, im in imgs.items():
        im.save(out / "png" / f"{name}-{s}.png")
    ico = out / f"{name}.ico"
    imgs[256].save(ico, format="ICO", sizes=[(s, s) for s in ICO_SIZES],
                   append_images=[imgs[s] for s in ICO_SIZES if s != 256])
    icns = out / f"{name}.icns"
    imgs[1024].save(icns, format="ICNS", append_images=[imgs[s] for s in ICNS_SIZES if s != 1024])
    log(f"png  {out / 'png'}  {', '.join(map(str, PNG_SIZES))}")
    if small is not None:
        log(f"small frames from {small_path.name}: {[s for s in PNG_SIZES if s <= small_max]}")
    log(f"ico  {ico}  frames={sorted(Image.open(ico).info.get('sizes', []))}")
    log(f"icns {icns}  sizes={sorted(Image.open(icns).info.get('sizes', []))}")
    if mobile:
        m = out / "mobile"; m.mkdir(exist_ok=True)
        bare, colour = strip_plate(svg)
        bg = Image.new("RGBA", (1024, 1024), colour)
        full = Image.alpha_composite(bg, render(bare, 1024)).convert("RGB")
        for s in (1024, 512, 216):
            (full if s == 1024 else full.resize((s, s), Image.LANCZOS)).save(m / f"{name}-fullbleed-{s}.png")
        render(scaled(bare, fg_scale), 1024).save(m / "foreground-1024.png")
        bg.convert("RGB").save(m / "background-1024.png")
        log(f"mobile {m}  plate={colour}  fg-scale={fg_scale}")
    return {str(p.relative_to(out)): p.stat().st_size for p in sorted(out.rglob("*")) if p.is_file()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--name", default="app", help="file prefix, lowercase-dashed (default app)")
    ap.add_argument("--small", type=Path, help="simplified SVG used for sizes <= --small-max")
    ap.add_argument("--small-max", type=int, default=32, help="largest size rendered from --small (default 32)")
    ap.add_argument("--mobile", action="store_true", help="also export full-bleed and layered mobile assets")
    ap.add_argument("--fg-scale", type=float, default=0.78,
                    help="foreground scale for Android/HarmonyOS layers (keeps art inside the ~66%% safe circle)")
    a = ap.parse_args()
    for p in (a.svg, a.small):
        if p is not None and not p.is_file():
            sys.exit(f"export_icon: no such file {p}")
    try:
        export(a.svg, a.outdir, a.name, a.small, a.small_max, a.mobile, a.fg_scale)
    except (ValueError, ET.ParseError) as e:
        sys.exit(f"export_icon: {e}")


if __name__ == "__main__":
    main()
