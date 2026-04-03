#!/bin/bash
# obsidian-kb skill setup
# 用法: bash init.sh [vault_path]

VAULT="${1:-vault}"

echo "📁 初始化 vault: $VAULT"
mkdir -p "$VAULT"/{concepts,papers,code,projects,_templates}

# 复制模板（不覆盖已有）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
for tpl in "$SCRIPT_DIR"/_templates/*.md; do
  name=$(basename "$tpl")
  if [ ! -f "$VAULT/_templates/$name" ]; then
    cp "$tpl" "$VAULT/_templates/"
    echo "  ✅ 模板: $name"
  fi
done

# 创建 .gitkeep
for dir in concepts papers code projects; do
  touch "$VAULT/$dir/.gitkeep"
done

echo ""
echo "✅ Vault 初始化完成: $VAULT"
echo ""
echo "使用方法:"
echo "  python3 scripts/obsidian_kb.py -v $VAULT new '笔记标题' -t concept"
echo "  python3 scripts/obsidian_kb.py -v $VAULT search '关键词'"
echo "  python3 scripts/obsidian_kb.py -v $VAULT ask '你的问题'"
