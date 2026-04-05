---
title: Linux LVM 逻辑卷管理
tags: [linux, lvm, storage, pv, vg, lv]
aliases: [LVM, 逻辑卷, pvcreate, vgcreate, lvcreate, 存储管理]
created: 2026-04-05
updated: 2026-04-05
---

# Linux LVM 逻辑卷管理

LVM（Logical Volume Manager）提供灵活的磁盘管理，支持动态调整大小、快照和跨磁盘卷。

## 三层架构

```
Physical Volume (PV) → Volume Group (VG) → Logical Volume (LV)
物理磁盘/分区          卷组（存储池）        逻辑卷（类似分区）
```

## 创建流程

```bash
# 1. 创建 PV
pvcreate /dev/sdb /dev/sdc
pvdisplay                      # 查看 PV
pvs                            # 简要信息

# 2. 创建 VG
vgcreate myvg /dev/sdb /dev/sdc
vgdisplay
vgs

# 3. 创建 LV
lvcreate -L 20G -n mylv myvg           # 指定大小
lvcreate -l 100%FREE -n mylv myvg      # 使用全部空间
lvdisplay
lvs

# 4. 格式化和挂载
mkfs.ext4 /dev/myvg/mylv
mount /dev/myvg/mylv /mnt/data
```

## 在线扩展

```bash
# 扩展 LV
lvextend -L +10G /dev/myvg/mylv
# 扩展文件系统
resize2fs /dev/myvg/mylv       # ext4
xfs_growfs /mnt/data           # XFS

# 一步到位
lvextend -r -L +10G /dev/myvg/mylv   # 自动 resize
```

## 缩减（ext4）

```bash
umount /mnt/data
e2fsck -f /dev/myvg/mylv
resize2fs /dev/myvg/mylv 15G
lvreduce -L 15G /dev/myvg/mylv
mount /dev/myvg/mylv /mnt/data
```

## 快照

```bash
lvcreate -s -n mylv_snap -L 1G /dev/myvg/mylv
mount /dev/myvg/mylv_snap /mnt/snapshot
# 用完删除
umount /mnt/snapshot
lvremove /dev/myvg/mylv_snap
```

## 关键要点

> LVM 最大优势是在线扩展：不停机就能扩大分区。`lvextend -r` 自动调整文件系统大小。

> XFS 文件系统只能扩展不能缩减，ext4 两者都支持但缩减需要先卸载。

## 相关笔记

- [[Linux 磁盘与分区管理]] — fdisk/mount
- [[Linux 文件系统层次标准]] — 目录结构
