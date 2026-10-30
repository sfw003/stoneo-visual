# 文字：一律用 HTML 后加

生成图里**不出现任何文字**（风格锚点已禁止）。标题、标签、数字都用 HTML/CSS 排在图上，再用无头 Chrome 截图。

## 模板

`assets/templates/label-overlay.html` 是一个可直接改的模板：
- 底图是 `<img>`，标签是绝对定位的 `<div class="tag">`，用百分比坐标贴在对应物体旁边。
- 字体：思源黑体 / Noto Sans CJK SC，medium 或 bold；颜色用墨色 `#2B2520`；需要强调时用杏色 `#EE9A55` 小圆点或下划线，不要大色块。
- 标签 2–6 个，每个尽量 2–8 个字，放在证据物体上或紧挨着它。

## 渲染

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1600,1200 \
  --screenshot=/abs/out.png file:///abs/label-overlay.html
```
`--window-size` 设成和页面一样大；需要高清时用 `--force-device-scale-factor=2`。没有 `google-chrome` 时试 `chromium` / `chromium-browser`。
