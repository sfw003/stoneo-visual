#!/usr/bin/env python3
"""Render a comparison board from ONE structured JSON file. No hand-edited HTML.

Usage:
    python3 render_board.py board.json compare.png

board.json - illustration / avatar board (assets/templates/compare-board.html, 1500px wide):
    {"board": "compare", "usage": "avatar" | "illustration",
     "title": "冬季限定头像 · 三个方案",
     "options": [{"img": "gen/a.jpg", "name": "A · 毛线帽 + 围巾",
                  "elements": "...", "pros": "...", "cost": "...", "rec": false}, ...]}
board.json - icon board (assets/templates/icon-board.html, 1080px wide):
    {"board": "icon", "view": "overview" | "detail" | "small", "title": "...", "appName": "文件搜索",
     "options": [{"icon": "export/1/png/app", "name": "...", "elements": "...", "pros": "...",
                  "cost": "...", "rec": true, "sketch": "concepts/1.jpg"}],
     "large": {...same fields as an option, no rec...},          # view "small" only, required
     "before": {"old": "prefix", "new": "prefix", "oldLabel": "...", "newLabel": "..."}}  # optional

Rules enforced (exit 1 with a message otherwise):
    2-4 options, exactly ONE "rec": true; name / elements / pros / cost non-empty, one sentence
    each (no "。" inside or at the end, <= 60 characters); every image / icon PNG exists;
    paths are relative to board.json; subtitle and the avatar name label are fixed by the
    template (not configurable); icon boards must stay <= 3000px tall (split views otherwise).

Internal helper render_html() is also used by render_labels.py.
"""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

SKILL = Path(__file__).resolve().parent.parent
TPL = {"compare": SKILL / "assets/templates/compare-board.html", "icon": SKILL / "assets/templates/icon-board.html"}
WIDTH = {"compare": 1500, "icon": 1080}
SUBTITLE = {
    "compare": "每行：原图 → 用途演示 → 一句讲解。推荐的那一行带橙色框和「推荐」。",
    "overview": "每个方案：成品、实际尺寸、讲解。推荐的那个带橙色框。",
    "detail": "每个方案：放进 Windows 任务栏和 macOS Dock，浅色、深色桌面各一次。",
    "small": "大图负责 48px 以上；32px 及以下换一张专门简化过的小图。图标文件里两张都有，系统按尺寸自动挑。",
}
ICON_SIZES = (16, 24, 32, 48, 64, 128, 1024)
PAPER = (247, 242, 234)
MAX_ICON_HEIGHT = 3000


class BoardError(Exception):
    pass


def chrome() -> str:
    for c in ("google-chrome", "chromium", "chromium-browser"):
        if shutil.which(c):
            return c
    raise BoardError("no google-chrome / chromium found")


def render_html(html: Path, out: Path, width: int, height: int = 4000, scale: float = 1, trim: bool = True) -> tuple[int, int]:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "shot.png"
        subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                        f"--force-device-scale-factor={scale}", "--virtual-time-budget=3000",
                        f"--window-size={width},{height}", f"--screenshot={tmp}", html.resolve().as_uri()],
                       check=True, capture_output=True)
        im = Image.open(tmp).convert("RGB")
    if trim:
        px = im.load(); w, h = im.size; last = 0
        for y in range(h - 1, -1, -1):
            if any(sum(abs(px[x, y][i] - PAPER[i]) for i in range(3)) > 12 for x in range(0, w, 3)):
                last = y; break
        im = im.crop((0, 0, w, min(h, last + int(46 * scale))))
    im.save(out)
    return im.size


def sentence(where: str, v) -> str:
    if not isinstance(v, str) or not v.strip():
        raise BoardError(f"{where}: must be a non-empty string")
    v = v.strip()
    if v.endswith("。") or "。" in v:
        raise BoardError(f'{where}: one sentence, no "。" (the template adds it): {v!r}')
    if len(v) > 60:
        raise BoardError(f"{where}: {len(v)} characters, keep it <= 60 (plain words, one sentence)")
    return v


def file_uri(base: Path, rel: str, where: str) -> str:
    p = (base / rel).resolve()
    if not p.is_file():
        raise BoardError(f"{where}: file not found: {p}")
    return p.as_uri()


def prefix_uri(base: Path, rel: str, where: str, sizes=ICON_SIZES) -> str:
    p = (base / rel).resolve()
    for s in sizes:
        if not Path(f"{p}-{s}.png").is_file():
            raise BoardError(f"{where}: missing {p}-{s}.png (run export_icon.py first)")
    return p.as_uri()


