---
title: C++ 线程安全的懒初始化
tags: [cpp, lazy-initialization, thread-safe, call_once, static-local]
aliases: [懒初始化, 懒加载, lazy init, 线程安全初始化]
created: 2026-04-04
updated: 2026-04-04
---

# 线程安全的懒初始化

C++ 提供了多种线程安全的懒初始化方式——函数内 static 变量、call_once、双重检查锁。

## 函数内 static（最推荐）

```cpp
// C++11 保证：函数内 static 变量的初始化是线程安全的
Config& get_config() {
    static Config config;  // 首次调用时初始化
    return config;         // 后续调用直接返回
}

// 多个线程同时首次调用时：
// - 只有一个线程执行初始化
// - 其他线程等待初始化完成
// - 编译器内部实现类似 call_once
```

## std::call_once

```cpp
std::once_flag flag;
std::unique_ptr<Config> config;

Config& get_config() {
    std::call_once(flag, []() {
        config = std::make_unique<Config>();
        config->load("settings.json");
    });
    return *config;
}
```

## 双重检查锁（高级场景）

```cpp
std::atomic<Config*> config{nullptr};
std::mutex mtx;

Config& get_config() {
    Config* p = config.load(std::memory_order_acquire);
    if (!p) {
        std::lock_guard<std::mutex> lock(mtx);
        p = config.load(std::memory_order_relaxed);
        if (!p) {
            p = new Config();
            config.store(p, std::memory_order_release);
        }
    }
    return *p;
}
```

## 选择

```
场景                          方式
───────────────────────────────────
通用场景                      函数内 static（最简洁）
需要清理/重置                 call_once + unique_ptr
需要异常传播                  call_once（调用者可捕获）
极端性能要求                  双重检查锁
```

## 关键要点

> 函数内 `static` 变量是 C++11 起最简洁、最安全的懒初始化方式——编译器保证线程安全，无需手动同步。

> `call_once` 适用于需要显式控制初始化时机或清理的场景。

## 相关模式 / 关联

- [[cpp-call_once与thread_local]] — call_once 详细
- [[cpp-atomic与内存序]] — 双重检查锁的内存序
