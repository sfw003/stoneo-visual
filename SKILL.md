---
name: stoneo-visual
description: "用一只沉稳、半眯眼斜着看人的水豚角色，以克制的漫画墨线 + 杏色网点风格出图；当用户要带水豚角色的专属配图、解释图、透明插画、头像、季节/节日限定图，或要做个人 logo、应用图标（桌面 / 移动端 icon、favicon）时使用。仅在用户明确点名 stoneo-visual 或要求带水豚角色出图时使用。"
disable-model-invocation: true
---

# Stoneo Visual

用同一只水豚、同一套画法出图。所有图都以参考图为底、用宿主的 **GenerateImage 做 edit**，文字一律用 HTML 后加。

例外是**图标 / logo 模式**：成品是手写 SVG（粗线 + 纯色，没有网点），AI 只出概念草图。走这个模式时直接读 `references/icon-mode.md`，下面第 3 节的出图流程不适用。

本文件里的相对路径都相对于本 skill 目录（下文记作 `<skill>`）。传给 GenerateImage 的参考图要换成绝对路径。

## 1. 角色设定

- **性格**：沉稳、不慌不忙，带一点冷幽默。默认表情是半眯眼、斜着看人的淡定脸。
- **外形**：胖乎乎的梨形身体，纸白色；大大的圆角方头约占身高 45%；前端是一大块杏色网点的钝吻部，两个小鼻孔、很小的嘴；两只小圆耳（耳内杏色）；头顶一块杏色网点；脖子一圈细杏色项圈；腿短，脚尖杏色、有三道小趾线；没有尾巴。
- **斜眼**：只画一只可见的眼睛，上眼皮平而重，上方一条小眉线，眼珠斜向一侧。这是角色的识别点，任何尺寸都要保住。
- **短圆手**：像星之卡比，手臂直接长在身体两侧，末端是光滑的圆头，带杏色网点。**没有手指、拇指、爪趾线**；动作靠整条手臂的角度表达。
- **主形象不穿戴任何东西**。服装、配件是可选扩展：
  - 服装：日常 T 恤、写代码卫衣（暖灰 + 杏色抽绳和口袋）、浅卡其外套（#E6D3B3，两个贴袋，一条背包带）。
  - 配件：耳机、头顶小橘子、冬季围巾（以及季节限定配件，见 `references/seasonal.md`）。
- 总览：`assets/refs/character-sheet.jpg`（转面、表情、动作、服装与配件、模板实测）。只给人或 agent 看，不要传给 GenerateImage。

## 2. 风格规则与配色

| 名称 | Hex | 用途 |
|---|---|---|
| 墨色 | `#2B2520` | 所有线条；粗外轮廓、细内部细节，干净有力，不抖不草 |
| 杏橘 | `#EE9A55` | **只在局部**用圆形网点：吻部、头顶、耳内、手脚尖、项圈，加最多一个道具强调 |
| 纸色 | `#F7F2EA` | 背景（带淡纸纹）和身体主体 |
| 浅卡其 | `#E6D3B3` | 仅外套 |
| 深底 | `#24201C` / 深底文字 `#F3ECE1` | 只用于 HTML 的深色界面演示，不进生成图 |

- 大面积留白；网点代替渐变；道具用墨线 + 浅暖灰网点。
- 禁止：满涂色块、渐变、高光、3D、写实、第二种大面积颜色（绿、粉、蓝、红、金）、图里的任何文字 / 数字 / 代码 / logo、水印。

## 3. 出图流程

1. **定模式**：
   - 模式 A：解释图。
   - 模式 B：透明插画。
   - 头像模式：方形头像，含季节限定头像。
   - 图标 / logo 模式：应用图标、个人 logo、favicon。全部按 `references/icon-mode.md` 做，不走下面 2–6 步。

   拿不准时：图片本身要讲清事情选 A；要放进别的排版选 B；要当头像选头像模式；要给软件、网站当图标或 logo 选图标模式。
2. **选参考图**：按 `references/reference-images.md` 选。第 1 张永远是 `assets/refs/capybara-master-34view.jpg`，总数 2–3 张。手里要拿东西时必须加 `pose-shrug-nub-hands.jpg`。
3. **拼提示词**：按 `references/prompt-template.md` 拼，顺序是 A 角色段 → B 槽位 → C 风格锚点 → D 模式。A、C 原样复制，只填 B、选 D。季节和节日的槽位见 `references/seasonal.md`，完整示例见 `references/examples/`。
4. **调用 GenerateImage**：
   - `description`：拼好的提示词。
   - `reference_image_paths`：参考图的绝对路径。
   - `aspect_ratio`：A 用 `4:3` 或 `16:9`，B 和头像用 `1:1`。
   - 输出文件不要存进本 skill 文件夹。
