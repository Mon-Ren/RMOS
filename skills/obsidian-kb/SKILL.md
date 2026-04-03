---
name: obsidian-kb
description: Obsidian 兼容的双链笔记知识库，面向大模型检索与问答。支持创建笔记、建立链接、关键词搜索、知识库问答、MOC 索引自动更新。触发词：笔记、知识库、obsidian、vault、双链、wikilink、note、kb。
---

# Obsidian KB Skill

用 Obsidian 兼容的双链笔记构建大模型知识库。

## 快速开始

```bash
# 设置 vault 路径（默认当前目录 vault/）
export OBSIDIAN_VAULT=./vault

# 创建笔记
python3 scripts/obsidian_kb.py new "笔记标题" --type concept

# 搜索
python3 scripts/obsidian_kb.py search "关键词"

# 知识库问答（检索相关上下文给 LLM）
python3 scripts/obsidian_kb.py ask "xv6 的进程调度是怎么实现的？"
```

## 命令一览

| 命令 | 说明 | 示例 |
|------|------|------|
| `new <title>` | 创建新笔记 | `new "页表机制" -t concept` |
| `link <src> <tgt>` | 建立双向链接 | `link "进程管理" "页表机制"` |
| `search <query>` | 关键词搜索 | `search "调度"` |
| `backlinks <title>` | 查找反向链接 | `backlinks "页表机制"` |
| `moc` | 更新 MOC 总索引 | `moc` |
| `ask <question>` | 知识库问答检索 | `ask "中断怎么处理"` |
| `graph` | 显示链接关系图 | `graph` |

### 参数

- `--vault <path>` / `-v`：指定 vault 目录路径（或设置 `OBSIDIAN_VAULT` 环境变量）
- `--type <concept|paper|code|project>`：笔记类型（仅 new 命令）

## 笔记类型与模板

| 类型 | 目录 | 用途 |
|------|------|------|
| concept | concepts/ | 概念、原理、机制 |
| paper | papers/ | 论文笔记 |
| code | code/ | 代码片段、技巧 |
| project | projects/ | 项目相关 |

模板位于 `_templates/` 目录，自动填入 title、date 等 frontmatter。

## 笔记格式规范

```markdown
---
title: "标题"
tags: [tag1, tag2]
aliases: ["别名"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# 标题

正文内容...

## 关联
- [[相关笔记1]] — 简述
- [[相关笔记2]] — 简述

## 关键结论
> 一句话核心
```

**规范要点：**
- frontmatter 的 tags 统一用英文，方便跨语言检索
- `[[wikilink]]` 与 Obsidian 完全兼容
- 「关键结论」区块方便 LLM 快速抓取核心信息
- 每篇笔记保持原子性（一个主题）

## Agent 工作流

### 写笔记
1. `new` 创建笔记
2. 阅读源码/资料，填充内容
3. 用 `[[链接]]` 关联已有笔记
4. `moc` 更新索引

### 问答检索
1. 用户提问 → `ask` 检索相关笔记
2. 返回的上下文作为 LLM prompt 的一部分
3. 基于上下文生成回答，引用笔记来源

### 日常维护
1. 定期 `moc` 更新总索引
2. `graph` 检查链接是否完整
3. 新笔记添加后 `backlinks` 检查关联

## 目录结构

```
vault/
├── MOC.md                    # 自动生成的总索引
├── _templates/               # 笔记模板
│   ├── concept.md
│   ├── paper.md
│   ├── code.md
│   └── project.md
├── concepts/                 # 概念笔记
├── papers/                   # 论文笔记
├── code/                     # 代码笔记
└── projects/                 # 项目笔记
```

## Obsidian 兼容性

- ✅ YAML frontmatter
- ✅ `[[wikilink]]` 双向链接
- ✅ `[[笔记|别名]]` 带别名的链接
- ✅ `#tag` 标签系统
- ✅ 标准 Markdown 渲染
- ⚠️ Obsidian 特有插件语法（如 Dataview、Canvas）不兼容
