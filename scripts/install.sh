#!/bin/sh
# 把当前提交的干净版本安装到 skills 目录（不含 .git、workbench/、.gitignore）
# 用法：sh scripts/install.sh <skills 目录>   或   SKILLS_DIR=<skills 目录> sh scripts/install.sh
set -e
SKILLS_DIR=${1:-$SKILLS_DIR}
if [ -z "$SKILLS_DIR" ]; then
  echo "用法：sh scripts/install.sh <skills 目录>（或设置 SKILLS_DIR）" >&2
  exit 1
fi
ROOT=$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)
NAME=$(basename "$ROOT")
D=$SKILLS_DIR/$NAME
if [ "$(cd "$ROOT" && pwd -P)" = "$(mkdir -p "$D" && cd "$D" && pwd -P)" ]; then
  echo "目标目录就是仓库本身，无需安装" >&2
  exit 1
fi
# 只覆盖空目录或已装过本 skill 的目录，避免误删别的东西
if [ -n "$(ls -A "$D")" ] && [ ! -f "$D/SKILL.md" ]; then
  echo "目标目录 $D 不是空的，也不像已安装的 skill，已停止" >&2
  exit 1
fi
find "$D" -mindepth 1 -delete
git -C "$ROOT" archive HEAD | tar -x -C "$D"
rm -f "$D/.gitignore"
echo "installed $NAME @ $(git -C "$ROOT" rev-parse --short HEAD) -> $D"
