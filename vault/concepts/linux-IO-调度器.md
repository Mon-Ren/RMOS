---
title: "Linux IO 调度器"
tags: [linux, io, scheduler, disk, mq-deadline, bfq]
aliases: [IO调度器, mq-deadline, bfq, kyber, IO调度]
created: 2026-04-05
updated: 2026-04-05
---

# Linux IO 调度器

IO 调度器决定磁盘 IO 请求的排序和合并策略，影响读写延迟和吞吐量。

## 调度器类型

| 调度器 | 特点 | 适用场景 |
|--------|------|----------|
| none | 无调度，直通 | NVMe SSD |
| mq-deadline | 按截止时间排序 | 通用 SSD/HDD |
| bfq | 公平带宽分配 | 桌面、交互式 |
| kyber | 低延迟，令牌限流 | 高速 NVMe |

## 查看和切换

```bash
# 查看当前调度器
cat /sys/block/sda/queue/scheduler
# [mq-deadline] none bfq kyber

# 临时切换
echo bfq > /sys/block/sda/queue/scheduler

# 持久化（udev 规则）
# /etc/udev/rules.d/60-io-scheduler.rules
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/scheduler}="mq-deadline"
ACTION=="add|change", KERNEL=="nvme[0-9]*", ATTR{queue/scheduler}="none"
```

## 调度器原理

### mq-deadline

```
读请求截止时间: 500ms（默认）
写请求截止时间: 5000ms（默认）

1. 合并相邻 IO
2. 按 LBA（逻辑块地址）排序
3. 超时请求提升优先级
```

### bfq（Budget Fair Queueing）

```
每个进程分配 IO 预算（budget）：
- 按预算轮流服务
- 交互式进程优先
- 减少桌面卡顿
```

## IO 参数调优

```bash
# 队列深度
cat /sys/block/sda/queue/nr_requests
echo 128 > /sys/block/sda/queue/nr_requests

# 预读
cat /sys/block/sda/queue/read_ahead_kb
echo 128 > /sys/block/sda/queue/read_ahead_kb

# 合并相邻请求
cat /sys/block/sda/queue/rotational    # 1=HDD, 0=SSD
```

## 关联
- [[linux-性能分析工具]] — iostat 监控 IO 性能
- [[linux-磁盘与分区管理]] — 磁盘和分区基础

## 关键结论

> NVMe 使用 none（无调度），因为 NVMe 本身的并行性比内核调度器更优。SSD 用 mq-deadline，桌面 HDD 用 bfq。
