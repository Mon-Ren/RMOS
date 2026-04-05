---
title: "Linux OOMD 系统级 OOM 守护进程"
tags: [linux, oomd, systemd, memory, oom]
aliases: [oomd, systemd-oomd, 系统OOM, 主动OOM]
created: 2026-04-05
updated: 2026-04-05
---

# Linux OOMD 系统级 OOM 守护进程

systemd-oomd 是用户空间的 OOM 守护进程，在内核 OOM Killer 触发前主动干预，基于 cgroup 压力信息（PSI）做决策。

## 与内核 OOM Killer 的区别

| | 内核 OOM Killer | systemd-oomd |
|---|-----------------|-------------|
| 触发时机 | 内存耗尽 | PSI 压力超标 |
| 决策依据 | oom_score | cgroup 压力 + 内存使用 |
| 可配置性 | 有限 | cgroup 层级 |
| 保护机制 | oom_score_adj | memory.low/memory.min |

## 工作原理

```
PSI (Pressure Stall Information)
  → 内存压力 > 阈值（默认 60% 持续 30s）
  → oomd 检查各 cgroup
  → 选择压力最大/保护最小的 cgroup
  → 发送 SIGTERM → 等待 → SIGKILL
```

## 配置

```bash
# 启用
systemctl enable --now systemd-oomd

# cgroup 配置
# /etc/systemd/system/myapp.service.d/oomd.conf
[Service]
MemoryPressureWatch=skip      # 或 auto/split

# 全局阈值 (/etc/systemd/oomd.conf)
[OOM]
SwapUsedLimit=90%
DefaultMemoryPressureLimit=60%
DefaultMemoryPressureDurationSec=30
```

## PSI 监控

```bash
# 查看压力信息
cat /proc/pressure/memory
# some avg10=0.00 avg60=0.00 avg300=0.00 total=0
# full avg10=0.00 avg60=0.00 avg300=0.00 total=0

# cgroup PSI
cat /sys/fs/cgroup/myapp/memory.pressure
```

## 关联
- [[linux-OOM-调优与内存保护]] — oom_score/memory.min
- [[linux-cgroup-资源限制]] — cgroup 资源控制

## 关键结论

> oomd 的优势是"主动干预"：在系统彻底 OOM 之前，基于压力指标提前杀死最不重要的进程。配合 cgroup 的 memory.min 保护关键服务，比内核 OOM Killer 更可控。
