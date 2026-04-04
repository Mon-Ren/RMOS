---
title: std::jthread 与协作式取消
tags: [cpp20, jthread, stop-token, cancellation, cooperative]
aliases: [jthread, stop_token, 协作式取消, 停止令牌, cooperative cancellation]
created: 2026-04-04
updated: 2026-04-04
---

# std::jthread 与协作式取消

`jthread` = `thread` + 自动 join + 停止令牌——C++20 解决了 `std::thread` 的大部分痛点。

## 自动 join

```cpp
#include <thread>

// std::thread 的问题：忘记 join/terminate
void bad() {
    std::thread t(work);
    // 抛异常 → t 析构 → std::terminate()
}

// std::jthread：析构自动 join
void good() {
    std::jthread t(work);
    // 抛异常 → t 析构 → 自动 join
}
```

## 停止令牌

```cpp
// jthread 的 lambda 可以接受 stop_token
std::jthread worker([](std::stop_token st) {
    while (!st.stop_requested()) {  // 检查停止请求
        do_work();
    }
    cleanup();
});

// 请求停止
worker.request_stop();  // 设置停止标志
// worker 析构时自动 join
```

## stop_callback

```cpp
// 停止时执行回调
std::jthread t([](std::stop_token st) {
    std::stop_callback cb(st, [] {
        std::cout << "Cleanup on stop\n";
    });
    while (!st.stop_requested()) {
        work();
    }
});

t.request_stop();  // 触发回调 "Cleanup on stop"
// 然后线程退出循环
```

## 与 condition_variable 配合

```cpp
std::jthread t([](std::stop_token st) {
    std::mutex mtx;
    std::condition_variable_any cv;  // 注意：_any 版本

    while (!st.stop_requested()) {
        std::unique_lock lock(mtx);
        cv.wait(lock, st, [&] { return has_data(); });  // 等待数据或停止
        if (st.stop_requested()) break;
        process_data();
    }
});

t.request_stop();  // 唤醒等待中的线程
```

## 关键要点

> `jthread` 的自动 join 消除了"忘记 join"的 bug。停止令牌是协作式的——线程必须主动检查 `stop_requested()`。

> `condition_variable_any` 支持任意锁类型（包括 `stop_token`），是 `jthread` 配合条件变量的选择。

## 相关模式 / 关联

- [[cpp-thread与线程管理]] — thread 基础
- [[cpp-condition-variable]] — 条件变量
