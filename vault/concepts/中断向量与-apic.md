---
title: "中断向量与 APIC"
tags: [x86, hardware, interrupt, vector, APIC]
aliases: ["中断向量", "IRQ", "中断分发"]
created: 2026-04-03
updated: 2026-04-03
---

# 中断向量与 APIC

## 中断向量号

x86 有 256 个中断向量（0-255），每个映射到 IDT 中的一个门描述符。

### 分配

```
0-31:   CPU 异常（固定）
  0 - 除零 (#DE)
  1 - 调试 (#DB)
  6 - 非法指令 (#UD)
  13 - 通用保护 (#GP)
  14 - 缺页 (#PF)

32-255: 可用（硬件中断 + 软件中断）
  32 (0x20) - IRQ0 时钟
  33 (0x21) - IRQ1 键盘
  ...
  64 (0x40) - xv6 系统调用 (T_SYSCALL)
```

### xv6 的分配

```c
#define T_SYSCALL 64     // 系统调用
#define T_IRQ0    32     // 硬件中断起始
#define IRQ_TIMER  0     // IRQ0 → 向量 32
#define IRQ_KBD    1     // IRQ1 → 向量 33
#define IRQ_IDE    14    // IRQ14 → 向量 46
```

## APIC 中断路由

### IOAPIC 路由表

```
IOAPIC 红线表条目:
┌─────────────────────────────────────────┐
│ Destination (目标 LAPIC ID)             │
│ Vector (中断向量号)                      │
│ Delivery Mode (Fixed/Lowest Priority)   │
│ Trigger Mode (Edge/Level)               │
│ Mask (是否屏蔽)                          │
└─────────────────────────────────────────┘
```

### 分发模式

| 模式 | 说明 |
|------|------|
| Fixed | 发送到指定 CPU |
| Lowest Priority | 发送到优先级最低的 CPU |
| SMI | 系统管理中断 |
| NMI | 不可屏蔽中断 |
| INIT | 初始化目标 CPU |

### IPI（处理器间中断）

```c
// 发送 IPI 到指定 CPU
void lapicstartap(uchar apicid, uint addr) {
  // 发送 INIT IPI
  lapicw(ICRHI, apicid << 24);
  lapicw(ICRLO, INIT | LEVEL | assert);
  // 发送 STARTUP IPI
  lapicw(ICRLO, STARTUP | (addr >> 12));
}
```

## 旧式 PIC vs APIC

| | 8259A PIC | APIC |
|---|-----------|------|
| 中断数 | 15 | 256+ |
| 多核 | 不支持 | 支持 |
| 路由 | 固定 | 灵活配置 |
| IPI | 不支持 | 支持 |
| 使用 | 单核嵌入式 | 现代多核系统 |

## 关键要点

> 中断向量是硬件事件到软件处理的映射号。APIC 架构通过 IOAPIC 路由表实现了灵活的中断分发——可以指定中断去哪个 CPU、用什么触发方式、什么优先级。IPI 让 CPU 之间可以互相中断，是多核协调（TLB shootdown、核间调度）的基础。

## 关联
- [[IDT 与中断机制]] — 向量号查 IDT 表
- [[LAPIC 与 IOAPIC]] — APIC 硬件实现
- [[xv6 中断与陷阱]] — trap() 按向量号分发处理
- [[调度算法比较]] — IPI 用于核间调度
