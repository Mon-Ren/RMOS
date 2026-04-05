---
title: "Linux Zram 压缩 swap"
tags: [linux, zram, swap, compression, memory]
aliases: [zram, 压缩交换, zramswap, 内存压缩]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Zram 压缩 swap

zram 在内存中创建压缩的块设备作为 swap，比磁盘 swap 快得多。

## 工作原理

```
内存页 → zram 压缩（LZ4/zstd）→ 压缩后存在 RAM 中
  4KB page → ~2KB（压缩后）→ 节省 50% 内存
```

## 配置

```bash
# 手动配置
modprobe zram
echo lz4 > /sys/block/zram0/comp_algorithm    # 压缩算法
echo 2G > /sys/block/zram0/disksize           # 大小
mkswap /dev/zram0
swapon /dev/zram0 -p 100                       # 优先级最高

# 使用 zram-generator（推荐）
apt install zram-generator

# /etc/systemd/zram-generator.conf
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
swap-priority = 100

systemctl daemon-reload
systemctl restart systemd-zram-setup@zram0
```

## 监控

```bash
# 查看状态
zramctl
cat /sys/block/zram0/mm_stat  # 原始大小 压缩后大小 等

# 指标解读
cat /sys/block/zram0/stat     # IO 统计
swapon --show                 # swap 设备优先级
```

## 算法对比

| 算法 | 压缩率 | 速度 |
|------|--------|------|
| lzo | 2:1 | 最快 |
| lz4 | 2:1 | 很快 |
| zstd | 2.5:1 | 快 |
| lz4hc | 2.1:1 | 中等 |

## 关联
- [[linux-内存管理基础]] — swap 基础
- [[linux-swappiness-与-swap-策略]] — swap 策略

## 关键结论

> zram 是无磁盘系统的最佳 swap 方案（如容器、嵌入式、云实例）。zstd 压缩算法在压缩率和速度之间取得最佳平衡。zram + zswap（内存中缓存压缩页）配合使用效果更好。
