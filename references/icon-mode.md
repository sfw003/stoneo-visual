# 图标 / logo 模式

给你做的桌面应用、开源产品出图标，也用来做个人 logo 和 favicon。和其他模式最大的不同：**成品是手写的 SVG，不是 AI 生成的位图**。AI 只用来出概念草图、定构图。

## 1. 原则

- **主角是产品功能，水豚是固定标记。** 用户一眼要看出这个应用是干什么的（搜索 = 放大镜，笔记 = 纸页……）。水豚可以整只出现，也可以只借一个特征：斜眼、小圆耳、圆角方头的轮廓、杏色吻部。
- **所有产品是一个系列**，下面这几条每个图标都一样：
  - 同一种圆角方形底板：viewBox `0 0 1024 1024`，底板 `x=y=64`、边长 896、圆角 `rx=208`，四周留 64 的透明边。
  - 底板只有两种颜色：纸色 `#F7F2EA`（加一圈 `#E3D8C8` 的浅边，免得放在白色桌面上看不出边界）或墨色 `#2B2520`。
  - 墨色 `#2B2520` 粗线，圆头圆角（`stroke-linecap/linejoin="round"`）。
  - 杏橘 `#EE9A55` **只用在一处**，通常就是那个「重点」：被找到的东西、耳朵、吻部。
  - 浅色填充用 `#FFFDF8`（比底板亮一点的纸白），用来区分主体和纸色底板。
  - 全图最多 3–4 种纯色，算上底板。
- **不要**：网点、纸纹、渐变、阴影、高光、细线、文字和字母。这些在 16px 时全都会糊掉。
- **线宽**（按 1024 画布）：主轮廓 90–132；次要结构 50–64；最细的细节不低于 40。原因：16px 时 1 像素 = 64 单位，低于 40 的线在 16px 就看不见了。
- **16px 能认出来**才算过关。认不出时先删元素，其次加粗；构图本身元素多（比如整只或半只水豚 + 道具）时，直接给 32px 及以下单独画一张小图，见第 3 节。

## 2. 流程（混合流程：AI 草图 + 手写 SVG）

实测下来，GenerateImage 出图标草图很快，但颜色和细节不受控：会自己换成藏青底、整块杏色底板，线宽和比例也不稳定，而且出的是位图，没法直接导出多尺寸。手写 SVG 每个数都能控制，小尺寸效果也是真实的。所以：

1. **写清产品事实**：产品名、做什么、最核心的一个动作（比如“输入几个字，瞬间找到文件”），用在哪些平台。
2. **定 3 个方向**：三个要真的不一样，常见的分法是：
   - 水豚特征和功能符号合成一个形状（最有辨识度）；
   - 纯功能符号 + 一处杏橘（最简洁、小尺寸最好）；
   - 水豚整只或半只 + 功能道具（最有个性，小尺寸最弱）。
3. **（可选）AI 概念草图**：每个方向一张，用来定构图，不进成品。用 `build_prompt.py` 的 mode `icon_sketch` 生成提示词（它会自动带母版参考图，并且不拼网点和纸纹的风格锚点）：
   ```json
   {"mode": "icon_sketch", "product": "a fast desktop file-search tool", "concept": "a magnifying glass whose lens is the capybara side-eye", "plate": "paper", "accent": "the inner ears"}
   ```
   草图常见问题：换底色、多出第二种强调色、水豚画成小熊、放大镜像棒棒糖。只取构图，颜色以本文件为准。
4. **手写 SVG**：从 `assets/templates/icon-plate.svg` 复制起步，按第 1 节的规则画。已有的写法示例在 `references/examples/icons/`。
   - 只用 `rect / circle / line / path / clipPath` 这些基本元素，不用滤镜、`mask`、外部图片和字体。
   - 底板必须带 `data-role="plate"`，浅边带 `data-role="plate-edge"`，导出移动端时脚本靠它们识别。
   - 斜眼的画法：一条平直的粗上眼皮（横线），黑眼珠是一个圆、只保留上眼皮**以下**的部分（用 clipPath 裁），眼珠靠向一侧。这样小尺寸也是“半眯眼斜着看”。
5. **规范检查**：`python3 <skill>/scripts/check_icon_svg.py svg/*.svg`。有 ERROR 必须改完（规则见第 8 节）。
6. **自查小尺寸**：用 `export_icon.py svg/a-large.svg export/a [--small svg/a-small.svg]` 导出，看 16 / 24 / 32 / 64px 原大和放大图。认不出就改，改完再导。大图删到不能再删还认不出时，按第 3 节另画小尺寸帧。
7. **对比板**：见第 5 节。这一步只交对比板，**不打包交付**，等用户选定。
8. **选定后打包**：`finalize.py icon --large … [--small …] --out final --name <slug>`。它会先跑 `check_icon_svg.py`，再导出桌面和移动端全套，复制 SVG 源文件，写 manifest，打成 zip。把 `final/<slug>.zip` 以文件附件发给用户，同时附上 `png/<name>-1024.png`。不要手动调用 export_icon 再自己打包。

