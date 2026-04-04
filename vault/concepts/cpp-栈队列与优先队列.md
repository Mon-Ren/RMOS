---
title: 栈、队列与优先队列
tags: [cpp, stl, stack, queue, priority-queue, adapter]
aliases: [stack, queue, priority_queue, 栈适配器, 队列, 优先队列, 堆]
created: 2026-04-04
updated: 2026-04-04
---

# 栈、队列与优先队列

STL 的容器适配器——在底层容器之上提供受限接口，表达意图的同时限制误用。

## std::stack

```cpp
#include <stack>

std::stack<int> stk;           // 默认底层 deque
stk.push(1);                   // O(1)
stk.push(2);
stk.top();                     // 2 — 查看栈顶
stk.pop();                     // O(1) — 移除栈顶（无返回值！）

// 自定义底层容器
std::stack<int, std::vector<int>> vec_stk;  // 用 vector 做底层
std::stack<int, std::list<int>> list_stk;   // 用 list 做底层

// ⚠️ stack 不提供迭代器——这是设计意图
// for (auto it = stk.begin(); ...) // 编译错误
```

## std::queue

```cpp
#include <queue>

std::queue<int> q;
q.push(1);                    // O(1) 入队
q.push(2);
q.front();                    // 1 — 队首
q.back();                     // 2 — 队尾
q.pop();                      // O(1) 出队（移除队首）

// 默认底层 deque，也可以用 list
std::queue<int, std::list<int>> q2;
```

## std::priority_queue

```cpp
#include <queue>

// 最大堆（默认）
std::priority_queue<int> max_pq;
max_pq.push(3);
max_pq.push(1);
max_pq.push(4);
max_pq.top();                 // 4 — 最大元素
max_pq.pop();                 // 移除最大元素

// 最小堆
std::priority_queue<int, std::vector<int>, std::greater<int>> min_pq;
min_pq.push(3);
min_pq.push(1);
min_pq.top();                 // 1 — 最小元素

// 自定义类型
struct Task {
    int priority;
    std::string name;
};

auto cmp = [](const Task& a, const Task& b) { return a.priority < b.priority; };
std::priority_queue<Task, std::vector<Task>, decltype(cmp)> task_queue(cmp);
```

## 用 vector 实现栈

```cpp
// 如果需要迭代能力，可以用 vector 模拟栈
class IterableStack {
    std::vector<int> data_;
public:
    void push(int x) { data_.push_back(x); }
    void pop() { data_.pop_back(); }
    int top() const { return data_.back(); }
    bool empty() const { return data_.empty(); }
    auto begin() { return data_.rbegin(); }  // 反向迭代：栈顶在前
    auto end() { return data_.rend(); }
};
```

## 关键要点

> stack/queue/priority_queue 是容器适配器，不是独立容器——它们限制底层容器的接口以表达 LIFO/FIFO/优先级语义。

> `pop()` 不返回元素（避免异常安全问题）。先 `top()` 取值再 `pop()`。

## 相关模式 / 关联

- [[cpp-vector深入]] — priority_queue 的底层容器
- [[算法-堆与优先队列]] — 优先队列的堆实现原理
