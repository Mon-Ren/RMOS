---
title: "Linux futex 快速用户空间互斥锁"
tags: [linux, futex, mutex, concurrency, kernel]
aliases: [futex, 快速互斥锁, 用户态锁, 内核辅助锁]
created: 2026-04-05
updated: 2026-04-05
---

# Linux futex 快速用户空间互斥锁

futex（Fast Userspace Mutex）是 Linux 同步原语的基石，pthread_mutex 和 Go 的 runtime 都基于它实现。

## 核心思想

```
无竞争时：纯用户空间操作（原子 CAS），零系统调用
有竞争时：内核挂起等待（futex 系统调用）
```

```
加锁：
1. CAS(futex_word, 0, 1)     ← 原子操作，成功则获得锁（无系统调用）
2. 失败 → futex(FUTEX_WAIT)  ← 进入内核等待队列

解锁：
1. atomic_sub(futex_word, 1)
2. 值变为 0 → futex(FUTEX_WAKE)  ← 唤醒一个等待者
```

## 系统调用

```c
// 等待（futex_word == expected 时挂起）
futex(int *uaddr, FUTEX_WAIT, int expected, 
      const struct timespec *timeout);

// 唤醒
futex(int *uaddr, FUTEX_WAKE, int n);
```

## 使用场景

| 用户空间接口 | 底层实现 |
|-------------|----------|
| pthread_mutex_t | futex |
| pthread_cond_t | futex |
| std::mutex (C++) | pthread_mutex → futex |
| Go mutex | runtime futex |
| Rust std::sync::Mutex | futex/parking_lot |
| Java synchronized | futex |

## 查看 futex 竞争

```bash
# strace 追踪
strace -e futex ./app

# perf 统计
perf stat -e futex:*

# /proc 信息
cat /proc/lock_stat              # 锁竞争统计
```

## 关联
- [[linux-进程基础与-ps-命令]] — 进程状态 S（等待 futex）
- [[linux-虚拟内存与-mmap]] — futex 基于共享内存的 futex_word

## 关键结论

> futex 的精髓是"乐观无竞争"：大多数锁获取无系统调用开销，只在真正竞争时才陷入内核。这是 pthread_mutex 比 System V semaphore 快得多的原因。
