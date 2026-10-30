#!/usr/bin/env python3
"""Assemble a stoneo-visual GenerateImage job from a small JSON spec.

The A (character) and C (style) blocks, the D (mode) block, every preset slot
sentence, the season presets and the reference-image rules all live in
assets/prompt/parts.json and are copied verbatim. Agents only choose presets or
write the free-text slots; they never edit A / C / D.

Usage:
    python3 build_prompt.py spec.json --out jobdir/      # writes prompt.txt + job.json
    python3 build_prompt.py spec.json                     # prints job.json only
    python3 build_prompt.py --list                        # list every preset key

Spec (JSON):
    {
      "mode": "A" | "B" | "avatar" | "fix",
      "aspect": "4:3" | "16:9",          # mode A only (default 4:3); B / avatar are always 1:1
      "season": "winter" | ...,           # optional, fills expression / accessory / scene
      "view": "<preset>" | {"text": "..."},
      "action": "<preset>" | {"text": "...", "holds": true|false, "object": "cup", "nub_ref": false},
      "expression": "<preset>" | {"text": "..."},
      "outfit": "<preset>" | {"text": "..."},
      "accessory": ["<preset>", ...] | {"text": "..."},
      "scene": "free text",               # props must say blank / no text when they could carry text
      "retry_without_paper": false        # mode B only: drop the paper-background sentence from C
    }
    mode "icon_sketch" (optional concept sketch before hand-writing the SVG, see icon-mode.md):
    {"mode": "icon_sketch", "product": "a fast desktop file-search tool", "concept": "...",
     "plate": "paper" | "ink", "accent": "the inner ears"}
    mode "fix" (local edit of an existing image):
    {"mode": "fix", "base": "/abs/image.jpg", "change": "Remove the extra ...", "nub_ref": false}

Reference rules (from references/reference-images.md, enforced here):
    1st = capybara-master-34view.jpg (always)
    2nd = highest-priority ref among: expression (focus/smug) > view (front/back/side)
          > outfit > action > accessory > avatar composition (avatar mode)
    +   = pose-shrug-nub-hands.jpg whenever something is held (or nub_ref) - never more than 3
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
PARTS = json.loads((SKILL / "assets/prompt/parts.json").read_text(encoding="utf-8"))
REFS = SKILL / "assets/refs"
SLOT_ORDER = [("view", "View"), ("action", "Pose / action"), ("expression", "Expression"),
              ("outfit", "Outfit"), ("accessory", "Accessory"), ("scene", "Scene / props")]
ORDINAL = {2: "second", 3: "third"}
KNOWN_KEYS = {"product", "concept", "plate", "accent", "mode", "aspect", "season", "view", "action", "expression", "outfit", "accessory",
              "scene", "retry_without_paper", "base", "change", "nub_ref", "_note"}
TEXTY = re.compile(r"\b(screen|chart|card|sign|board|book|envelope|packet|cake|poster|label|monitor|whiteboard|note)s?\b", re.I)
BLANK = re.compile(r"\b(blank|no text|no labels|no numbers|no characters|no symbols)\b", re.I)
HANDS = re.compile(r"(?<!no )(?<!NO )\b(hand|hands|paw|paws|finger|fingers|thumb|thumbs|claw|claws)\b")


class SpecError(Exception):
    pass


def preset(slot: str, value):
    """Return (text, meta) for a slot value: preset key or {"text": ...}."""
    table = PARTS["slots"].get(slot, {})
    if isinstance(value, str):
        if slot == "scene":
            return value.strip(), {}
        if value not in table:
            raise SpecError(f'{slot}: unknown preset "{value}". Choose one of: {", ".join(table)} '
                            f'or use {{"text": "..."}}')
        meta = dict(table[value]); return meta.pop("text"), meta
    if isinstance(value, dict) and isinstance(value.get("text"), str) and value["text"].strip():
        meta = {k: v for k, v in value.items() if k != "text"}
        return value["text"].strip(), meta
    raise SpecError(f'{slot}: must be a preset key or {{"text": "..."}}, got {value!r}')


def ensure_period(t: str) -> str:
    return t if t.endswith((".", "!", "?")) else t + "."


def lint(slot: str, text: str) -> None:
    if HANDS.search(text):
        raise SpecError(f'{slot}: write "nub" / "nub arm", never hand / paw / finger ("{HANDS.search(text).group(0)}")')
    if slot in ("scene", "action") and TEXTY.search(text) and not BLANK.search(text):
        raise SpecError(f'{slot}: mentions "{TEXTY.search(text).group(0)}" - add "blank" / "no text" / "no labels, no numbers"')


def build(spec: dict) -> dict:
    unknown = set(spec) - KNOWN_KEYS
    if unknown:
        raise SpecError(f"unknown spec keys: {sorted(unknown)}")
    mode = spec.get("mode")
    if mode == "fix":
        return build_fix(spec)
    if mode == "icon_sketch":
        return build_icon_sketch(spec)
    if mode not in PARTS["D"]:
        raise SpecError('mode must be "A", "B", "avatar", "icon_sketch" or "fix"')
    aspect = spec.get("aspect", "4:3" if mode == "A" else "1:1")
    if mode == "A" and aspect not in ("4:3", "16:9"):
        raise SpecError("mode A aspect must be 4:3 or 16:9")
    if mode != "A" and aspect != "1:1":
        raise SpecError(f"mode {mode} is always 1:1")
    if spec.get("retry_without_paper") and mode != "B":
        raise SpecError("retry_without_paper is only for mode B")

    slots = {k: spec[k] for k, _ in SLOT_ORDER if k in spec}
    season_meta = {}
    if "season" in spec:
        if spec["season"] not in PARTS["seasons"]:
            raise SpecError(f'season must be one of {", ".join(PARTS["seasons"])}')
        season_meta = PARTS["seasons"][spec["season"]]
        for k in ("expression", "accessory", "scene"):
            if k in season_meta and k not in slots:
                slots[k] = {"text": season_meta[k]}
    if mode != "avatar":
        slots.setdefault("view", "default")
    slots.setdefault("expression", "deadpan")

    lines, cands, holds, nub, obj = [], [], False, False, "object"
    for key, label in SLOT_ORDER:
        if key not in slots:
            continue
        v = slots[key]
        if key == "accessory" and isinstance(v, list):
            if not v:
                raise SpecError("accessory list is empty")
            texts = []
            for i, item in enumerate(v):
                t, meta = preset("accessory", item)
                if isinstance(item, dict): lint("accessory", t)
                texts.append(t if i == 0 else t[0].upper() + t[1:])
                if "ref" in meta: cands.append((meta["ref_rank"], meta["ref"]))
            text = " ".join(ensure_period(t) for t in texts)
        else:
            text, meta = preset(key, v)
            if "ref" in meta: cands.append((meta["ref_rank"], meta["ref"]))
            if key == "action":
                if isinstance(v, dict) and "holds" not in meta:
                    raise SpecError('free-text action needs "holds": true|false (is something held / cradled?)')
                if isinstance(v, dict) and meta.get("holds") and not meta.get("object"):
                    raise SpecError('free-text action with "holds": true needs "object": "<the held thing>"')
                holds = bool(meta.get("holds")); nub = bool(meta.get("nub_ref"))
                obj = meta.get("object", "object")
        if key == "scene" or isinstance(v, dict):   # presets in parts.json are already vetted
            lint(key, text)
        lines.append((key, label, ensure_period(text)))
    if season_meta.get("holds") and not holds:
        holds, obj = True, season_meta.get("object", "object")
        hold_slot = "scene"
    else:
        hold_slot = "action"
    if mode == "avatar":
        cands.append((5, PARTS["refs_rules"]["avatar"]))

    refs = [PARTS["refs_rules"]["master"]]
    if cands:
        refs.append(sorted(cands, key=lambda c: c[0])[0][1])
    if holds or nub or spec.get("nub_ref"):
        if PARTS["refs_rules"]["nub"] not in refs:
            refs.append(PARTS["refs_rules"]["nub"])
    refs = refs[:PARTS["refs_rules"]["max"]]
    if holds:
        suffix = PARTS["hold_suffix"].format(object=obj, ordinal=ORDINAL[refs.index(PARTS["refs_rules"]["nub"]) + 1])
        lines = [(k, l, f"{t} {suffix}" if k == hold_slot else t) for k, l, t in lines]
        if hold_slot not in [k for k, _, _ in lines]:
            raise SpecError("season holds an object but has no scene line")

    style = PARTS["C"]
    if spec.get("retry_without_paper"):
        style = style.replace(PARTS["C_paper_sentence"], "")
    prompt = "\n".join([PARTS["A"]] + [f"{l}: {t}" for _, l, t in lines] + [style, PARTS["D"][mode]])
    return {"mode": mode, "aspect_ratio": aspect, "prompt": prompt,
            "reference_image_paths": [str(REFS / r) for r in refs], "holds": holds,
            "season": spec.get("season"), "season_verified": season_meta.get("verified")}


def build_icon_sketch(spec: dict) -> dict:
    for k in ("product", "concept", "accent"):
        if not isinstance(spec.get(k), str) or not spec[k].strip():
            raise SpecError(f"icon_sketch: {k} is required")
    if spec.get("plate") not in PARTS["icon_plates"]:
        raise SpecError('icon_sketch: plate must be "paper" or "ink"')
    concept = ensure_period(spec["concept"].strip()); concept = concept[0].upper() + concept[1:]
    lint("concept", concept)
    prompt = PARTS["icon_sketch"].format(product=spec["product"].strip().rstrip("."), concept=concept,
                                         plate=PARTS["icon_plates"][spec["plate"]], accent=spec["accent"].strip())
    return {"mode": "icon_sketch", "aspect_ratio": "1:1", "prompt": prompt,
            "reference_image_paths": [str(REFS / PARTS["refs_rules"]["master"])],
            "note": "sketch only fixes the composition; colours come from icon-mode.md, the deliverable is a hand-written SVG"}


def build_fix(spec: dict) -> dict:
    base = Path(spec.get("base", ""))
    change = (spec.get("change") or "").strip()
    if not base.is_file():
        raise SpecError("fix: base must be an existing image path")
    if not change:
        raise SpecError("fix: change is required (one concrete change)")
    lint("change", change)
    from PIL import Image
    w, h = Image.open(base).size
    r = w / h
    aspect = min(("1:1", 1), ("4:3", 4 / 3), ("3:4", 3 / 4), ("16:9", 16 / 9), ("9:16", 9 / 16), key=lambda a: abs(a[1] - r))[0]
    refs = [str(base.resolve())]
    if spec.get("nub_ref"):
        refs.append(str(REFS / PARTS["refs_rules"]["nub"]))
    return {"mode": "fix", "aspect_ratio": aspect, "prompt": PARTS["fix"].format(change=ensure_period(change[0].upper() + change[1:])),
            "reference_image_paths": refs}


def list_presets() -> None:
    for slot, table in PARTS["slots"].items():
        print(f"[{slot}]")
        for k, v in table.items():
            extra = "".join([f"  +ref {v['ref']}" if "ref" in v else "", "  (holds)" if v.get("holds") else ""])
            print(f"  {k:<12} {v['zh']}{extra}")
    print("[season]")
    for k, v in PARTS["seasons"].items():
        print(f"  {k:<16} {v['zh']}{'' if v['verified'] else '  (未实测)'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", type=Path)
    ap.add_argument("--out", type=Path, help="job directory: writes prompt.txt and job.json")
    ap.add_argument("--list", action="store_true", help="list presets and seasons")
    a = ap.parse_args()
    if a.list:
        list_presets(); return
    if not a.spec:
        ap.error("spec.json is required (or --list)")
    try:
        spec = json.loads(a.spec.read_text(encoding="utf-8"))
        if not isinstance(spec, dict):
            raise SpecError("spec must be a JSON object")
        job = build(spec)
    except (SpecError, json.JSONDecodeError, OSError) as e:
        sys.exit(f"build_prompt: {e}")
    for r in job["reference_image_paths"]:
        if not Path(r).is_file():
            sys.exit(f"build_prompt: reference image missing: {r}")
    if a.out:
        a.out.mkdir(parents=True, exist_ok=True)
        (a.out / "prompt.txt").write_text(job["prompt"] + "\n", encoding="utf-8")
        (a.out / "job.json").write_text(json.dumps(job, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(job, ensure_ascii=False, indent=1))
    if job.get("season_verified") is False:
        print(f"note: season {job['season']} is not verified yet - expect to iterate", file=sys.stderr)


if __name__ == "__main__":
    main()
