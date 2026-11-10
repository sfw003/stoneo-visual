<p align="center">
  <img src="./assets/readme/banner.jpg" width="100%" alt="stoneo-visual：沉稳、半眯眼斜看人的水豚">
</p>

<p align="center"><b>给 AI Agent 用的水豚配图 Skill，为文章、产品和个人主页制作同一角色风格的解释图、透明插画、头像与图标。</b></p>

## 看看效果

<p align="center">
  <img src="./assets/readme/demo-explainer-gaming.jpg" width="49%" alt="解释图：穿卫衣打游戏的水豚，标题和标签用 HTML 后加">
  <img src="./assets/readme/demo-explainer-chart.jpg" width="49%" alt="解释图：水豚指向无字柱状图">
</p>

<p align="center">解释图 · 先画场景，再用 HTML 加标题和标签。</p>

<p align="center">
  <img src="./assets/readme/demo-transparent-noodles.png" width="36%" alt="透明插画：穿 T 恤吃面的水豚">
  &nbsp;&nbsp;
  <img src="./assets/readme/demo-avatar-winter.jpg" width="40%" alt="冬季头像：戴杏色围巾、头顶落雪的水豚">
</p>

<p align="center">透明插画可直接放进排版；头像会检查圆形裁切和小尺寸效果。</p>

## 安装

将整个仓库放进你所用 Agent 的 **skills 目录**。在该目录下运行：

```bash
git clone https://github.com/sfw003/stoneo-visual.git
```

按宿主说明重新加载 Skill，确认它能识别 `stoneo-visual/SKILL.md`。

### 需要什么

- **Agent 能力**：读图、执行本地脚本，以及能带参考图进行编辑的生图工具。当前流程按 `GenerateImage` 工具编写；其他宿主需要对应适配，并非只复制文件就能运行。
- **Python 3**（建议 3.10+），以及 Pillow、cairosvg：

  ```bash
  python3 -m pip install "pillow>=10" cairosvg
  ```

- **Chrome / Chromium**：可执行文件需在 `PATH` 中，用于将 HTML 标签和对比板渲染成图片。中文排版建议安装 Noto Sans CJK SC 或思源黑体。

生图由宿主提供；仓库本身不包含生图服务。

## 直接这样说

```text
用 stoneo-visual 画一张解释图：水豚指着上升的柱状图，标题写“这个月的进度”。
```

```text
用 stoneo-visual 画一张透明插画：水豚戴耳机敲键盘，放在文章开头。
```

```text
用 stoneo-visual 做一个冬季头像，给我 3 个方案对比。
```

默认先出 3 个方案，附对比板和推荐理由；选定后导出成品 PNG。只需要一张时可以直接说明。应用图标和 logo 使用手写 SVG，可导出多尺寸 PNG、ICO、ICNS 等格式。

出图以参考图约束角色和画法；生成画面不带文字，标题、标签随后排版。脚本负责拼提示词、检查图片、抠图、渲染和打包，角色是否走样仍需 Agent 看图确认。

## 角色与画法

<p align="center">
  <img src="./assets/readme/character-sheet.jpg" width="100%" alt="水豚设定：转面、表情、动作、服装和配件">
</p>

圆胖身体、大圆角方头、短圆手；默认半眯眼斜看人，沉稳，带一点冷幽默。主形象不穿衣服，可按场景加 T 恤、卫衣、外套或配件。

画面以留白和漫画墨线为主，用网点代替渐变。主色是墨色 `#2B2520`、纸色 `#F7F2EA`、局部杏橘 `#EE9A55`。

## 进一步使用

- [SKILL.md](./SKILL.md)：完整规则和文件索引。
- [出图流程](./references/pipeline.md)：各模式的命令、检查和交付。
- [提示词与示例](./references/prompt-template.md) · [已验证示例与验证范围](./references/examples/README.md)：自己编写或调整生成任务。
- [图标规范](./references/icon-mode.md)：SVG 绘制、小尺寸检查与平台导出。
- [常见问题](./references/troubleshooting.md)：出图跑偏时怎么修。

## 目前的限制

- 画不出纯侧面，最多到 3/4 侧。
- 头像缩到 32px 左右时斜眼不明显；图标在 16px 下只剩轮廓。
- 季节和节日主题目前只验证过冬季。

## 致谢与许可

结构与工作流参考了 [oil-visual](https://github.com/oil-oil/oil-visual)。其中 [`scripts/cutout.py`](./scripts/cutout.py) 改编自其同名脚本，沿用 MIT 许可；原版权声明和完整条款保留在 [`scripts/LICENSE-oil-visual`](./scripts/LICENSE-oil-visual)。复制或分发该部分时，须保留版权与许可声明。

本仓库整体（包括脚本、文档、水豚角色形象和图片）以 [MIT 许可](./LICENSE) 开源。
