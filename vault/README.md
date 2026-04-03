---
name: obsidian-kb
description: Obsidian-compatible bi-directional linked note knowledge base for LLMs. Create, link, search, and query notes with wikilinks and YAML frontmatter. Designed for use as an LLM knowledge vault.
---

# Obsidian KB

Obsidian 兼容的双向链接笔记知识库，面向大模型检索和问答。

## Commands

```bash
python3 tools/obsidian_kb.py new <title> --type concept|paper|code|project [--vault vault]
python3 tools/obsidian_kb.py link <source> <target> [--vault vault]
python3 tools/obsidian_kb.py search <query> [--vault vault]
python3 tools/obsidian_kb.py backlinks <title> [--vault vault]
python3 tools/obsidian_kb.py moc [--vault vault]
python3 tools/obsidian_kb.py ask <question> [--vault vault]
python3 tools/obsidian_kb.py graph [--vault vault]
```

## Directory Structure

```
vault/
├── MOC.md                    # Map of Content 总索引（自动生成）
├── concepts/                 # 概念笔记
├── papers/                   # 论文笔记
├── code/                     # 代码片段/技巧
├── projects/                 # 项目相关
└── _templates/               # 笔记模板
```

## Note Format

```markdown
---
title: "笔记标题"
tags: [tag1, tag2]
aliases: ["别名1"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# 标题

内容...

## 关联
- [[相关笔记1]] — 简述
- [[相关笔记2]] — 简述

## 关键结论
> 核心要点
```

## Workflow

1. `new` 创建笔记 → 自动填 frontmatter + 模板
2. 编辑内容，添加 `[[链接]]`
3. `moc` 更新总索引
4. `search` / `ask` 检索知识库
