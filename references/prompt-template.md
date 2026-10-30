# 提示词：spec 格式与槽位键

提示词**只由 `scripts/build_prompt.py` 生成**。所有英文原文（A 角色段、C 风格锚点、D 三种模式、每个槽位预设、季节、修图句式、图标草图句式）都在 `assets/prompt/parts.json`，那里是唯一来源。要改措辞就改 parts.json 并提交，不要在单次任务的提示词里改。

## 拼装顺序（脚本固定）

`A 角色段` → 槽位行（`View` → `Pose / action` → `Expression` → `Outfit` → `Accessory` → `Scene / props`，没填的整行不出现）→ `C 风格锚点` → `D 模式段`。

默认值：A、B 模式没写 `view` 时用 `default`；没写 `expression` 时用 `deadpan`；头像模式不出 `View` 行（构图写在 D 段里）。

## spec 字段

| 字段 | 取值 | 说明 |
|---|---|---|
| `mode` | `A` / `B` / `avatar` / `fix` / `icon_sketch` | 必填 |
| `aspect` | `4:3` / `16:9` | 只用于 A，默认 `4:3`；B 和头像固定 `1:1` |
| `season` | 见 `seasonal.md` | 自动填表情、配件、场景；spec 里显式写的槽位优先 |
| `view` `action` `expression` `outfit` | 预设键，或 `{"text": "..."}` | 键写错会报错并列出可选键 |
| `accessory` | 预设键列表，或 `{"text": "..."}` | 多个配件按顺序拼 |
| `scene` | 自由文本 | 提到屏幕、图表、卡片、书、红包、蛋糕等时必须写 `blank` / `no text` / `no labels, no numbers`，否则报错 |
| `retry_without_paper` | `true` | 只用于 B：出成纸色底时，删掉 C 段里纸色背景那一句（这是唯一允许改 C 段的情况） |
| `nub_ref` | `true` | 额外带短圆手参考图（指东西这类容易长手指的动作） |

自由文本的 `action` 必须写 `"holds": true/false`。为 `true` 时还要写 `"object": "cup"`：脚本会在动作句尾加「圆头手贴着物体两侧、不包住」那句，并自动带上 `pose-shrug-nub-hands.jpg`，句子里「第几张参考图」也由脚本算。

所有自由文本都会检查：出现 hand / paw / finger / thumb / claw 就报错（手一律写 nub）。

## 修图 spec（mode `fix`）

```json
{"mode": "fix", "base": "gen/a-v1.jpg", "change": "Remove the small extra dot next to the bowl.", "nub_ref": false}
```

输出「其余一切不变，只改这一处」的固定句式。参考图第 1 张是 base，比例按 base 自动算。

## 图标草图 spec（mode `icon_sketch`）

```json
{"mode": "icon_sketch", "product": "a fast desktop file-search tool", "concept": "a magnifying glass whose lens is the capybara side-eye", "plate": "paper", "accent": "the inner ears"}
```

## 槽位键

`python3 scripts/build_prompt.py --list` 会打印同样的内容。

### view

| 键 | 含义 | 自动带的参考图 | 拿东西 |
|---|---|---|---|
| `default` | 默认 3/4 全身 | — | — |
| `front` | 正面 | capybara-turn-front.jpg | — |
| `back` | 背面 | capybara-turn-back.jpg | — |
| `bust` | 半身 | — | — |
| `sitting` | 坐姿 | — | — |
| `side` | 侧身（实际偏 3/4） | capybara-turn-side.jpg | — |

### action

| 键 | 含义 | 自动带的参考图 | 拿东西 |
|---|---|---|---|
| `point` | 指东西 | pose-point-nub.jpg | 短圆手参考 |
| `hold_card` | 拿卡片 | pose-hold-card.jpg | 是（card） |
| `typing` | 敲键盘 | pose-typing-laptop.jpg | — |
| `eat_noodles` | 吃面 | — | 是（bowl） |
| `game` | 打游戏 | — | 是（controller） |
| `shrug` | 摊手 | pose-shrug-nub-hands.jpg | — |
| `mug` | 捧杯子 | — | 是（mug） |

### expression

| 键 | 含义 | 自动带的参考图 | 拿东西 |
|---|---|---|---|
| `deadpan` | 淡定斜眼（默认） | — | — |
| `smug` | 轻微得意 | expr-smug.jpg | — |
| `speechless` | 无语 | — | — |
| `focus` | 专注（自动带 expr-focus-calm.jpg） | expr-focus-calm.jpg | — |
| `content` | 满足 | — | — |
| `sleepy` | 困 | — | — |

### outfit

| 键 | 含义 | 自动带的参考图 | 拿东西 |
|---|---|---|---|
| `tee` | T 恤 | outfit-tee.jpg | — |
| `hoodie` | 写代码卫衣 | outfit-hoodie-coding.jpg | — |
| `jacket` | 浅卡其外套 | outfit-jacket-khaki.jpg | — |

### accessory

| 键 | 含义 | 自动带的参考图 | 拿东西 |
|---|---|---|---|
| `headphones` | 耳机 | acc-headphones.jpg | — |
| `mandarin` | 头顶小橘子 | acc-mandarin.jpg | — |
| `scarf` | 冬季围巾 | — | — |
| `snowflakes` | 雪花 | — | — |
| `beanie` | 毛线帽 | — | — |
