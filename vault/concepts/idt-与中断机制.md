---
title: "IDT 与中断机制"
tags: [x86, hardware, IDT, interrupt, exception]
aliases: ["Interrupt Descriptor Table", "中断描述符表"]
created: 2026-04-03
updated: 2026-04-03
---

# IDT 与中断机制

IDT（Interrupt Descriptor Table）是 x86 处理异常和中断的核心机制，类似实模式下的中断向量表（IVT）的保护模式版本。

## 中断门描述符（8 字节）

```
 63              48 47       40 39     35 34    32
┌─────────────────┬───────────┬─────────┬────────┐
│ Offset 31:16    │  P DPL 0  │ Type    │ 保留    │
├─────────────────┴───────────┴─────────┴────────┤
│ Segment Selector              │ Offset 15:0    │
└───────────────────────────────┴────────────────┘
```

- **Offset**: 中断处理函数的入口地址
- **Segment Selector**: 代码段选择子（通常是内核代码段）
- **Type**: 0xE=中断门（关中断进入）, 0xF=陷阱门（保持中断）
- **DPL**: 允许触发的最低特权级

## 三类异常事件

| 类型 | 来源 | 示例 |
|------|------|------|
| **中断** | 外部硬件 | 时钟、键盘、磁盘 |
| **陷阱** | 软件指令 | `int 0x80` 系统调用 |
| **故障** | CPU 检测 | 缺页(#PF)、除零(#DE) |

## 中断处理流程

```
1. CPU 收到中断/异常
2. 从 IDT[id] 查找门描述符
3. 检查特权级：CPL <= 门描述符 DPL（软件中断）或无条件（硬件）
4. 如果需要切换特权级：
   a. 从 TSS 获取内核栈 (SS0:ESP0)
   b. 压入用户 SS、ESP、EFLAGS、CS、EIP、ErrorCode
5. 加载新的 CS:EIP（中断处理函数入口）
6. 如果是中断门：清除 IF 位（关中断）
7. 开始执行处理函数
```

## xv6 的 IDT 初始化

```c
void tvinit(void) {
  for(i = 0; i < 256; i++)
    SETGATE(idt[i], 0, SEG_KCODE<<3, vectors[i], 0);       // 内核态可触发
  SETGATE(idt[T_SYSCALL], 1, SEG_KCODE<<3, vectors[T_SYSCALL], DPL_USER); // 用户态可触发
}
```

- 所有 256 个向量都指向 `vectors.S` 中预生成的入口
- 只有 `int 0x80`（T_SYSCALL）设 DPL=3，允许用户态调用
- 其他向量 DPL=0，用户态触发会 #GP（General Protection）

## 错误码

某些异常会压入错误码：
```
 15       3  2   1   0
┌─────────┬───┬───┬───┐
│ Index   │TI │EXT│ I │
└─────────┴───┴───┴───┘
I:   外部事件
EXT: 异常来源外部
TI:  0=GDT, 1=LDT/LDT
Index: 选择子索引
```

## 关键要点

> IDT 是 x86 异常处理的路由表——256 个槽位对应 256 种事件。硬件中断时 CPU 自动切换到内核栈、保存现场、跳转到处理函数。xv6 用 `vectors.pl` 脚本批量生成 256 个入口代码，每个入口压入不同的 trapno 后跳转到统一的 `alltraps`。

## 关联
- [[xv6 中断与陷阱]] — tvinit 和 trap() 的实现
- [[x86 特权级]] — DPL 检查机制
- [[GDT 与段描述符]] — 门描述符引用的代码段
- [[LAPIC 与 IOAPIC]] — 外部中断如何到达 CPU
- [[中断向量与 APIC]] — 多核中断分发
