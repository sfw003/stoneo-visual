# 季节 / 节日限定

## 原则

- **底永远是主形象**：参考图第 1 张 = `capybara-master-34view.jpg`；角色段 A、风格锚点 C 一字不改。
- 限定感只靠 **1 件服装或配件 + 最多 1–2 个小场景元素** 表达，不换脸、不换画风、不改比例。
- **配色不破**：节日的“代表色”（春节红、圣诞红绿、樱花粉、夏天蓝）一律**翻译成杏色网点或浅暖灰 / 浅冷灰网点**，不引入大面积第二种颜色。
- 不写字：春联、福字、Merry Christmas、生日快乐都不画；需要文字时用 HTML 后加。
- 头像用“头像模式”，配图用模式 A，素材用模式 B。
- 交付按 `output-format.md`：默认 3 个方案的对比板。

## 拼法

`A 角色段` + 下面某个季节的槽位句 + `C 风格锚点` + `D 模式`。参考图：master + 最接近的一张（头像构图范本 `avatar-winter-snow-scarf.jpg`；有衣服时用对应服装图）。

## 示例槽位（已按规则翻译好颜色，直接用）

### 冬季（已验证，见 `avatar-winter-snow-scarf.jpg`）
```text
Expression: calm half-lidded deadpan side-eye glancing upward at the snowflakes on its head, a faint apricot halftone blush on the cheek from the cold.
Accessory: a chunky knitted scarf in apricot halftone wrapped around the neck, replacing the collar, a few simple knit lines. Three or four small simple snowflakes as thin ink six-point stars with very light cool-gray halftone, two resting on top of the head between the ears.
```
变体：毛线帽 `a simple knitted beanie with a small pom-pom and ribbed fold in light warm-gray halftone; both ears poke out at the sides.`；捧热饮见 prompt-template 的“捧杯子”。

### 夏季（未实测）
```text
Expression: calm half-lidded deadpan side-eye, totally unbothered by the heat.
Accessory: a simple woven straw sun hat with a thin apricot halftone band, drawn in ink with light warm-gray halftone; both ears visible under the brim.
Scene / props: holds a slice of watermelon between both nub arms, the flesh drawn as apricot halftone (not red) with a few tiny ink seeds and a pale rind; one tiny ink sweat drop.
```
变体：头顶一块小毛巾（`a small folded towel on its head, paper white with light warm-gray halftone`）——水豚泡温泉梗，很适合冷幽默；或一根冰棍（`a simple popsicle in apricot halftone`）。

### 春节（未实测）
```text
Expression: calm half-lidded deadpan side-eye with a very subtle smirk.
Accessory: wears a simple padded Chinese-style jacket with frog buttons, in very light apricot halftone, mostly paper white with sparse dots.
Scene / props: holds a small plain red-envelope-shaped packet rendered in apricot halftone (NOT red), completely blank with no characters or symbols; one small round paper lantern in apricot halftone hanging nearby, no tassel text.
```
提醒：`no red, no gold, no Chinese characters, no 福` 要加在槽位末尾；模型很容易自动加红色和“福”字。

### 春季（未实测）
```text
Accessory: two or three small five-petal blossoms resting on top of the head, drawn as thin ink outlines with very light apricot halftone (NOT pink).
Scene / props: a few tiny petals drifting nearby, ink outline only.
```

### 中秋（未实测）
```text
Scene / props: holds a round mooncake between both nub arms, drawn in apricot halftone with a simple blank ink pattern (no characters); a large pale full moon behind the head as a thin ink circle with very light warm-gray halftone.
```

### 万圣节（未实测）
```text
Accessory: a small carved pumpkin sits on top of its head in apricot halftone with a simple ink face, NOT glossy, NOT saturated orange.
```

### 圣诞（未实测）
```text
Accessory: a simple Santa-style hat in apricot halftone (NOT red) with a paper-white fluffy trim and pom-pom; both ears poke out.
Scene / props: one small pine sprig in light warm-gray halftone (NOT green).
```

### 生日（未实测）
```text
Accessory: a small cone party hat with thin apricot halftone stripes, tilted on the head.
Scene / props: holds a small round cake between both nub arms, paper white frosting with apricot halftone dots and one plain candle with a tiny ink flame. No text on the cake.
```

## 验收补充

- 节日元素去掉后，剩下的角色和主形象一模一样。
- 画面里没有红 / 绿 / 粉 / 蓝 / 金的大面积色块；没有任何字。
- 头像：圆裁不切耳、帽子；64px 认得出斜眼。