5. **验收**：逐条过 `references/troubleshooting.md` 的清单。不合格时，把这张图当第 1 张参考图，用 "Keep everything exactly the same … Change ONLY …" 做局部 edit，不要整张重抽。例外：手长出手指时，局部 edit 往往修不掉，要带上 `pose-shrug-nub-hands.jpg` 重新出图。
6. **后处理**：
   - 模式 A：按 `references/html-labels.md` 用 HTML 加标题和标签，模板是 `assets/templates/label-overlay.html`。
   - 模式 B：绿幕出图后抠图，命令是 `python3 <skill>/scripts/cutout.py src.jpg out.png`。默认 `--opaque-threshold 160`，不要改回 220，否则身体会发灰透底。抠完在深色和纸色底上各合成一次检查。
   - 头像：运行 `python3 <skill>/scripts/avatar_preview.py src.jpg outdir/ --name avatar-x`。两项 ink outside 都要是 0，64px 时要能认出斜眼。
7. **交付**：
   - 给用户挑选的交付（默认 3 个方案）一律按 `references/output-format.md` 做对比板。模板是 `assets/templates/compare-board.html`，渲染命令是 `python3 <skill>/scripts/render_board.py`。
   - 只要一张图时，直接交付成品，并说明存在的问题。
   - **用户选定方案后**：必须单独导出该方案的 1024×1024 高清 PNG（方形，满版纸色底；透明插画则保留透明底），以文件附件形式发给用户，方便直接下载使用。不要只发对比板。

## 4. 文字

生成图里**不出现任何文字**，图表、屏幕、卡片、红包、蛋糕上都写 `blank / no text`。标题、标签、数字全部用 HTML/CSS 叠加后截图。这里和 oil-visual 不同：oil-visual 让模型直接写字，这里不让。

## 5. 文件索引

- `references/prompt-template.md`：A 角色段、B 槽位（视角、动作、表情、服装、配件、场景）、C 风格锚点、D 三种模式。
- `references/reference-images.md`：每张参考图的用途，以及怎么选。
- `references/troubleshooting.md`：验收清单、常见问题和修正写法。
- `references/output-format.md`：固定输出规范（3 方案对比板）。
- `references/seasonal.md`：季节和节日限定的做法，以及提示词例子。
- `references/html-labels.md`：用 HTML 加文字。
- `references/icon-mode.md`：图标 / logo 模式：系列规则、AI 草图 + 手写 SVG 流程、各平台导出规格、图标对比板。
- `references/examples/`：已验证的完整提示词；`examples/icons/` 是图标 SVG 写法示例。
- `assets/refs/`：参考图，清单见 reference-images.md。
- `assets/templates/compare-board.html`：方案对比板模板。
- `assets/templates/label-overlay.html`：解释图加标签模板。
- `assets/templates/icon-plate.svg`：图标起手 SVG（统一底板）。
- `assets/templates/icon-board.html`：图标对比板（总览 + 桌面实测两张）。
- `scripts/cutout.py`：绿幕抠图，改编自 oil-visual，MIT 许可，见 `scripts/LICENSE-oil-visual`。
- `scripts/avatar_preview.py`：头像的圆裁、小尺寸预览和安全边距检查。
- `scripts/render_board.py`：用无头 Chrome 把 HTML 渲染成 PNG，并自动裁掉底部空白。
- `scripts/export_icon.py`：SVG 导出 16–1024 PNG、Windows `.ico`、macOS `.icns`，`--mobile` 再出 iOS / Android / HarmonyOS 用的铺满图和前景、背景两层。

脚本依赖：Python 3 和 Pillow（`pip install pillow`），以及 google-chrome 或 chromium。`export_icon.py` 另需 `pip install cairosvg`。

## 6. 已知局限

- 纯侧面画不出来，模型总会画成偏 3/4。
- 「专注」表情必须带 `expr-focus-calm.jpg`，只写文字无效。
- 32px 时斜眼基本看不清。
- 小橘子、耳机、背包带、衣服颜色容易跑偏，修正写法见 troubleshooting。
- 图标 16px 时水豚特征基本只剩轮廓，功能符号更耐缩小；详见 icon-mode.md。
