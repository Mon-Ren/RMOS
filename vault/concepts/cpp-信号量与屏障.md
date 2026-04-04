---
title: 信号量、屏障与 latch（C++20）
tags: [cpp20, semaphore, barrier, latch, synchronization, counting]
aliases: [信号量, counting_semaphore, binary_semaphore, barrier, latch, 同步原语]
created: 2026-04-04
updated: 2026-04-04
---

# 信号量、屏障与 latch（C++20）

C++20 补充了三种同步原语——信号量、latch 和 barrier，填补了并发工具箱的空缺。

## counting_semaphore

```cpp
#include <semaphore>

// 信号量：控制同时访问资源的线程数
std::counting_semaphore<10> sem{3};  // 最大值10，初始值3

// P 操作（acquire）：计数减1，为0时阻塞
sem.acquire();

// V 操作（release）：计数加1，可能唤醒一个等待者
sem.release();

// 尝试获取（不阻塞）
if (sem.try_acquire()) { /* 获取成功 */ }

// 带超时
if (sem.try_acquire_for(std::chrono::seconds(1))) { /* 获取成功 */ }

// binary_semaphore：计数为1的信号量，等价于互斥量
std::binary_semaphore sem{1};  // 初始可用
sem.acquire();
sem.release();
```

## latch（一次性屏障）

```cpp
#include <latch>

// latch：等待 N 个事件到达，一次性使用
std::latch ready{3};  // 等待 3 个线程

// 工作线程
void worker(int id) {
    do_setup(id);
    ready.count_down();     // 通知到达
    ready.wait();           // 等待所有线程到达
    do_actual_work();       // 所有线程同时开始
}

// 主线程
ready.arrive_and_wait();  // 计数减1并等待（也可以参与）
```

## barrier（可重用屏障）

```cpp
#include <barrier>

// barrier：可重复使用的同步点（用于迭代算法）
std::barrier sync_point{4};  // 4 个线程

void parallel_loop(int thread_id) {
    for (int iter = 0; iter < 100; ++iter) {
        compute_chunk(thread_id, iter);
        sync_point.arrive_and_wait();  // 每轮迭代同步
    }
}

// completion function：每次所有线程到达时调用
std::barrier sync{4, []() { std::cout << "all arrived\n"; }};
```

## 关键要点

> `counting_semaphore` 控制资源并发数（如限制数据库连接数）。`latch` 用于一次性同步（如初始化阶段）。`barrier` 用于迭代同步（如并行迭代算法）。

> 这些原语的实现比 mutex + condition_variable 更高效——它们是底层原子操作的封装。

## 相关模式 / 关联

- [[cpp-mutex与lock]] — 传统同步原语
- [[cpp-condition-variable]] — 条件变量
