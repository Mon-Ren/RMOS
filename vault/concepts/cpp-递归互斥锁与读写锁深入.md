---
title: 递归互斥锁与读写锁深入
tags: [cpp, recursive-mutex, shared-mutex, read-write-lock, timed-mutex]
aliases: [递归互斥锁, recursive_mutex, timed_mutex, shared_mutex深入, 读写锁]
created: 2026-04-04
updated: 2026-04-04
---

# 递归互斥锁与读写锁深入

除了普通 mutex，C++ 还提供递归、超时和读写三种变体——各自解决特定场景的同步需求。

## recursive_mutex

```cpp
#include <mutex>

// 递归锁：同一线程可多次加锁
std::recursive_mutex rmtx;

void method_a() {
    std::lock_guard<std::recursive_mutex> lock(rmtx);
    // ...
    method_b();  // method_b 也会加锁——普通 mutex 死锁！
}

void method_b() {
    std::lock_guard<std::recursive_mutex> lock(rmtx);
    // OK：同一线程可以递归加锁
}

// ⚠️ recursive_mutex 是设计问题的信号：
// 通常意味着锁的粒度不清晰
// 优先考虑重构代码避免递归锁
```

## timed_mutex

```cpp
#include <mutex>

std::timed_mutex tmtx;

// 带超时的加锁
if (tmtx.try_lock_for(std::chrono::milliseconds(100))) {
    // 100ms 内获取到锁
    std::lock_guard<std::timed_mutex, std::adopt_lock_t> lock(tmtx, std::adopt_lock);
}

// 绝对时间
if (tmtx.try_lock_until(deadline)) {
    // 在 deadline 前获取到锁
}

// shared_timed_mutex：带超时的读写锁
std::shared_timed_mutex stm;
stm.try_lock_shared_for(100ms);   // 超时共享锁
stm.try_lock_for(100ms);          // 超时独占锁
```

## shared_mutex 深入

```cpp
#include <shared_mutex>

std::shared_mutex rwmtx;
std::vector<int> cache;

// 读操作：多个线程可并发
int read_cache(int idx) {
    std::shared_lock<std::shared_mutex> lock(rwmtx);
    return cache[idx];  // 多个读线程同时持有 shared_lock
}

// 写操作：独占
void write_cache(int idx, int val) {
    std::unique_lock<std::shared_mutex> lock(rwmtx);
    cache[idx] = val;  // 写线程独占
}

// 性能考虑：
// 读多写少：shared_mutex 胜
// 读少写多：普通 mutex 胜（shared_mutex 有额外开销）
// 争用激烈：普通 mutex 胜
```

## 关键要点

> `recursive_mutex` 允许同一线程递归加锁——但它是代码设计问题的信号，应优先重构。

> `shared_mutex` 在读多写少的场景性能好于普通 mutex——但有额外开销，需要实测验证。

## 相关模式 / 关联

- [[cpp-mutex与lock]] — mutex 基础
- [[cpp-condition-variable]] — 条件变量
