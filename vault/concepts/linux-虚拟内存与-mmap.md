---
title: Linux 虚拟内存与 mmap
tags: [linux, memory, virtual, mmap, vm, brk]
aliases: [虚拟内存, mmap, brk, 内存映射, page fault]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 虚拟内存与 mmap

虚拟内存是现代操作系统的核心抽象，为每个进程提供独立的地址空间。

## 虚拟内存布局（64位）

```
高地址
┌──────────────┐
│    Kernel    │ ← 内核空间（不可访问）
├──────────────┤
│     Stack    │ ← 向下增长
├──────────────┤
│      ↓       │
├──────────────┤
│  mmap 区域   │ ← 文件映射、共享库、匿名映射
├──────────────┤
│      ↑       │
├──────────────┤
│     Heap     │ ← 向上增长（malloc）
├──────────────┤
│    BSS       │ ← 未初始化全局变量
├──────────────┤
│    Data      │ ← 已初始化全局变量
├──────────────┤
│    Text      │ ← 代码段（只读）
└──────────────┘
低地址
```

## mmap

```c
// 文件映射
void *addr = mmap(NULL, length, PROT_READ|PROT_WRITE,
                  MAP_SHARED, fd, 0);
munmap(addr, length);

// 匿名映射（不关联文件）
void *buf = mmap(NULL, 4096, PROT_READ|PROT_WRITE,
                 MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
```

## 查看进程内存

```bash
cat /proc/<pid>/maps           # 内存映射
cat /proc/<pid>/smaps          # 详细映射（含 RSS/PSS）
pmap -x <pid>                  # 内存映射汇总
cat /proc/<pid>/status | grep Vm  # 虚拟内存统计
```

## 关键内存概念

| 概念 | 含义 |
|------|------|
| VIRT | 虚拟内存总量（mmap + malloc） |
| RSS | 常驻内存（实际占用物理内存） |
| PSS | 按比例分配的共享内存 |
| SWAP | 被换出到 swap 的内存 |
| Shared | 共享内存（多个进程共享） |

## Copy-on-Write (COW)

fork() 后父子进程共享物理页，只在写入时才复制：

```bash
# 观察 COW
cat /proc/<pid>/smaps | grep Rss   # fork 前后对比
```

## 关键要点

> `mmap` 比 `read()` 更高效：不需要内核缓冲区拷贝，直接映射文件到进程地址空间（page fault 时按需加载）。

> top 中的 VIRT 不代表实际内存占用，RSS 才是真正的物理内存使用量。

## 相关笔记

- [[Linux 内存管理基础]] — free/swap/OOM
- [[cow-写时复制]] — xv6 COW 实现
