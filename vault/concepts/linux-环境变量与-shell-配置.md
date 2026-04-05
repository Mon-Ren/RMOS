---
title: Linux 环境变量与 shell 配置
tags: [linux, env, shell, bashrc, profile, 变量]
aliases: [环境变量, PATH, bashrc, profile, env, export]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 环境变量与 shell 配置

环境变量控制 shell 行为和程序运行环境，理解配置文件加载顺序很重要。

## 环境变量操作

```bash
# 查看
env                            # 所有环境变量
echo $PATH                     # 查看 PATH
printenv HOME                  # 查看指定变量

# 设置
export PATH="/usr/local/bin:$PATH"  # 追加 PATH
export EDITOR=vim              # 设置编辑器
export LANG=en_US.UTF-8        # 设置语言
unset VARIABLE                 # 删除变量

# 临时环境变量
VAR=value command              # 只对这条命令生效
```

## 常用环境变量

| 变量 | 用途 |
|------|------|
| PATH | 命令搜索路径 |
| HOME | 用户主目录 |
| USER | 用户名 |
| SHELL | 默认 shell |
| LANG | 系统语言 |
| TERM | 终端类型 |
| EDITOR | 默认编辑器 |
| PS1 | 命令提示符 |
| LD_LIBRARY_PATH | 动态库搜索路径 |

## 配置文件加载顺序

```
登录 shell：
/etc/profile → ~/.bash_profile → ~/.bash_login → ~/.profile

非登录交互 shell：
~/.bashrc

非交互 shell（脚本）：
$BASH_ENV 指定的文件
```

```bash
# ~/.bash_profile（推荐）
source ~/.bashrc               # 确保 bashrc 被加载
export PATH="$HOME/bin:$PATH"

# ~/.bashrc
alias ll='ls -la'
alias gs='git status'
PS1='\u@\h:\w\$ '
```

## 关键要点

> `/etc/profile` 是全局登录配置，`~/.bashrc` 是用户级交互配置。一般在 `~/.bash_profile` 里 source `~/.bashrc`。

> 修改 PATH 时把新路径放在前面（`NEW:$PATH`）优先级高于后面（`$PATH:NEW`）。

## 相关笔记

- [[Linux Shell 基础语法]] — Shell 脚本
- [[Linux sudo 与提权机制]] — sudo 环境变量
