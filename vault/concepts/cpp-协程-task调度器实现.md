---
title: 协程 task 调度器实现
tags: [cpp20, coroutine, task, scheduler, thread-pool]
aliases: [协程调度器, task 调度, 异步任务执行器]
created: 2026-04-05
updated: 2026-04-05
---

# 协程 task 调度器实现

**一句话概述：** 协程本身不决定在哪个线程恢复——调度器决定。一个完整的 async task 需要：promise_type 管理协程状态、co_await 时挂起并注册回调、调度器（线程池）在合适的线程恢复执行。

## Task 类型设计

```cpp
#include <coroutine>
#include <thread>
#include <functional>
#include <optional>
#include <exception>

template <typename T>
class Task {
public:
    struct promise_type {
        std::optional<T> result_;
        std::exception_ptr exception_;
        std::coroutine_handle<> continuation_;  // 谁在等待这个 task

        Task get_return_object() {
            return Task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        // 惰性启动：创建后不立即执行
        std::suspend_always initial_suspend() { return {}; }

        // co_return 时保存结果
        void return_value(T value) {
            result_ = std::move(value);
        }

        // 最终挂起：如果有 continuation，唤醒它
        auto final_suspend() noexcept {
            struct Awaiter {
                bool await_ready() noexcept { return false; }
                std::coroutine_handle<> await_suspend(
                    std::coroutine_handle<promise_type> h) noexcept
                {
                    auto cont = h.promise().continuation_;
                    if (cont) return cont;  // 返回 continuation handle → 恢复它
                    return std::noop_coroutine();  // 没有等待者 → 什么都不做
                }
                void await_resume() noexcept {}
            };
            return Awaiter{};
        }

        void unhandled_exception() {
            exception_ = std::current_exception();
        }
    };

    // co_await 一个 Task：等待它完成，获取结果
    auto operator co_await() const& {
        struct Awaiter {
            std::coroutine_handle<promise_type> handle_;

            bool await_ready() const {
                return handle_ && handle_.done();
            }

            std::coroutine_handle<promise_type> await_suspend(
                std::coroutine_handle<> caller) noexcept
            {
                // 把调用者设为 continuation，等 task 完成后恢复
                handle_.promise().continuation_ = caller;
                return handle_;  // 跳转到 task 继续执行
            }

            T await_resume() {
                if (handle_.promise().exception_)
                    std::rethrow_exception(handle_.promise().exception_);
                return std::move(*handle_.promise().result_);
            }
        };
        return Awaiter{handle_};
    }

    ~Task() { if (handle_) handle_.destroy(); }

private:
    std::coroutine_handle<promise_type> handle_;
    explicit Task(std::coroutine_handle<promise_type> h) : handle_(h) {}
};
```

## 简单线程池调度器

```cpp
#include <queue>
#include <mutex>
#include <condition_variable>
#include <vector>

class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mtx_;
    std::condition_variable cv_;
    bool stop_ = false;

public:
    explicit ThreadPool(size_t n) {
        for (size_t i = 0; i < n; ++i) {
            workers_.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock lock(mtx_);
                        cv_.wait(lock, [this] { return stop_ || !tasks_.empty(); });
                        if (stop_ && tasks_.empty()) return;
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();
                }
            });
        }
    }

    void post(std::function<void()> task) {
        {
            std::lock_guard lock(mtx_);
            tasks_.push(std::move(task));
        }
        cv_.notify_one();
    }

    ~ThreadPool() {
        {
            std::lock_guard lock(mtx_);
            stop_ = true;
        }
        cv_.notify_all();
        for (auto& w : workers_) w.join();
    }
};

// 全局线程池
inline ThreadPool& global_pool() {
    static ThreadPool pool(std::thread::hardware_concurrency());
    return pool;
}
```

## 调度 Awaiter

```cpp
// co_await switch_to(thread_pool) → 切换到线程池执行
struct SwitchTo {
    ThreadPool& pool;

    bool await_ready() { return false; }
    void await_suspend(std::coroutine_handle<> h) {
        pool.post([h] { h.resume(); });  // 投递到线程池恢复
    }
    void await_resume() {}
};

auto switch_to(ThreadPool& pool) {
    return SwitchTo{pool};
}

// 使用
Task<int> compute_heavy(int input) {
    // 当前线程（可能是主线程）
    co_await switch_to(global_pool());  // 切到线程池
    // 现在在工作线程上执行
    int result = 0;
    for (int i = 0; i < input * 1000; ++i) result += i;
    co_return result;
}
```

## 关键要点

> 协程调度的本质是"决定在哪个线程调用 `handle.resume()`"。`await_suspend` 中拿到 continuation handle，可以选择立即恢复、投递到线程池、注册为 IO 回调等。

> `final_suspend` 返回 `suspend_always` 意味着协程结束后不会自动销毁——等待 continuation 来触发销毁。这是 task 的标准模式：co_await 一个 task 时，调用者负责在最终结果不需要时 destroy。

> 链式 task 的展开：`co_await task_a(); co_await task_b();` → task_a 完成后通过 continuation 唤醒调用者，调用者再启动 task_b。整个链是事件驱动的，不阻塞线程。

## 相关模式 / 关联

- [[cpp-协程机制深入]] — 协程帧、promise_type 原理
- [[cpp-协程]] — 协程基础语法
- [[cpp-线程池设计]] — 线程池实现
- [[cpp-异步编程模型对比]] — callback vs future vs 协程
- [[cpp-future与async]] — std::async 的局限
