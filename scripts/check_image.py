#!/usr/bin/env python3
"""Automatic acceptance checks for a generated stoneo-visual image.

Usage:
    python3 check_image.py IMAGE --mode A [--aspect 4:3]   # explainer (paper background)
    python3 check_image.py IMAGE --mode B-src               # green-screen source, before cutout.py
    python3 check_image.py IMAGE --mode B                   # transparent PNG after cutout.py
    python3 check_image.py IMAGE --mode avatar              # square avatar
    add --previews DIR to write check images (B: on dark / paper; avatar: circle 64/32)
    add --json to print machine-readable results

Exit code 0 = every automatic check passed (warnings allowed), 1 = at least one
FAIL, 2 = bad input. The script always ends with the checklist of things only a
human can judge (fingers, expression, text in the image ...). Those are not
optional: look at the image and tick them before delivering.

Thresholds were calibrated on the skill's own references and demos (all 0%
off-palette) against a known-bad sketch (navy background, 74% off-palette).
"""
from __future__ import annotations
import argparse, colorsys, json, sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("check_image: pip install pillow")

PAPER = (247, 242, 234)
DARK = (36, 32, 28)
ASPECTS = {"A": ("4:3", "16:9"), "B-src": ("1:1",), "B": ("1:1",), "avatar": ("1:1",)}
RATIO = {"1:1": 1.0, "4:3": 4 / 3, "16:9": 16 / 9}
MIN_SIDE = {"A": 1024, "B-src": 1024, "B": 512, "avatar": 1024}
# off-palette: saturated colour outside the apricot / khaki hue band
OFF_FAIL, OFF_WARN = 0.005, 0.001
# apricot is a local accent. A / avatar: share of the whole picture; B: share of the character only
APRICOT = {"A": (0.20, 0.30), "avatar": (0.20, 0.30), "B": (0.35, 0.60), "B-src": (0.35, 0.60)}  # (warn, fail)
SEMI_WARN, SEMI_FAIL = 0.20, 0.40  # good cutouts ~14% (edges + halftone); the 220-threshold bug ~99%

MANUAL = {
    "common": [
        "同一只：大钝吻（杏色网点）+ 一只半眯斜眼 + 两只小圆耳，和母版一眼是同一只",
        "比例：头约占身高 45%，梨形身体，短腿，没有尾巴",
        "手：圆头短手，没有手指、拇指、爪趾线",
        "图里没有任何字、数字、符号、logo（屏幕、图表、卡片、蛋糕上也没有）",
        "表情是要的那个（专注不瞪人；得意只有吻部里那一张嘴）",
        "没有多余小杂物、没有第二种大面积颜色",
    ],
    "A": ["一个焦点动作，最多三块区域；留出了放标签的空白纸面"],
    "B": ["在深色和纸色预览上看边缘：没有绿边、白边、缺块"],
    "B-src": ["绿幕四角一致、角色没贴边"],
    "avatar": ["64px 圆形预览里认得出斜眼", "节日元素去掉后和主形象一样"],
}


def pixels(im):
    f = getattr(im, "get_flattened_data", None)
    return f() if f else im.getdata()


