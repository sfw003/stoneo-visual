# 验收与常见问题

## 验收分两半

1. **自动**：`check_image.py <图> --mode A|B-src|B|avatar`。它会检查比例、尺寸、背景（纸色或绿幕）、色板偏离、杏色是否只在局部；透明图还查四角透明、残绿和身体是否透底；头像还查圆形裁切会不会切到墨线。有 FAIL 就不能往下走。
2. **人眼**：脚本最后会打印一份勾选清单（是不是同一只、手指、字、表情、杂物……）。逐条看图勾完才算过。这部分脚本判断不了，不能跳过。

## 不合格时怎么修

- 默认做局部 edit：写一个 `{"mode": "fix", "base": "gen/a-v1.jpg", "change": "<只改这一处>"}` 的 spec，跑 `build_prompt.py`。不要整张重抽，重抽会把别处已经对的地方也换掉。
- 例外：手长出手指时，局部 edit 往往修不掉，要用原 spec 重新出图。拿东西的动作会自动带上短圆手参考图；指东西这类动作在 spec 里加 `"nub_ref": true`。
- 下表「修正」一列的英文：fix 时写进 `change`；重新出图时写进对应槽位的 `{"text": ...}`。如果某条修正每次都要用，就把它改进 `assets/prompt/parts.json` 的预设里并提交，不要每次手写。

## 常见问题 → 修正

| 问题 | 表现 | 修正 |
|---|---|---|
| 手长出手指 | 指东西出现食指；敲键盘 / 握手柄时手上有爪趾线 | **局部 edit 往往修不掉**（实测改完没变化），直接带 `pose-shrug-nub-hands.jpg` 作第 3 张参考重出，并在动作句尾加 “The nubs do not wrap around the object …”；写 `ends in a plain smooth rounded nub ... NO fingers, NO pointing finger`；方向靠手臂角度 + 动线 |
| “专注”像瞪人 / 和默认一样 | 写眉毛下压就凶；不写就画回半眯眼 | 用预设 `"expression": "focus"`（自动带 `expr-focus-calm.jpg`）；不要自己写 lowered / pulled down / angled / frown |
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
| 头像变成圆盘 | 模型自己画了纸色圆盘，四角发白；`check_image.py --mode avatar` 报 paper background | fix：`Make the background a full-bleed flat paper #F7F2EA square edge to edge: no circle, no disc, no vignette, no frame.` |
| 绿幕不是纯绿 | 例如 #3DBC2C | 不用管，四角一致即可（`check_image.py --mode B-src` 会查）；`cutout.py` 从边缘取色 |
| 抠图后身体发灰透底 | 身体 alpha≈240，`check_image.py --mode B` 报 body opaque | 用 `cutout.py` 默认值（160），不要传阈值 |
| 模式 B 出成纸色底 | `check_image.py --mode B-src` 报不是绿幕 | spec 加 `"retry_without_paper": true` 重新生成 |
