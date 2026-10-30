#!/usr/bin/env python3
"""Render an HTML page (compare board / label overlay) to PNG with headless Chrome.

Usage:
    python3 render_board.py board.html out.png [--width 1500] [--scale 1] [--no-trim]

Renders into a tall window, then trims the empty paper-colored bottom
(background #F7F2EA) and keeps a 46px bottom margin. Use --no-trim for
fixed-size pages such as label-overlay.html (pass --width and --height).
"""
from __future__ import annotations
import argparse, shutil, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

PAPER = (247, 242, 234)


def chrome() -> str:
    for c in ("google-chrome", "chromium", "chromium-browser"):
        if shutil.which(c):
            return c
    sys.exit("No Chrome/Chromium found")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--width", type=int, default=1500)
    ap.add_argument("--height", type=int, default=4000)
    ap.add_argument("--scale", type=float, default=1)
    ap.add_argument("--no-trim", action="store_true")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "shot.png"
        subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                        f"--force-device-scale-factor={a.scale}", "--virtual-time-budget=3000",
                        f"--window-size={a.width},{a.height}", f"--screenshot={tmp}",
                        a.html.resolve().as_uri()], check=True, capture_output=True)
        im = Image.open(tmp).convert("RGB")
    if not a.no_trim:
        px = im.load(); w, h = im.size; last = 0
        for y in range(h - 1, -1, -1):
            if any(sum(abs(px[x, y][i] - PAPER[i]) for i in range(3)) > 12 for x in range(0, w, 3)):
                last = y; break
        im = im.crop((0, 0, w, min(h, last + int(46 * a.scale))))
    im.save(a.out)
    print(f"{a.out} {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
