---
title: "Linux OOM 调优与内存保护"
tags: [linux, oom, memory, cgroup, protection]
aliases: [OOM调优, oom_score, 内存保护, memory.low, memory.min]
created: 2026-04-05
updated: 2026-04-05
---

# Linux OOM 调优与内存保护

OOM Killer 在内存耗尽时选择进程杀死，正确配置可以保护关键进程不被误杀。

## OOM 评分机制

```bash
# 查看进程 OOM 分数
cat /proc/<pid>/oom_score       # 0-1000+（越大越容易被杀）
cat /proc/<pid>/oom_score_adj   # -1000 到 1000（用户调整）

# 保护关键进程
echo -900 > /proc/<pid>/oom_score_adj   # 几乎不会被杀
echo -1000 > /proc/1/oom_score_adj      # 完全保护

# 优先杀测试进程
echo 1000 > /proc/<pid>/oom_score_adj
```

## cgroup v2 内存保护

```bash
# memory.min：硬保护（保证最小内存）
echo "256M" > /sys/fs/cgroup/production/memory.min

# memory.low：软保护（尽力保护）
echo "512M" > /sys/fs/cgroup/production/memory.low

# memory.max：硬限制
echo "2G" > /sys/fs/cgroup/production/memory.max

# memory.high：软限制（触发回收但不 OOM）
echo "1G" > /sys/fs/cgroup/production/memory.high
```

## 保护层级

```
cgroup A: memory.min = 512M  ← 硬保证
cgroup B: memory.low = 256M  ← 软保护（剩余内存时）
cgroup C: 无保护              ← 先被回收
```

## OOM 日志分析

```bash
# 查看 OOM 事件
dmesg | grep -i "oom\|killed"
journalctl -k | grep -i oom

# 分析：谁被杀、为什么
# oom-kill: constraint=CONSTRAINT_MEMCG  → cgroup 限制触发
# oom-kill: constraint=CONSTRAINT_NONE   → 全局内存不足
```

## 关联
- [[linux-内存管理基础]] — free/swap/OOM 基础
- [[linux-cgroup-资源限制]] — cgroup 内存限制

## 关键结论

> cgroup v2 的 memory.min 是"硬保证"：即使其他 cgroup OOM，也会保留这部分内存。memory.low 是"软保护"：有剩余内存时优先保护，但压力大时可回收。数据库和关键服务应设置 memory.min。
