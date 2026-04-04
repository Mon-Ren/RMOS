---
title: atomic 与内存序
tags: [cpp, concurrency, atomic, memory-order, lock-free, CAS]
aliases: [atomic, 原子操作, 内存序, memory order, lock-free, CAS, compare_exchange]
created: 2026-04-04
updated: 2026-04-04
---

# atomic 与内存序

`std::atomic` 提供无锁的线程安全操作——比 mutex 快，但正确使用内存序是并发编程中最难的部分之一。

## 意图与场景

- 简单计数器、标志位的线程安全更新
- 高性能无锁数据结构
- 线程间信号传递

## std::atomic 基础

```cpp
#include <atomic>

std::atomic<int> counter{0};

// 基本操作（默认 memory_order_seq_cst）
counter.store(42);             // 原子写
int val = counter.load();      // 原子读
counter++;                     // 原子递增（等价于 fetch_add(1) + 1）
counter.fetch_add(5);          // 原子加，返回旧值
counter.fetch_sub(3);          // 原子减

// compare_exchange：CAS（Compare-And-Swap）
int expected = 0;
bool success = counter.compare_exchange_strong(expected, 42);
// 如果 counter == expected（0），设为 42，返回 true
// 否则 expected 更新为当前值，返回 false

// compare_exchange_weak：允许虚假失败（更高效）
int expected = 0;
while (!counter.compare_exchange_weak(expected, expected + 1)) {
    // expected 已被更新为当前值，循环重试
}
```

## 原子标志

```cpp
std::atomic_flag lock_flag = ATOMIC_FLAG_INIT;

void spin_lock() {
    while (lock_flag.test_and_set(std::memory_order_acquire)) {
        // 自旋等待
    }
}

void spin_unlock() {
    lock_flag.clear(std::memory_order_release);
}

// C++20: atomic_flag 支持 wait/notify
lock_flag.wait(true);  // 等待 flag 变为 false（比自旋高效）
lock_flag.notify_one();
```

## 内存序

```
内存序约束从强到弱：

1. memory_order_seq_cst（默认）—— 顺序一致
   所有线程看到的原子操作顺序一致。最安全，性能最低。

2. memory_order_acquire —— 获取（读操作）
   本线程中，此操作之后的读写不会被重排到此操作之前。

3. memory_order_release —— 释放（写操作）
   本线程中，此操作之前的读写不会被重排到此操作之后。

4. memory_order_acq_rel —— 获取+释放

5. memory_order_consume —— 数据依赖（实践中未完全实现，避免使用）

6. memory_order_relaxed —— 松弛
   只保证原子性，不保证顺序。
```

```cpp
// acquire-release 配对：建立 happens-before 关系
std::atomic<bool> ready{false};
int data = 0;

// 线程 1：生产数据
data = 42;
ready.store(true, std::memory_order_release);  // release

// 线程 2：等待数据
while (!ready.load(std::memory_order_acquire)) { }  // acquire
assert(data == 42);  // 保证成立！release 之前的写入对 acquire 之后可见
```

## 常见用法

```cpp
// 懒汉式单例（高效版本）
class Singleton {
    static std::atomic<Singleton*> instance;
    static std::mutex mtx;
public:
    static Singleton* get() {
        auto* p = instance.load(std::memory_order_acquire);
        if (!p) {
            std::lock_guard<std::mutex> lock(mtx);
            p = instance.load(std::memory_order_relaxed);
            if (!p) {
                p = new Singleton();
                instance.store(p, std::memory_order_release);
            }
        }
        return p;
    }
};
```

## 关键要点

> 除非你完全理解内存序，否则用默认的 `memory_order_seq_cst`。性能敏感时从 `acquire-release` 开始，`relaxed` 只用于纯统计计数器等不建立同步关系的场景。

> `atomic` 只保证自身的原子性，不保证复合操作的原子性。`counter++; counter++;` 是两次独立操作。

## 相关模式 / 关联

- [[cpp-mutex与lock]] — 有锁方案的对比
- [[cpp-condition-variable]] — 有锁同步
