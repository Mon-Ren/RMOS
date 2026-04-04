---
title: 协程（C++20）
tags: [cpp20, coroutine, co_await, co_yield, co_return, generator]
aliases: [协程, coroutine, co_await, co_yield, generator, 异步编程]
created: 2026-04-04
updated: 2026-04-04
---

# 协程（C++20）

协程是可以暂停和恢复执行的函数——无需线程切换开销就能编写异步和惰性生成器代码。

## 意图与场景

- 异步 I/O：避免回调地狱
- 惰性序列生成：类似 Python 的 generator
- 状态机：用协程替代手写状态机
- 任务调度：cooperative multitasking

## 三个关键字

```cpp
co_await   // 挂起协程，等待异步操作完成
co_yield   // 挂起协程并返回一个值（生成器模式）
co_return  // 协程返回最终值并结束
// 函数体中出现任何一个 → 该函数就是协程
```

## Generator 示例（C++23 std::generator）

```cpp
#include <generator>  // C++23

// 惰性生成斐波那契数列
std::generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;          // 暂停并返回当前值
        auto next = a + b;
        a = b;
        b = next;
    }
}

// 使用
for (int fib : fibonacci() | std::views::take(10)) {
    std::cout << fib << " ";  // 0 1 1 2 3 5 8 13 21 34
}
```

## 协程机制

```cpp
// 编译器将协程转换为状态机：
// 1. 创建 coroutine frame（堆上或优化到栈上）
// 2. 在 co_await/co_yield/co_return 处保存局部变量到 frame
// 3. 返回控制权给调用者
// 4. 恢复时从 frame 恢复局部变量，继续执行

// co_await 表达式需要 Awaitable 对象
struct Task {
    struct promise_type {
        Task get_return_object() { return {}; }
        std::suspend_never initial_suspend() { return {}; }  // 立即开始
        std::suspend_always final_suspend() noexcept { return {}; }  // 结束时挂起
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
};

// Awaitable 接口
struct Timer {
    bool await_ready() { return false; }                           // 是否已就绪
    void await_suspend(std::coroutine_handle<> h) {               // 挂起时做什么
        schedule_resume_after(h, std::chrono::seconds(1));
    }
    int await_resume() { return 42; }                              // 恢复时返回什么
};
```

## 关键要点

> C++20 协程是无栈协程（stackless），协程帧在堆上分配（编译器可能优化）。它比线程轻量得多，但需要配套的调度器和 Awaitable 类型。

> C++20 只提供了底层机制（三个关键字 + promise_type 接口），标准库在 C++23 才补充了 `std::generator`。实际项目通常需要第三方库（cppcoro, libunifex）。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — 协程与 lambda 的交互
- [[cpp-异步编程模型]] — future/async/协程的对比
