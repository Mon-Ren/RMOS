---
title: future、async 与 promise
tags: [cpp, concurrency, future, async, promise, packaged-task]
aliases: [future, async, promise, 异步任务, packaged_task, 异步返回值]
created: 2026-04-04
updated: 2026-04-04
---

# future、async 与 promise

`std::future` 是一次性异步结果的接收端——比直接用线程更高层，自动处理线程管理和结果传递。

## 意图与场景

- 异步执行函数并获取返回值
- 线程间传递单次结果
- 简单的并行计算（不需要线程池）

## std::async

```cpp
#include <future>
#include <iostream>

int compute(int n) {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    return n * n;
}

int main() {
    // 异步执行，返回 future
    std::future<int> fut = std::async(std::launch::async, compute, 42);

    // 做其他事...
    std::cout << "Computing...\n";

    // 获取结果（阻塞直到完成）
    int result = fut.get();  // 只能调用一次！
    std::cout << "Result: " << result << "\n";
}
```

## launch 策略

```cpp
// std::launch::async — 强制异步执行（新线程）
auto f1 = std::async(std::launch::async, compute, 10);

// std::launch::deferred — 延迟执行（调用 get/wait 时在当前线程执行）
auto f2 = std::async(std::launch::deferred, compute, 20);

// 默认：由实现决定（可能是 async 也可能是 deferred）
// ⚠️ 默认策略可能导致"不是真异步"——重要场景显式指定 async
auto f3 = std::async(compute, 30);  // 不确定是否异步！
```

## std::promise

```cpp
#include <future>

// promise：结果的写入端
std::promise<int> prom;
std::future<int> fut = prom.get_future();  // 获取对应的 future

// 生产者线程
std::thread producer([&prom] {
    int result = expensive_computation();
    prom.set_value(result);     // 设置结果
    // prom.set_exception(e);  // 或设置异常
});

// 消费者
int value = fut.get();  // 阻塞等待结果
producer.join();
```

## std::packaged_task

```cpp
// packaged_task：包装可调用对象为异步任务
std::packaged_task<int(int)> task(compute);
std::future<int> fut = task.get_future();

std::thread t(std::move(task), 42);
int result = fut.get();
t.join();
```

## future 的局限

```cpp
// ❌ future 不支持连续（continuation）
// ❌ future 不支持组合（when_all, when_any）
// ❌ future::get() 只能调用一次

// C++20 的改进有限，实际项目推荐：
// - Boost.Asio（异步 I/O）
// - libunifex（Facebook）
// - cppcoro（协程库）
// - 自定义 task + coroutine
```

## 关键要点

> `std::async` 是最简单的异步方式，但默认策略可能不是真异步——重要场景显式指定 `std::launch::async`。

> `future::get()` 只能调用一次且会阻塞——第二次调用是未定义行为。future 不是并发的全部解决方案，复杂场景需要更强大的库。

## 相关模式 / 关联

- [[cpp-协程]] — C++20 的现代异步方案
- [[cpp-thread与线程管理]] — 底层线程控制
