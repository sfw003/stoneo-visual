#!/usr/bin/env python3
"""Export a square avatar and check it for circular crops and small sizes.

Usage:
    python3 avatar_preview.py generated.jpg out_dir/ [--name avatar]

Writes:
    <name>.png             1024x1024 square (paper background kept)
    <name>-circle-512.png  circular crop, transparent corners
    <name>-circle-64.png   64px circular preview (real pixels)
    <name>-circle-32.png   32px circular preview (real pixels)
    <name>-check.png       64/32px previews enlarged 4x (nearest) for eyeballing
Prints how many ink pixels fall outside the inscribed circle and outside a 5% inset
circle. Both must be 0, otherwise ears / hats get clipped by a round avatar frame.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw


def circle(im: Image.Image, size: int) -> Image.Image:
    s = size * 4
    big = im.resize((s, s), Image.LANCZOS)
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.paste(big, (0, 0), mask)
    return out.resize((size, size), Image.LANCZOS)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--name", default="avatar")
    ap.add_argument("--ink", type=int, default=300, help="R+G+B below this counts as ink")
    a = ap.parse_args()
    a.outdir.mkdir(parents=True, exist_ok=True)
    im = Image.open(a.input).convert("RGB").resize((1024, 1024), Image.LANCZOS)
    im.save(a.outdir / f"{a.name}.png")
    for s in (512, 64, 32):
        circle(im, s).save(a.outdir / f"{a.name}-circle-{s}.png")
    px = im.load()
    out1 = out5 = 0
    c = 511.5
    for y in range(0, 1024, 2):
        for x in range(0, 1024, 2):
            r, g, b = px[x, y]
            if r + g + b < a.ink:
                d = ((x - c) ** 2 + (y - c) ** 2) ** 0.5
                out1 += d > 512
                out5 += d > 486
    sheet = Image.new("RGB", (256 + 16 + 128, 256), (255, 255, 255))
    for i, (s, z) in enumerate(((64, 256), (32, 128))):
        t = circle(im, s)
        bg = Image.new("RGBA", t.size, (255, 255, 255, 255))
        bg.alpha_composite(t)
        sheet.paste(bg.resize((z, z), Image.NEAREST), (0 if i == 0 else 272, 0 if i == 0 else 64))
    sheet.save(a.outdir / f"{a.name}-check.png")
    print(f"ink outside circle: {out1}  ink outside 5% inset: {out5}  (both should be 0)")


if __name__ == "__main__":
    main()
