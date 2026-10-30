# 提示词模板

> 拼法（顺序固定）：**A 角色段 → B 槽位 → C 风格锚点 → D 输出模式**。
> A、C 一个字都不要改；只填 B、选 D。提示词正文用英文，说明用中文。
> 每次都用宿主的 GenerateImage 做 edit：`reference_image_paths` 必须带参考图（见 `reference-images.md`），不要从零生成。

## A. 角色段（固定）

```text
Edit of the reference image: keep exactly the same capybara character, same face, same proportions and same art style as the reference.
The character: a chubby, calm capybara with a big rounded-rectangular head (about 45% of total height), a large blunt muzzle patch in apricot halftone with two small dark nostrils and a tiny simple mouth, two small round ears with apricot inner, an apricot halftone patch on top of the head, and a thin apricot collar band at the neck. Signature look: ONE visible half-lidded eye with a flat heavy upper lid and a small eyebrow line, glancing sideways in a cool deadpan side-eye — calm, unbothered, dry humor.
Short stubby rounded nub arms attached directly to the sides of the body like Kirby: each arm ends in a plain smooth rounded nub with an apricot halftone tip. NO fingers, NO thumb, NO pointing finger, NO paw digits on the hands. Short stubby legs, rounded feet with three tiny toe lines and apricot halftone tips. Pear-shaped round body, paper white, no tail.
```

## B. 槽位（按需填写；用不到的整行删掉）

```text
View: {VIEW}
Pose / action: {ACTION}
Expression: {EXPRESSION}
Outfit: {OUTFIT}
Accessory: {ACCESSORY}
Scene / props: {SCENE}
```

### VIEW 视角
- 默认：`3/4 view facing left, full body, centered with generous padding.`
- 正面：`straight front view facing the viewer, symmetrical, both ears and both half-lidded eyes visible, wide blunt muzzle patch.`
- 背面：`seen from behind, back of head, ears and collar visible, no face.`
- 半身：`head-and-shoulders close-up (bust portrait), same 3/4 view facing left.`
- 坐姿：`sitting on the floor in 3/4 view facing left, full body.`

### ACTION 动作（手一律写 "nub"，不要写 hand / paw / finger）

凡是手里拿东西的动作，在句尾追加：`The nubs do not wrap around the object: they are smooth round mitten ends pressed against its sides, exactly like the arm tips in the third reference image.`（并按 reference-images.md 加 `pose-shrug-nub-hands.jpg` 作第 3 张参考）
- 指东西：`the front nub arm raised forward toward the empty left side of the image, the direction shown only by the angle of the arm plus two tiny ink motion ticks; the other nub rests at its side. Leave the left third of the image empty.`
- 拿东西：`holds up a small blank paper card in front of its chest, both nub arms pressed against the two sides of the card.`
- 敲键盘：`sits on a low round cushion in front of a small open laptop, both nub tips resting on the keyboard; the laptop screen faces away and shows only its plain back lid.`
- 吃饭：`holds a round noodle bowl at chest height cradled between both nub arms, slurping noodles from the bowl, chopsticks resting in the bowl, a tiny ink steam curl.`
- 打游戏：`sits on the floor holding a simple rounded game controller in front of its belly, nub tips resting on the two grips, plain round buttons with no symbols.`
- 摊手：`shrugs, both nub arms raised outward at shoulder height, nub tips turned up, two tiny ink motion ticks near the shoulders.`
- 捧杯子：`holds a simple round mug in front of its chest cradled between both nub arms, the drink rendered as light apricot halftone, two thin ink steam curls.`

### EXPRESSION 表情
- 淡定斜眼（默认）：`calm half-lidded deadpan side-eye.`
- 轻微得意：`the side-eye narrowed a little with a knowing look, eyebrow slightly arched, chin slightly raised; the ONLY mouth is the tiny mouth inside the muzzle, curved up at one corner in a subtle smirk. No extra mouth on the cheek.`
- 无语：`eye fully flat with a perfectly straight heavy upper lid, pupil looking at the viewer, mouth a tiny flat line, one small ink-outline sweat drop near the forehead.`
- 专注：**直接写文字基本无效**（模型会画回默认的半眯眼；写眉毛下压又会像瞪人）。做法：把 `assets/refs/expr-focus-calm.jpg` 作为第 2 张参考图，并写 `Expression: calm focus exactly like the second reference image — eye a little more open with a soft relaxed upper lid covering the top third, pupil looking down toward the task, eyebrow relaxed, gently curved and level (not lowered, not angled), mouth a flat neutral line. Serene, not glaring.`
- 满足：`eye closed into a gentle downward happy arc, tiny contented smile inside the muzzle, two tiny ink sparkles, a faint apricot halftone blush on the cheek.`
- 困：`eye closed as one heavy drooping line with no eyelashes, head drooping forward to one side, mouth slightly open, no tongue. Nothing attached to the nose, no bubble, no Z.`

