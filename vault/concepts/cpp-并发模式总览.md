---
title: C++ 并发模式总览
tags: [cpp, concurrency, pattern, overview, thread, async, coroutine]
aliases: [并发模式, concurrency pattern, 并发概述, 异步模式]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 并发模式总览

C++ 提供多个层次的并发抽象——从底层原子操作到高层协程，选择合适的层次是设计的关键。

## 并发层次

```
高层 ──────────────────────────────── 低层

协程 (C++20)
  ↓ co_await/co_yield 挂起恢复
async/future (C++11)
  ↓ 异步任务 + 结果获取
线程池 (第三方库)
  ↓ 复用线程 + 任务队列
jthread (C++20)
  ↓ 自动 join + 停止令牌
thread (C++11)
  ↓ 手动管理线程
mutex/condition_variable (C++11)
  ↓ 同步原语
atomic (C++11)
  ↓ 无锁操作
内存序 (C++11)
  ↓ 最底层的可见性保证
```

## 选择指南

```
场景                          推荐方案
────────────────────────────────────────
简单并行计算                  std::async
长时间运行的后台任务          jthread + stop_token
大量短任务                    线程池
异步 I/O                      协程
高并发无锁数据结构            atomic
读多写少                      shared_mutex
生产者-消费者                 mutex + condition_variable
```

## 组合使用

```cpp
// 线程池 + future 获取结果
ThreadPool pool(4);
auto future = pool.submit([] { return compute(); });
int result = future.get();

// jthread + condition_variable
std::jthread worker([](std::stop_token st) {
    std::mutex mtx;
    std::condition_variable_any cv;
    while (!st.stop_requested()) {
        cv.wait(lock, st, [&] { return has_work(); });
        do_work();
    }
});

// 协程 + 异步 I/O
Task<int> async_read(std::string path) {
    auto data = co_await async_read_file(path);
    co_return parse(data);
}
```

## 关键要点

> 简单并行用 `async`，长期任务用 `jthread`，大量任务用线程池，异步 I/O 用协程。不要用 `thread` 做短期任务——创建开销太大。

> 并发编程的核心原则：减少共享可变状态。优先用不可变数据、消息传递、或 `atomic`。

## 相关模式 / 关联

- [[cpp-thread与线程管理]] — 线程基础
- [[cpp-future与async]] — 异步任务
- [[cpp-协程]] — C++20 协程
