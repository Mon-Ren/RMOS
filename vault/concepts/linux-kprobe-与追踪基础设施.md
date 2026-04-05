---
title: "Linux kprobe 与追踪基础设施"
tags: [linux, kprobe, ftrace, tracing, 内核追踪]
aliases: [kprobe, ftrace, 内核追踪, tracepoint, 追踪]
created: 2026-04-05
updated: 2026-04-05
---

# Linux kprobe 与追踪基础设施

Linux 内核追踪（tracing）基础设施提供多种探针机制，用于在内核运行时收集事件数据。

## 追踪机制对比

| 机制 | 性能开销 | 动态性 | 使用场景 |
|------|----------|--------|----------|
| tracepoint | 极低 | 静态（编译时定义） | 生产环境 |
| kprobe | 低 | 动态（任意函数） | 调试 |
| uprobe | 低 | 动态（用户函数） | 应用追踪 |
| ftrace | 低 | 静态 | 函数调用图 |

## tracefs 挂载

```bash
mount -t tracefs tracefs /sys/kernel/tracing
# 或
mount -t tracefs nodev /sys/kernel/tracing
```

## ftrace 使用

```bash
cd /sys/kernel/tracing

# 查看可用追踪器
cat available_tracers
# function_graph wakeup_rt nop

# 函数调用图追踪
echo function_graph > current_tracer
echo 1 > tracing_on
cat trace_pipe
echo 0 > tracing_on
cat trace

# 追踪特定函数
echo tcp_sendmsg > set_ftrace_filter
echo function > current_tracer
echo 1 > tracing_on
```

## kprobe 使用

```bash
cd /sys/kernel/tracing

# 添加 kprobe
echo 'p:myprobe tcp_sendmsg' > kprobe_events
echo 1 > events/kprobes/myprobe/enable

# 查看事件
cat trace_pipe

# 清理
echo 0 > events/kprobes/myprobe/enable
echo '-:myprobe' >> kprobe_events
```

## 关联
- [[linux-BPF-与-eBPF]] — eBPF 基于 kprobe/tracepoint
- [[linux-perf-性能剖析]] — perf 使用追踪基础设施

## 关键结论

> tracepoint 是最安全的追踪点（稳定性保证），kprobe 可以追踪任意内核函数（但内核版本变化可能导致失败）。生产环境优先使用 tracepoint。
