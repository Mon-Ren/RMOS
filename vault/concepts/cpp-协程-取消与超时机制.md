---
title: 协程取消与超时机制
tags: [cpp20, coroutine, cancellation, timeout, stop-token]
aliases: [协程取消, 异步超时, stop_token 协程]
created: 2026-04-05
updated: 2026-04-05
---

# 协程取消与超时机制

**一句话概述：** 协程的取消不是"杀死线程"——而是通过共享的 stop_flag 让协程在下一个检查点自愿退出。超时 = 取消 + 定时器：设置一个定时器，到期时设置 stop_flag，协程恢复时检查并退出。

## 取消机制设计

```cpp
#include <coroutine>
#include <atomic>
#include <chrono>
#include <functional>

// 取消令牌
class CancellationToken {
    std::shared_ptr<std::atomic<bool>> flag_;
public:
    CancellationToken()
        : flag_(std::make_shared<std::atomic<bool>>(false)) {}

    void cancel() { flag_->store(true, std::memory_order_release); }
    bool is_cancelled() const {
        return flag_->load(std::memory_order_acquire);
    }
};

// 协程取消点 Awaitable
struct CancellationPoint {
    CancellationToken token;

    bool await_ready() const { return token.is_cancelled(); }
    void await_suspend(std::coroutine_handle<>) {}
    void await_resume() {
        if (token.is_cancelled())
            throw OperationCancelled{};
    }
};

struct OperationCancelled : std::exception {
    const char* what() const noexcept override {
        return "Operation cancelled";
    }
};
```

## 超时实现

```cpp
// 带超时的 co_await
template <typename Awaitable>
struct WithTimeout {
    Awaitable awaitable;
    std::chrono::milliseconds timeout;
    CancellationToken token;

    bool await_ready() { return awaitable.await_ready(); }

    void await_suspend(std::coroutine_handle<> h) {
        // 注册超时定时器
        TimerWheel::instance().add(timeout, [this, h]() {
            token.cancel();  // 超时 → 取消
            if (!awaitable.await_ready()) {
                h.resume();  // 恢复协程让它检查取消状态
            }
        });
        // 注册 IO 等待
        awaitable.await_suspend(h);
    }

    auto await_resume() -> decltype(awaitable.await_resume()) {
        if (token.is_cancelled())
            throw TimeoutError{};
        return awaitable.await_resume();
    }
};

// 使用
Task<std::string> fetch_with_timeout(int fd) {
    char buf[4096];
    CancellationToken token;

    try {
        auto n = co_await WithTimeout{
            AsyncRead(fd, buf, sizeof(buf)),
            std::chrono::seconds(5),  // 5 秒超时
            token
        };
        co_return std::string(buf, n);
    } catch (const TimeoutError&) {
        co_return "timeout";
    }
}
```

## 协作式取消循环

```cpp
Task<void> long_running_computation(CancellationToken token, Data data) {
    for (size_t i = 0; i < data.size(); ++i) {
        // 每处理 1000 个元素检查一次取消状态
        if (i % 1000 == 0) {
            co_await CancellationPoint{token};  // 取消点
        }
        process(data[i]);
    }
    co_return;
}

// 调用者
auto token = CancellationToken{};
auto task = long_running_computation(token, huge_data);
task.resume();

// 3 秒后取消
std::thread([&token] {
    std::this_thread::sleep_for(std::chrono::seconds(3));
    token.cancel();
}).detach();
```

## 关键要点

> 协程取消必须是协作式的——协程自己决定何时检查取消状态。这和线程的 `pthread_cancel` 不同（可以强制中断）。协作式取消更安全（不会在不安全的点中断），但需要协程代码显式放置取消点。

> `CancellationToken` 用 shared_ptr<atomic<bool>> 而非普通 atomic 是因为 token 需要跨协程、跨线程共享。如果 token 是值拷贝，取消操作只影响副本。

> 超时机制的核心：定时器和 IO 操作竞争。谁先完成，谁决定协程的下一步。定时器先到 → 设置取消标志 → 协程恢复时抛异常。IO 先到 → 正常返回结果。

## 相关模式 / 关联

- [[cpp-协程-task调度器实现]] — task 调度器
- [[cpp-协程-异步IO集成]] — 异步 IO
- [[cpp-jthread与协作式取消]] — std::jthread 的 stop_token
- [[cpp-condition-variable]] — 条件变量与超时
- [[cpp-异步编程模型对比]] — 各异步模型对比
