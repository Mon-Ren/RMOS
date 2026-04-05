---
title: "Linux Btrfs 文件系统"
tags: [linux, btrfs, filesystem, snapshot, cow]
aliases: [Btrfs, copy-on-write, 快照, 子卷, CoW文件系统]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Btrfs 文件系统

Btrfs（B-tree File System）是 Linux 的现代 CoW 文件系统，内置快照、压缩和多设备支持。

## 核心特性

- **CoW（Copy-on-Write）**：写入时复制，不覆盖原数据
- **快照**：瞬间创建，几乎零成本
- **子卷（Subvolume）**：轻量级隔离目录
- **透明压缩**：zstd/lzo/zlib
- **RAID**：软件 RAID 0/1/10/5/6
- **校验和**：数据完整性验证

## 基本操作

```bash
# 创建
mkfs.btrfs -L mydata /dev/sdb
mount -o compress=zstd /dev/sdb /mnt/data

# 子卷
btrfs subvolume create /mnt/data/@home
btrfs subvolume create /mnt/data/@snapshots
btrfs subvolume list /mnt/data

# 快照
btrfs subvolume snapshot /mnt/data/@home /mnt/data/@snapshots/home-2026-04-05
btrfs subvolume snapshot -r /mnt/data/@home /mnt/data/@snapshots/home-readonly

# 只读快照 → 可写
btrfs property set /mnt/data/@snapshots/home-readonly ro false
```

## 压缩

```bash
# 挂载时启用压缩
mount -o compress=zstd:3 /dev/sdb /mnt    # zstd 级别 3

# 持久化 (/etc/fstab)
UUID=xxx /mnt btrfs compress=zstd:3,subvol=@ 0 0

# 查看压缩效果
btrfs filesystem du -s /mnt/data
```

## 多设备与 RAID

```bash
# 添加设备
btrfs device add /dev/sdc /mnt/data
btrfs balance start -dconvert=raid1 /mnt/data

# 查看
btrfs filesystem show
btrfs device stats /mnt/data
```

## 关联
- [[linux-磁盘与分区管理]] — ext4/xfs 等传统文件系统
- [[linux-inode-与文件系统原理]] — 传统 inode 模型 vs Btrfs B-tree

## 关键结论

> Btrfs 的快照是 CoW 的：只记录变化的块，瞬间完成，适合系统回滚和备份。openSUSE 和 Fedora 默认使用 Btrfs，支持开机自动快照（snapper）。
