---
title: 并发队列与线程池设计
tags: [cpp, concurrent-queue, thread-pool, producer-consumer, work-stealing]
aliases: [并发队列, 线程池, thread pool, 生产者消费者, work stealing]
created: 2026-04-04
updated: 2026-04-04
---

# 并发队列与线程池设计

线程池是并发编程的核心模式——固定数量的工作线程 + 任务队列，避免频繁创建销毁线程。

## 基本线程池

```cpp
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <functional>

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
                        std::unique_lock<std::mutex> lock(mtx_);
                        cv_.wait(lock, [this] { return stop_ || !tasks_.empty(); });
                        if (stop_ && tasks_.empty()) return;
                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }
                    task();  // 执行任务（不在锁内）
                }
            });
        }
    }

    template <typename F>
    void submit(F&& f) {
        {
            std::lock_guard<std::mutex> lock(mtx_);
            tasks_.emplace(std::forward<F>(f));
        }
        cv_.notify_one();
    }

    ~ThreadPool() {
        {
            std::lock_guard<std::mutex> lock(mtx_);
            stop_ = true;
        }
        cv_.notify_all();
        for (auto& w : workers_) w.join();
    }
};

// 使用
ThreadPool pool(4);
pool.submit([]{ std::cout << "Task 1\n"; });
pool.submit([]{ std::cout << "Task 2\n"; });
```

## 带返回值的任务提交

```cpp
template <typename F>
auto submit(F&& f) -> std::future<decltype(f())> {
    using ReturnType = decltype(f());
    auto task = std::make_shared<std::packaged_task<ReturnType()>>(
        std::forward<F>(f));
    auto future = task->get_future();
    {
        std::lock_guard<std::mutex> lock(mtx_);
        tasks_.emplace([task]() { (*task)(); });
    }
    cv_.notify_one();
    return future;
}

// 使用
auto future = pool.submit([] { return compute_result(); });
int result = future.get();  // 阻塞等待结果
```

## 关键要点

> 任务执行在 `task()` 调用时释放锁——持锁时间只覆盖队列操作，不覆盖任务执行。

> `std::jthread`（C++20）可以简化线程池的停止逻辑——内置停止令牌替代手动的 `stop_` 标志。

## 相关模式 / 关联

- [[cpp-thread与线程管理]] — 线程基础
- [[cpp-condition-variable]] — 任务队列的等待机制
