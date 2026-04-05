---
title: Linux 磁盘与分区管理
tags: [linux, disk, partition, fdisk, mount, 存储]
aliases: [fdisk, mount, 分区, 磁盘管理, lsblk, blkid]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 磁盘与分区管理

Linux 磁盘管理涉及分区、格式化、挂载等操作，是系统管理的基础。

## 查看磁盘信息

```bash
lsblk                            # 列出所有块设备（树状）
lsblk -f                         # 显示文件系统类型
blkid                            # 显示所有分区的 UUID 和类型
df -h                            # 磁盘使用情况
du -sh /var/*                    # 目录大小
fdisk -l                         # 列出所有磁盘分区
```

## 分区操作

```bash
# fdisk 交互分区（MBR）
fdisk /dev/sdb
# m 帮助, n 新建, d 删除, p 打印, t 改类型, w 保存

# parted（GPT 支持）
parted /dev/sdb mklabel gpt
parted /dev/sdb mkpart primary ext4 0% 100%
```

## 格式化

```bash
mkfs.ext4 /dev/sdb1              # 格式化为 ext4
mkfs.xfs /dev/sdb1               # 格式化为 XFS
mkswap /dev/sdb2                 # 格式化为 swap
swapon /dev/sdb2                 # 启用 swap
```

## 挂载

```bash
mount /dev/sdb1 /mnt/data        # 临时挂载
umount /mnt/data                 # 卸载
mount -o ro /dev/sdb1 /mnt       # 只读挂载

# /etc/fstab 持久挂载
# <设备>  <挂载点>  <类型>  <选项>  <dump>  <fsck>
UUID=xxx  /mnt/data  ext4  defaults  0  2

# 验证 fstab
mount -a                         # 挂载所有 fstab 条目
```

## LVM 简介

```bash
pvcreate /dev/sdb                # 创建物理卷
vgcreate myvg /dev/sdb           # 创建卷组
lvcreate -L 10G -n mylv myvg     # 创建逻辑卷
mkfs.ext4 /dev/myvg/mylv         # 格式化
# 扩展
lvextend -L +5G /dev/myvg/mylv
resize2fs /dev/myvg/mylv
```

## 关键要点

> 挂载分区用 UUID 比用设备名更可靠，因为设备名（/dev/sdb）可能在重启后变化。

> 修改 `/etc/fstab` 后务必先 `mount -a` 测试，否则 fstab 错误可能导致系统无法启动。

## 相关笔记

- [[Linux 文件系统层次标准]] — 目录结构
- [[Linux inode 与文件系统原理]] — 文件系统内部原理
