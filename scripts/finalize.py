#!/usr/bin/env python3
"""Package the option the user picked. One fixed layout for every agent.

Usage:
    python3 finalize.py image --mode A|B|avatar SRC --out OUTROOT --name SLUG [--aspect 4:3] [--force]
    python3 finalize.py icon  --large big.svg [--small small.svg] --out OUTROOT --name SLUG [--file-name app] [--force]

SLUG: lowercase letters, digits and '-' (e.g. winter-avatar, search-tool-icons).
Writes OUTROOT/SLUG/ and OUTROOT/SLUG.zip (the zip contains the SLUG/ folder).

image
    A       SRC = the labelled explainer (render_labels.py output) or the raw image
            SLUG/SLUG.png            1600px wide, original 4:3 / 16:9 aspect
            SLUG/SLUG-1024.png       1024x1024, letterboxed on paper #F7F2EA
    B       SRC = transparent PNG from cutout.py
            SLUG/SLUG-1024.png       1024x1024 RGBA, trimmed and centred, 64px margin
            SLUG/preview/SLUG-on-dark.png, SLUG-on-paper.png
    avatar  SRC = square avatar
            SLUG/SLUG-1024.png       1024x1024, full-bleed paper
            SLUG/preview/SLUG-circle-{512,64,32}.png, SLUG-check.png
icon
    runs check_icon_svg.py on both SVGs, then export_icon.py with --mobile (and --small)
            SLUG/<file-name>.ico, .icns, png/, mobile/, svg/icon-large.svg, svg/icon-small.svg
Always: SLUG/manifest.json (inputs, sha256, checks). The source image / SVG must
pass check_image.py / check_icon_svg.py first; --force packages anyway and records
the failures in the manifest (only when the user accepted the known issue).
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, sys, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from PIL import Image, ImageDraw  # noqa: E402
import check_image, check_icon_svg, export_icon  # noqa: E402

PAPER = (247, 242, 234)
SLUG = re.compile(r"[a-z0-9][a-z0-9-]*")
ZIP_DATE = (2026, 1, 1, 0, 0, 0)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_zip(folder: Path) -> Path:
    zp = folder.parent / f"{folder.name}.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        root = zipfile.ZipInfo(f"{folder.name}/", ZIP_DATE); root.external_attr = 0o40755 << 16
        z.writestr(root, b"")
        for p in sorted(folder.rglob("*")):
            arc = f"{folder.name}/{p.relative_to(folder).as_posix()}" + ("/" if p.is_dir() else "")
            info = zipfile.ZipInfo(arc, ZIP_DATE)
            if p.is_dir():
                info.external_attr = 0o40755 << 16; z.writestr(info, b"")
            else:
                info.external_attr = 0o644 << 16; info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, p.read_bytes())
    return zp


def circle(im, size):
    s = size * 4
    big = im.resize((s, s), Image.LANCZOS)
    m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0)); out.paste(big, (0, 0), m)
    return out.resize((size, size), Image.LANCZOS)


def prepare(out_root: Path, slug: str) -> Path:
    if not SLUG.fullmatch(slug):
        raise ValueError(f"--name must be lowercase letters, digits and '-', got {slug!r}")
    d = out_root / slug
    if d.exists():
        if not (d / "manifest.json").is_file():
            raise ValueError(f"{d} exists and was not made by finalize.py - pick another --name or --out")
        shutil.rmtree(d)
    d.mkdir(parents=True)
    return d


def finalize_image(mode, src: Path, out_root: Path, slug: str, aspect, force) -> Path:
    res = check_image.check(src, mode, aspect)
    fails = [c for c in res["checks"] if c["result"] == "FAIL"]
    if fails and not force:
        raise ValueError("source fails check_image: " + "; ".join(f"{c['check']}: {c['detail']}" for c in fails))
    d = prepare(out_root, slug)
    im = Image.open(src)
    files = []
    if mode == "A":
        rgb = im.convert("RGB")
        w = 1600; h = round(rgb.height * w / rgb.width)
        big = rgb.resize((w, h), Image.LANCZOS); big.save(d / f"{slug}.png"); files.append(f"{slug}.png")
        sq = Image.new("RGB", (1024, 1024), PAPER)
        t = rgb.copy(); t.thumbnail((1024, 1024), Image.LANCZOS)
        sq.paste(t, ((1024 - t.width) // 2, (1024 - t.height) // 2)); sq.save(d / f"{slug}-1024.png")
    elif mode == "B":
        rgba = im.convert("RGBA")
        bbox = rgba.getchannel("A").getbbox()
        if not bbox:
            raise ValueError("B: image is fully transparent")
        t = rgba.crop(bbox); t.thumbnail((1024 - 128, 1024 - 128), Image.LANCZOS)
        sq = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        sq.alpha_composite(t, ((1024 - t.width) // 2, (1024 - t.height) // 2)); sq.save(d / f"{slug}-1024.png")
        (d / "preview").mkdir()
        for nm, col in (("on-dark", (36, 32, 28)), ("on-paper", PAPER)):
            bg = Image.new("RGBA", sq.size, col + (255,)); bg.alpha_composite(sq)
            bg.convert("RGB").save(d / "preview" / f"{slug}-{nm}.png")
    else:
        sq = im.convert("RGB").resize((1024, 1024), Image.LANCZOS); sq.save(d / f"{slug}-1024.png")
        (d / "preview").mkdir()
        for s in (512, 64, 32):
            circle(sq, s).save(d / "preview" / f"{slug}-circle-{s}.png")
        check_image.check(d / f"{slug}-1024.png", "avatar", None, d / "preview")
        (d / "preview" / f"{slug}-1024-check.png").rename(d / "preview" / f"{slug}-check.png")
    manifest = {"kind": "image", "mode": mode, "slug": slug, "source": str(src.resolve()), "source_sha256": sha(src),
                "checks": res["checks"], "forced": bool(fails), "manual_checklist": res["manual"],
                "files": {str(p.relative_to(d)): p.stat().st_size for p in sorted(d.rglob("*")) if p.is_file()}}
    (d / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return d


def finalize_icon(large: Path, small, out_root: Path, slug: str, file_name: str, force) -> Path:
    results = [check_icon_svg.lint(large)] + ([check_icon_svg.lint(small)] if small else [])
    if results[0]["grid"] != "large":
        raise ValueError("--large must use the 1024 grid")
    if small and results[1]["grid"] != "small":
        raise ValueError("--small must use the 32 grid")
    errs = [f"{Path(r['file']).name}: {e}" for r in results for e in r["errors"]]
    if errs and not force:
        raise ValueError("SVG fails check_icon_svg: " + "; ".join(errs))
    d = prepare(out_root, slug)
    export_icon.export(large, d, file_name, small, 32, True, 0.78, log=lambda *_: None)
    (d / "svg").mkdir()
    shutil.copyfile(large, d / "svg" / "icon-large.svg")
    if small:
        shutil.copyfile(small, d / "svg" / "icon-small.svg")
    manifest = {"kind": "icon", "slug": slug, "file_name": file_name,
                "large": str(large.resolve()), "large_sha256": sha(large),
                "small": str(small.resolve()) if small else None, "small_sha256": sha(small) if small else None,
                "small_max": 32 if small else None, "lint": results, "forced": bool(errs),
                "files": {str(p.relative_to(d)): p.stat().st_size for p in sorted(d.rglob("*")) if p.is_file()}}
    (d / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="kind", required=True)
    a1 = sub.add_parser("image", help="explainer / transparent illustration / avatar")
    a1.add_argument("src", type=Path)
    a1.add_argument("--mode", required=True, choices=["A", "B", "avatar"])
    a1.add_argument("--aspect", choices=["4:3", "16:9"])
    a2 = sub.add_parser("icon", help="app icon / logo")
    a2.add_argument("--large", required=True, type=Path)
    a2.add_argument("--small", type=Path)
    a2.add_argument("--file-name", default="app")
    for p in (a1, a2):
        p.add_argument("--out", required=True, type=Path)
        p.add_argument("--name", required=True, help="slug: lowercase letters, digits, '-'")
        p.add_argument("--force", action="store_true", help="package even if checks fail (recorded in manifest)")
    a = ap.parse_args()
    try:
        if a.kind == "image":
            if not a.src.is_file():
                raise ValueError(f"no such file {a.src}")
            d = finalize_image(a.mode, a.src, a.out, a.name, a.aspect, a.force)
        else:
            for p in (a.large, a.small):
                if p is not None and not p.is_file():
                    raise ValueError(f"no such file {p}")
            d = finalize_icon(a.large, a.small, a.out, a.name, a.file_name, a.force)
    except ValueError as e:
        sys.exit(f"finalize: {e}")
    zp = write_zip(d)
    print(f"folder {d}")
    print(f"zip    {zp}")
    for k in json.loads((d / "manifest.json").read_text())["files"]:
        print(f"  {k}")


if __name__ == "__main__":
    main()
