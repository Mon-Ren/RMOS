---
title: Linux Shell 基础语法
tags: [linux, shell, bash, script, 基础]
aliases: [bash, shell脚本, shell语法, 变量, 条件判断, 循环]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Shell 基础语法

Shell 脚本是 Linux 自动化的核心工具，掌握 bash 语法是系统管理和 DevOps 的基础。

## 脚本结构

```bash
#!/bin/bash
# 脚本说明
set -euo pipefail             # 严格模式：出错即退出、未定义变量报错

echo "Hello, $1"
```

## 变量

```bash
name="alice"                  # 赋值（无空格）
echo "$name"                  # 使用变量
echo "${name}s"               # 花括号消除歧义
readonly PI=3.14              # 只读变量
unset name                    # 删除变量

# 特殊变量
$0    # 脚本名称
$1-$9 # 位置参数
$#    # 参数个数
$@    # 所有参数（分别引用）
$*    # 所有参数（整体引用）
$?    # 上一条命令退出码
$$    # 当前 PID
```

## 条件判断

```bash
# test 命令 / [ ]
[ -f "/etc/passwd" ] && echo "文件存在"
[ -d "/tmp" ] && echo "目录存在"
[ -z "$var" ] && echo "变量为空"
[ "$a" = "$b" ] && echo "相等"
[ "$a" -gt 5 ] && echo "大于5"

# [[ ]] (bash 增强)
[[ "$file" == *.txt ]] && echo "是 txt 文件"
[[ "$str" =~ ^[0-9]+$ ]] && echo "是数字"

# if-elif-else
if [[ -f "$1" ]]; then
    echo "文件: $1"
elif [[ -d "$1" ]]; then
    echo "目录: $1"
else
    echo "未知: $1"
fi
```

## 循环

```bash
# for 循环
for i in {1..10}; do echo $i; done
for file in *.txt; do wc -l "$file"; done
for ((i=0; i<10; i++)); do echo $i; done

# while 循环
while read -r line; do
    echo "$line"
done < file.txt

# case 语句
case "$1" in
    start) echo "启动" ;;
    stop)  echo "停止" ;;
    *)     echo "用法: $0 {start|stop}" ;;
esac
```

## 关键要点

> `set -euo pipefail` 是生产脚本的必备开头：`-e` 遇错退出，`-u` 未定义变量报错，`-o pipefail` 管道中任何命令失败都算失败。

> `[ ]` 是 POSIX 标准，`[[ ]]` 是 bash 增强（支持正则、逻辑运算），脚本中推荐用 `[[ ]]`。

## 相关笔记

- [[Linux 管道与重定向]] — 输入输出控制
- [[Linux 文本处理三剑客]] — grep/sed/awk
