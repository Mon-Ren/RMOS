---
title: 内存模型与数据竞争
tags: [cpp, concurrency, memory-model, data-race, happens-before, visibility]
aliases: [内存模型, 数据竞争, happens-before, 可见性, memory model, 并发安全]
created: 2026-04-04
updated: 2026-04-04
---

# 内存模型与数据竞争

C++ 内存模型定义了多线程中操作的可见性和排序规则——理解它是编写正确并发程序的基础。

## 数据竞争

```cpp
// 数据竞争：两个线程同时访问同一内存位置，至少一个是写操作
int shared = 0;

// 线程 1
shared = 42;        // 写

// 线程 2
int x = shared;     // 读——与线程 1 的写并发 → 数据竞争 → UB！

// 数据竞争 = 未定义行为，不只是"结果不确定"
// 编译器可以做任何优化，包括生成错误代码
```

## happens-before 关系

```
操作 A happens-before 操作 B 意味着：
1. A 在 B 之前执行
2. A 的所有副作用对 B 可见

建立 happens-before 的方式：
- 同一线程内：按程序顺序（sequenced-before）
- 跨线程：
  - mutex unlock → 另一线程 lock（同 mutex）
  - atomic release → 另一线程 acquire（同变量）
  - thread 创建 → 线程函数的开始
  - thread::join() 返回 → join 之后的操作
```

## 避免数据竞争

```cpp
// 方式一：mutex
std::mutex mtx;
int shared = 0;

void safe_update() {
    std::lock_guard<std::mutex> lock(mtx);
    shared = 42;  // 临界区内，无竞争
}

// 方式二：atomic
std::atomic<int> atomic_shared{0};

void atomic_update() {
    atomic_shared.store(42, std::memory_order_release);
}

// 方式三：thread_local——每个线程独立副本
thread_local int local_counter = 0;

// 方式四：消息传递——不共享可变状态
// 生产者通过队列传数据给消费者
```

## 编译器重排

```cpp
// 编译器和 CPU 可以重排指令（只要单线程语义不变）
int x = 0, y = 0;

// 线程 1          线程 2
x = 1;             y = 1;
int r1 = y;        int r2 = x;

// 理论上 r1 和 r2 可以同时为 0！
// 因为没有同步机制保证可见性顺序
// 加上 acquire-release 后可以排除这种情况
```

## 关键要点

> 数据竞争是 UB——不是"结果不确定"，而是"程序行为完全不可预测"。用 mutex、atomic、message passing 避免所有数据竞争。

> C++ 内存模型保证 happens-before 关系——只有建立了 happens-before 的操作之间才有可见性保证。

## 相关模式 / 关联

- [[cpp-atomic与内存序]] — 建立跨线程的 happens-before
- [[cpp-mutex与lock]] — mutex 建立 happens-before
