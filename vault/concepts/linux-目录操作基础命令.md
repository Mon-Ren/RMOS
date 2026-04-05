---
title: Linux 目录操作基础命令
tags: [linux, filesystem, 基础命令, shell]
aliases: [cd, ls, pwd, mkdir, rmdir, 文件目录操作]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 目录操作基础命令

Linux 下一切皆文件，目录操作是最基础的技能。

## 核心命令

```bash
# 目录导航
pwd                    # 显示当前目录
cd /var/log            # 切换目录
cd -                   # 返回上一个目录
cd ~                   # 回到 home 目录

# 创建与删除
mkdir project          # 创建目录
mkdir -p a/b/c         # 递归创建
rmdir project          # 删除空目录
rm -rf project         # 强制删除（慎用）

# 列出文件
ls -la                 # 长格式含隐藏文件
ls -lh                 # 人类可读大小
ls -lt                 # 按修改时间排序
ls -R                  # 递归列出

# 目录树
tree -L 2              # 两层深度目录树
tree -d                # 只显示目录
```

## 特殊目录符号

| 符号 | 含义 |
|------|------|
| `.` | 当前目录 |
| `..` | 上级目录 |
| `~` | 当前用户 home |
| `-` | 上一个工作目录 |
| `$OLDPWD` | 上一个目录（环境变量） |

## 关键要点

> `mkdir -p` 是最常用的目录创建方式，自动创建中间目录，不会因已存在而报错。

> `ls -l` 输出的第一个字符：`d` 目录、`-` 普通文件、`l` 链接、`b` 块设备、`c` 字符设备。

## 相关笔记

- [[Linux 文件系统层次标准]] — FHS 目录结构
- [[Linux 硬链接与软链接]] — ln 命令
