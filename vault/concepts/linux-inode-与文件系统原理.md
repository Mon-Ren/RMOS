---
title: Linux inode 与文件系统原理
tags: [linux, filesystem, inode, ext4, block]
aliases: [inode, ext4, 文件系统, block, 超级块, 数据块]
created: 2026-04-05
updated: 2026-04-05
---

# Linux inode 与文件系统原理

Linux 文件系统（如 ext4）通过 inode 管理文件元数据和数据块位置。

## inode 结构

每个文件有一个 inode，存储：
- 文件类型和权限（mode）
- UID / GID
- 文件大小
- 时间戳（atime/mtime/ctime）
- 硬链接计数
- 数据块指针（直接 + 间接）

**不含**：文件名（文件名在目录条目中）

## 文件查找过程

```
文件名 → 目录条目 → inode → 数据块
```

```
/var/log/syslog
1. / (inode 2) → 找到 var 的 inode
2. var 目录条目 → 找到 log 的 inode
3. log 目录条目 → 找到 syslog 的 inode
4. syslog inode → 读取数据块
```

## 查看 inode

```bash
ls -li file                    # 查看 inode 号
stat file                      # 详细 inode 信息
df -i                          # 各分区 inode 使用情况
tune2fs -l /dev/sda1           # 文件系统 inode 信息
```

## ext4 结构

```
┌──────────┬──────────┬─────────────┬───────────┐
│ Boot     │ Super    │ Inode       │ Data      │
│ Block    │ Block    │ Table       │ Blocks    │
└──────────┴──────────┴─────────────┴───────────┘
```

- **Super Block**：文件系统元数据（总块数、inode 数、挂载次数）
- **Inode Table**：所有 inode 的数组
- **Data Blocks**：实际文件内容

## 硬链接与 inode

```bash
ln source.txt link.txt         # 创建硬链接
ls -li source.txt link.txt     # 两个文件名指向同一 inode
stat source.txt                # Links 计数 = 2
rm source.txt                  # 删除一个名字，Links -1
cat link.txt                   # 仍然可以访问
```

## 关键要点

> inode 在格式化时确定数量和大小，运行中无法增加。大量小文件可能耗尽 inode 但磁盘空间还有剩余。

> `df -i` 可以查看 inode 使用情况，和 `df -h`（空间使用）配合判断磁盘状态。

## 相关笔记

- [[Linux 硬链接与软链接]] — 链接与 inode
- [[Linux 磁盘与分区管理]] — 分区和格式化
