---
title: C++20 异步编程模型对比
tags: [cpp20, async, future, coroutine, callback, comparison]
aliases: [异步编程对比, future vs coroutine, callback vs coroutine, 异步模型]
created: 2026-04-04
updated: 2026-04-04
---

# C++20 异步编程模型对比

C++ 有四种异步模型——各有优劣，选择取决于场景和复杂度。

## 四种模型

```cpp
// 1. 回调（传统方式）
void async_read(const std::string& path,
    std::function<void(std::string)> callback) {
    // 异步完成后调用 callback
}
// ❌ 回调地狱、错误处理困难

// 2. future/async（C++11）
auto fut = std::async(std::launch::async, [] {
    return read_file("data.txt");
});
std::string data = fut.get();  // 阻塞
// ❌ 只能 get 一次、不支持连续、阻塞

// 3. 协程（C++20）
Task<std::string> async_read(std::string path) {
    auto data = co_await io_awaitable(path);  // 挂起等待 I/O
    co_return data;
}
// ✅ 同步写法、支持连续、不阻塞

// 4. callback + promise（手动实现）
std::promise<std::string> prom;
auto fut = prom.get_future();
std::thread([&prom] {
    prom.set_value(read_file("data.txt"));
}).detach();
// ✅ 灵活、❌ 繁琐
```

## 对比

```
                callback    future      coroutine   promise
代码可读性      差           中          好          中
错误处理        困难         异常        异常/expected 手动
组合能力        差           弱          强          中
性能开销        低           中          低-中       中
学习曲线        低           低          高          中
生态成熟度      高           高          低          高
```

## 实际选择

```cpp
// 简单并行计算 → async
auto f = std::async(compute, arg);

// 异步 I/O → 协程（需要配套库）
Task<int> result = co_await async_fetch(url);

// 现有代码改造 → future/promise（侵入性小）
std::promise<int> p;
std::thread([&p]{ p.set_value(compute()); }).detach();

// 高性能服务端 → 协程 + io_uring/epoll（Boost.Asio）
```

## 关键要点

> 协程是 C++ 异步编程的未来——同步写法、异步性能。但标准库缺少配套设施（调度器、I/O awaitable），需要第三方库。

> 简单场景不要过度设计——`std::async` 对一次性任务足够。

## 相关模式 / 关联

- [[cpp-协程]] — 协程详细
- [[cpp-future与async]] — future 详细
