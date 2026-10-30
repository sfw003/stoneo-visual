# 季节 / 节日限定

## 原则

- **底永远是主形象**：参考图第 1 张 = `capybara-master-34view.jpg`；角色段 A、风格锚点 C 一字不改。
- 限定感只靠 **1 件服装或配件 + 最多 1–2 个小场景元素** 表达，不换脸、不换画风、不改比例。
- **配色不破**：节日的“代表色”（春节红、圣诞红绿、樱花粉、夏天蓝）一律**翻译成杏色网点或浅暖灰 / 浅冷灰网点**，不引入大面积第二种颜色。
- 不写字：春联、福字、Merry Christmas、生日快乐都不画；需要文字时用 HTML 后加。
- 头像用“头像模式”，配图用模式 A，素材用模式 B。
- 交付按 `output-format.md`：默认 3 个方案的对比板。
- 以上规则已经写进 `assets/prompt/parts.json` 的 `seasons`，用 season 键即可，不用自己翻译颜色。

## 用法

spec 里加 `season`，它会填上对应的槽位；spec 里自己写了的槽位优先，季节不覆盖。

```json
{"mode": "avatar", "season": "winter"}
{"mode": "A", "aspect": "4:3", "season": "summer", "outfit": "tee"}
{"mode": "avatar", "season": "winter", "accessory": "beanie"}
```

带“拿东西”的季节会自动加短圆手参考图和“不要裹住”的后缀。未实测的季节，`build_prompt.py` 会提示 `not verified yet`，要预期多改几次；验证通过后把 parts.json 里的 `verified` 改成 `true` 并提交。

| 键 | 节日 | 填哪些槽位 | 拿东西 | 实测 |
|---|---|---|---|---|
| `winter` | 冬季 | expression, accessory | — | 已验证 |
| `summer` | 夏季 | expression, accessory, scene | 是 | 未实测 |
| `spring_festival` | 春节 | expression, accessory, scene | 是 | 未实测 |
| `spring` | 春季 | accessory, scene | — | 未实测 |
| `mid_autumn` | 中秋 | scene | 是 | 未实测 |
| `halloween` | 万圣节 | accessory | — | 未实测 |
| `christmas` | 圣诞 | accessory, scene | — | 未实测 |
| `birthday` | 生日 | accessory, scene | 是 | 未实测 |
春节的槽位末尾自动带 `No red, no gold, no Chinese characters, no 福.`，模型很容易自己加红色和“福”字。

## 变体

- 冬季：`"accessory": "beanie"`（毛线帽）；捧热饮用 `"action": "mug"`。
- 夏季：头顶一块小毛巾（水豚泡温泉梗，很适合冷幽默）`{"text": "a small folded towel on its head, paper white with light warm-gray halftone"}`；或冰棍 `{"text": "holds a simple popsicle in apricot halftone", "holds": true, "object": "popsicle"}`。

## 验收补充

- 节日元素去掉后，剩下的角色和主形象一模一样。
- 画面里没有红 / 绿 / 粉 / 蓝 / 金的大面积色块；没有任何字。
- 头像：圆裁不切耳、帽子；64px 认得出斜眼。
