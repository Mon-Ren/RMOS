---
title: "Linux 中断子系统"
tags: [linux, interrupt, irq, apic, softirq, tasklet]
aliases: [中断, IRQ, 硬中断, 软中断, 上半部, 下半部]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 中断子系统

Linux 中断处理分上半部（硬中断）和下半部（软中断/tasklet/工作队列），保证中断响应快速。

## 中断处理流程

```
硬件中断 → IDT → 硬中断处理（上半部）→ 软中断处理（下半部）
                     ↑ 快速、关中断         ↑ 可延迟、开中断
```

## 上半部（硬中断）

```c
// 注册中断处理程序
request_irq(irq_number, handler, IRQF_SHARED, "mydev", dev_id);

// 中断处理函数（尽量短）
irqreturn_t handler(int irq, void *dev_id) {
    // 读取硬件状态
    // 标记下半部工作
    tasklet_schedule(&my_tasklet);
    return IRQ_HANDLED;
}
```

## 下半部机制对比

| 机制 | 上下文 | 特点 |
|------|--------|------|
| 软中断 | 中断上下文 | 编译时静态分配，不可睡眠 |
| tasklet | 中断上下文 | 基于软中断，同类型不并行 |
| 工作队列 | 进程上下文 | 可睡眠，可调度 |
| 线程化中断 | 进程上下文 | `IRQF_ONESHOT`，现代首选 |

```c
// tasklet
DECLARE_TASKLET(my_tasklet, my_func, data);
tasklet_schedule(&my_tasklet);

// 工作队列
struct work_struct work;
INIT_WORK(&work, work_func);
schedule_work(&work);

// 线程化中断
request_threaded_irq(irq, NULL, threaded_handler, IRQF_ONESHOT, "mydev", dev);
```

## 查看中断

```bash
cat /proc/interrupts            # 中断计数（每 CPU）
watch cat /proc/interrupts      # 实时监控
cat /proc/softirqs              # 软中断统计
```

## 关联
- [[idt-与中断机制]] — 中断描述符表
- [[linux-文件描述符与-IO-模型]] — IO 中断与多路复用

## 关键结论

> 上半部必须快速（微秒级），关中断期间不能做重活。下半部做实际处理。现代驱动推荐线程化中断（request_threaded_irq），简化并发控制。
