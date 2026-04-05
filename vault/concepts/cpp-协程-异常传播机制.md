---
title: 协程异常传播机制
tags: [cpp20, coroutine, exception, unhandled-exception, propagation]
aliases: [协程异常处理, co_await 异常, 协程栈展开]
created: 2026-04-05
updated: 2026-04-05
---

# 协程异常传播机制

**一句话概述：** 协程中的异常不会跨挂起点自动传播——co_await 的 await_resume() 是异常的传播点。如果协程体抛出未捕获异常，调用 promise_type::unhandled_exception() 存储异常，等调用者 co_await 时在 await_resume() 中重新抛出。

## 异常传播链路

```cpp
Task<int> might_fail(int x) {
    if (x < 0) throw std::invalid_argument("negative");
    co_return x * 2;
}

Task<int> caller() {
    try {
        // might_fail 抛异常时：
        // 1. 异常在 might_fail 协程帧中捕获
        // 2. promise.unhandled_exception() 存储到 exception_ptr
        // 3. 跳到 final_suspend
        // 4. caller co_await 时，awaiter::resume 检查 exception_ptr
        // 5. 在 caller 的 await_resume 中重新抛出
        int result = co_await might_fail(-1);
        co_return result;
    } catch (const std::invalid_argument& e) {
        // 在 caller 中捕获 → 异常跨协程传播成功
        co_return -1;
    }
}
```

## 三种异常处理策略

```cpp
// 策略 1：promise_type 中直接 terminate
struct Promise1 {
    void unhandled_exception() { std::terminate(); }
    // 适合：不期望异常的简单协程
};

// 策略 2：存储异常，延迟抛出（标准做法）
struct Promise2 {
    std::exception_ptr exception_;
    void unhandled_exception() {
        exception_ = std::current_exception();
    }
    // 在 await_resume 中检查并重新抛出
};

// 策略 3：将异常转为错误值（expected 风格）
struct Promise3 {
    std::variant<int, std::exception_ptr> result_;
    void unhandled_exception() {
        result_ = std::current_exception();
    }
    // await_resume 返回 expected 而非直接抛出
};
```

## 关键要点

> 协程的异常不会"穿透"多个 co_await。每个 co_await 是独立的异常边界。协程 A co_await 协程 B，B 的异常在 A 的 co_await 点被重新抛出，A 可以 catch 它。

> co_await 的 await_ready 返回 true 时不会调用 await_suspend，异常直接在 await_resume 中抛出。所以 await_ready 不能抛异常——它应该是纯粹的无副作用检查。

## 相关模式 / 关联

- [[cpp-协程机制深入]] — promise_type 完整机制
- [[cpp-异常处理]] — 异常基础
- [[cpp-异常安全深入]] — 异常安全保证
- [[cpp-Rust风格Result在C++中的实践]] — expected 替代异常
