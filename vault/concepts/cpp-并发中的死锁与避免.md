---
title: C++ 并发中的死锁与避免
tags: [cpp, deadlock, lock-ordering, scoped-lock, lock-hierarchy]
aliases: [死锁, deadlock, 锁顺序, lock hierarchy, 避免死锁]
created: 2026-04-04
updated: 2026-04-04
---

# 并发中的死锁与避免

死锁是两个或多个线程互相等待对方持有的锁——永远无法继续执行。

## 死锁的原因

```cpp
// 经典死锁：两个线程以不同顺序获取锁
std::mutex m1, m2;

// 线程 1
{
    std::lock_guard<std::mutex> lock1(m1);
    std::lock_guard<std::mutex> lock2(m2);  // 等待 m2
    // 如果线程 2 持有 m2 等待 m1 → 死锁
}

// 线程 2
{
    std::lock_guard<std::mutex> lock2(m2);
    std::lock_guard<std::mutex> lock1(m1);  // 等待 m1
}
```

## 避免策略

```cpp
// 策略 1：统一锁顺序
// 所有线程按相同顺序获取锁（如按地址排序）
void safe_transfer(Account& a, Account& b) {
    auto first = &a < &b ? &a : &b;
    auto second = &a < &b ? &b : &a;
    std::lock_guard<std::mutex> lock1(first->mtx);
    std::lock_guard<std::mutex> lock2(second->mtx);
}

// 策略 2：std::lock 同时获取多个锁（内部避免死锁）
void safe_transfer2(Account& a, Account& b) {
    std::unique_lock<std::mutex> lock1(a.mtx, std::defer_lock);
    std::unique_lock<std::mutex> lock2(b.mtx, std::defer_lock);
    std::lock(lock1, lock2);  // 同时锁，无死锁
}

// 策略 3：scoped_lock（C++17，最简洁）
void safe_transfer3(Account& a, Account& b) {
    std::scoped_lock lock(a.mtx, b.mtx);  // 同时锁任意多个 mutex
}

// 策略 4：锁层级——设计时定义锁的层级，运行时检查
// thread_local int lock_level = INT_MAX;
// 每次获取锁时检查：lock_level < mtx.level 才允许
```

## 关键要点

> 避免死锁的最佳策略：**用 `std::scoped_lock` 同时获取多个锁**——简洁且安全。

> 设计原则：尽量减少需要同时持有多个锁的场景。如果必须，统一锁的获取顺序。

## 相关模式 / 关联

- [[cpp-mutex与lock]] — mutex 基础
- [[cpp-递归互斥锁与读写锁深入]] — 其他 mutex 变体
