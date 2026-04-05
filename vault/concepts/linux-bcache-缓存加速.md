---
title: "Linux bcache 缓存加速"
tags: [linux, bcache, ssd, cache, storage]
aliases: [bcache, SSD缓存, 分级存储, 缓存加速]
created: 2026-04-05
updated: 2026-04-05
---

# Linux bcache 缓存加速

bcache 使用 SSD 作为 HDD 的缓存层，自动将热点数据缓存到 SSD 提升读写性能。

## 架构

```
应用 → bcache 设备 → SSD 缓存（命中？读SSD）
                          ↓ 未命中
                      HDD 后端（读HDD，写回SSD）
```

## 配置

```bash
# 安装（内核默认支持）
modprobe bcache

# 创建后端设备（HDD）
make-bcache -B /dev/sdb

# 创建缓存设备（SSD）
make-bcache -C /dev/nvme0n1

# 关联
echo <cache_set_uuid> > /sys/block/bcache0/bset/attach

# 挂载
mkfs.ext4 /dev/bcache0
mount /dev/bcache0 /mnt/data
```

## 缓存模式

```bash
# writethrough（安全）：写同时写 SSD 和 HDD
echo writethrough > /sys/block/bcache0/cache_mode

# writeback（快速）：写只到 SSD，后台回写 HDD
echo writeback > /sys/block/bcache0/cache_mode

# writearound：只缓存读
echo writearound > /sys/block/bcache0/cache_mode

# none：禁用缓存
echo none > /sys/block/bcache0/cache_mode
```

## 监控

```bash
# 缓存统计
cat /sys/block/bcache0/bset/stats_total/*
# 缓存命中率
cat /sys/block/bcache0/bset/stats_total/cache_hits
cat /sys/block/bcache0/bset/stats_total/cache_misses
```

## 关联
- [[linux-LVM-逻辑卷管理]] — LVM cache 是替代方案
- [[linux-Btrfs-文件系统]] — Btrfs 自带 SSD 缓存优化

## 关键结论

> bcache 的 writeback 模式性能最好但有数据丢失风险（SSD 故障时未回写的数据丢失）。生产环境建议用 writethrough（安全）或 LVM cache 作为替代。
