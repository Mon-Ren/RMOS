---
title: futex 与用户态锁
tags: [system, futex, mutex, user-space, kernel, linux]
aliases: [futex 原理, 用户态互斥锁, 快速路径慢速路径]
created: 2026-04-05
updated: 2026-04-05
---

# futex 与用户态锁

**一句话概述：** futex（Fast Userspace muTEX）是 Linux 互斥锁的底层机制——无竞争时纯用户态操作（原子 CAS），不陷入内核；有竞争时通过 futex 系统调用将线程挂起在内核等待队列上。这使得无竞争场景的加锁/解锁成本只有几次原子操作。

```cpp
// futex 的两层结构
// 无竞争路径（快速）：
lock() {
    if (state.compare_exchange_strong(0, 1)) return;  // 用户态 CAS，拿到锁
    // CAS 失败 → 有竞争
}
// 有竞争路径（慢速）：
    futex_wait(&state, 1);  // 系统调用，线程挂起

unlock() {
    state.store(0);  // 用户态释放
    futex_wake(&state, 1);  // 唤醒一个等待线程
}
```

## 关键要点

> pthread_mutex_t、std::mutex（Linux 实现）底层都用 futex。这就是为什么无竞争的 mutex lock/unlock 只有 ~20ns（一次 CAS），比有竞争时的 ~1μs（系统调用）快 50 倍。

## 相关模式 / 关联

- [[cpp-mutex与lock]] — std::mutex
- [[cpp-自旋锁与排队自旋锁]] — 自旋锁对比
- [[cpp-并发中的死锁与避免]] — 锁的正确使用
