---
title: "Linux DAMON 内存监控"
tags: [linux, damon, memory, monitoring, profiling]
aliases: [DAMON, 数据访问监控, 内存访问分析, 冷热页]
created: 2026-04-05
updated: 2026-04-05
---

# Linux DAMON 内存监控

DAMON（Data Access MONitor）是 Linux 5.15+ 引入的轻量级内存访问监控框架，用于分析应用的内存访问模式。

## 架构

```
DAMON 核心
├─ Region-based sampling（自适应采样）
├─ 访问频率统计
└─ 冷热页识别
    ├─ DAMOS：自动优化（回收冷页、预取热页）
    └─ 用户空间：报告/分析
```

## 使用方式

```bash
# 通过 debugfs
cd /sys/kernel/debug/damon

# 目标进程
echo 1234 > attrs/target_id    # PID

# 参数设置
echo 5000 100000 100 1000 > attrs/scheme
# min/max region, 采样间隔, 聚合间隔

# 启动
echo on > attrs/state

# 查看访问模式
cat monitoring/target_regions
```

## DAMOS（自动优化）

```bash
# 自动回收冷页（access frequency < 阈值）
echo "pageout 100 1000 0 0 0 0 0 0 10 0" > schemes
# 含义：pageout 动作，每 100ms 采样，连续 1000ms 访问 < 0% 的页回收
```

## 应用场景

- **冷热页分析**：识别工作集大小
- **自动内存回收**：DAMOS 回收不访问的页
- **NUMA 优化**：将热页移到本地节点
- **内存泄漏检测**：观察访问频率变化

## 关联
- [[linux-内存管理基础]] — 内存管理
- [[linux-huge-pages-大页内存]] — 大页管理

## 关键结论

> DAMON 是"内存访问的 perf"：低开销地监控哪些内存页被访问、多频繁。DAMOS 可以自动基于访问模式回收冷页，在容器和虚拟化场景中显著节省内存。
