---
title: C++ 容器适配器深入
tags: [cpp, stl, adapter, container-adapter, stack, queue, priority-queue]
aliases: [容器适配器, container adapter, adapter pattern, 适配器模式]
created: 2026-04-04
updated: 2026-04-04
---

# 容器适配器深入

容器适配器在底层容器之上提供受限接口——它们不是新容器，而是已有容器的"视图"。

## 适配器的本质

```cpp
// stack 默认用 deque 做底层
template <typename T, typename Container = std::deque<T>>
class stack {
protected:
    Container c_;  // 底层容器
public:
    bool empty() const { return c_.empty(); }
    size_t size() const { return c_.size(); }
    T& top() { return c_.back(); }
    void push(const T& x) { c_.push_back(x); }
    void pop() { c_.pop_back(); }
    // 注意：没有 begin()/end()——这是设计意图
};

// 可以换底层容器
std::stack<int, std::vector<int>> stk;  // 用 vector 做底层
std::stack<int, std::list<int>> stk2;   // 用 list 做底层
```

## 自定义适配器

```cpp
// 用 vector 模拟环形缓冲区
template <typename T, size_t Capacity>
class RingBuffer {
    std::vector<T> data_;
    size_t head_ = 0, tail_ = 0, count_ = 0;
public:
    RingBuffer() : data_(Capacity) {}

    void push(T val) {
        data_[tail_] = std::move(val);
        tail_ = (tail_ + 1) % Capacity;
        if (count_ < Capacity) ++count_;
        else head_ = (head_ + 1) % Capacity;
    }

    T pop() {
        T val = std::move(data_[head_]);
        head_ = (head_ + 1) % Capacity;
        --count_;
        return val;
    }

    bool empty() const { return count_ == 0; }
    bool full() const { return count_ == Capacity; }
    size_t size() const { return count_; }
};
```

## 关键要点

> 容器适配器的核心价值是**限制接口**——stack 不暴露 begin/end，强制只能 LIFO 操作。这是类型安全的设计。

> 自定义底层容器的条件：必须支持适配器需要的操作（如 stack 需要 back/push_back/pop_back）。

## 相关模式 / 关联

- [[cpp-栈队列与优先队列]] — 三种标准适配器
- [[cpp-vector深入]] — 常用底层容器
