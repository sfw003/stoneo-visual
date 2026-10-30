# 已验证的完整提示词

| 文件 | 模式 | 参考图 | 结果 |
|---|---|---|---|
| `mode-a-point-chart.prompt.txt` | A 解释图，4:3 | master + pose-shrug-nub-hands | 一次通过：圆头手指向无字柱状图 |
| `mode-b-noodles-tee.prompt.txt` | B 透明插画，1:1 | master + outfit-tee | 通过；T 恤杏色偏满（模板已改成 sparse dots） |
| `mode-a-hoodie-gaming.prompt.txt` | A 解释图，4:3 | master + outfit-hoodie-coding + pose-shrug-nub-hands | skill 打包后的独立验证图；第一次没带 shrug 参考，手长出手指，加上后通过 |
| `avatar-winter.prompt.txt` | 头像模式，1:1 | master + avatar-winter-snow-scarf | 按当前模板重新拼的；原始头像是经过两次局部 edit 才定稿的（去圆盘、去杂点） |

这些文件就是“A + B 槽位 + C + D”逐字拼出来的结果，可直接对照自己的拼接是否正确。

## 图标 SVG 示例（`icons/`）

第一个实例：桌面文件搜索工具（类似 Everything）的三个方向，按 `../icon-mode.md` 手写。用来抄写法（统一底板、`data-role`、斜眼的 clipPath 画法、被底板裁切的构图），不是定稿。

- `search-1-eye-lens.svg`：水豚当放大镜，镜片是斜眼。
- `search-2-dot-lens.svg`：墨色底板，放大镜 + 杏橘点。
- `search-3-peek.svg`：水豚从下沿探半个头，头顶放大镜。
