---
title: Linux 性能分析工具
tags: [linux, performance, top, vmstat, iostat, sar]
aliases: [性能分析, top, vmstat, iostat, sar, mpstat, 系统监控]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 性能分析工具

Linux 提供了丰富的性能分析工具，覆盖 CPU、内存、磁盘、网络各个维度。

## CPU 分析

```bash
top / htop                       # 实时进程监控
mpstat -P ALL 1                  # 每个 CPU 核心使用率
sar -u 1 10                      # CPU 使用率（1秒间隔，10次）
uptime                           # 系统负载（1/5/15 分钟）
perf top                         # 实时热点函数
perf record -g ./app && perf report  # 采样分析
```

## 内存分析

```bash
free -h                          # 内存使用概况
vmstat 1                         # 虚拟内存统计
smem -t                          # 进程 PSS（实际内存占用）
pmap <pid>                       # 进程内存映射
cat /proc/<pid>/smaps            # 详细内存映射
valgrind --leak-check=full ./app # 内存泄漏检测
```

## 磁盘 I/O

```bash
iostat -xz 1                     # 磁盘 I/O（扩展统计）
iotop                            # 进程级 I/O 监控
hdparm -t /dev/sda               # 磁盘读速度测试
dd if=/dev/zero of=test bs=1M count=1024 oflag=direct  # 写速度
```

## 网络

```bash
iftop                            # 实时网络流量
nethogs                          # 按进程显示网络流量
sar -n DEV 1                     # 网卡流量统计
ss -s                            # 连接统计摘要
```

## 综合工具

```bash
dstat                            # CPU/磁盘/网络/内存综合
sar -A 1                         # 全面系统活动报告
nmon                             # 终端性能监控（交互式）
```

## 关键要点

> 性能排查顺序：`uptime`（负载）→ `top`（哪个进程）→ 具体工具（CPU/内存/IO/网络）。

> `iostat -xz` 的 `%util` 接近 100% 表示磁盘是瓶颈；`await` 高表示 I/O 响应慢。

## 相关笔记

- [[Linux 进程基础与 ps 命令]] — 进程管理
- [[Linux 内存管理基础]] — 内存管理
