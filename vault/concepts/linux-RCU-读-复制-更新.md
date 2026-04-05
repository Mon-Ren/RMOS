---
title: "Linux RCU 读-复制-更新"
tags: [linux, kernel, rcu, concurrency, lockless]
aliases: [RCU, Read-Copy-Update, 读复制更新, 无锁并发]
created: 2026-04-05
updated: 2026-04-05
---

# Linux RCU 读-复制-更新

RCU 是 Linux 内核的无锁同步机制，读操作零开销、写操作延迟更新，适合读多写少场景。

## 核心思想

```
读取：直接访问，不需要锁
写入：复制 → 修改副本 → 发布新版本 → 等待所有读者退出 → 释放旧版本
```

```
读者（任意多）                    写者
  │                               │
  ├─ rcu_read_lock()              │
  ├─ 读取数据                     ├─ 分配新数据
  ├─ 使用数据                     ├─ 修改新数据
  ├─ rcu_read_unlock()            ├─ rcu_assign_pointer()
  │                               ├─ synchronize_rcu() ← 等待读者
  │                               ├─ kfree(旧数据)
```

## 内核 API

```c
// 读者
rcu_read_lock();
ptr = rcu_dereference(global_ptr);
// 使用 ptr...
rcu_read_unlock();

// 写者
new = kmalloc(...);
// 初始化 new
rcu_assign_pointer(global_ptr, new);
synchronize_rcu();      // 等待所有读者退出
kfree(old);

// 异步版本
call_rcu(&old->rcu, my_free_func);  // 不阻塞
```

## 应用场景

- **路由表**：读远多于写
- **文件系统**：dentry/inode 缓存查找
- **网络栈**：连接表查询
- **模块卸载**：等待所有读者退出
- **数据结构**：链表、哈希表的无锁读取

## 关联
- [[linux-中断子系统]] — 软中断中使用 RCU
- [[linux-Slab-分配器]] — SLAB 缓存支持 RCU 释放

## 关键结论

> RCU 的核心优势：读操作完全无锁（零开销），适合读 99%+ / 写 1% 的场景。Linux 的链表（list_head）、路由表、dentry 缓存都大量使用 RCU。
