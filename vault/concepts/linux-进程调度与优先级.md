---
title: Linux 进程调度与优先级
tags: [linux, scheduler, nice, priority, cfs, 调度]
aliases: [进程调度, nice, renice, CFS, 调度器, 优先级]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 进程调度与优先级

Linux 调度器决定哪个进程在何时获得 CPU 时间，CFS（Completely Fair Scheduler）是默认调度器。

## 调度策略

| 策略 | 说明 | 使用场景 |
|------|------|----------|
| SCHED_NORMAL | CFS 默认，公平调度 | 普通进程 |
| SCHED_BATCH | 批处理，不抢占 | 后台计算 |
| SCHED_IDLE | 最低优先级 | 空闲任务 |
| SCHED_FIFO | 实时，先进先出 | 实时系统 |
| SCHED_RR | 实时，时间片轮转 | 实时系统 |

## nice 与优先级

```bash
# nice 值（-20 到 19，默认 0）
nice -n 10 ./task              # 以 nice=10 启动（低优先级）
nice -n -5 ./task              # 以 nice=-5 启动（高优先级，需 root）
renice -n 15 -p <pid>          # 修改已运行进程的 nice 值

# 查看
ps -eo pid,ni,comm             # nice 值
top                            # NI 列
chrt -p <pid>                  # 查看调度策略
```

## CFS 原理

```
CFS 用红黑树按 vruntime 排序所有进程：
- vruntime = 进程已运行的虚拟时间
- 调度器总是选择 vruntime 最小的进程
- I/O 密集型进程 vruntime 增长慢（经常睡眠），获得更多调度
- CPU 密集型进程 vruntime 增长快，相对减少调度
```

## CPU 亲和性

```bash
taskset -c 0,1 ./app           # 绑定到 CPU 0 和 1
taskset -p <pid>               # 查看进程的 CPU 亲和性
taskset -cp 0-3 <pid>          # 修改已运行进程
```

## 关键要点

> `nice` 值越小优先级越高。普通用户只能调高 nice（降低优先级），只有 root 能调低 nice（提高优先级）。

> CFS 是"完全公平"调度器，通过 vruntime 保证每个进程获得公平的 CPU 时间比例。

## 相关笔记

- [[Linux 进程基础与 ps 命令]] — 进程管理
- [[调度算法比较]] — RR/优先级/MLFQ/CFS 对比
