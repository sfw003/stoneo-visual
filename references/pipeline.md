# 流水线：每一步的命令、目录和命名

`S=<skill>/scripts`。所有命令都在任务目录里运行。

## 任务目录（固定结构）

放在当前项目的过程目录下（有 `workbench/` 就放 `workbench/stoneo/`，否则放 `./stoneo/`），**不要放进 skill 目录**：

```text
stoneo/<YYYYMMDD>-<slug>/          slug：小写字母、数字、-，如 20261030-winter-avatar
├── spec-a.json  spec-b.json  spec-c.json      每个方案一个 spec（方案 id 固定 a / b / c）
├── a/prompt.txt  a/job.json  …                build_prompt.py --out 的输出
├── gen/a-v1.jpg  gen/a-v2.jpg  …               GenerateImage 结果，复制过来并按 <方案>-v<第几次> 命名
├── cut/a.png                                   模式 B 抠图结果
├── labels-a.json  labeled/a.png                模式 A 加字
├── check/                                      check_image.py --previews 输出
├── board.json  compare.png                     对比板
└── final/<slug>/ + final/<slug>.zip            finalize.py 输出（发给用户的就是这里的文件）
```

图标任务：

```text
stoneo/<YYYYMMDD>-<slug>/
├── sketch/a.json  sketch/a.jpg …   可选的 AI 构图草图（build_prompt mode icon_sketch）
├── svg/a-large.svg  svg/a-small.svg
├── export/a/                       export_icon.py 输出，只给对比板用
├── board-overview.json  board-detail.json  board-small.json  和对应的 PNG
└── final/<slug>/ + final/<slug>.zip
```

## 模式 A：解释图

```bash
python3 $S/build_prompt.py spec-a.json --out a            # 3 个方案各跑一次
# GenerateImage：description / reference_image_paths / aspect_ratio 全部取自 a/job.json
python3 $S/check_image.py gen/a-v1.jpg --mode A --aspect 4:3
python3 $S/render_labels.py labels-a.json labeled/a.png
python3 $S/render_board.py board.json compare.png         # board "compare", usage "illustration"
python3 $S/finalize.py image labeled/a.png --mode A --aspect 4:3 --out final --name <slug>
```

## 模式 B：透明插画

```bash
python3 $S/build_prompt.py spec-a.json --out a
python3 $S/check_image.py gen/a-v1.jpg --mode B-src       # 绿幕本身合格吗
python3 $S/cutout.py gen/a-v1.jpg cut/a.png               # 默认参数，不传阈值
python3 $S/check_image.py cut/a.png --mode B --previews check
python3 $S/render_board.py board.json compare.png         # usage "illustration"，img 用 cut/a.png
python3 $S/finalize.py image cut/a.png --mode B --out final --name <slug>
```

`B-src` 报「不是绿幕 / 出成纸色底」时，在 spec 里加 `"retry_without_paper": true` 重新生成。

## 头像（含季节限定）

```bash
python3 $S/build_prompt.py spec-a.json --out a            # {"mode": "avatar", "season": "winter", ...}
python3 $S/check_image.py gen/a-v1.jpg --mode avatar --previews check
python3 $S/render_board.py board.json compare.png         # usage "avatar"
python3 $S/finalize.py image gen/a-v1.jpg --mode avatar --out final --name <slug>
```

## 修图（局部 edit）

```bash
python3 $S/build_prompt.py fix.json --out a-fix1          # {"mode": "fix", "base": "gen/a-v1.jpg", "change": "..."}
```

修好的图存为 `gen/a-v2.jpg`，从「自动验收」那一步重新走。手长出手指时局部 edit 往往修不掉，要用原 spec 重新出图；原 spec 里有拿东西的动作时，会自动带短圆手参考图。

## 图标 / logo

```bash
python3 $S/build_prompt.py sketch/a.json                  # 可选：AI 构图草图
python3 $S/check_icon_svg.py svg/*.svg
python3 $S/export_icon.py svg/a-large.svg export/a --small svg/a-small.svg   # 只给对比板用
python3 $S/render_board.py board-overview.json compare-overview.png
python3 $S/finalize.py icon --large svg/a-large.svg --small svg/a-small.svg --out final --name <slug>
```

## 交付给用户

- 挑选阶段：发 `compare.png`（图标是 overview + detail，或 small），写推荐理由和实际问题。
- 选定之后：把 `final/<slug>/` 里的成品以文件附件发出。配图和头像发 `<slug>-1024.png`；图标发 `final/<slug>.zip`，同时附上 `png/<name>-1024.png`。`manifest.json` 留在任务目录，不发给用户。
