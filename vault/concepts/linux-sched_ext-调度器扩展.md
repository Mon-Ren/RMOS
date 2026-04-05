---
title: "Linux sched_ext 调度器扩展"
tags: [linux, sched_ext, scheduler, bpf, 调度]
aliases: [sched_ext, 调度器扩展, BPF调度器, 自定义调度]
created: 2026-04-05
updated: 2026-04-05
---

# Linux sched_ext 调度器扩展

sched_ext 是 Linux 6.12+ 的调度器扩展框架，允许用 BPF 程序实现自定义 CPU 调度策略。

## 核心概念

```
传统：调度策略硬编码在内核中（CFS/RT/Deadline）
sched_ext：BPF 程序实现调度逻辑，动态加载
```

## 工作原理

```c
// BPF 调度器核心回调
SEC("sched")
void BPF_STRUCT_OPS(my_enqueue, struct task_struct *p, u64 enq_flags) {
    // 将任务放入队列
}

SEC("sched")
void BPF_STRUCT_OPS(my_dispatch, s32 cpu, struct task_struct *prev) {
    // 选择下一个运行的任务
}

SEC("sched")
s32 BPF_STRUCT_OPS(my_select_cpu, struct task_struct *p, s32 prev_cpu, u64 wake_flags) {
    // 选择运行 CPU
}
```

## 使用示例

```bash
# 加载 BPF 调度器
scx_loader my_scheduler.bpf.o

# 切换到 sched_ext
echo scx > /sys/kernel/debug/sched/ext

# 回退到 CFS
echo 0 > /sys/kernel/debug/sched/ext
```

## 应用场景

- **游戏优化**：低延迟调度策略
- **特定工作负载**：批处理/交互式混合优化
- **实验研究**：测试新调度算法
- **容器编排**：Kubernetes 自定义 Pod 调度

## 关联
- [[linux-进程调度与优先级]] — CFS 默认调度器
- [[linux-BPF-与-eBPF]] — BPF 是 sched_ext 的编程基础

## 关键结论

> sched_ext 让调度策略可以像 eBPF 网络程序一样动态加载，无需重新编译内核。这是 Linux 调度子系统最大的架构变革：从"选择固定策略"到"编程自定义策略"。
