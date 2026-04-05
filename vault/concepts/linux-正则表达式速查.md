---
title: Linux 正则表达式速查
tags: [linux, regex, grep, sed, awk, pcre]
aliases: [正则表达式, regex, BRE, ERE, PCRE, 字符匹配]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 正则表达式速查

正则表达式是文本处理的基础，Linux 工具中分 BRE/ERE/PCRE 三种模式。

## 基础匹配

| 符号 | 含义 | 示例 |
|------|------|------|
| `.` | 任意字符 | `a.c` → abc, a1c |
| `*` | 前一个字符 0+ 次 | `ab*c` → ac, abc, abbc |
| `^` | 行首 | `^Hello` |
| `$` | 行尾 | `world$` |
| `[]` | 字符类 | `[abc]` → a 或 b 或 c |
| `[^]` | 排除 | `[^0-9]` → 非数字 |
| `\` | 转义 | `\.` → 字面点号 |

## 扩展正则（ERE / grep -E）

| 符号 | 含义 | 示例 |
|------|------|------|
| `+` | 1+ 次 | `ab+c` → abc, abbc |
| `?` | 0 或 1 次 | `colou?r` → color, colour |
| `|` | 或 | `cat\|dog` |
| `()` | 分组 | `(ab)+` |
| `{n,m}` | 重复 | `a{2,4}` → aa, aaa, aaaa |

## POSIX 字符类

```
[:alnum:]    字母数字
[:alpha:]    字母
[:digit:]    数字
[:lower:]    小写字母
[:upper:]    大写字母
[:space:]    空白字符
[:punct:]    标点符号
```

```bash
grep '[[:digit:]]\+' file      # 匹配数字（BRE）
grep -E '[[:digit:]]+' file    # ERE
```

## Perl 正则（PCRE / grep -P）

| 符号 | 含义 | 示例 |
|------|------|------|
| `\d` | 数字 | `\d{3}` |
| `\w` | 单词字符 | `\w+` |
| `\s` | 空白 | `\s+` |
| `(?=)` | 正向前行 | `foo(?=bar)` |
| `(?<=)` | 正向后行 | `(?<=user=)\w+` |
| `(?!)` | 负向前行 | `foo(?!bar)` |
| `(?<!)` | 负向后行 | `(?<!\d)\d+` |

## 常用模式

```bash
# IP 地址
grep -P '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# Email
grep -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# URL
grep -P 'https?://[^\s]+'

# 日期 YYYY-MM-DD
grep -P '\d{4}-\d{2}-\d{2}'
```

## 关键要点

> BRE 中 `+?|{}` 需要转义，ERE 中不需要。PCRE 功能最强但不是所有系统默认支持。

> 写正则时先用 `grep -oP` 测试匹配结果，确认无误再用于 sed/awk。

## 相关笔记

- [[Linux grep 高级用法]] — grep 正则应用
- [[Linux 文本处理三剑客]] — grep/sed/awk 基础
