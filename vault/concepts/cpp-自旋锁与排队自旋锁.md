---
title: 自旋锁与排队自旋锁
tags: [cpp, concurrency, spinlock, mcs-lock, ticket-lock, fairness]
aliases: [自旋锁实现, ticket lock, MCS lock, 排队自旋锁]
created: 2026-04-05
updated: 2026-04-05
---

# 自旋锁与排队自旋锁

**一句话概述：** 基础自旋锁用 CAS 忙等，简单但不公平（后来的线程可能先抢到锁）；Ticket Lock 用两个计数器实现 FIFO 公平；MCS Lock 用链表让每个线程在自己的节点上自旋，解决多核扩展性问题。

## 意图与场景

- 临界区极短（<1μs）时自旋锁比互斥锁高效
- 理解不同自旋锁的公平性和扩展性权衡
- 知道什么时候该用什么锁

## 三种实现

### 1. 基础自旋锁（Test-and-Set）

```cpp
#include <atomic>

class SpinLock {
    std::atomic<bool> locked_{false};
public:
    void lock() {
        for (;;) {
            // 尝试从 false 改为 true
            if (!locked_.exchange(true, std::memory_order_acquire)) {
                return;  // 拿到锁
            }
            // 拿不到就自旋：先读一下，减少缓存行流量
            while (locked_.load(std::memory_order_relaxed)) {
                __builtin_ia32_pause();  // x86 提示 CPU 这是在自旋
                // pause 的作用：
                // 1. 减少功耗
                // 2. 减少内存顺序违规（memory order violation）
                // 3. 让超线程伙伴有机会执行
            }
        }
    }

    void unlock() {
        locked_.store(false, std::memory_order_release);
    }
};
```

**问题：** 不公平。10 个线程竞争，可能某个线程永远抢不到（饥饿）。而且所有线程都在同一个 `locked_` 上自旋，释放锁时所有线程同时醒来抢，造成缓存行乒乓（cache line bouncing）。

### 2. Ticket Lock（排队锁）

```cpp
#include <atomic>

class TicketLock {
    std::atomic<size_t> next_ticket_{0};   // 发号器
    std::atomic<size_t> now_serving_{0};   // 当前叫号
public:
    void lock() {
        const auto ticket = next_ticket_.fetch_add(1, std::memory_order_relaxed);
        // 拿到号码后，等叫到自己的号
        while (now_serving_.load(std::memory_order_acquire) != ticket) {
            __builtin_ia32_pause();
        }
    }

    void unlock() {
        // 叫下一个号
        const auto next = now_serving_.load(std::memory_order_relaxed) + 1;
        now_serving_.store(next, std::memory_order_release);
    }
};
```

**优势：** 严格 FIFO，绝对公平。每个线程按拿号顺序获得锁。

**问题：** 在大量核心（>16 核）上扩展性差——`now_serving_` 变成热点，所有核心都要读这个变量来检查是否轮到自己。释放锁时所有等待的缓存行都要失效。

### 3. MCS Lock（链表排队锁）

```cpp
#include <atomic>

class MCSLock {
public:
    struct Node {
        std::atomic<Node*> next{nullptr};
        std::atomic<bool> waiting{true};  // 是否需要等待
    };

private:
    std::atomic<Node*> tail_{nullptr};

public:
    void lock(Node* my_node) {
        my_node->next.store(nullptr, std::memory_order_relaxed);
        my_node->waiting.store(true, std::memory_order_relaxed);

        // 把自己接到链表尾部
        Node* prev = tail_.exchange(my_node, std::memory_order_acquire);

        if (prev != nullptr) {
            // 前面有人，把自己设为前驱的 next
            prev->next.store(my_node, std::memory_order_release);
            // 在自己的 waiting 标志上自旋（不是共享变量！）
            while (my_node->waiting.load(std::memory_order_acquire)) {
                __builtin_ia32_pause();
            }
        }
        // prev == nullptr → 我是第一个，直接拿锁
    }

    void unlock(Node* my_node) {
        // 检查有没有后继
        Node* succ = my_node->next.load(std::memory_order_acquire);

        if (succ == nullptr) {
            // 没有后继，尝试把 tail 设回 nullptr
            Node* expected = my_node;
            if (tail_.compare_exchange_strong(expected, nullptr,
                    std::memory_order_release, std::memory_order_relaxed)) {
                return;  // 成功，锁空闲
            }
            // CAS 失败说明有新线程刚进来，等它设置 next
            while ((succ = my_node->next.load(std::memory_order_acquire)) == nullptr) {
                __builtin_ia32_pause();
            }
        }
        // 唤醒后继
        succ->waiting.store(false, std::memory_order_release);
    }
};
```

**MCS 的关键创新：** 每个线程在**自己的 `Node::waiting`** 上自旋，而不是在共享变量上。释放锁时只唤醒下一个线程。这消除了缓存行乒乓，在多核上扩展性极好。

## 三种锁对比

| 特性 | TAS Spinlock | Ticket Lock | MCS Lock |
|------|-------------|-------------|----------|
| 公平性 | 不公平 | 严格 FIFO | 严格 FIFO |
| 缓存行流量 | 高（共享变量） | 中（热点变量） | 低（各自节点） |
| 16+ 核扩展性 | 差 | 中 | 好 |
| 实现复杂度 | 极简 | 简单 | 中等 |
| 锁内必须持有 Node | 否 | 否 | **是** |

## 关键要点

> 自旋锁只在临界区极短时才有意义（< 1 微秒）。如果临界区可能被调度出去（比如做系统调用），应该用互斥锁（futex-based），否则自旋白白浪费 CPU。

> `__builtin_ia32_pause()`（或 C++20 的 `std::this_thread::yield()` 的轻量版）不是"让出 CPU"，而是告诉 CPU"我在自旋等一个很快会变的值"——CPU 会降低流水线密度、减少功耗、给超线程伙伴腾出执行资源。

> Linux 内核使用的是 Ticket Lock 的变体和 qspinlock（基于 MCS 的队列锁）。用户态一般用 futex（`pthread_mutex_t`）就够，只有极低延迟场景需要自旋锁。

## 相关模式 / 关联

- [[cpp-mutex与lock]] — 标准库互斥锁
- [[cpp-atomic与内存序]] — 原子操作基础
- [[cpp-并发中的死锁与避免]] — 锁的正确使用
- [[cpp-内存屏障与CPU重排]] — 硬件内存屏障
- [[无锁数据结构]] — CAS-based 并发数据结构
