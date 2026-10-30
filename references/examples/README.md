# 已验证的完整提示词

每个 `*.prompt.txt` 都是 `build_prompt.py specs/<同名>.json` 的原样输出。改了 `assets/prompt/parts.json` 之后要重新生成这些文件，并检查和之前的差异：

```bash
for f in specs/*.json; do n=$(basename $f .json); python3 ../../scripts/build_prompt.py $f --out /tmp/$n && diff /tmp/$n/prompt.txt $n.prompt.txt; done
```

| spec | 模式 | 参考图（脚本自动选） | 结果 |
|---|---|---|---|
| `mode-a-point-chart.json` | A 解释图，4:3 | master + pose-shrug-nub-hands | 一次通过：圆头手指向无字柱状图 |
| `mode-b-noodles-tee.json` | B 透明插画，1:1 | master + outfit-tee + pose-shrug-nub-hands | 通过（见下面的差异说明） |
| `mode-a-hoodie-gaming.json` | A 解释图，4:3 | master + outfit-hoodie-coding + pose-shrug-nub-hands | skill 打包后的独立验证图；第一次没带 shrug 参考，手长出手指，加上后通过 |
| `avatar-winter.json` | 头像模式，1:1 | master + avatar-winter-snow-scarf | 原始头像经过两次局部 edit 才定稿（去圆盘、去杂点），两处修正已经写进模板 |

和当时实际出图所用文字的差异：前三个逐字相同。`mode-b-noodles-tee` 有 3 行不同，都是出图之后根据结果收紧的规则：拿东西的句子加了“不要裹住碗”的后缀并带上 shrug 参考图；T 恤从 `light apricot halftone` 改成 `very light …, mostly paper white with sparse dots`（原图杏色偏满）；模式 B 结尾加了 `No garnish, no extra small objects.`。新文字还没单独重新出图验证过。

## 图标 SVG 示例（`icons/`）

第一个实例：桌面文件搜索工具（类似 Everything）的三个方向，按 `../icon-mode.md` 手写。用来抄写法（统一底板、`data-role`、斜眼的 clipPath 画法、被底板裁切的构图）。全部能通过 `check_icon_svg.py`。

- `search-1-eye-lens.svg`：水豚当放大镜，镜片是斜眼。
- `search-2-dot-lens.svg`：墨色底板，放大镜 + 杏橘点。
- `search-3-peek.svg`：水豚从下沿探半个头，头顶放大镜（用户选定后打磨过的大图，48px 以上用）。
- `search-3-peek-small-s1/s2/s3.svg`：同一图标的三种小尺寸帧写法（32 格网、像素对齐）：S1 大头 + 角上放大镜，S2 镜框当耳朵，S3 放大镜套住斜眼。**用户选定的是大图 `search-3-peek.svg` + 小图 S3。** S3 是换了画面的写法：16px 最清楚，代价是和大图不是同一个画面。
