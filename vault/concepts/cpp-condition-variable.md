---
title: condition_variable
tags: [cpp, concurrency, condition-variable, wait, notify, producer-consumer]
aliases: [条件变量, condition_variable, wait, notify_one, notify_all, 生产者消费者]
created: 2026-04-04
updated: 2026-04-04
---

# condition_variable

条件变量让线程在条件不满足时休眠等待，条件满足时被唤醒——比忙等高效得多。

## 意图与场景

- 生产者-消费者模型
- 等待某个状态变化（如队列非空）
- 线程间协调

## 基本用法

```cpp
#include <condition_variable>
#include <mutex>
#include <queue>

std::mutex mtx;
std::condition_variable cv;
std::queue<int> q;
bool finished = false;

// 生产者
void producer() {
    for (int i = 0; i < 10; ++i) {
        {
            std::lock_guard<std::mutex> lock(mtx);
            q.push(i);
        }
        cv.notify_one();  // 唤醒一个等待的消费者
    }
    {
        std::lock_guard<std::mutex> lock(mtx);
        finished = true;
    }
    cv.notify_all();  // 唤醒所有等待者
}

// 消费者
void consumer() {
    while (true) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [&] { return !q.empty() || finished; });  // 等待条件满足

        if (q.empty() && finished) break;

        int val = q.front();
        q.pop();
        lock.unlock();  // 处理数据前释放锁

        process(val);
    }
}
```

## wait 的机制

```cpp
// cv.wait(lock, predicate) 等价于：
while (!predicate()) {
    cv.wait(lock);  // 释放锁并休眠，被唤醒后重新获取锁
}

// ⚠️ 虚假唤醒（spurious wakeup）：
// wait 可能在条件未满足时被唤醒，所以必须用 while 或带谓词的 wait

// 不带谓词的 wait（容易出错）：
cv.wait(lock);  // 可能虚假唤醒！
if (!q.empty()) { /* 不安全 */ }
// 正确做法：永远用带谓词的 wait
```

## notify_one vs notify_all

```cpp
// notify_one：唤醒一个等待者（适合只有一个消费者）
cv.notify_one();

// notify_all：唤醒所有等待者（适合多个消费者或等待不同条件）
cv.notify_all();

// 性能考虑：
// notify_one 比 notify_all 高效——避免惊群效应
// 只有所有等待者需要检查不同条件时才用 notify_all
```

## 生产者-消费者完整模式

```cpp
class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mtx_;
    std::condition_variable cv_;
    bool stop_ = false;

public:
    ThreadPool(size_t n) {
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
                    task();
                }
            });
        }
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
```

## 关键要点

> 条件变量必须配合 mutex 使用——`wait()` 释放锁、休眠、被唤醒后重新获取锁。永远用带谓词的 `wait()` 防止虚假唤醒。

> 在持有锁时调用 `notify` 不是错误，但先释放锁再 `notify` 可能更高效（避免被唤醒的线程立刻又阻塞在锁上）。

## 相关模式 / 关联

- [[cpp-mutex与lock]] — 条件变量配套的 mutex
- [[cpp-atomic与内存序]] — 无锁替代方案
