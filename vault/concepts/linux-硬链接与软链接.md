---
title: Linux 硬链接与软链接
tags: [linux, filesystem, ln, inode, hardlink, symlink]
aliases: [硬链接, 软链接, 符号链接, ln, hard link, soft link, symlink]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 硬链接与软链接

链接是文件系统中实现文件多路径访问的机制，分为硬链接和软链接两种。

## 硬链接（Hard Link）

硬链接是同一 inode 的多个目录条目，本质是同一个文件。

```bash
ln source.txt hardlink.txt     # 创建硬链接
ls -li source.txt              # 查看 inode 号
# 硬链接和原文件 inode 相同
```

**特点：**
- 共享同一 inode，修改任一文件，另一个同步变化
- 删除原文件，硬链接仍可访问（引用计数 -1）
- 不能跨文件系统
- 不能链接目录（root 也不行，防止循环）
- 不占用额外磁盘空间

## 软链接（Symbolic Link）

软链接是一个独立文件，内容是目标路径的字符串。

```bash
ln -s /usr/local/bin/tool tool  # 创建软链接
ls -la tool                    # 显示 -> 指向目标
readlink tool                  # 读取链接目标
```

**特点：**
- 独立 inode，有自己的权限
- 可以跨文件系统
- 可以链接目录
- 删除原文件后，软链接变成"悬空链接"（dangling link）
- 目标路径是相对路径时，相对于链接文件自身位置

## 对比

| 特性 | 硬链接 | 软链接 |
|------|--------|--------|
| inode | 相同 | 不同 |
| 跨文件系统 | ❌ | ✅ |
| 链接目录 | ❌ | ✅ |
| 原文件删除 | 仍可用 | 悬空 |
| 大小 | 不额外占用 | 存储路径字符串 |

## 关键要点

> 硬链接是"别名"，多个名字指向同一个 inode。软链接是"快捷方式"，存储目标路径。

> `ln` 不带 `-s` 创建硬链接，`ln -s` 创建软链接。日常使用软链接更多。

## 相关笔记

- [[Linux 文件系统层次标准]] — 目录结构
- [[Linux inode 与文件系统原理]] — inode 数据结构
