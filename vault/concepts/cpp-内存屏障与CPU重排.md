---
title: 内存屏障与 CPU 重排
tags: [cpp, memory-barrier, cpu-reorder, fence, SFENCE, LFENCE, MFENCE]
aliases: [内存屏障, CPU重排, fence, SFENCE, LFENCE, MFENCE, 编译器屏障]
created: 2026-04-04
updated: 2026-04-04
---

# 内存屏障与 CPU 重排

CPU 和编译器都会重排指令——内存屏障确保操作的可见性和顺序。

## 为什么需要屏障

```cpp
// 单线程：重排不影响结果
int x = 1;
int y = 2;
// CPU 可能先写 y 再写 x——单线程无影响

// 多线程：重排导致意外结果
int data = 0;
bool ready = false;

// 线程 1
data = 42;           // 写数据
ready = true;        // 标记就绪

// 线程 2
while (!ready) {}    // 等待就绪
// data 可能还是 0！因为 CPU 可以重排写操作
// 线程 2 看到 ready=true 时，data=42 可能还没对线程 2 可见
```

## 内存屏障类型

```cpp
#include <atomic>

// 编译器屏障（不阻止 CPU 重排）
asm volatile ("" ::: "memory");

// CPU 内存屏障
// SFENCE：写屏障（store fence）——确保之前的写操作在之后的写操作之前完成
// LFENCE：读屏障（load fence）——确保之前的读操作在之后的读操作之前完成
// MFENCE：全屏障（full fence）——确保所有之前的读写在之后的读写之前完成

// C++ 中通过 atomic 的内存序间接使用
std::atomic<bool> flag{false};
int data = 0;

// 生产者：release 保证之前的写对 acquire 之后可见
data = 42;
flag.store(true, std::memory_order_release);  // 隐含写屏障

// 消费者：acquire 保证之后的读能看到 release 之前的写
while (!flag.load(std::memory_order_acquire)) {}  // 隐含读屏障
assert(data == 42);  // 保证成立
```

## 关键要点

> C++ 中不需要直接使用 CPU 内存屏障——`atomic` 的 `memory_order_release/acquire` 自动插入必要的屏障。

> `memory_order_seq_cst` 在所有原子操作上插入全屏障——最安全但最慢。

## 相关模式 / 关联

- [[cpp-atomic与内存序]] — atomic 的内存序
- [[cpp-内存模型与数据竞争]] — 内存模型
