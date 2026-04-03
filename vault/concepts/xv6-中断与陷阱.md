---
title: "xv6 中断与陷阱"
tags: [xv6, trap, interrupt, IDT, syscall]
aliases: ["trap", "interrupt", "中断", "陷阱"]
created: 2026-04-03
updated: 2026-04-03
---

# xv6 中断与陷阱

xv6 统一处理三类异常事件：**中断**（外部设备）、**陷阱**（系统调用）、**故障**（异常如缺页）。

## IDT 初始化

```c
void tvinit(void) {
  for(i = 0; i < 256; i++)
    SETGATE(idt[i], 0, SEG_KCODE<<3, vectors[i], 0);       // 内核态
  SETGATE(idt[T_SYSCALL], 1, SEG_KCODE<<3, vectors[T_SYSCALL], DPL_USER); // 用户态可触发
}
```

- 256 个中断向量，`vectors[]` 是 `vectors.pl` 生成的入口地址数组
- 只有 `T_SYSCALL`（系统调用，int 0x80）设为 DPL_USER，允许用户态触发

## trap() — 统一入口

```c
void trap(struct trapframe *tf)
```

CPU 触发异常时：
1. 硬件将寄存器压入内核栈（形成 trapframe）
2. 跳转到 IDT 对应的入口（`vectors[n]`）
3. 入口代码保存更多寄存器，调用 `trap(tf)`

### 处理逻辑

```
trapno == T_SYSCALL → syscall() 系统调用
trapno == T_IRQ0+IRQ_TIMER → 时钟中断 → ticks++ + yield()
trapno == T_IRQ0+IRQ_IDE   → 磁盘中断 → ideintr()
trapno == T_IRQ0+IRQ_KBD   → 键盘中断 → kbdintr()
内核态未知陷阱 → panic()
用户态未知陷阱 → 标记 killed=1
```

### 时钟中断驱动调度

```c
if(myproc() && myproc()->state == RUNNING &&
   tf->trapno == T_IRQ0+IRQ_TIMER)
  yield();
```

每次时钟中断（`IRQ_TIMER`），当前 RUNNING 进程调用 `yield()` → 状态变 RUNNABLE → 回到调度器。这就是**抢占式调度**的实现。

## trapframe 结构

```c
struct trapframe {
  // pushal 保存的
  uint edi, esi, ebp, oesp;
  uint ebx, edx, ecx, eax;
  // 段寄存器
  ushort gs, padding1, fs, padding2, es, padding3, ds, padding4;
  uint trapno;
  // 硬件压入
  uint err, eip;
  ushort cs, padding5;
  uint eflags, esp;
  ushort ss, padding6;
};
```

## 关键要点

> xv6 的陷阱处理是**分层的**：硬件保存最小状态 → IDT 入口补充保存 → trap() 统一分发。时钟中断是抢占式调度的驱动力，没有它就退化为协作式调度。系统调用通过 `int 0x80` 触发，是唯一允许用户态主动进入内核的入口。

## 关联
- [[xv6 进程管理]] — yield() 实现调度切换，killed 标记终止进程
- [[上下文切换]] — trap 返回时恢复用户态上下文
- [[xv6 系统调用]] — syscall() 的分发表
- [[页表机制]] — 缺页故障的处理（xv6 中直接 panic）