def validate(spec: dict, base: Path) -> tuple[str, dict]:
    kind = spec.get("board")
    if kind not in TPL:
        raise BoardError('"board" must be "compare" or "icon"')
    allowed = {"board", "usage", "view", "title", "options", "appName", "large", "before", "_note"}
    extra = set(spec) - allowed
    if extra:
        raise BoardError(f"unknown keys {sorted(extra)} (subtitle / label are fixed by the template)")
    title = spec.get("title")
    if not isinstance(title, str) or not (4 <= len(title) <= 30):
        raise BoardError("title: 4-30 characters")
    opts = spec.get("options")
    if not isinstance(opts, list) or not 2 <= len(opts) <= 4:
        raise BoardError("options: 2-4 options (default 3)")
    if sum(1 for o in opts if o.get("rec") is True) != 1:
        raise BoardError('exactly one option must have "rec": true')
    out = {"title": title}
    clean = []
    for i, o in enumerate(opts):
        w = f"options[{i}]"
        c = {k: sentence(f"{w}.{k}", o.get(k)) for k in ("elements", "pros", "cost")}
        if not isinstance(o.get("name"), str) or not o["name"].strip():
            raise BoardError(f"{w}.name: required")
        c["name"] = o["name"].strip(); c["rec"] = o.get("rec") is True
        if kind == "compare":
            c["img"] = file_uri(base, o.get("img", ""), f"{w}.img")
        else:
            c["icon"] = prefix_uri(base, o.get("icon", ""), f"{w}.icon")
            if o.get("sketch"):
                c["sketch"] = file_uri(base, o["sketch"], f"{w}.sketch")
        clean.append(c)
    out["options"] = clean
    if kind == "compare":
        if spec.get("usage") not in ("avatar", "illustration"):
            raise BoardError('usage must be "avatar" or "illustration"')
        out.update(usage=spec["usage"], label="昵称", subtitle=SUBTITLE["compare"])
    else:
        view = spec.get("view")
        if view not in ("overview", "detail", "small"):
            raise BoardError('view must be "overview", "detail" or "small"')
        out.update(view=view, subtitle=SUBTITLE[view], appName=spec.get("appName", "应用"))
        if view == "small":
            L = spec.get("large")
            if not isinstance(L, dict):
                raise BoardError('view "small" needs "large"')
            out["large"] = {k: sentence(f"large.{k}", L.get(k)) for k in ("elements", "pros", "cost")}
            out["large"].update(name=L.get("name", "大图"), icon=prefix_uri(base, L.get("icon", ""), "large.icon"))
            if "before" in spec:
                B = spec["before"]
                out["before"] = {"old": prefix_uri(base, B["old"], "before.old", (16, 32)),
                                 "new": prefix_uri(base, B["new"], "before.new", (16, 32)),
                                 "oldLabel": B.get("oldLabel", "旧版"), "newLabel": B.get("newLabel", "新版")}
    return kind, out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("board", type=Path, help="board.json")
    ap.add_argument("out", type=Path, help="output PNG")
    a = ap.parse_args()
    try:
        if a.board.suffix.lower() != ".json":
            raise BoardError("input must be a board .json file (hand-edited HTML is no longer accepted)")
        spec = json.loads(a.board.read_text(encoding="utf-8"))
        kind, data = validate(spec, a.board.resolve().parent)
        tpl = TPL[kind].read_text(encoding="utf-8")
        html, n = re.subn(r"/\*@BOARD\*/.*?/\*@END\*/", lambda _: json.dumps(data, ensure_ascii=False), tpl, flags=re.S)
        if n != 1:
            raise BoardError(f"template {TPL[kind].name} is missing the /*@BOARD*/ marker")
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "board.html"; page.write_text(html, encoding="utf-8")
            w, h = render_html(page, a.out, WIDTH[kind])
        if kind == "icon" and h > MAX_ICON_HEIGHT:
            raise BoardError(f"board is {h}px tall (> {MAX_ICON_HEIGHT}); split it into overview + detail")
    except (BoardError, json.JSONDecodeError, OSError, subprocess.CalledProcessError, KeyError) as e:
        sys.exit(f"render_board: {e}")
    print(f"{a.out} {w}x{h}")


if __name__ == "__main__":
    main()
