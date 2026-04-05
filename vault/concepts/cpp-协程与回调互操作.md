---
title: 协程与回调互操作
tags: [cpp20, coroutine, callback, bridge, legacy-code]
aliases: [协程回调桥接, 异步回调转协程, legacy 异步集成]
created: 2026-04-05
updated: 2026-04-05
---

# 协程与回调互操作

**一句话概述：** 现实中大量异步 API 是回调风格的——协程的实用价值取决于能否与现有回调代码无缝桥接。核心技巧：写一个 Awaitable，在 `await_suspend` 中注册回调，回调触发时 `resume` 协程。

## 回调 → Awaitable 桥接

```cpp
#include <coroutine>
#include <functional>
#include <memory>

// 假设这是现有的回调风格 API
using Callback = std::function<void(int error_code, std::string data)>;
void legacy_async_fetch(const std::string& url, Callback cb);

// 桥接：回调风格 → co_await 风格
class AsyncFetch {
    std::string url_;
    std::string result_;
    int error_ = 0;

public:
    explicit AsyncFetch(std::string url) : url_(std::move(url)) {}

    bool await_ready() const { return false; }

    void await_suspend(std::coroutine_handle<> h) {
        // 注册回调：回调触发时恢复协程
        legacy_async_fetch(url_, [this, h](int err, std::string data) {
            error_ = err;
            result_ = std::move(data);
            h.resume();  // ← 关键：回调中恢复协程
        });
    }

    std::string await_resume() {
        if (error_) throw std::runtime_error("fetch failed: " + std::to_string(error_));
        return std::move(result_);
    }
};

// 使用：回调代码的调用方式变了，但内部仍是回调
Task<std::string> fetch_page(const std::string& url) {
    auto html = co_await AsyncFetch(url);  // 像同步代码
    co_return html;
}
```

## 多次回调（事件流）→ Generator

```cpp
// 假设有一个事件回调 API
using EventHandler = std::function<void(const Event&)>;
void register_handler(EventHandler cb);

// 转为 generator
std::generator<Event> event_stream() {
    struct State {
        std::coroutine_handle<> continuation;
        std::optional<Event> event;
    };
    auto state = std::make_shared<State>();

    register_handler([state](const Event& e) {
        state->event = e;
        if (state->continuation) {
            state->continuation.resume();
        }
    });

    while (true) {
        co_await SuspendWith([state](std::coroutine_handle<> h) {
            state->continuation = h;
        });
        co_yield std::move(*state->event);
    }
}
```

## 关键要点

> 桥接的关键是 `await_suspend` 中捕获 `coroutine_handle` 并在回调中调用 `resume`。`coroutine_handle` 可以安全地跨线程传递——但要注意回调可能在不同线程触发，需要确保线程安全。

> 如果回调可能多次触发（如数据流、事件系统），应该用 generator 而非 task。task 产生一个值后结束，generator 可以持续产生值。

> 逐步迁移策略：先将核心异步路径从回调改为协程，边缘的回调 API 用 Awaitable 桥接。不需要一次性重写所有代码。

## 相关模式 / 关联

- [[cpp-协程机制深入]] — 协程底层
- [[cpp-协程-task调度器实现]] — task 调度
- [[cpp-协程-generator与惰性序列]] — generator
- [[cpp-异步编程模型对比]] — 回调 vs future vs 协程
- [[cpp-函数指针与function]] — std::function
