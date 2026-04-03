---
title: "COW 写时复制"
tags: [linux, memory, fork, COW, optimization]
aliases: ["Copy-on-Write", "写时复制"]
created: 2026-04-03
updated: 2026-04-03
---

# COW 写时复制

COW（Copy-on-Write）是 fork 的经典优化——父子进程共享物理页，只在写入时才复制。

## xv6 的问题

xv6 的 `fork()` 调用 `copyuvm()` **完整拷贝**所有用户页：
- 4MB 进程 → fork 时复制 4MB 数据
- 大多数情况下，子进程马上 exec → 刚复制的数据立即废弃
- 严重的性能浪费

## COW 方案

```
fork 时：
  父进程页表 ──→ 物理页 X (只读)
  子进程页表 ──↗

写入时（缺页异常）：
  OS 检测到写入只读页（PTE_W=0 但 PTE_P=1）
  → 分配新物理页 Y
  → 复制 X 的内容到 Y
  → 更新页表指向 Y，设置 PTE_W=1
  → 返回继续执行
```

## 实现细节

### 1. fork 时

```c
// 不复制物理页，只复制页表，PTE 清除 W 位
for each PTE in parent:
  child_pte = *parent_pte;
  child_pte &= ~PTE_W;        // 设为只读
  page_ref[pa]++;              // 引用计数 +1
```

### 2. 缺页处理

```c
void pagefault(uint addr) {
  pte = walkpgdir(pgdir, addr, 0);
  if(*pte & PTE_P && !(*pte & PTE_W)) {
    // COW 缺页
    pa = PTE_ADDR(*pte);
    if(page_ref[pa] > 1) {
      newpa = kalloc();
      memmove(P2V(newpa), P2V(pa), PGSIZE);
      page_ref[pa]--;
      *pte = newpa | PTE_P | PTE_W | PTE_U;
    } else {
      // 最后一个引用，直接加写权限
      *pte |= PTE_W;
    }
    lcr3(V2P(pgdir));  // 刷新 TLB
  }
}
```

### 3. 引用计数

```c
// 需要新增的全局结构
int page_ref[PHYSTOP / PGSIZE];  // 每个物理页的引用计数

void incref(uint pa) { page_ref[pa/PGSIZE]++; }
void decref(uint pa) {
  if(--page_ref[pa/PGSIZE] == 0)
    kfree(P2V(pa));
}
```

## 性能收益

| 场景 | 无 COW | 有 COW |
|------|--------|--------|
| fork + exec | 复制全部页 → exec 立即丢弃 | 不复制 → exec 只建新页表 |
| fork + 少量写入 | 复制全部页 | 只复制写入的页 |
| fork + 只读 | 复制全部页 | 完全不复制 |

## 关键要点

> COW 的核心思想是**延迟复制**——99% 的 fork 后跟 exec，不值得复制。用 PTE 权限位"欺骗"硬件：标记只读但实际可写，让硬件在写入时通知 OS。这种"先假装不能做，被抓住了再补救"的模式在系统设计中非常常见（Lazy Allocation、Demand Paging 等）。

## 关联
- [[页表机制]] — PTE 权限位的利用
- [[xv6 进程管理]] — xv6 的 fork 是完整拷贝
- [[x86 内存模型与 TLB]] — 缺页后需要刷新 TLB
- [[xv6 内存分配]] — kalloc/kfree + 引用计数
- [[多级页表]] — 64 位下的 COW 实现
