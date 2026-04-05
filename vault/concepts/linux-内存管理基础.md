---
title: Linux 内存管理基础
tags: [linux, memory, swap, oom, 内存]
aliases: [内存管理, free, swap, OOM Killer, 虚拟内存]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 内存管理基础

Linux 内存管理涉及物理内存、虚拟内存、交换空间和 OOM Killer 等机制。

## 查看内存

```bash
free -h                        # 人类可读内存使用
cat /proc/meminfo              # 详细内存信息
vmstat 1                       # 每秒输出系统状态
smem -t                        # 进程实际内存使用（PSS）
```

## free 输出解读

```
              total    used    free    shared  buff/cache  available
Mem:          16Gi     4Gi    2Gi     256Mi      10Gi       11Gi
Swap:         4Gi      0Gi    4Gi
```

- **buff/cache**：内核缓冲区和页面缓存，可以回收
- **available**：实际可用内存（free + 可回收的 cache）
- **shared**：tmpfs 等共享内存

## Swap 管理

```bash
swapon --show                  # 查看 swap 使用
swapoff /dev/sdb2              # 禁用 swap
swapon /dev/sdb2               # 启用 swap

# 创建 swap 文件
dd if=/dev/zero of=/swapfile bs=1G count=4
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
# /etc/fstab: /swapfile none swap sw 0 0
```

## OOM Killer

当内存不足时，内核的 OOM Killer 会选择进程杀死：

```bash
# 查看 OOM 事件
dmesg | grep -i "oom\|killed process"
journalctl -k | grep -i oom

# 调整 OOM 优先级（-1000 到 1000）
echo -500 > /proc/<pid>/oom_score_adj   # 降低被杀概率
echo 1000 > /proc/<pid>/oom_score_adj   # 提高被杀概率（如测试进程）
echo -1000 > /proc/1/oom_score_adj      # 保护 PID 1
```

## 关键要点

> Linux 会尽量使用所有内存做缓存（buff/cache），所以 `free` 少不代表内存紧张，要看 `available`。

> OOM Killer 选择进程看 oom_score，值越大越容易被杀。重要进程应设置负的 oom_score_adj。

## 相关笔记

- [[Linux 进程基础与 ps 命令]] — 进程内存查看
- [[Linux 性能分析工具]] — vmstat/iostat/sar
