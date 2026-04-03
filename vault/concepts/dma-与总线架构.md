---
title: "DMA 与总线架构"
tags: [hardware, DMA, bus, PCI, memory]
aliases: ["DMA", "Direct Memory Access", "总线", "PCI"]
created: 2026-04-03
updated: 2026-04-03
---

# DMA 与总线架构

## DMA（Direct Memory Access）

CPU 不参与数据搬运，硬件设备直接读写内存。

### 无 DMA（PIO - Programmed IO）

```
CPU: 从磁盘读一个字 → 写到内存 → 读下一个字 → 写到内存 ...
     CPU 100% 被占用，不能做其他事
```

### 有 DMA

```
1. CPU 告诉 DMA 控制器：源地址、目标地址、传输长度
2. DMA 控制器完成数据搬运
3. DMA 完成后发中断通知 CPU
4. CPU 继续做其他事
```

### DMA 与缓存一致性

```
问题: DMA 写入的数据在 CPU cache 中可能是旧值
      CPU cache 中的数据可能还没写回内存

解决:
  - Cache flush: 传输前将 cache 写回内存
  - Cache invalidate: 传输后丢弃 cache 中的旧副本
  - 非缓存区域 (uncacheable): DMA 缓冲区标记为不缓存
```

## x86 总线架构演进

```
ISA (16-bit, 8MHz)
  ↓
PCI (32/64-bit, 33/66MHz)  ← xv6 IDE 设备
  ↓
PCIe (串行, 1-16 lanes)    ← 现代系统
```

### PCIe

```
┌──────┐    ┌──────┐    ┌──────┐
│ CPU  │───→│ Root │───→│ NVMe │
│      │    │Complex│   │ SSD  │
└──────┘    └──────┘    └──────┘
              ↓
            ┌──────┐
            │ GPU  │
            └──────┘
```

- 点对点串行连接（不是共享总线）
- 每个 lane 双向 8 GT/s
- 支持 1/2/4/8/16 lanes

## IO 空间 vs 内存空间

### Port IO（xv6 使用）

```c
outb(0x1F7, cmd);   // 写磁盘命令寄存器
uchar status = inb(0x1F7);  // 读状态
```

- 专用 IO 地址空间（65536 个端口）
- 用 `in/out` 指令访问
- xv6 的 IDE 驱动使用端口 `0x1F0-0x1F7`

### MMIO（Memory-Mapped IO）

```c
volatile uint *reg = (uint*)0xFEE00000;  // LAPIC 基址
*reg = value;  // 像访问内存一样访问设备寄存器
```

- 设备寄存器映射到物理地址空间
- 用普通内存指令访问
- xv6 的 LAPIC 使用 MMIO

## 关键要点

> DMA 解放了 CPU——让它不必浪费时间搬运数据。但引入了缓存一致性问题，这是系统编程中最微妙的 bug 来源之一。现代总线（PCIe）用点对点串行替代共享并行，大幅提升带宽和可扩展性。IO 方式的选择（PIO vs MMIO）是硬件设计决策——MMIO 更灵活但需要处理缓存。

## 关联
- [[设备驱动模型]] — 三种 IO 方式
- [[LAPIC 与 IOAPIC]] — LAPIC 用 MMIO 访问
- [[xv6 内存分配]] — DMA 缓冲区需要物理连续内存
- [[x86 内存模型与 TLB]] — MMIO 区域标记为 uncacheable
