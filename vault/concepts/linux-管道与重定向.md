---
title: Linux 管道与重定向
tags: [linux, pipe, redirect, shell, stdin, stdout]
aliases: [管道, 重定向, pipe, redirect, stdin, stdout, stderr]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 管道与重定向

管道和重定向是 Linux 命令行的灵魂，将小工具组合成强大工作流。

## 文件描述符

| FD | 名称 | 含义 |
|----|------|------|
| 0 | stdin | 标准输入 |
| 1 | stdout | 标准输出 |
| 2 | stderr | 标准错误 |

## 重定向

```bash
# 输出重定向
echo "hello" > file.txt          # 覆盖写入
echo "world" >> file.txt         # 追加写入
cmd 2> errors.log                # 错误输出重定向
cmd &> all.log                   # 所有输出重定向
cmd > out.log 2>&1               # 等价于 &>（顺序重要）
cmd 2>/dev/null                  # 丢弃错误输出

# 输入重定向
sort < unsorted.txt              # 从文件读取输入
wc -l < file.txt                 # 统计行数
cat << EOF
多行文本
EOF
```

## 管道

```bash
# 管道将前一个命令的 stdout 作为后一个命令的 stdin
cat file.txt | grep "error" | wc -l
ps aux | grep nginx | awk '{print $2}' | xargs kill
find /var/log -name "*.log" | head -5

# 管道只传递 stdout，stderr 不经过管道
cmd1 2>&1 | cmd2                 # 合并 stderr 到管道
cmd1 |& cmd2                     # bash 简写
```

## xargs

```bash
# 将 stdin 转为命令行参数
find . -name "*.tmp" | xargs rm -f
echo "file1 file2 file3" | xargs ls -l
cat urls.txt | xargs -I {} curl -O {}

# 处理含空格文件名
find . -name "*.txt" -print0 | xargs -0 rm
```

## 关键要点

> `2>&1` 必须写在 `>` 之后，如 `cmd > file 2>&1`。写成 `cmd 2>&1 > file` 则 stderr 仍然输出到终端。

> 管道 `|` 只传递 stdout，stderr 默认忽略。用 `|&` 或 `2>&1 |` 合并两者。

## 相关笔记

- [[Linux 文本处理三剑客]] — grep/sed/awk 管道组合
- [[Linux Shell 基础语法]] — 变量、条件、循环