## 3. 大图和小尺寸分开画

一个图标文件里本来就装着很多尺寸的帧（`.ico` 7 帧、`.icns` 8 个槽），系统按显示尺寸挑最接近的那帧。所以**大图和小图可以是两张画**，Windows 和 macOS 自己的系统图标也是这么做的。

- **什么时候要分**：构图里有角色 + 道具、或者 3 个以上元素，32px 时已经挤、16px 认不出。只有一个符号（比如纯放大镜）的图标不用分。
- **分界线**：默认 32px（`--small-max 32`）。大图管 48px 以上（桌面、Dock、开始菜单大图标），小图管 16/24/32（标题栏、任务栏、文件列表、托盘）。
- **小图怎么画**：
  - 默认是大图的**简化版**，讲的是同一个画面，颜色、底板、元素位置都对得上，让用户一眼知道任务栏里的小图和桌面上的大图是同一个应用。换一个画面（比如大图放大镜在头顶、小图放大镜套在眼睛上）16px 更清楚，但会像两个图标，只在用户明确选了时才用。搜索工具这个实例，用户就选了换画面的 S3。
  - 只留 3 样：主体轮廓、一个识别点（斜眼：一道横线 + 一个黑点）、杏橘那一处。删掉眉线、鼻孔、耳朵这类加分细节；功能符号缩小但保留，不保留就看不出是干什么的。
  - 主体放大，尽量顶满底板，元素之间至少留 1 像素（16px 时）的空。
  - **在 32 格网上画**：`viewBox="0 0 32 32"`，底板 `x=y=2`、边长 28、`rx=6.5`（和 1024 版等比）。主线宽 2：落在 16px 正好 1 像素、32px 正好 2 像素。横竖方向、偶数线宽的线，中心必须放在**奇数**坐标上（比如横线 `y=21`），`check_icon_svg.py` 会报错拦住。填充块的边最好放在偶数坐标上（比如 `x=6`），至少要落在整数上，否则脚本给 WARN。这样 16 和 32px 都对齐整像素，不发虚。24px 对不齐是正常的，看一眼不糊就行。
  - 小图同样要带 `data-role="plate"` / `plate-edge`。
- **导出**：`export_icon.py big.svg outdir/ --small small.svg [--small-max 32]`；交付时由 `finalize.py icon --small` 调用，分界线固定 32。≤ 分界线的 PNG、`.ico` 帧和 `.icns` 槽（16@2x 实际是 32px，用小图；32@2x 是 64px，用大图）都从小图渲染，移动端只用大图。脚本会打印哪些尺寸用了小图。
- **对比板**：board.json 里写 `"view": "small"`。顶上是大图（48/64/128 + Dock），中间一行“旧版 vs 新版”的 16/32px，下面三个小图写法并排，各自带 16–64 原大、像素放大和 Windows 任务栏。`options[].icon` 指向带 `--small` 导出的 `png/` 前缀，这样 16–32 是小图、48 以上是大图，和真实文件一致。
- 示例：`references/examples/icons/search-3-peek.svg`（大图）和 `search-3-peek-small-s1/s2/s3.svg`（三种小图写法，用户最后选了 S3）。

## 4. 导出

交付用 `finalize.py icon`（固定带 `--mobile`，目录和命名都写死）。下面这些单独的命令只用于对比板和自查：

```bash
python3 <skill>/scripts/export_icon.py icon.svg outdir/ --name myapp           # 桌面
python3 <skill>/scripts/export_icon.py icon.svg outdir/ --name myapp --mobile  # 加移动端
python3 <skill>/scripts/export_icon.py icon.svg outdir/ --name myapp --small icon-small.svg  # 32px 及以下用小图
```

依赖：`pip install cairosvg pillow`（Pillow ≥ 10）。

| 平台 | 产物 | 说明 |
|---|---|---|
| 通用 PNG | `png/<name>-{16,24,32,48,64,128,256,512,1024}.png` | 透明底，带底板圆角。每个尺寸都从矢量直接渲染，不是从大图缩小 |
| Windows | `<name>.ico` | 内含 16/24/32/48/64/128/256 七帧。任务栏 100% 缩放用 24px，150% 用 32/36px，桌面默认 48px |
| macOS | `<name>.icns` | 内含 128/256/512/1024 和 16@2x、32@2x、128@2x、256@2x。没有 16/32 的 1x 帧（Pillow 不写这两种旧格式），系统会从 @2x 缩小，实测不影响使用。Apple 的官方网格是 1024 画布里 824 的圆角方形；我们用 896，系列统一，比系统图标略大一点 |
| iOS | `mobile/<name>-fullbleed-1024.png` | App Store / Xcode 只要一张 1024×1024，**不透明、不带圆角**，系统自己加圆角。脚本会去掉底板、用底板颜色铺满 |
| Android | `mobile/foreground-1024.png` + `background-1024.png`；Play 商店用 `<name>-fullbleed-512.png` | 自适应图标是前景 + 背景两层（108dp 画布，中间直径 66dp 的圆是安全区）。脚本把主体缩到 `--fg-scale 0.78` 放进安全区。旧式 mipmap 是 48/72/96/144/192px，直接用 Android Studio 的 Image Asset 从这两层生成 |
| HarmonyOS | 同 Android 的两层 | 分层图标：前景透明 PNG、背景纯色不透明 PNG，**都必须 1024×1024**，不许自己裁圆角、不许在资源里加内边距（背景铺满）。在 `layered-image` 里引用。AppGallery 上架图标用 1024 或 216（`<name>-fullbleed-216.png`） |

