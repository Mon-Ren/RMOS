---
title: Linux find 命令
tags: [linux, find, search, filesystem, 命令]
aliases: [find, 文件查找, locate, 文件搜索]
created: 2026-04-05
updated: 2026-04-05
---

# Linux find 命令

find 是最强大的文件搜索工具，支持按名称、类型、大小、时间等多维度查找。

## 基本语法

```bash
find [路径] [条件] [动作]
```

## 按名称查找

```bash
find /var/log -name "*.log"              # 精确匹配文件名
find /var/log -iname "*.log"             # 忽略大小写
find / -name "nginx.conf" 2>/dev/null    # 全局搜索，忽略错误
find . -name "*.tmp" -o -name "*.bak"    # 多条件 OR
```

## 按类型和时间

```bash
find / -type f -name "*.conf"            # 只找文件
find / -type d -name "config"            # 只找目录
find . -type l                           # 只找符号链接

# 时间条件
find /var/log -mtime -7                  # 最近 7 天修改的
find /tmp -mtime +30                     # 30 天前修改的
find . -newer reference.txt              # 比 reference.txt 新的
find / -mmin -30                         # 30 分钟内修改的
```

## 按大小

```bash
find / -size +100M                       # 大于 100MB
find /tmp -size 0                        # 空文件
find . -size +10M -size -50M             # 10M~50M 之间
```

## 执行动作

```bash
# -exec 逐个执行
find . -name "*.tmp" -exec rm {} \;
find . -name "*.txt" -exec wc -l {} \;

# -exec 批量执行（更快）
find . -name "*.tmp" -exec rm {} +
find . -name "*.log" -exec grep "error" {} +

# -print0 配合 xargs（处理空格文件名）
find . -name "*.txt" -print0 | xargs -0 wc -l

# -delete 动作
find /tmp -mtime +7 -delete              # 删除 7 天前的临时文件

# -ls 列出详细信息
find /etc -name "*.conf" -ls
```

## 关键要点

> `find -exec {} \;` 会对每个文件执行一次命令，`find -exec {} +` 会批量合并执行。后者性能好得多。

> `find . -name "*.log" -delete` 不需要 `-exec`，`-delete` 本身就是动作。但注意 `-delete` 会自动开启 `-depth`。

## 相关笔记

- [[Linux 文件操作基础命令]] — cp/mv/rm
- [[Linux 文本处理三剑客]] — grep/sed/awk
