---
title: "xv6 内存分配"
tags: [xv6, memory, kalloc, kfree, page-frame]
aliases: ["物理内存分配", "kalloc", "page allocator"]
created: 2026-04-03
updated: 2026-04-03
---

# xv6 内存分配

xv6 的物理内存管理极其简洁——用**空闲链表**管理 4KB 页帧。

## 数据结构

```c
struct run {
  struct run *next;
};

struct {
  struct spinlock lock;
  int use_lock;
  struct run *freelist;  // 空闲页链表头
} kmem;
```

每个空闲页的**第一个字**被复用为链表指针。零开销。

## kalloc — 分配一页

```c
char* kalloc(void) {
  struct run *r;
  if(kmem.use_lock) acquire(&kmem.lock);
  r = kmem.freelist;
  if(r) kmem.freelist = r->next;
  if(kmem.use_lock) release(&kmem.lock);
  return (char*)r;
}
```

头插法取一个节点，O(1)。

## kfree — 释放一页

```c
void kfree(char *v) {
  struct run *r;
  if((uint)v % PGSIZE || v < end || V2P(v) >= PHYSTOP)
    panic("kfree");
  memset(v, 1, PGSIZE);  // 填充垃圾值，暴露悬垂引用
  if(kmem.use_lock) acquire(&kmem.lock);
  r = (struct run*)v;
  r->next = kmem.freelist;
  kmem.freelist = r;
  if(kmem.use_lock) release(&kmem.lock);
}
```

- 检查地址对齐和范围
- `memset(v, 1, PGSIZE)` 用垃圾值填充，如果其他代码还持有旧指针，会立即崩溃（调试技巧）
- 头插法归还

## 两阶段初始化

```c
// 阶段一：entrypgdir 时期，只有 [end, 4MB) 可用
kinit1(end, P2V(4*1024*1024));  // use_lock=0（单核，无锁）

// 阶段二：完整页表建立后，所有物理内存可用
kinit2(P2V(4*1024*1024), P2V(PHYSTOP));  // use_lock=1（多核，有锁）
```

为什么分两阶段？因为 `kinit1` 时还没有完整的页表，高地址物理页无法访问。`startothers()` 启动其他核之前必须建立完整映射，所以 `kinit2` 在其后。

## 内存布局

```
物理地址
0x00000000 ┌──────────────┐
           │ 未使用        │
0x00000000 ├──────────────┤
           │ I/O 空间      │
0x000A0000 ├──────────────┤
           │ BIOS         │
0x00100000 ├──────────────┤
           │ 内核代码+数据  │ ← end（内核末尾）
           ├──────────────┤
           │ 可用物理页     │ ← freelist 管理
           ├──────────────┤
           │ ...          │
0x0E000000 ├──────────────┤
           │ I/O 设备映射  │
0x10000000 └──────────────┘ (PHYSTOP)
```

虚拟地址：内核通过 `KERNBASE + 物理地址` 访问所有物理内存。

## 关键要点

> xv6 的物理内存分配只有约 40 行代码。核心是**复用空闲页自身作为链表节点**，零额外开销。但没有碎片整理、没有分配策略（除了 LIFO）、没有 per-CPU 缓存——这些是教学 OS 的有意简化。`memset` 填垃圾值的调试技巧非常实用。

## 关联
- [[页表机制]] — kpgdir 和用户 pgdir 都由 kalloc 分配
- [[xv6 进程管理]] — 内核栈、进程页表都需要 kalloc
- [[xv6 锁与同步]] — kmem.lock 保护空闲链表
- [[xv6 启动流程]] — kinit1/kinit2 两阶段初始化