def corner_patches(im, k=24):
    w, h = im.size
    boxes = [(0, 0), (w - k, 0), (0, h - k), (w - k, h - k), (w // 2 - k // 2, 0), (w // 2 - k // 2, h - k),
             (0, h // 2 - k // 2), (w - k, h // 2 - k // 2)]
    out = []
    for x, y in boxes:
        p = im.crop((x, y, x + k, y + k)).convert("RGB").resize((1, 1), Image.BOX).getpixel((0, 0))
        out.append(p)
    return out


def dist(a, b):
    return max(abs(a[i] - b[i]) for i in range(3))


def palette(im, exclude_key=False):
    t = im.convert("RGBA").copy(); t.thumbnail((400, 400))
    n = off = apr = 0
    for r, g, b, a in pixels(t):
        if a < 128 or (exclude_key and g > r + 40 and g > b + 40):
            continue
        n += 1
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > 0.30 and v > 0.30:
            if 10 / 360 <= h <= 48 / 360:
                apr += 1
            else:
                off += 1
    return (off / n, apr / n) if n else (0.0, 0.0)


def ink_outside(im):
    im = im.convert("RGB").resize((1024, 1024), Image.LANCZOS); px = im.load()
    o1 = o5 = 0; c = 511.5
    for y in range(0, 1024, 2):
        for x in range(0, 1024, 2):
            if sum(px[x, y]) < 300:
                d = ((x - c) ** 2 + (y - c) ** 2) ** 0.5
                o1 += d > 512; o5 += d > 486
    return o1, o5


def check(path: Path, mode: str, aspect: str | None = None, previews: Path | None = None) -> dict:
    res = {"image": str(path), "mode": mode, "checks": []}
    def add(name, ok, detail, level="FAIL"):
        res["checks"].append({"check": name, "result": "PASS" if ok else level, "detail": detail})
    im = Image.open(path); im.load()
    w, h = im.size
    allowed = ASPECTS[mode]
    if aspect and aspect not in allowed:
        raise ValueError(f"mode {mode} only allows aspect {allowed}")
    target = aspect or min(allowed, key=lambda a: abs(RATIO[a] - w / h))
    add("aspect", abs(w / h - RATIO[target]) / RATIO[target] < 0.03, f"{w}x{h}, expected {target}")
    add("size", min(w, h) >= MIN_SIDE[mode] * (0.75 if mode == "A" else 1), f"short side {min(w, h)}px (want >= {MIN_SIDE[mode] if mode != 'A' else int(MIN_SIDE[mode]*0.75)})")

    if mode == "B":
        add("rgba", im.mode in ("RGBA", "LA") or "transparency" in im.info, f"mode {im.mode}")
        rgba = im.convert("RGBA")
        corners = [rgba.getpixel(p)[3] for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
        add("corners transparent", max(corners) == 0, f"corner alpha {corners}")
        t = rgba.copy(); t.thumbnail((512, 512))
        vis = semi = green = 0
        for r, g, b, a in pixels(t):
            if a == 0: continue
            vis += 1
            if 16 < a < 250: semi += 1
            if a > 32 and g > max(r, b) + 30: green += 1
        add("green spill", vis and green / vis < 0.002, f"{green}/{vis} visible px are green-tinted")
        sr = semi / max(vis, 1)
        if sr >= SEMI_FAIL:
            add("body opaque", False, f"{sr:.1%} of visible px semi-transparent - body see-through (did you pass --opaque-threshold 220?)")
        else:
            add("body opaque", sr < SEMI_WARN, f"{sr:.1%} of visible px semi-transparent", level="WARN")
        off, apr = palette(rgba)
    elif mode == "B-src":
        cs = corner_patches(im)
        key = cs[0]
        add("green screen", key[1] > key[0] + 40 and key[1] > key[2] + 40, f"corner colour {key}")
        add("uniform key", max(dist(c, key) for c in cs) < 30, f"border patches {cs}")
        off, apr = palette(im, exclude_key=True)
    else:
        cs = corner_patches(im)
        add("paper background", max(dist(c, PAPER) for c in cs) < 32, f"border patches vs paper {PAPER}: max diff {max(dist(c, PAPER) for c in cs)}" + (" - avatar must be full-bleed (no disc / vignette)" if mode == "avatar" else ""))
        off, apr = palette(im)
    if off >= OFF_FAIL:
        add("palette", False, f"{off:.2%} saturated off-palette pixels (green / blue / pink / red ...)")
    else:
        add("palette", off < OFF_WARN, f"{off:.2%} saturated off-palette pixels", level="WARN")
    aw, af = APRICOT[mode]
    what = "of the character" if mode.startswith("B") else "of the picture"
    if apr >= af:
        add("apricot is local", False, f"apricot covers {apr:.1%} {what} (fail >= {af:.0%}) - big apricot block / fill")
    else:
        add("apricot is local", apr < aw, f"apricot covers {apr:.1%} {what} (warn >= {aw:.0%})", level="WARN")

    if mode == "avatar":
        o1, o5 = ink_outside(im)
        add("circle safe", o1 == 0 and o5 == 0, f"ink outside circle {o1}, outside 5% inset {o5}")
    if previews:
        previews.mkdir(parents=True, exist_ok=True)
        stem = path.stem
        if mode == "B":
            for nm, col in (("on-dark", DARK), ("on-paper", PAPER)):
                bg = Image.new("RGBA", im.size, col + (255,)); bg.alpha_composite(im.convert("RGBA"))
                bg.convert("RGB").save(previews / f"{stem}-{nm}.png")
        if mode == "avatar":
            sq = im.convert("RGB").resize((256, 256), Image.LANCZOS)
            m = Image.new("L", (256, 256), 0); ImageDraw.Draw(m).ellipse((0, 0, 255, 255), fill=255)
            sheet = Image.new("RGB", (256 + 16 + 128 + 16 + 64, 256), (255, 255, 255))
            for i, (s, z) in enumerate(((64, 256), (32, 128))):
                c = Image.new("RGB", (256, 256), (255, 255, 255)); c.paste(sq, (0, 0), m)
                small = c.resize((s, s), Image.LANCZOS)
                sheet.paste(small.resize((z, z), Image.NEAREST), (0 if i == 0 else 272, 0 if i == 0 else 64))
            sheet.save(previews / f"{stem}-check.png")
    res["manual"] = MANUAL["common"] + MANUAL.get(mode, [])
    res["ok"] = all(c["result"] != "FAIL" for c in res["checks"])
    return res


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", type=Path)
    ap.add_argument("--mode", required=True, choices=list(ASPECTS))
    ap.add_argument("--aspect", choices=["1:1", "4:3", "16:9"])
    ap.add_argument("--previews", type=Path)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.image.is_file():
        print(f"check_image: no such file {a.image}", file=sys.stderr); sys.exit(2)
    try:
        res = check(a.image, a.mode, a.aspect, a.previews)
    except (ValueError, OSError) as e:
        print(f"check_image: {e}", file=sys.stderr); sys.exit(2)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for c in res["checks"]:
            print(f"{c['result']:<5} {c['check']:<20} {c['detail']}")
        print("人眼必查（脚本查不了，逐条看图确认）：")
        for m in res["manual"]:
            print(f"  [ ] {m}")
        print("RESULT", "PASS" if res["ok"] else "FAIL")
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main()
