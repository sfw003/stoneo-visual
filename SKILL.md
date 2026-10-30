---
name: stoneo-visual
description: "用一只沉稳、半眯眼斜着看人的水豚角色，以克制的漫画墨线 + 杏色网点风格出图；当用户要带水豚角色的专属配图、解释图、透明插画、头像、季节/节日限定图，或要做个人 logo、应用图标（桌面 / 移动端 icon、favicon）时使用。仅在用户明确点名 stoneo-visual 或要求带水豚角色出图时使用。"
disable-model-invocation: true
---

# Stoneo Visual

同一只水豚、同一套画法、同一条流水线。**能用脚本做的步骤一律用脚本**：提示词由 `build_prompt.py` 拼，验收由 `check_*.py` 判，对比板和加字由 JSON 渲染，交付由 `finalize.py` 打包。agent 只做三件事：选槽位、看图、写大白话讲解。

`<skill>` = 本文件所在目录。脚本依赖：Python 3、Pillow、cairosvg（`pip install pillow cairosvg`）、google-chrome 或 chromium。所有脚本都有 `--help`，输入不合法会报错退出，不会静默继续。

## 1. 角色与配色（摘要）

- 沉稳、冷幽默的水豚：圆角方大头（约占身高 45%）、杏色网点钝吻、两只小圆耳、头顶杏色块、细杏色项圈、梨形纸白身体、短腿、没尾巴。
- 识别点是**一只半眯斜眼**：平而重的上眼皮 + 小眉线 + 眼珠斜向一侧。
- **短圆手**，像星之卡比：没有手指、拇指、爪趾线。
- 主形象什么都不穿；服装、配件、季节是可选槽位（`build_prompt.py --list`）。
- 配色只有：墨 `#2B2520`、纸 `#F7F2EA`、杏 `#EE9A55`（局部网点）、浅卡其 `#E6D3B3`（仅外套）。深底 `#24201C` / `#F3ECE1` 只用于 HTML 演示。
- 总览图 `assets/refs/character-sheet.jpg` 只给人看，不传给 GenerateImage。

## 2. 硬规则（必须遵守）

1. 提示词只能由 `scripts/build_prompt.py` 生成。A 角色段、C 风格锚点、D 模式段不手改；只改 spec 里的槽位。
2. GenerateImage 的 `description`、`reference_image_paths`、`aspect_ratio` 原样使用 `job.json` 里的值，不增删参考图。
3. 生成图里没有任何文字。标题、标签只用 `render_labels.py` 加。
4. 透明插画只用 `cutout.py` 默认参数抠图，不传阈值。
5. 给用户挑的交付一律是 `render_board.py` 渲染的对比板：默认 3 个方案，只推荐 1 个。
6. 用户选定后只用 `finalize.py` 打包（1024 PNG / 图标全套 + zip + manifest），以文件附件发给用户。
7. 图标成品是手写 SVG，必须过 `check_icon_svg.py`。AI 只出构图草图。
8. 过程文件放任务目录（见 `references/pipeline.md`），不写进 skill 目录；任何文件和画面里都不写用户真名（头像占位用「昵称」）。
9. 脚本报 FAIL 就修，不绕过。`finalize.py --force` 只在用户明确接受已知问题时用，并在回复里说明。

## 3. 流程

完整命令、任务目录和文件命名见 `references/pipeline.md`。

