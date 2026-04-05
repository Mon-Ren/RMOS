---
title: Linux sed 高级用法
tags: [linux, sed, text, regex, stream]
aliases: [sed高级, 流编辑, sed命令]
created: 2026-04-05
updated: 2026-04-05
---

# Linux sed 高级用法

sed（Stream Editor）除基础替换外，支持地址范围、多命令、保持空间等高级功能。

## 地址范围

```bash
# 行号范围
sed '1,5d' file                  # 删除 1-5 行
sed '10,$ s/foo/bar/' file       # 第 10 行到末尾替换

# 正则范围
sed '/start/,/end/d' file        # 删除 start 到 end 之间的行
sed '/^#/,/^$/d' file            # 删除注释块

# 否定
sed '/pattern/!d' file           # 只保留匹配行
```

## 多命令组合

```bash
# -e 多命令
sed -e 's/foo/bar/' -e 's/old/new/' file

# 分号
sed 's/foo/bar/; s/old/new/' file

# 花括号分组
sed '/pattern/{ s/a/b/; s/c/d/; }' file

# -f 从文件读取命令
sed -f script.sed file
```

## 插入与修改

```bash
sed '3i\第三行前插入' file        # 在第3行前插入
sed '3a\第三行后插入' file        # 在第3行后追加
sed '3c\替换整行' file           # 替换第3行整行
sed '$a\最后一行后追加' file     # 文件末尾追加
```

## 保持空间（高级）

```bash
# h/H: 保持空间 ← 模式空间（覆盖/追加）
# g/G: 模式空间 ← 保持空间（覆盖/追加）
# x: 交换

# 倒序输出
sed -n '1!G; h; $p' file

# 每两行合并
sed 'N;s/\n/ /' file

# 交换相邻行
sed 'N;s/\(.*\)\n\(.*\)/\2\n\1/' file
```

## 实用示例

```bash
# 删除行尾空白
sed 's/[[:space:]]*$//' file

# 删除空行
sed '/^$/d' file

# 在每行前加行号
sed = file | sed 'N;s/\n/\t/'

# 替换换行符为逗号
sed ':a; N; $!ba; s/\n/, /g' file

# 去掉 HTML 标签
sed 's/<[^>]*>//g' file
```

## 关键要点

> sed 默认输出到 stdout，不修改原文件。加 `-i` 才原地修改，建议先测试再加 `-i`。

> sed 的正则是 BRE（基础正则），加 `-E` 或 `-r` 启用 ERE（扩展正则），无需转义 `+?|{}()`。

## 相关笔记

- [[Linux 文本处理三剑客]] — grep/sed/awk 基础
- [[Linux awk 高级用法]] — awk 进阶
