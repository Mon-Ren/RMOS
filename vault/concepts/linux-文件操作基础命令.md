---
title: Linux 文件操作基础命令
tags: [linux, filesystem, 基础命令, shell]
aliases: [cat, cp, mv, rm, touch, 文件操作]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 文件操作基础命令

文件的创建、复制、移动、删除是日常运维和开发的基本功。

## 核心命令

```bash
# 创建文件
touch file.txt             # 创建空文件或更新时间戳
echo "hello" > file.txt    # 创建并写入（覆盖）
echo "world" >> file.txt   # 追加内容

# 查看文件
cat file.txt               # 输出全部内容
less file.txt              # 分页查看（推荐）
head -n 20 file.txt        # 前 20 行
tail -n 20 file.txt        # 后 20 行
tail -f /var/log/syslog    # 实时追踪（日志常用）
wc -l file.txt             # 统计行数

# 复制
cp source.txt dest.txt         # 复制文件
cp -r src_dir/ dst_dir/        # 递归复制目录
cp -p file.txt backup.txt      # 保留权限和时间

# 移动/重命名
mv old.txt new.txt         # 重命名
mv file.txt /tmp/          # 移动文件

# 删除
rm file.txt                # 删除文件
rm -i file.txt             # 删除前确认
rm -rf dir/                # 强制递归删除（危险）
```

## 文件状态查看

```bash
stat file.txt              # 详细文件信息
file file.txt              # 文件类型检测
du -sh file.txt            # 文件大小
ls -i file.txt             # 查看 inode 号
```

## 关键要点

> `>` 是覆盖重定向，`>>` 是追加重定向。混淆两者可能导致数据丢失。

> `tail -f` 是运维必备命令，实时查看日志变化。

## 相关笔记

- [[Linux 文件权限与 chmod]] — 权限管理
- [[Linux 文本处理三剑客]] — grep/sed/awk
