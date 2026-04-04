---
title: mutex 与锁
tags: [cpp, concurrency, mutex, lock-guard, unique-lock, shared-mutex]
aliases: [mutex, 互斥锁, lock_guard, unique_lock, shared_mutex, 读写锁]
created: 2026-04-04
updated: 2026-04-04
---

# mutex 与锁

互斥锁（mutex）是并发编程的基础同步原语——保护共享数据不被多个线程同时修改。

## 意图与场景

- 保护共享数据的读写
- 实现临界区（同一时刻只有一个线程进入）
- 读写锁优化读多写少的场景

## std::mutex

```cpp
#include <mutex>

std::mutex mtx;
int shared_counter = 0;

void increment() {
    mtx.lock();              // 加锁（阻塞等待）
    ++shared_counter;        // 临界区
    mtx.unlock();            // 解锁
    // ⚠️ 异常时 unlock 不会被调用 → 死锁
}
```

## lock_guard（RAII 锁）

```cpp
// 推荐：RAII 自动管理锁的生命周期
void safe_increment() {
    std::lock_guard<std::mutex> lock(mtx);  // 构造时 lock，析构时 unlock
    ++shared_counter;
    // 即使抛异常，析构时也会 unlock
}

// C++17: 类模板参数推导
std::lock_guard lock(mtx);  // 自动推导为 lock_guard<mutex>
```

## unique_lock（灵活锁）

```cpp
#include <unique_lock>

// unique_lock：比 lock_guard 更灵活，支持延迟加锁、手动解锁
void transfer(Account& from, Account& to, int amount) {
    std::unique_lock<std::mutex> lock1(from.mtx, std::defer_lock);  // 不立即加锁
    std::unique_lock<std::mutex> lock2(to.mtx, std::defer_lock);

    std::lock(lock1, lock2);  // 同时锁两个，避免死锁

    if (from.balance >= amount) {
        from.balance -= amount;
        to.balance += amount;
    }
}

// 支持手动解锁（lock_guard 不行）
std::unique_lock<std::mutex> lock(mtx);
do_something_with_shared_data();
lock.unlock();                 // 手动释放锁
do_something_else_without_lock();
lock.lock();                   // 重新加锁
do_more_with_shared_data();
```

## shared_mutex（读写锁）

```cpp
#include <shared_mutex>

std::shared_mutex rw_mtx;
std::map<std::string, int> cache;

// 读操作：共享锁（多个读者可同时进入）
int read(const std::string& key) {
    std::shared_lock<std::shared_mutex> lock(rw_mtx);  // 共享锁
    return cache[key];
}

// 写操作：独占锁（排斥所有读者和写者）
void write(const std::string& key, int val) {
    std::unique_lock<std::shared_mutex> lock(rw_mtx);  // 独占锁
    cache[key] = val;
}
```

## scoped_lock（C++17，多锁）

```cpp
// 同时锁多个 mutex，无死锁
std::mutex m1, m2;

void safe_transfer() {
    std::scoped_lock lock(m1, m2);  // 同时锁 m1 和 m2
    // ... 修改两个共享数据 ...
}
// 比 unique_lock + std::lock 更简洁
```

## 关键要点

> 永远用 RAII 锁（`lock_guard`, `unique_lock`, `scoped_lock`）代替手动 `lock()/unlock()`——异常安全是不可协商的。

> 持有锁时尽量不调用可能阻塞的操作（I/O、获取另一个锁），避免死锁和性能问题。

## 相关模式 / 关联

- [[cpp-thread与线程管理]] — 线程创建
- [[cpp-condition-variable]] — 配合 mutex 的条件变量
