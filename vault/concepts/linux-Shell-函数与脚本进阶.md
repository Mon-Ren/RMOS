---
title: Linux Shell 函数与脚本进阶
tags: [linux, shell, bash, function, script, 进阶]
aliases: [bash函数, shell进阶, trap, 函数, 脚本调试]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Shell 函数与脚本进阶

Shell 函数和高级特性让脚本更模块化、更健壮。

## 函数

```bash
# 定义方式一
function greet() {
    echo "Hello, $1"
}

# 定义方式二（POSIX 兼容）
greet() {
    echo "Hello, $1"
    return 0
}

# 调用
greet "World"
name=$(greet "Alice")          # 捕获输出
```

## 局部变量

```bash
process() {
    local name="$1"            # local 声明局部变量
    local count=0
    ((count++))
    echo "$name: $count"
}
```

## 错误处理

```bash
set -euo pipefail

# trap 捕获错误和退出
cleanup() {
    rm -f /tmp/lockfile
    echo "清理完成"
}
trap cleanup EXIT              # 退出时清理
trap 'echo "第 $LINENO 行出错"' ERR  # 出错时提示

# 临时禁用 set -e
set +e
some_command_that_might_fail
result=$?
set -e

# || 提供默认值
value=$(get_config) || value="default"
```

## 数组

```bash
# 索引数组
files=("file1.txt" "file2.txt" "file3.txt")
echo "${files[0]}"             # 第一个
echo "${#files[@]}"            # 长度
echo "${files[@]}"             # 全部
for f in "${files[@]}"; do echo "$f"; done

# 关联数组（bash 4+）
declare -A config
config[host]="localhost"
config[port]="8080"
echo "${config[host]}"
for key in "${!config[@]}"; do echo "$key=${config[$key]}"; done
```

## 字符串操作

```bash
str="Hello World"
echo "${str:0:5}"              # 子串 → Hello
echo "${str/World/Shell}"      # 替换 → Hello Shell
echo "${#str}"                 # 长度 → 11
echo "${str^^}"                # 大写 → HELLO WORLD
echo "${str,,}"                # 小写 → hello world
echo "${str%.txt}.bak"         # 后缀替换
echo "${str#*/}"               # 删除最短前缀
echo "${str##*/}"              # 删除最长前缀
```

## 调试

```bash
bash -x script.sh              # 执行并打印每条命令
set -x                         # 脚本内开启调试
set +x                         # 关闭调试

# 自定义调试输出
DEBUG=1 ./script.sh
[[ "${DEBUG:-0}" == "1" ]] && echo "debug: variable=$var"
```

## 关键要点

> `local` 关键字只在函数内有效，声明局部变量避免污染全局作用域。

> `set -euo pipefail` 三件套：`-e` 出错退出、`-u` 未定义报错、`-o pipefail` 管道任何环节失败都算失败。

## 相关笔记

- [[Linux Shell 基础语法]] — 变量/条件/循环
- [[Linux 管道与重定向]] — IO 控制
