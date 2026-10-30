# 固定输出规范：方案对比板

只要是“给用户挑”的交付（头像、配图、节日限定、新服装……），一律按这个格式出，不要只丢几张散图。

## 规则

1. **默认 3 个方案**（用户指定数量时按用户的）。三个方案要真的有差别：换元素 / 换动作 / 换构图，不是同一张抽三次。
2. **每个方案一行**，每行三块，从左到右：
   - **原图**：方形（或原比例）成品图。
   - **按用途的效果演示**：
     - 头像 → 圆形裁切大图 + 64px、32px 真实尺寸 + 64px 方形 + 放进浅色和深色界面（名字用“昵称”占位，绝不写真名）。
     - 配图 / 插画 → 放进文章里的样子 + 放进浅色卡片、深色卡片的样子。
     - 图标 / logo → 用 `assets/templates/icon-board.html`，不用本模板：16/32/64px 原大和放大、浅色 / 深色桌面、Windows 任务栏和 macOS Dock。做法见 `icon-mode.md` 第 5 节；分开画小尺寸帧时用 `view: "small"`（第 3 节）。
   - **一句讲解**：固定三段 **元素 / 优点 / 代价**，大白话，每段一句。
3. **推荐的那一行要加标**：橙色边框 + 标题后的「推荐」徽标。只推荐一个。
4. 对比板用 HTML 做，文字全部在 HTML 里，图里不生成字。
5. 交付时同时给：对比板 PNG + 每个方案的单独成品文件（头像 1024×1024 PNG；配图原比例 PNG；透明插画 RGBA PNG；图标先给 SVG，ico / icns 等选定后再导）。
6. 回复里说清：推荐哪个、为什么（一两句）、实际存在的问题（诚实写，比如“32px 看不清斜眼”）。

## 做法

1. 复制 `assets/templates/compare-board.html` 到工作目录（不要改 skill 里的原件）。
2. 只改顶部 `BOARD` 对象：
   - `title`、`subtitle`
   - `usage`: `"avatar"` 或 `"illustration"`
   - `options`: 每项 `{ img, name, elements, pros, cost, rec }`，`img` 写相对这个 html 的路径或 `file://` 绝对路径。
3. 渲染：`python3 <skill>/scripts/render_board.py board.html compare.png`（自动截掉底部空白；默认宽 1500）。
4. 用 Read 看一遍 PNG：推荐标在不在、图有没有加载失败（空白框）、文字有没有溢出。

## 头像额外检查

每个头像先跑 `python3 <skill>/scripts/avatar_preview.py src.jpg outdir/ --name avatar-x`：两项 ink outside 都要是 0（圆裁不切耳）；再看 `-check.png` 里 64px 能否认出斜眼。把结果写进“代价”。

## 选定后的交付

用户选定某个方案后，必须单独导出该方案的 1024×1024 高清 PNG（方形；透明插画保留透明底），以文件附件发给用户，不要只发对比板。
