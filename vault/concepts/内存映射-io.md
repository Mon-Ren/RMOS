---
title: "内存映射 I/O"
tags: [io, mmio, memory-mapped, hardware, device-driver]
aliases: ["MMIO", "memory mapped IO", "内存映射"]
created: 2026-04-04
updated: 2026-04-04
---

# 内存映射 I/O

内存映射 I/O（MMIO）是 CPU 与外设通信的一种方式：将设备寄存器映射到物理地址空间，用普通的 load/store 指令访问硬件。

## 两种 I/O 方式

### 端口映射 I/O（PMIO / Port I/O）

- x86 有独立的 I/O 地址空间（64K 端口）
- 用 `in`/`out` 指令访问
- 例：`outb(0x3F8, 'A')` 向串口发送字符

### 内存映射 I/O（MMIO）

- 设备寄存器映射到物理地址空间
- 用普通的 `mov`/`load`/`store` 访问
- 现代系统的主流方式

## xv6 中的 MMIO 映射

xv6 在 `memlayout.h` 中定义设备地址映射：

```c
// 物理地址映射
#define DEVSPACE 0xFE000000

// IOAPIC
#define IOAPIC  0xFEC00000

// Local APIC
#define LAPIC   0xFEE00000

// VGA 文本模式
#define CGA     0xB8000
```

内核在 `main.c` 的 `kinit1()`/`kinit2()` 之后，通过 `setupkvm()` 建立这些映射：

```c
// kvm.c — 内核页表中添加设备映射
mappages(pgdir, (void*)0xFE000000, 0x100000, 0xFE000000, PTE_W);
mappages(pgdir, (void*)LAPIC,      4096,       LAPIC,       PTE_W);
```

## 访问示例

### 读 LAPIC 寄存器

```c
// lapic.c
static uint
lapicr(int index) {
  return *((volatile uint*)(lapic + index));
}

static void
lapicw(int index, int value) {
  *((volatile uint*)(lapic + index)) = value;
  lapicr(0x20);  // 读 ID 寄存器，保证写入完成（flush）
}
```

### 读 VGA 显示缓冲

```c
// console.c
#define CRTPORT 0x3D4

static ushort *crt = (ushort*)0xB8000;  // VGA 文本缓冲区

static void
cgaputc(int c) {
  // 写入显存 = 显示字符
  crt[pos] = ' ' | 0x0700;  // 清除光标
  // ...
  crt[pos] = c | 0x0700;    // 写字符（白底黑字）
}
```

## volatile 关键字

MMIO 访问**必须用 `volatile`**：

```c
volatile uint *reg = (uint*)0xFEE00000;
```

原因：
- 设备寄存器的值可能随时变化（由硬件修改）
- 编译器不应该优化掉重复读取
- 编译器不应该重排读写顺序

## 写后读屏障

有些设备需要确保写操作真正到达硬件后才继续：

```c
lapicw(TICR, 1000000);
lapicr(0x20);  // flush — 强制完成前面的写
```

在更强的架构（ARM）上需要显式的内存屏障指令（`dmb`/`dsb`）。

## MMIO vs PMIO 对比

| 特性 | MMIO | PMIO |
|------|------|------|
| 地址空间 | 与内存共享 | 独立的 I/O 空间 |
| 指令 | 普通 load/store | 专用 in/out |
| 缓存 | 可配置为 uncacheable | 不经过缓存 |
| 性能 | 通常更高 | 较低（指令开销） |
| 使用场景 | 现代设备、APIC、PCIe | 传统串口、IDE、PS/2 |

## 关键要点

> MMIO 让设备寄存器像普通内存一样被访问，简化了编程模型。但必须用 `volatile` 防止编译器优化，并用屏障保证硬件操作的顺序性。

## 关联
- [[xv6 磁盘驱动]] — IDE 端口 I/O 和中断的配合
- [[设备驱动模型]] — 设备抽象的整体设计
- [[lapic-与-ioapic]] — 两个中断控制器的 MMIO 访问
- [[x86 内存模型与 TLB]] — 页表中的设备映射和缓存策略
- [[内存分配与总线架构]] — DMA 与 MMIO 的协作
