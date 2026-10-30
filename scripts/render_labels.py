#!/usr/bin/env python3
"""Add the title and tags to an explainer (mode A) with fixed fonts, sizes and colours.

Usage:
    python3 render_labels.py labels.json out.png

labels.json:
    {"image": "gen/explainer.jpg",          # relative to labels.json
     "aspect": "4:3" | "16:9",              # page = 1600x1200 or 1600x900
     "title": "一句话标题",                  # 4-16 characters, optional only if the user said no title
     "tags": [{"text": "标签一", "x": 12, "y": 70}, ...]}   # 2-6 tags, 2-8 characters,
                                                           # x 0-85 / y 0-92 (% of the page, top-left of the tag)

Fonts / sizes / colours live in assets/templates/label-overlay.html (:root variables):
Noto Sans CJK SC, title 56px bold, tags 34px semibold, ink #2B2520 text, apricot dot,
chip #FBF8F2 with a 2px ink border. They are not configurable per job.
Output is always rendered at device scale 1 (1600px wide); finalize.py makes the 1024 square.
"""
from __future__ import annotations
import argparse, json, re, sys, tempfile
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_board import render_html, BoardError  # noqa: E402

TPL = Path(__file__).resolve().parent.parent / "assets/templates/label-overlay.html"
PAGES = {"4:3": (1600, 1200), "16:9": (1600, 900)}


def validate(spec: dict, base: Path) -> dict:
    extra = set(spec) - {"image", "aspect", "title", "tags", "_note"}
    if extra:
        raise BoardError(f"unknown keys {sorted(extra)} (font, size and colour are fixed)")
    if spec.get("aspect") not in PAGES:
        raise BoardError('aspect must be "4:3" or "16:9"')
    w, h = PAGES[spec["aspect"]]
    img = (base / spec.get("image", "")).resolve()
    if not img.is_file():
        raise BoardError(f"image not found: {img}")
    iw, ih = Image.open(img).size
    if abs(iw / ih - w / h) / (w / h) > 0.03:
        raise BoardError(f"image is {iw}x{ih}, does not match aspect {spec['aspect']}")
    title = spec.get("title")
    if title is not None and not (isinstance(title, str) and 4 <= len(title) <= 16):
        raise BoardError("title: 4-16 characters")
    tags = spec.get("tags")
    if not isinstance(tags, list) or not 2 <= len(tags) <= 6:
        raise BoardError("tags: 2-6 tags")
    clean = []
    for i, t in enumerate(tags):
        txt = t.get("text") if isinstance(t, dict) else None
        if not isinstance(txt, str) or not 2 <= len(txt) <= 8:
            raise BoardError(f"tags[{i}].text: 2-8 characters")
        x, y = t.get("x"), t.get("y")
        if not all(isinstance(v, (int, float)) for v in (x, y)) or not (0 <= x <= 85 and 0 <= y <= 92):
            raise BoardError(f"tags[{i}]: x must be 0-85 and y 0-92 (percent)")
        clean.append({"text": txt, "x": x, "y": y})
    return {"width": w, "height": h, "image": img.as_uri(), "title": title, "tags": clean}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("labels", type=Path)
    ap.add_argument("out", type=Path)
    a = ap.parse_args()
    try:
        spec = json.loads(a.labels.read_text(encoding="utf-8"))
        data = validate(spec, a.labels.resolve().parent)
        html, n = re.subn(r"/\*@LABELS\*/.*?/\*@END\*/", lambda _: json.dumps(data, ensure_ascii=False),
                          TPL.read_text(encoding="utf-8"), flags=re.S)
        if n != 1:
            raise BoardError("label-overlay.html is missing the /*@LABELS*/ marker")
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "labels.html"; page.write_text(html, encoding="utf-8")
            size = render_html(page, a.out, data["width"], data["height"], trim=False)
    except (BoardError, json.JSONDecodeError, OSError) as e:
        sys.exit(f"render_labels: {e}")
    print(f"{a.out} {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
