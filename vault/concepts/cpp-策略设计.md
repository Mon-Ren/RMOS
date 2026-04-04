---
title: Policy-Based Design 策略设计
tags: [cpp, idiom, policy, template, design]
aliases: [Policy-Based Design, 策略设计, 模板策略, Policy Classes]
created: 2026-04-04
updated: 2026-04-04
---

# Policy-Based Design 策略设计

**一句话概述：** 通过模板参数将类的行为策略化，在编译时组合不同的策略类——将运行时的"策略模式"提升为零开销的编译时组合。

## 意图与场景

Policy-Based Design 由 Andrei Alexandrescu 在《Modern C++ Design》中推广：

- **策略作为模板参数**：每个模板参数定义一种行为策略
- **编译时组合**：零虚函数开销，编译器可内联
- **正交组合**：n 个策略 × m 个策略 = n×m 种组合

**适用场景：**
- 库设计（如智能指针的删除器、容器的分配器）
- 编译时配置（线程模型、错误处理策略）
- 需要大量行为变体但不想写大量子类

## C++ 实现代码

### 基本 Policy 设计

```cpp
#include <iostream>
#include <fstream>
#include <memory>
#include <mutex>

// 策略 1：输出策略
struct CoutPolicy {
    static void write(const std::string& msg) {
        std::cout << msg << '\n';
    }
};

struct FilePolicy {
    static inline std::ofstream file_;
    static void write(const std::string& msg) {
        if (!file_.is_open()) file_.open("log.txt");
        file_ << msg << '\n';
    }
};

// 策略 2：线程安全策略
struct SingleThreadPolicy {
    struct Lock { /* 空操作 */ };
    Lock acquire_lock() { return {}; }
};

struct MultiThreadPolicy {
    std::mutex mtx_;
    using Lock = std::lock_guard<std::mutex>;
    Lock acquire_lock() { return Lock(mtx_); }
};

// 策略 3：时间戳策略
struct NoTimestampPolicy {
    static std::string timestamp() { return ""; }
};

struct TimestampPolicy {
    static std::string timestamp() {
        // 获取当前时间...
        return "[2026-04-04] ";
    }
};

// 组合策略
template <
    typename OutputPolicy = CoutPolicy,
    typename ThreadPolicy = SingleThreadPolicy,
    typename TimePolicy = NoTimestampPolicy
>
class Logger : private OutputPolicy, private ThreadPolicy, private TimePolicy {
public:
    void log(const std::string& msg) {
        auto lock = this->acquire_lock();
        OutputPolicy::write(TimePolicy::timestamp() + msg);
    }
};

// 使用：零开销的编译时组合
using MyLogger = Logger<FilePolicy, MultiThreadPolicy, TimestampPolicy>;
```

### std::allocator 的设计思想

```cpp
#include <vector>
#include <memory>

// 自定义分配器作为策略
template <typename T>
class PoolAllocator {
public:
    using value_type = T;
    
    PoolAllocator() = default;
    
    template <typename U>
    PoolAllocator(const PoolAllocator<U>&) noexcept {}
    
    T* allocate(std::size_t n) {
        // 从内存池分配
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    
    void deallocate(T* p, std::size_t n) noexcept {
        ::operator delete(p);
    }
};

// 分配器作为策略注入容器
void demo() {
    std::vector<int, PoolAllocator<int>> vec;
    vec.push_back(42);
}
```

### C++20 Concepts 约束 Policy

```cpp
#include <concepts>

// 定义策略接口（C++20 Concepts）
template <typename P>
concept OutputPolicy = requires(const std::string& msg) {
    { P::write(msg) } -> std::same_as<void>;
};

template <typename P>
concept LockPolicy = requires(P p) {
    { p.acquire_lock() } -> std::movable;
};

// 使用 Concepts 约束策略
template <OutputPolicy Out, LockPolicy Lock>
class SecureLogger {
    Lock lock_;
public:
    void log(const std::string& msg) {
        auto guard = lock_.acquire_lock();
        Out::write(msg);
    }
};
```

### 智能指针删除器策略

```cpp
#include <memory>
#include <cstdio>

// 自定义删除器策略
struct FileCloser {
    void operator()(std::FILE* fp) const {
        if (fp) std::fclose(fp);
    }
};

struct ArrayDeleter {
    template <typename T>
    void operator()(T* p) const {
        delete[] p;
    }
};

void demo() {
    // unique_ptr 的第二个模板参数就是删除器策略
    std::unique_ptr<std::FILE, FileCloser> file(std::fopen("data.txt", "r"));
    
    // shared_ptr 的删除器在构造时传入（类型擦除）
    std::shared_ptr<int> arr(new int[10], [](int* p) { delete[] p; });
}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 零运行时开销（无虚函数） | 编译时间增加 |
| 策略可自由组合 | 错误信息难以阅读 |
| 编译器可内联优化 | 所有组合导致代码膨胀 |
| 编译时类型检查 | 运行时无法切换策略 |

> [!tip] 关键要点
> Policy-Based Design 是**编译时策略模式**。与运行时策略模式（虚函数）的关键区别：运行时策略允许运行时切换行为，编译时策略则在编译时确定行为并允许编译器深度优化。选择依据：**行为是否需要在运行时切换？** 是→虚函数；否→Policy。

> [!example] std::unique_ptr 作为策略容器
> `unique_ptr<T, Deleter>` 的第二个模板参数就是一个删除器策略。标准库提供的 `default_delete<T>` 是默认策略，你可以传入任何可调用对象作为自定义策略。

## 相关链接

- [[策略模式]] — Policy-Based 是策略模式的编译时版本
- [[cpp-crtp-奇异递归模板模式]] — 另一种编译时技术
- [[cpp-sfinae-与编译期多态]] — 约束策略模板的工具
- [[设计模式-cpp-选型指南]] — 编译时 vs 运行时多态选择
