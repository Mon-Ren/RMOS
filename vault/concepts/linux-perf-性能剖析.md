---
title: "Linux perf 性能剖析"
tags: [linux, perf, profiling, flamegraph, 性能]
aliases: [perf, perf record, perf report, 火焰图, 性能剖析]
created: 2026-04-05
updated: 2026-04-05
---

# Linux perf 性能剖析

perf 是 Linux 内核自带的性能分析工具，支持硬件计数器采样、追踪点和调用图分析。

## 基本使用

```bash
# 实时热点（类似 top 但看函数）
perf top
perf top -g                       # 带调用图

# 记录和报告
perf record -g ./app              # 记录程序执行
perf report                       # 查看报告
perf report --stdio               # 文本模式

# 系统级记录
perf record -a -g -- sleep 30     # 记录全系统 30 秒

# 特定事件
perf stat ./app                   # 统计各类事件
perf stat -e cache-misses,cache-references ./app
perf stat -e cycles,instructions ./app
```

## 硬件事件

```bash
# 查看可用事件
perf list

# 常用事件
perf stat -e cycles                    # CPU 周期
perf stat -e instructions             # 指令数
perf stat -e cache-misses             # 缓存未命中
perf stat -e branch-misses            # 分支预测失败
perf stat -e LLC-load-misses          # L3 缓存未命中
perf stat -e context-switches         # 上下文切换
```

## 火焰图

```bash
# 1. 记录
perf record -F 99 -g -p <pid> -- sleep 30

# 2. 折叠调用栈
perf script | stackcollapse-perf.pl > out.perf-folded

# 3. 生成火焰图
flamegraph.pl out.perf-folded > flamegraph.svg
```

## 追踪点

```bash
# 内核追踪点
perf probe --add tcp_sendmsg           # 添加探针
perf record -e probe:tcp_sendmsg -a
perf probe --del tcp_sendmsg           # 删除探针

# 用户空间追踪点
perf probe -x /usr/bin/app my_func     # 用户函数探针
```

## 关联
- [[linux-性能分析工具]] — top/vmstat/iostat 综合
- [[linux-BPF-与-eBPF]] — bpftrace 是 perf 的补充

## 关键结论

> `perf stat` 用硬件计数器看宏观指标（IPC、缓存命中率），`perf record -g` 用采样看微观热点函数。两者配合定位 CPU 性能瓶颈。火焰图是最直观的性能可视化方式。