移动端注意：被底板裁切的构图（比如水豚从下沿探头），去掉底板后裁切线会露在中间，需要单独为移动端调构图。

## 5. 对比板

只用 `render_board.py` 从 board.json 渲染（宽 1080，手机上也能看清），规则见 `output-format.md`。三种 `view`：

- `overview`：三个方案并排。每个方案有成品大图、元素 / 优点 / 代价、浅色和深色底上的 64/32/16px 原大、32 和 16px 的像素放大图。高度约 1000px。
- `detail`：每个方案一块。16/24/32/48/64 原大（浅、深两种底），再放进四个模拟桌面：Windows 任务栏浅色 / 深色（任务栏 24px 图标 + 桌面 48px 图标和名字）、macOS Dock 浅色 / 深色。别的应用用中性灰色圆角块占位，不模仿任何真实品牌。三个方案约 2600px。
- `small`：定稿大图加三个小尺寸写法，见第 3 节。

```bash
python3 <skill>/scripts/export_icon.py svg/a-large.svg export/a      # 每个方案各导一次，只为拿 png/
python3 <skill>/scripts/render_board.py board-overview.json compare-overview.png
python3 <skill>/scripts/render_board.py board-detail.json compare-detail.png
```

```json
{"board": "icon", "view": "overview", "title": "搜索工具图标 · 三个方向", "appName": "文件搜索",
 "options": [{"icon": "export/a/png/app", "name": "1 · 水豚当放大镜", "elements": "镜片就是水豚的斜眼，顶上两只杏色小圆耳",
              "pros": "一眼是搜索，又一眼是你的水豚", "cost": "16px 时眼睛只剩一条横线加一个黑点", "rec": true}, ...]}
```

“代价”里必须写清楚 16px 时实际丢了什么。推荐只给一个；如果实测发现推荐的方向在小尺寸明显不如别的，照实写。

## 6. 个人 logo / favicon

个人 logo 用同一套规则，区别是主角就是水豚本身（通常是头部 + 斜眼），不需要功能符号。favicon 要 16/32/48 的 `.ico` 加一张 180px 的 `apple-touch-icon`（用 `png/<name>-1024.png` 缩，或单独导 180）。另外再出一个**单色版**（全部墨色，或深色底上全部纸色），给印章、水印、只能用一种颜色的地方用。

## 7. 已知局限

- 16px 下水豚的特征基本只剩轮廓：斜眼剩一条横线加一个点，耳朵的杏色看不出来。功能符号（放大镜、文件）比角色特征更耐缩小。另画小尺寸帧能救回来一部分，但 16px 仍然只是“认得出是它”，看不清表情。
- 圆耳放在圆形上方容易被看成小熊。耳朵画小一点、贴紧一点会好些。
- AI 草图的颜色不可信，见第 2 节第 3 步。

## 8. SVG 规范（`check_icon_svg.py` 逐条检查）

| 项 | 大图（1024 格） | 小图（32 格） |
|---|---|---|
| viewBox | `0 0 1024 1024` | `0 0 32 32` |
| 底板 `data-role="plate"`，必须是第一个绘制元素 | `x=y=64`，边长 896，`rx=208` | `x=y=2`，边长 28，`rx=6.5` |
| 底板颜色 | 纸色 `#F7F2EA` 或墨色 `#2B2520` | 同左 |
| 浅边 `data-role="plate-edge"` | 纸色底板必须有：`70/70/884/884`、`rx=202`、`stroke=#E3D8C8`、宽 12；墨色底板不能有 | 纸色底板必须有：`2.5/2.5/27/27`、`rx=6`、`stroke=#DDD1C0`、宽 1 |
| 允许的颜色 | 墨、纸、杏 `#EE9A55`、亮纸白 `#FFFDF8`、浅边色、`none` | 同左 |
| 最细线宽 | 40 | 2 |
| 网格对齐 | — | 横竖方向、偶数宽的线，中心必须在奇数坐标上（ERROR）；填充块边不在整数上（WARN） |
| 禁止 | `<text>`、`<image>`、渐变、`<pattern>`、`<filter>`、`<mask>`、`<use>`、`<style>`、`style=`、`opacity`、虚线、外部链接 | 同左 |
| 杏橘 | 用在超过 2 个元素上时 WARN（一对耳朵算一处） | 同左 |

注释里不能出现 `--`（XML 不允许），脚本会报“not well-formed”。
