---
title: "x86 内存模型与 TLB"
tags: [x86, hardware, paging, TLB, MMU]
aliases: ["TLB", "translation lookaside buffer", "地址转换"]
created: 2026-04-03
updated: 2026-04-03
---

# x86 内存模型与 TLB

## 地址转换全路径

```
逻辑地址        线性地址        物理地址
(段:偏移)  →   (虚拟地址)  →   (RAM)
   │               │              │
  GDT/LDT         页表           实际
  段基址+偏移      CR3→PDE→PTE    内存
```

xv6 平坦模型下，段基址=0，线性地址=偏移，所以虚拟地址=逻辑地址。

## CR3 寄存器

- 存储当前页目录的**物理地址**
- 进程切换时：`lcr3(V2P(p->pgdir))` 切换页表
- 每个进程有独立的 CR3 值

## TLB（Translation Lookaside Buffer）

页表查询需要 2 次内存访问（PDE + PTE），TLB 是页表的硬件缓存。

### TLB 条目

```
VPN (虚拟页号)  →  PPN (物理页号) + 权限位 + 标记
```

### TLB 命中

```
虚拟地址 → 拆分 VPN → TLB 查找 → 命中 → 直接拼接 PPN+偏移 → 物理地址
                                        （1 个时钟周期）
```

### TLB 未命中

```
TLB 未命中 → 硬件遍历页表 (page walk) → 填充 TLB → 返回结果
              （10-100 个时钟周期）
```

### TLB 刷新

**进程切换时必须刷新 TLB**，因为不同进程的 VPN 可能映射到不同物理页。

xv6 的做法：
```c
void switchuvm(struct proc *p) {
  lcr3(V2P(p->pgdir));  // 切换 CR3 = 自动刷新 TLB
}
```

更先进的 CPU 用 **ASID（Address Space Identifier）** 标记 TLB 条目，避免切换时全部刷新。

## 页表条目（PTE）详解

```
 31           12 11    9  8  7  6  5  4  3  2  1  0
┌──────────────┬───────┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│ 物理页帧地址  │ Avail │G │D │A │PC│WT│U │W │P │  │
└──────────────┴───────┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
P:   Present (存在)
W:   Writable (可写)
U:   User accessible (用户可访问)
PWT: Page-level Write-Through
PCD: Page-level Cache Disable
A:   Accessed (CPU 自动设置，已被读/写)
D:   Dirty (CPU 自动设置，已被写)
G:   Global (不随 CR3 切换刷新)
```

## 关键要点

> TLB 是页表性能的关键——没有 TLB，每次内存访问都要 2 次额外查表。TLB 本质是虚拟→物理映射的 cache。CR3 切换刷新全部 TLB 条目是性能杀手，ASID 是多核/多进程场景的优化。理解 TLB 失效场景（上下文切换、mmap 修改）对系统性能调优至关重要。

## 关联
- [[页表机制]] — xv6 的二级页表实现
- [[x86 特权级]] — PTE_U 控制用户态访问
- [[上下文切换]] — switchuvm/lcr3 切换页表
- [[COW 写时复制]] — 利用 PTE 权限位触发缺页
- [[多级页表]] — x86-64 四级页表
