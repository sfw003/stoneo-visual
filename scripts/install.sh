#!/bin/sh
# 把当前提交的干净版本同步到全局 skill 目录（不含 .git、workbench/、.gitignore）
set -e
ROOT=$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)
NAME=$(basename "$ROOT")
D=/home/box/agent-data/workflows/$NAME
mkdir -p "$D"
find "$D" -mindepth 1 -delete
git -C "$ROOT" archive HEAD | tar -x -C "$D"
rm -f "$D/.gitignore"
echo "installed $NAME @ $(git -C "$ROOT" rev-parse --short HEAD) -> $D"
