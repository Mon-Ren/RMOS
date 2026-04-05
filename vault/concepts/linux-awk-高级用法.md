---
title: Linux awk 高级用法
tags: [linux, awk, text, programming, report]
aliases: [awk高级, gawk, awk编程, 文本分析]
created: 2026-04-05
updated: 2026-04-05
---

# Linux awk 高级用法

awk 不仅是文本提取工具，更是一门完整的编程语言，支持变量、数组、函数和流程控制。

## awk 程序结构

```awk
BEGIN { 初始化 }
pattern { 每行处理 }
END { 收尾 }
```

## 内置变量

| 变量 | 含义 |
|------|------|
| `$0` | 整行 |
| `$1-$NF` | 第 1 到最后一个字段 |
| `NF` | 当前行字段数 |
| `NR` | 当前行号 |
| `FNR` | 当前文件行号（多文件时重置） |
| `FS` | 输入分隔符（默认空格） |
| `OFS` | 输出分隔符 |
| `FILENAME` | 当前文件名 |

## 数组与统计

```bash
# 分组统计
awk '{count[$1]++} END {for (k in count) print k, count[k]}' log
# 统计每个 IP 出现次数

# 求和与平均
awk '{sum+=$1; count++} END {print sum, sum/count}' nums.txt

# 去重（保持顺序）
awk '!seen[$0]++' file.txt

# 最大值
awk 'NR==1 || $1>max {max=$1} END {print max}' file
```

## 流程控制

```awk
# if-else
awk '{if ($3 > 100) print $1, "高"; else print $1, "低"}' data

# for 循环
awk '{for (i=1; i<=NF; i++) print NR, i, $i}' file

# while 循环
awk '{i=1; while(i<=NF) {print $i; i++}}' file
```

## 自定义函数

```awk
function factorial(n) {
    if (n <= 1) return 1
    return n * factorial(n-1)
}
BEGIN { print factorial(10) }
```

## 实用示例

```bash
# 格式化输出
awk -F: '{printf "%-15s UID:%-5s Shell:%s\n", $1, $3, $7}' /etc/passwd

# 合并两文件
awk 'NR==FNR {a[$1]=$2; next} {print $0, a[$1]}' file1 file2

# 提取 IP 并统计 Top 10
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 列转行
awk '{printf "%s%s", sep, $0; sep=", "} END {print ""}' file

# CSV 处理
awk -F, 'NR>1 {print $2, $5}' data.csv    # 跳过表头
```

## 关键要点

> awk 的数组是关联数组（类似 map），可以字符串做 key，非常适合分组统计。

> `!seen[$0]++` 是 awk 去重的黄金模式：第一次出现时 seen 为 0，取反为真，然后自增为 1，后续出现时取反为假。

## 相关笔记

- [[Linux 文本处理三剑客]] — grep/sed/awk 基础
- [[Linux 管道与重定向]] — 管道组合
