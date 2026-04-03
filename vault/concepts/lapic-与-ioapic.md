---
title: "LAPIC 与 IOAPIC"
tags: [x86, hardware, APIC, interrupt-controller, multicore]
aliases: ["Local APIC", "IO APIC", "中断控制器"]
created: 2026-04-03
updated: 2026-04-03
---

# LAPIC 与 IOAPIC

x86 多核系统使用 APIC（Advanced Programmable Interrupt Controller）架构替代老式 8259A PIC。

## 架构总览

```
外部设备 → IOAPIC → 系统总线 → LAPIC (每个CPU一个)
                  ↘ LAPIC0 → CPU0
                  ↘ LAPIC1 → CPU1
                  ↘ LAPIC2 → CPU2
```

## LAPIC（Local APIC）

每个 CPU 核心一个，功能：
- 接收中断（来自 IOAPIC 或其他 CPU）
- 管理本地定时器
- 处理处理器间中断（IPI）
- 发送 EOI（End of Interrupt）确认

### 关键寄存器

| 寄存器 | 功能 |
|--------|------|
| ID | LAPIC ID |
| TPR | 任务优先级（低于此优先级的中断被屏蔽） |
| EOI | 写入确认中断处理完成 |
| SVR | Spurious Interrupt Vector |
| LVT Timer | 本地定时器配置 |

### xv6 中的使用

```c
void lapicinit(void) {
  // 设置定时器：每 100Hz 触发一次 IRQ_TIMER
  lapicw(TDCR, X1);
  lapicw(TIMER, PERIODIC | (T_IRQ0 + IRQ_TIMER));
  lapicw(TICR, 10000000);  // 初始计数
}

void lapiceoi(void) {
  lapicw(EOI, 0);  // 发送 EOI
}
```

## IOAPIC

系统中通常一个（或多个），功能：
- 接收外部设备中断（IRQ 0-15 等）
- 将中断路由到指定的 LAPIC
- 可配置中断目标 CPU 和触发方式

### 中断路由表

```c
void ioapicinit(void) {
  for(i = 0; i < nioapic; i++) {
    // 将 IRQ 路由到所有 CPU
    ioapicwritel(REG_TABLE+2*i, T_IRQ0 + (ioapicid[i]<<24));
    ioapicwritel(REG_TABLE+2*i+1, 0xffffffff);  // 所有 CPU
  }
}
```

## IPI（Inter-Processor Interrupt）

CPU 之间互相发送中断：
- 用于启动 AP（Application Processor）
- 用于 TLB shootdown（页表修改后通知其他核刷新 TLB）
- 用于 IPI 预占调度

## xv6 中禁用旧 PIC

```c
void picinit(void) {
  // 写 ICW1-ICW4 禁用 8259A
  outb(IO_PIC1+1, 0xFF);  // 屏蔽所有 IRQ
  outb(IO_PIC2+1, 0xFF);
}
```

## 关键要点

> APIC 架构的核心是**分布式中断处理**：每个 CPU 有独立的 LAPIC，共享一个或多个 IOAPIC。IOAPIC 负责外部中断的路由，LAPIC 负责本地处理和 CPU 间通信。LAPIC 定时器是 xv6 抢占式调度的硬件基础——没有它就没有时钟中断，没有时钟中断就没有 yield。

## 关联
- [[IDT 与中断机制]] — 中断到达 CPU 后进入 IDT
- [[xv6 中断与陷阱]] — lapiceoi 确认中断处理完成
- [[中断向量与 APIC]] — 多核中断分发策略
- [[xv6 启动流程]] — lapicinit 和 ioapicinit