### OUTFIT 服装（主形象 = 什么都不穿；需要时才加）
- T 恤：`wears a simple short-sleeve tee in very light apricot halftone, mostly paper white with sparse dots, one small dot on the chest.`
- 写代码卫衣：`wears a warm light-gray halftone hoodie with apricot drawstrings and an apricot halftone front pocket.`
- 浅卡其外套：`wears a zip-up jacket in warm light khaki (#E6D3B3) halftone with two simple patch side pockets low on the front, and exactly ONE apricot backpack strap over the far shoulder only. No green.`

### ACCESSORY 配件
- 耳机：`wears simple over-ear headphones with a thin ink band over the head; BOTH ear cups visible, the far ear cup peeking out behind the head.`
- 小橘子：`a small mandarin sits on top of its head, drawn as a pale apricot halftone circle with ink outline and one tiny leaf — NOT a glossy saturated orange.`
- 冬季围巾：`a chunky knitted scarf in apricot halftone wrapped around the neck, replacing the collar, a few simple knit lines.`
- 雪花（冬季）：`three or four small simple snowflakes as thin ink six-point stars with very light cool-gray halftone, two resting on top of the head between the ears.`
- 毛线帽（冬季）：`a simple knitted beanie with a small pom-pom and ribbed fold in light warm-gray halftone; both ears poke out at the sides.`

### SCENE 场景 / 道具
只放讲清楚事情必需的 1–3 个道具：墨线 + 浅暖灰网点，最多一个杏色强调。图表、屏幕、卡片一律写 `blank` / `no labels, no numbers`。

## C. 风格锚点（固定）

```text
Style: restrained editorial manga ink illustration, in the spirit of a clean Japanese manga explainer. Warm off-white paper background #F7F2EA with subtle paper fiber texture (not pure white). Clean confident warm near-black ink outlines #2B2520 with varied line weight: thick for outer contours, thin for details; not wobbly, not sketchy. Large areas left as plain paper white — generous white space. Classic circular halftone dot screentone in soft apricot #EE9A55 ONLY on the muzzle, head-top patch, inner ears, nub tips, feet tips and collar (plus at most one small prop accent); props use ink outline with light warm-gray halftone. Colors limited to ink #2B2520, paper #F7F2EA, apricot #EE9A55 and its lighter tints. No solid heavy fills, no gradients, no 3D, no gloss, no photorealism, no extra colors, no green, no pink. No text, letters, numbers, logos, symbols or code anywhere in the image (labels are added later in HTML). No watermark.
```

## D. 输出模式（选一个，放在最后）

### 模式 A · 解释图
```text
Mode: finished explanatory scene on the paper background. One clear focal action, at most three visual regions. Leave clean empty paper areas where labels will be placed later. Small hatched ground shadow under the character.
```
- 比例常用 `4:3` 或 `16:9`；角色放一侧，另一侧留给道具和后加的标签。
- 标签用 HTML 叠加，见 `html-labels.md`。

### 模式 B · 透明插画
```text
Mode: isolated character asset. The background must be a perfectly uniform flat #00FF00 rectangle with zero gradient, texture, noise, shadow or floor plane. Keep generous padding; nothing touches the image border. No ground shadow. No garnish, no extra small objects.
```
出图后：
```bash
python3 <skill>/scripts/cutout.py src.jpg out.png          # 默认 --opaque-threshold 已是 160
```
- 模型给的绿常不是纯 #00FF00（见过 #3DBC2C），只要四角一致就行，脚本从边缘取色。
- 不要把阈值调回 220：纸白身体会只有约 94% 不透明，发灰透底。
- 若出成纸色底：把 C 段里 `Warm off-white paper background ... (not pure white).` 这一句删掉再出（这是唯一允许改 C 段的情况）。
- 抠完在深色（#24201C）和纸色（#F7F2EA）上各合成一次看边缘。

### 头像模式（社交头像 / 节日限定）
```text
Mode: square social-media avatar. Head-and-shoulders bust in 3/4 view facing left, centered, the head occupying about 55% of the image width, with a wide safe margin on all sides so a circular crop keeps the whole head, both ears and any hat inside the circle. FULL-BLEED square paper background #F7F2EA edge to edge — no circle, no disc, no vignette, no frame, no border. Few elements, clean bold readable silhouette, slightly bold contour lines; the eye must stay large and clear enough to read at 64px.
```
- 比例 `1:1`。参考图：母版 + `avatar-winter-snow-scarf.jpg`（构图范本）。
- 节日元素只用：杏色网点（围巾、帽边条纹）+ 很淡的暖灰 / 冷灰点缀；不引入大面积第二种颜色。
- 出图后：`python3 <skill>/scripts/avatar_preview.py src.jpg outdir/ --name avatar-xxx`，确认两项“ink outside”都是 0，再看 `-check.png` 里 64px 能否认出斜眼。
- 已知：32px 时斜眼基本看不清；主要用在很小尺寸时，把头放大到约 65% 宽（安全边距会变小，务必重跑检查）。
