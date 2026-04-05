---
title: "Linux tmpfs 与 ramdisk"
tags: [linux, tmpfs, ramdisk, memory, 虚拟文件系统]
aliases: [tmpfs, ramdisk, 内存文件系统, shm, /dev/shm]
created: 2026-04-05
updated: 2026-04-05
---

# Linux tmpfs 与 ramdisk

tmpfs 是基于内存的文件系统，内容存在 RAM 中（可被换出），重启清空。

## 基本使用

```bash
# 挂载 tmpfs
mount -t tmpfs -o size=1G tmpfs /mnt/ram

# /etc/fstab 持久化
tmpfs  /mnt/ram  tmpfs  size=1G,noatime,mode=1777  0  0

# 系统自动挂载的 tmpfs
df -h | grep tmpfs
# /dev/shm   → 共享内存（POSIX shm_open）
# /run       → 运行时数据
# /tmp       → 临时文件（部分发行版）
```

## 常见用途

```bash
# /dev/shm 共享内存
ls /dev/shm/

# /run 运行时文件
ls /run/          # PID 文件、socket 等

# 临时编译目录
mount -t tmpfs tmpfs /var/tmp/build
cd /var/tmp/build && make -j$(nproc)

# 测试数据库（内存中）
mkdir /mnt/pgtmpfs
mount -t tmpfs -o size=2G tmpfs /mnt/pgtmpfs
initdb -D /mnt/pgtmpfs
pg_ctl -D /mnt/pgtmpfs start
```

## 与 ramfs 的区别

| | tmpfs | ramfs |
|---|-------|-------|
| 大小限制 | ✅ size 参数 | ❌ 无限制，可能耗尽 RAM |
| 可换出 | ✅ 可以被 swap | ❌ 不可换出 |
| 满了 | 返回 ENOSPC | 可能系统卡死 |
| 推荐度 | ✅ 推荐 | ❌ 谨慎使用 |

## 大小调优

```bash
# 查看当前使用
df -h /dev/shm

# 调整大小
mount -o remount,size=4G /dev/shm

# /etc/fstab
tmpfs  /dev/shm  tmpfs  size=4G  0  0
```

## 关联
- [[linux-内存管理基础]] — tmpfs 消耗内存
- [[linux-虚拟内存与-mmap]] — tmpfs 支持 mmap

## 关键结论

> tmpfs 的内容在 RAM 中但可以被换出到 swap，所以不完全等于 ramdisk。默认 /dev/shm 大小是 RAM 的 50%。tmpfs 适合临时文件、编译目录、小规模缓存，不适合大数据存储。
