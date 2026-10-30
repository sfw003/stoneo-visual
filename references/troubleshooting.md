# 验收清单与常见问题

## 每张图都要过的验收清单

1. **同一只**：大方吻部（杏色网点）+ 一只半眯斜眼 + 两只小圆耳 + 杏色项圈（围巾场景可替代），和母版一眼看是同一只。
2. **比例**：头约占身高 45%，身体梨形圆胖，腿短，没有尾巴。
3. **手**：圆头短手，**没有手指、拇指、爪趾线**。
4. **配色**：只有墨 `#2B2520`、纸 `#F7F2EA`、杏 `#EE9A55`（及浅色）、浅暖灰网点；没有绿、粉、蓝等第二种颜色，没有渐变、高光、3D。
5. **克制**：身体大部分是纸白，杏色只在局部。
6. **无字**：图里没有任何字、数字、代码、logo、符号（包括屏幕、图表、卡片上）。
7. **模式要求**：A 有纸色底和留给标签的空白；B 四角透明、无灰边；头像满版纸色底、圆裁不切耳、64px 认得出斜眼。
8. 不合格时：把这张图当第 1 张参考，写“Keep everything exactly the same … Change ONLY …”做局部 edit；不要整张重抽（重抽会换掉别处已经对的地方）。

## 常见问题 → 修正

| 问题 | 表现 | 修正 |
|---|---|---|
| 手长出手指 | 指东西出现食指；敲键盘 / 握手柄时手上有爪趾线 | **局部 edit 往往修不掉**（实测改完没变化），直接带 `pose-shrug-nub-hands.jpg` 作第 3 张参考重出，并在动作句尾加 “The nubs do not wrap around the object …”；写 `ends in a plain smooth rounded nub ... NO fingers, NO pointing finger`；方向靠手臂角度 + 动线 |
| “专注”像瞪人 / 和默认一样 | 写眉毛下压就凶；不写就画回半眯眼 | 带 `expr-focus-calm.jpg`；眉毛只写 `relaxed, gently curved and level`，**不要写 lowered / pulled down / angled / frown** |
| 小橘子变亮面橙 | 高饱和、有高光 | `pale apricot halftone circle with ink outline, NOT glossy, NOT saturated` |
| 耳机少一个耳罩 | 远侧耳罩被头挡住 | `BOTH ear cups visible, the far ear cup peeking out behind the head` |
| 背景变纯白 | 纸纹没了 | `keep the same cream paper background as the reference` |
| 多出一张嘴 | 笑 / 得意时脸颊上多一条嘴线 | `the ONLY mouth is the tiny mouth inside the muzzle` |
| “困”变成鼻环 / 对话框 | 鼻泡像圆环；冒出对话气泡 | 不要鼻泡：`nothing attached to the nose, no bubble, no Z` |
| 粉色舌头 | 张嘴时有粉红舌头 | `mouth slightly open, no tongue, no pink` |
| 侧面不够侧 | 侧面仍像 3/4，手像挂在肚子上的口袋 | 模型局限；用 `capybara-turn-side.jpg`，不要反复重抽 |
| 正面像小熊 | 头变圆 | 强调 `wide blunt muzzle patch`，带 `capybara-turn-front.jpg` |
| 衣服颜色跑偏 | 出现草绿、灰蓝 | 写死 hex（如 `#E6D3B3`）并加 `no green` |
| 背包带数量错 | 两条或零条 | `exactly ONE strap over the far shoulder only`；仍错就单独 edit 加 / 删 |
| 衣服涂太满 | 整件杏色网点 | `very light apricot halftone, mostly paper white with sparse dots` |
| 饮料 / 食物颜色太深 | 深褐色咖啡、酱色 | `the drink rendered as light apricot halftone, no dark brown` |
| 多出小杂物 | 碗边葱花、远处小点 | `no garnish, no extra small objects`；不行就局部 edit 删除 |
| 头像变成圆盘 | 模型自己画了纸色圆盘，四角发白 | `FULL-BLEED square paper background edge to edge, no circle, no vignette, no frame` |
| 绿幕不是纯绿 | 例如 #3DBC2C | 不用管，四角一致即可；`cutout.py` 从边缘取色 |
| 抠图后身体发灰透底 | 身体 alpha≈240 | 用 `cutout.py` 默认值（160），不要传 220 |
| 模式 B 出成纸色底 | 风格锚点和模式 B 冲突 | 删掉 C 段的 paper background 那一句再出 |
