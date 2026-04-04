---
title: C++ 并发安全的数据结构设计
tags: [cpp, concurrent, thread-safe, data-structure, lock-free, fine-grained]
aliases: [并发数据结构, 线程安全容器, 细粒度锁, 无锁队列]
created: 2026-04-04
updated: 2026-04-04
---

# 并发安全的数据结构设计

设计并发数据结构有两种思路：粗粒度锁（简单但慢）和细粒度锁/无锁（复杂但快）。

## 粗粒度锁

```cpp
// 一把锁保护整个数据结构——简单但争用激烈
template <typename T>
class ThreadSafeStack {
    std::mutex mtx_;
    std::vector<T> data_;
public:
    void push(T val) {
        std::lock_guard<std::mutex> lock(mtx_);
        data_.push_back(std::move(val));
    }
    std::optional<T> pop() {
        std::lock_guard<std::mutex> lock(mtx_);
        if (data_.empty()) return std::nullopt;
        auto val = std::move(data_.back());
        data_.pop_back();
        return val;
    }
};
```

## 细粒度锁（链表）

```cpp
// 每个节点一把锁——并发度高
template <typename T>
class ConcurrentList {
    struct Node {
        T data;
        std::unique_ptr<Node> next;
        std::mutex mtx;
    };
    Node head_;  // 哨兵节点
public:
    void insert(T val) {
        auto node = std::make_unique<Node>(std::move(val));
        std::lock_guard<std::mutex> lock(head_.mtx);
        node->next = std::move(head_.next);
        head_.next = std::move(node);
    }
};
```

## 无锁栈（CAS）

```cpp
template <typename T>
class LockFreeStack {
    struct Node {
        T data;
        Node* next;
    };
    std::atomic<Node*> head_{nullptr};
public:
    void push(T val) {
        auto node = new Node{std::move(val), head_.load()};
        while (!head_.compare_exchange_weak(node->next, node)) {}
    }
    std::optional<T> pop() {
        Node* old = head_.load();
        while (old && !head_.compare_exchange_weak(old, old->next)) {}
        if (!old) return std::nullopt;
        T val = std::move(old->data);
        delete old;  // ⚠️ ABA 问题！实际需要 hazard pointer 或 epoch-based 回收
        return val;
    }
};
```

## 设计选择

```
争用低（<4 线程）     → 粗粒度锁（简单，性能够用）
争用高（读多写少）    → shared_mutex
争用高（写也多）      → 细粒度锁或无锁
性能极端要求          → 无锁（但正确性难保证）
```

## 关键要点

> 无锁数据结构的难点不是 CAS，而是**内存回收**——CAS 后被删除的节点可能正被其他线程读取。需要 hazard pointer、RCU 或 epoch-based 回收。

> 大部分场景粗粒度锁就够了——无锁只在性能分析证明锁是瓶颈时才考虑。

## 相关模式 / 关联

- [[cpp-atomic与内存序]] — CAS 操作
- [[cpp-并发队列与线程池]] — 并发队列
