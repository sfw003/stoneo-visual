# 参考图：用途与选择

所有参考图在 `assets/refs/`，传给 GenerateImage 时用**绝对路径**（= 本 skill 目录 + `/assets/refs/文件名`）。

## 每张图的用途

| 文件 | 内容 | 用途 |
|---|---|---|
| `capybara-master-34view.jpg` | 主形象母版，3/4 侧面，不穿戴 | **每次必带，永远放第 1 张**。脸、比例、斜眼、网点位置都以它为准 |
| `capybara-turn-front.jpg` | 正面 | 需要正面时作第 2 张 |
| `capybara-turn-side.jpg` | 侧面（实际偏 3/4） | 需要侧身时参考；纯侧面模型画不出来，别反复重抽 |
| `capybara-turn-back.jpg` | 背面 | 需要背影时作第 2 张 |
| `expr-focus-calm.jpg` | 专注表情（平静、看向下方） | 需要“专注”时作第 2 张，文字描述单独用无效 |
| `expr-smug.jpg` | 轻微得意 | 需要得意 / 小嘚瑟表情时作第 2 张 |
| `pose-point-nub.jpg` | 用圆头手指向左侧 | 讲解、指向内容时 |
| `pose-hold-card.jpg` | 双手举空白卡片 | 拿 / 展示东西时 |
| `pose-typing-laptop.jpg` | 坐垫上敲笔记本 | 写代码、工作场景 |
| `pose-shrug-nub-hands.jpg` | 摊手 | 摊手，以及**任何动作的“短圆手”范本**（手长出手指时加它） |
| `outfit-tee.jpg` | 日常 T 恤 | 穿 T 恤时（注意它的杏色偏满，提示词里要求 sparse dots） |
| `outfit-hoodie-coding.jpg` | 写代码卫衣（暖灰 + 杏色抽绳和口袋） | 穿卫衣时 |
| `outfit-jacket-khaki.jpg` | 浅卡其外套，两个贴袋，一条背包带 | 出门、通勤、旅行场景 |
| `acc-headphones.jpg` | 戴耳机 | 听歌 / 专注写代码 / 游戏（注意：远侧耳罩被挡住，提示词要写 BOTH ear cups visible） |
| `acc-mandarin.jpg` | 头顶小橘子 | 幽默、吃东西场景 |
| `avatar-winter-snow-scarf.jpg` | 冬季头像：围巾 + 头顶落雪 | 头像模式的构图范本；冬季 / 节日限定图 |
| `character-sheet.jpg` | 整张角色设定板（转面、表情、动作、服装与配件、模板实测） | **给人看 / 给 agent 读的总览**，不要放进 reference_image_paths（拼图会被模型当成要画的内容） |

## 怎么选：由 `build_prompt.py` 自动决定

参考图不手选，`job.json` 的 `reference_image_paths` 是什么就传什么。规则（写在 `assets/prompt/parts.json` 的 `refs_rules` 和各预设的 `ref` / `ref_rank` 里）：

1. 第 1 张永远是 `capybara-master-34view.jpg`。
2. 第 2 张选“这张图最难画对的东西”：表情 > 转面（正面 / 背面）> 服装 > 动作 > 配件 > 头像构图（`avatar-winter-snow-scarf.jpg`，仅头像模式）。自由文字槽位不带参考图。
3. 只要拿 / 握 / 捧东西（预设动作、season 自带的道具，或自由文字写了 `"holds": true`），以及 `"nub_ref": true` 的动作（如指向），都会把 `pose-shrug-nub-hands.jpg` 放进来。实测：不加时手柄场景长出了弯曲的手指，事后局部 edit 也修不掉；加上后一次通过。
4. 所以最多 3 张：母版 + 优先级最高的 1 张 + 需要时的短圆手。其余槽位的参考图不带，只靠文字。参考图越多，角色特征越容易被“平均”掉。
5. 修一张已有的图：mode `fix`，那张图自动放第 1 张，不带母版（见 `troubleshooting.md`）。
