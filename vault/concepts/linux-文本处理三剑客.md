---
title: Linux 文本处理三剑客
tags: [linux, grep, sed, awk, text, shell]
aliases: [grep, sed, awk, 文本处理, 正则]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 文本处理三剑客

grep（查找）、sed（编辑）、awk（格式化处理）是 Linux 文本处理的三大利器。

## grep — 文本搜索

```bash
# 基础搜索
grep "error" /var/log/syslog           # 搜索包含 error 的行
grep -i "error" log.txt                # 忽略大小写
grep -r "TODO" /src/                   # 递归搜索目录
grep -n "error" log.txt                # 显示行号
grep -c "error" log.txt                # 统计匹配行数
grep -v "debug" log.txt                # 反选（排除 debug）

# 正则
grep -E "error|warn" log.txt           # 扩展正则（ERE）
grep -E "^[0-9]" file.txt              # 数字开头的行
grep -P "\d{3}-\d{4}" file.txt         # Perl 正则（PCRE）

# 上下文
grep -B 2 -A 3 "error" log.txt         # 匹配前后各2/3行
```

## sed — 流编辑器

```bash
# 替换
sed 's/old/new/' file.txt              # 每行首次替换
sed 's/old/new/g' file.txt             # 全局替换
sed -i 's/old/new/g' file.txt          # 原地修改（慎用）
sed -i.bak 's/old/new/g' file.txt      # 原地修改并备份

# 删除行
sed '3d' file.txt                      # 删除第 3 行
sed '/^#/d' file.txt                   # 删除注释行
sed '/^$/d' file.txt                   # 删除空行

# 插入与追加
sed '2i\新行内容' file.txt             # 第 2 行前插入
sed '2a\新行内容' file.txt             # 第 2 行后追加
```

## awk — 文本分析工具

```bash
# 打印列
awk '{print $1, $3}' file.txt          # 打印第1和第3列
awk -F: '{print $1}' /etc/passwd       # 自定义分隔符

# 条件过滤
awk '$3 > 100 {print $1, $3}' data.txt # 第3列>100
awk '/error/ {print}' log.txt          # 包含 error 的行

# 统计
awk '{sum += $1} END {print sum}' nums.txt  # 求和
awk '{print NR, $0}' file.txt              # 加行号

# 综合示例
awk -F: '{printf "%-15s %s\n", $1, $7}' /etc/passwd
```

## 关键要点

> grep 用于搜索，sed 用于编辑，awk 用于格式化提取——三者配合管道可处理绝大部分文本场景。

> `sed -i` 直接修改原文件，建议先不带 `-i` 确认结果正确后再执行。

## 相关笔记

- [[Linux 管道与重定向]] — 管道组合
- [[Linux 正则表达式速查]] — 正则语法
