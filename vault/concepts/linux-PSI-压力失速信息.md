---
title: "Linux PS 压力失速信息"
tags: [linux, psi, pressure, stall, monitoring]
aliases: [PSI, Pressure Stall Information, 压力监控, 资源压力]
created: 2026-04-05
updated: 2026-04-05
---

# Linux PSI 压力失速信息

PSI（Pressure Stall Information）是 Linux 4.20+ 引入的资源压力度量，量化 CPU/内存/IO 资源不足导致的任务延迟。

## 核心概念

```
some: 至少一个任务因资源不足被延迟
full: 所有任务都因资源不足被延迟（系统级瓶颈）
```

## 查看 PSI

```bash
# 系统级
cat /proc/pressure/cpu
cat /proc/pressure/memory
cat /proc/pressure/io

# 输出格式
some avg10=1.23 avg60=0.45 avg300=0.12 total=12345678
full avg10=0.00 avg60=0.00 avg300=0.00 total=0

# avg10/60/300: 10秒/60秒/300秒平均压力百分比
# total: 累计微秒数
```

## cgroup PSI

```bash
# cgroup 级别
cat /sys/fs/cgroup/myapp/memory.pressure
cat /sys/fs/cgroup/myapp/cpu.pressure
cat /sys/fs/cgroup/myapp/io.pressure
```

## 监控触发

```bash
# 监听压力事件（阻塞等待）
# 当 avg10 > 阈值时触发
cat > /proc/pressure/memory << EOF
some 1000000 60000000
full 1000000 60000000
EOF
# some: 阈值 10% (1000000us)，窗口 60s
# 触发后 poll() /proc/pressure/memory 返回可读
```

## oomd 使用 PSI

```bash
# oomd 基于 PSI 决策
# /etc/systemd/oomd.conf
[OOM]
DefaultMemoryPressureLimit=60%
DefaultMemoryPressureDurationSec=30
```

## 关联
- [[linux-oomd-系统级-OOM-守护进程]] — oomd 使用 PSI
- [[linux-性能分析工具]] — 综合性能监控

## 关键结论

> PSI 比 load average 更精确地反映资源压力：load average 只看 CPU，PSI 覆盖 CPU/内存/IO 三个维度且区分"部分受影响"和"完全受影响"。oomd 和 Kubernetes 都使用 PSI 做调度决策。
