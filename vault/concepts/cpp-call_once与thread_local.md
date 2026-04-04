---
title: call_once 与线程局部存储
tags: [cpp, concurrency, call_once, once_flag, thread_local, TLS]
aliases: [call_once, once_flag, thread_local, 线程局部存储, TLS, 懒初始化]
created: 2026-04-04
updated: 2026-04-04
---

# call_once 与线程局部存储

`std::call_once` 保证函数在多线程环境中恰好执行一次，`thread_local` 给每个线程独立的数据副本。

## std::call_once

```cpp
#include <mutex>

std::once_flag init_flag;
std::unique_ptr<Config> global_config;

void init_config() {
    std::call_once(init_flag, []() {
        global_config = std::make_unique<Config>();
        global_config->load("settings.json");
    });
}
// 多个线程同时调用 init_config()，Config 只初始化一次

// 对比 double-checked locking：
// call_once 更简洁且无常见陷阱
```

## static 局部变量（C++11 线程安全）

```cpp
// C++11 保证：函数内 static 变量的初始化是线程安全的
Config& get_config() {
    static Config config;  // 线程安全的懒初始化
    return config;
}
// 多线程同时首次调用时，只有一个线程初始化 config
// 编译器内部实现类似 call_once
```

## thread_local

```cpp
// 每个线程有独立的副本
thread_local int counter = 0;

void increment() {
    ++counter;  // 每个线程独立计数，无需加锁
}

// thread_local 生命周期：
// - 每个线程首次使用时初始化
// - 线程退出时销毁
// - 在线程间完全独立

// 常见用法：线程局部缓存
thread_local std::mt19937 rng(std::random_device{}());  // 每线程独立随机数生成器
thread_local std::unordered_map<int, int> local_cache;   // 每线程独立缓存

// 注意：thread_local 有内存开销（每个线程一份副本）
// 不适合大量线程 + 大对象的场景
```

## 关键要点

> `call_once` + `once_flag` 是"恰好执行一次"的标准实现。C++11 的函数内 `static` 变量也提供线程安全初始化——两者都可以放心使用。

> `thread_local` 的开销是每个线程一份副本的内存——线程多时注意总内存消耗。

## 相关模式 / 关联

- [[cpp-thread与线程管理]] — 线程基础
- [[cpp-mutex与lock]] — 替代 call_once 的有锁方案
