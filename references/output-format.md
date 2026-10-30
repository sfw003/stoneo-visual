# 输出规范：对比板与选定后的交付

只要是“给用户挑”的交付（头像、配图、节日限定、新服装、图标……），一律出对比板，不要只丢几张散图。对比板只能由 `scripts/render_board.py` 从一份 `board.json` 渲染，版式全部固定在模板里。

```bash
python3 <skill>/scripts/render_board.py board.json compare.png
```

## 配图 / 头像对比板（`"board": "compare"`，宽 1500）

```json
{"board": "compare", "usage": "avatar",
 "title": "冬季限定头像 · 三个方案",
 "options": [
  {"img": "gen/a-v1.jpg", "name": "A · 毛线帽 + 围巾", "elements": "暖灰毛线帽 + 杏色围巾",
   "pros": "轮廓最有冬天感，小图辨识度高", "cost": "帽子盖住头顶杏色块，少一点幽默", "rec": false},
  ...]}
```

- `usage`：`avatar` 会出圆形裁切、64/32px 和浅色 / 深色界面（名字固定写「昵称」）；`illustration` 会出放进文章和浅色 / 深色卡片里的样子。透明插画的 `img` 用抠好的 PNG。
- 路径相对 `board.json`。

## 图标对比板（`"board": "icon"`，宽 1080）

`view` 三选一：`overview`（三个方案并排）、`detail`（Windows 任务栏和 macOS Dock 实测）、`small`（定稿大图 + 小尺寸帧，需要 `large`，可选 `before`）。`icon` 写 `export_icon.py` 输出的 PNG 前缀，例如 `export/a/png/app`。完整例子见 `icon-mode.md` 第 5 节。

## 脚本强制的规则

- 2–4 个方案（默认 3 个），**只有一个** `"rec": true`。三个方案要真的不一样：换元素、换动作或换构图，不是同一张抽三次。
- `elements` / `pros` / `cost` 各写一句大白话：不能为空，不带「。」，不超过 60 个字。代价要写实际问题，比如「32px 看不清斜眼」。
- 图片和图标 PNG 必须存在（脚本会逐个检查）。
- 副标题、名字占位、宽度、配色都固定，不能配置。
- 图标板高度超过 3000px 会报错，要拆成 overview 和 detail 两张。

渲染完用 Read 看一遍 PNG：推荐标在不在、文字有没有溢出。

## 回复里要写

推荐哪个、为什么（一两句），以及实际存在的问题（照实写）。

## 选定后的交付

用户选定后，跑 `finalize.py`（命令见 `pipeline.md`），把 `final/<slug>/` 里的成品以文件附件发给用户，不要只发对比板。

| 模式 | 交付文件 |
|---|---|
| 解释图 A | `<slug>.png`（1600 宽，原比例，带标签）+ `<slug>-1024.png`（方形，纸色补边） |
| 透明插画 B | `<slug>-1024.png`（RGBA，裁掉空白后居中，四周留 64px） |
| 头像 | `<slug>-1024.png`（满版纸色），`preview/` 里有圆形预览 |
| 图标 | `<slug>.zip`（SVG + ico + icns + PNG + 移动端）+ `png/<name>-1024.png` |
