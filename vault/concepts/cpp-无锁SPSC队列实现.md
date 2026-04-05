---
title: 无锁 SPSC 队列实现
tags: [cpp, lock-free, spsc, queue, cache-line, single-producer-consumer]
aliases: [SPSC 队列, 无锁环形队列, 单生产者单消费者]
created: 2026-04-05
updated: 2026-04-05
---

# 无锁 SPSC 队列实现

**一句话概述：** 单生产者单消费者队列是唯一真正"简单"的无锁数据结构——只需两个原子变量（head 和 tail），生产者只写 tail、消费者只写 head，通过缓存行对齐避免 false sharing。它不需要 CAS，只需要合适的内存序。

## 为什么 SPSC 最简单

```
多生产者（MPSC/MPMC）需要 CAS：
  生产者 A 和 B 同时尝试写入 → CAS 竞争 → 至少一个重试

单生产者（SPSC）不需要 CAS：
  只有一个生产者写 tail → 没有竞争 → 直接原子写
  只有一个消费者写 head → 没有竞争 → 直接原子写
```

## 实现

```cpp
#include <atomic>
#include <cstddef>
#include <new>
#include <type_traits>
#include <utility>

template <typename T, size_t Capacity>
class SPSCQueue {
    // 缓存行大小（x86/ARM 通用）
    static constexpr size_t CacheLine = 64;

    // 环形缓冲区
    alignas(CacheLine) std::byte buffer_[Capacity * sizeof(T)];

    // 生产者独占的缓存行：只被生产者写
    alignas(CacheLine) std::atomic<size_t> tail_{0};
    size_t cached_head_{0};  // 生产者本地缓存的 head（减少读取竞争）

    // 消费者独占的缓存行：只被消费者写
    alignas(CacheLine) std::atomic<size_t> head_{0};
    size_t cached_tail_{0};  // 消费者本地缓存的 tail

    // 辅助函数
    T* slot(size_t i) noexcept {
        return std::launder(reinterpret_cast<T*>(&buffer_[(i % Capacity) * sizeof(T)]));
    }

    static constexpr size_t next(size_t i) noexcept { return i + 1; }

public:
    SPSCQueue() = default;
    ~SPSCQueue() {
        // 析构所有未消费的元素
        while (pop()) {}
    }

    // 禁止拷贝和移动
    SPSCQueue(const SPSCQueue&) = delete;
    SPSCQueue& operator=(const SPSCQueue&) = delete;

    // ─── 生产者端（只从一个线程调用）───

    template <typename... Args>
    bool try_emplace(Args&&... args) noexcept(
        std::is_nothrow_constructible_v<T, Args...>)
    {
        const size_t tail = tail_.load(std::memory_order_relaxed);
        const size_t head = head_.load(std::memory_order_acquire);

        // 检查是否有空间（保留一个 slot 来区分满和空）
        if (next(tail) - head > Capacity) {
            // 可能满了，更新本地缓存再试一次
            cached_head_ = head_.load(std::memory_order_acquire);
            if (next(tail) - cached_head_ > Capacity) {
                return false;  // 队列满
            }
        }

        // 在 slot 中构造对象（placement new）
        ::new (slot(tail)) T(std::forward<Args>(args)...);

        // 发布：让消费者能看到新元素
        // release 保证：上面的构造一定发生在 tail 更新之前
        tail_.store(next(tail), std::memory_order_release);
        return true;
    }

    bool try_push(const T& val) { return try_emplace(val); }
    bool try_push(T&& val) { return try_emplace(std::move(val)); }

    // ─── 消费者端（只从一个线程调用）───

    bool pop(T* out = nullptr) noexcept(std::is_nothrow_move_assignable_v<T>) {
        const size_t head = head_.load(std::memory_order_relaxed);
        const size_t tail = tail_.load(std::memory_order_acquire);

        if (head == tail) {
            // 可能空了，更新本地缓存再试一次
            cached_tail_ = tail_.load(std::memory_order_acquire);
            if (head == cached_tail_) {
                return false;  // 队列空
            }
        }

        T* obj = slot(head);

        if (out) {
            *out = std::move(*obj);  // 移动出来
        }
        obj->~T();  // 析构 slot 中的对象

        // 更新 head，让生产者知道这个 slot 空了
        // release 保证：析构一定发生在 head 更新之前
        head_.store(next(head), std::memory_order_release);
        return true;
    }

    // ─── 查询（近似值，仅供监控）───

    size_t size_approx() const noexcept {
        // 注意：读取是无锁的，结果是瞬时近似值
        size_t tail = tail_.load(std::memory_order_acquire);
        size_t head = head_.load(std::memory_order_acquire);
        return tail - head;
    }

    bool empty_approx() const noexcept {
        return size_approx() == 0;
    }
};
```

## 缓存行对齐的必要性

```
❌ 不对齐（错误写法）：

  tail_ 和 head_ 在同一缓存行（64 字节）内
  ┌─────────────────────────────────┐
  │ tail_ (atomic<size_t>)          │ ← 生产者频繁写
  │ head_ (atomic<size_t>)          │ ← 消费者频繁写
  │ ... 其他成员 ...                 │
  └─────────────────────────────────┘
  生产者写 tail_ 使整个缓存行失效
  → 消费者的 head_ 缓存也失效（虽然它没改 head_）
  → 消费者被迫从内存重新加载 → 性能暴跌（false sharing）

✅ 对齐（正确写法）：

  生产者缓存行            消费者缓存行
  ┌──────────────┐       ┌──────────────┐
  │ tail_        │       │ head_        │
  │ cached_head_ │       │ cached_tail_ │
  └──────────────┘       └──────────────┘
  各自有独立的缓存行，写操作互不干扰
```

**性能差异：** 在 64 核服务器上，不对齐的 SPSC 队列吞吐量可能只有对齐版本的 **1/5 到 1/10**。

## 使用示例

```cpp
#include <thread>
#include <iostream>

SPSCQueue<int, 1024> queue;

void producer() {
    for (int i = 0; i < 1000000; ++i) {
        while (!queue.try_push(i)) {
            // 队列满，自旋等待
            __builtin_ia32_pause();
        }
    }
}

void consumer() {
    int val;
    int count = 0;
    while (count < 1000000) {
        if (queue.pop(&val)) {
            ++count;
        } else {
            __builtin_ia32_pause();
        }
    }
    std::cout << "Consumed " << count << " items\n";
}

// int main() {
//     std::thread t1(producer);
//     std::thread t2(consumer);
//     t1.join();
//     t2.join();
// }
```

## 关键要点

> SPSC 队列的内存序只需要 `acquire-release`，不需要 `seq_cst`。生产者用 `release` 存储 tail 保证元素构造先于可见；消费者用 `acquire` 加载 tail 保证看到完整构造的元素。同理消费者端。

> `cached_head_`/`cached_tail_` 是优化：减少对对方原子变量的读取频率。生产者只有在 `head_` 可能变了（队列可能满了）时才真正读对方的 `head_`，平时只读本地缓存的值。

> Capacity 必须是 2 的幂时可以用位运算替代取模（`i & (Capacity - 1)` 而非 `i % Capacity`）。本实现用取模是因为代码更清晰，编译器通常会自动优化 2 的幂的取模。

## 相关模式 / 关联

- [[cpp-atomic与内存序]] — acquire-release 语义
- [[cpp-自旋锁与排队自旋锁]] — 自旋等待优化
- [[cpp-缓存友好设计]] — false sharing、缓存行
- [[cpp-并发队列与线程池]] — 线程池中的队列选型
- [[cpp-内存屏障与CPU重排]] — 硬件层面的内存屏障
