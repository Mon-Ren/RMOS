---
title: Linux grep 高级用法
tags: [linux, grep, regex, text, search]
aliases: [grep高级, egrep, fgrep, PCRE, 正则搜索]
created: 2026-04-05
updated: 2026-04-05
---

# Linux grep 高级用法

grep 除了基础搜索外，还有很多强大的高级用法。

## 正则模式

```bash
# 基础正则（BRE，默认）
grep "err\|warn" file           # BRE 中 | 需要转义

# 扩展正则（ERE，-E）
grep -E "err|warn" file         # 不用转义
grep -E "^[[:space:]]*" file    # POSIX 字符类

# Perl 正则（PCRE，-P，最强大）
grep -P "\d{3}-\d{4}" file      # \d 数字
grep -P "(?<=error: ).*" file   # 正向后行断言
grep -P "\t" file               # 制表符
```

## 上下文控制

```bash
grep -B 5 -A 10 "error" log     # 匹配前5行、后10行
grep -C 3 "error" log           # 前后各3行
grep -n "error" log             # 显示行号
grep -H "error" log             # 显示文件名
grep -l "error" *.log           # 只显示匹配的文件名
grep -L "error" *.log           # 只显示不匹配的文件名
```

## 高级技巧

```bash
# 递归搜索，排除目录
grep -r --exclude-dir={.git,node_modules} "TODO" .
grep -r --include="*.py" "import os" .

# 只输出匹配部分
grep -oP "\d+\.\d+\.\d+\.\d+" log     # 提取所有 IP 地址
grep -oP "(?<=user=)\w+" log           # 提取 user= 后面的单词

# 多模式匹配
grep -e "error" -e "fatal" log         # 多个 -e
grep -f patterns.txt log               # 从文件读取模式

# 统计
grep -c "error" log                    # 匹配行数
grep -c "" log                         # 总行数

# 二进制文件
grep -a "string" binary.dat            # 当作文本处理
grep -I "string" binary.dat            # 跳过二进制文件
```

## 关键要点

> `-P`（PCRE）是 grep 最强模式，支持零宽断言、非贪婪匹配等高级特性，但不是所有系统默认支持。

> `grep -o` 只输出匹配部分，配合正则可以做文本提取，效果类似 sed/awk。

## 相关笔记

- [[Linux 文本处理三剑客]] — grep/sed/awk 基础
- [[Linux 管道与重定向]] — 管道组合