| 步骤 | 解释图 A / 透明插画 B / 头像（含季节） | 图标 / logo |
|---|---|---|
| 1 定模式 | 讲清一件事 → A；放进别的排版 → B；当头像 → avatar；季节节日 → 加 `season` | 见 `references/icon-mode.md` |
| 2 拼提示词 | 每个方案写一个 spec，跑 `build_prompt.py spec.json --out job/<opt>` | （可选草图）`build_prompt.py`，mode `icon_sketch` |
| 3 出图 | GenerateImage，参数取自 `job.json`；输出存为 `job/gen/<opt>-v1.jpg` | 手写 SVG，从 `assets/templates/icon-plate.svg` 起步 |
| 4 自动验收 | `check_image.py`（A / B-src / avatar）；B 先跑 `cutout.py` 再 `check_image.py --mode B` | `check_icon_svg.py`，再 `export_icon.py` 看 16/32px |
| 5 人眼验收 | 逐条勾 `check_image.py` 末尾的人眼清单；修图用 mode `fix` 的 spec | 看 16/24/32px 原大和放大 |
| 6 加字 | 仅 A：`render_labels.py labels.json` | — |
| 7 对比板 | `render_board.py board.json compare.png`（board `compare`） | `render_board.py`（board `icon`，overview / detail / small） |
| 8 选定后交付 | `finalize.py image --mode A/B/avatar` | `finalize.py icon --large … [--small …]` |

只要一张图、不需要挑时，跳过第 7 步，其余照走。

## 4. 交付前必过清单

| # | 检查 | 由谁判定 |
|---|---|---|
| 1 | 提示词和参考图来自 `job.json`，没有手改 | `build_prompt.py`（spec 不合法直接报错） |
| 2 | 比例、尺寸、纸色背景或绿幕、色板、杏色只在局部 | `check_image.py` |
| 3 | 透明图四角透明、没有残绿、身体不透底 | `check_image.py --mode B` |
| 4 | 头像满版纸底，圆形裁切不切耳朵 | `check_image.py --mode avatar` |
| 5 | 同一只水豚、没有手指、没有字、表情对、没有杂物 | **人眼**：逐条勾 `check_image.py` 末尾的清单 |
| 6 | 加字的字体、字号、颜色、数量、位置范围符合规范 | `render_labels.py` |
| 7 | 对比板：2–4 个方案、只推荐 1 个、讲解每段一句、图都在 | `render_board.py` |
| 8 | 图标的 viewBox、底板、配色、线宽、小图网格合规，没有文字和渐变 | `check_icon_svg.py` |
| 9 | 图标 16px 能认出来 | **人眼**：看 `render_board.py` 的像素放大图 |
| 10 | 选定方案的 1024 PNG / 图标全套 + zip + manifest | `finalize.py` |
| 11 | 回复里写了推荐理由和实际存在的问题 | agent |

## 5. 文件索引

- `references/pipeline.md`：每种模式的完整命令、任务目录和文件命名。
- `references/prompt-template.md`：spec 格式和全部槽位键。提示词原文在 `assets/prompt/parts.json`，是唯一来源。
- `references/reference-images.md`：参考图用途，以及 build_prompt 的自动选图规则。
- `references/seasonal.md`：季节和节日限定的原则，以及 season 键。
- `references/troubleshooting.md`：常见问题和修图 spec 写法。
- `references/html-labels.md`：`render_labels.py` 的输入规范。
- `references/output-format.md`：对比板 `board.json` 规范和选定后的交付。
- `references/icon-mode.md`：图标系列规则、SVG 规范、大小图分开画、导出规格。
- `references/examples/`：已验证的 spec 和由它们生成的提示词，以及图标 SVG 示例。
- `scripts/`：`build_prompt.py`、`check_image.py`、`cutout.py`、`render_labels.py`、`render_board.py`、`check_icon_svg.py`、`export_icon.py`、`finalize.py`、`install.sh`（提交后同步，钩子自动运行）。
- `assets/`：`refs/` 参考图、`prompt/parts.json` 提示词片段、`templates/` 对比板、加字和图标起手 SVG。

## 6. 已知局限

- 纯侧面画不出来，总会偏 3/4。
- 「专注」必须带 `expr-focus-calm.jpg`（build_prompt 会自动带）。
- 32px 头像基本看不清斜眼；图标 16px 只剩轮廓，见 icon-mode.md。
- 季节除冬季外都没实测，`build_prompt.py` 会提示。
- 手指、表情、图里有没有字、像不像同一只，脚本判断不了，只能人眼看。
