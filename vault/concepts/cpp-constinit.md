---
title: C++ constinit（C++20）
tags: [cpp20, constinit, compile-time-initialization, static]
aliases: [constinit, 编译期初始化, 静态初始化, constinit vs const]
created: 2026-04-04
updated: 2026-04-04
---

# constinit（C++20）

`constinit` 保证变量在编译期初始化——但它不是 `const`，初始化后可以修改。

## 与 const 的区别

```cpp
const int x = 42;           // 编译期初始化 + 不可修改
constinit int y = 42;       // 编译期初始化 + 可修改

// constinit 解决的问题：
const std::string s = get_name();  // OK：运行时初始化
// constinit std::string s2 = get_name();  // 编译错误：必须编译期初始化

constinit int z = 0;
z = 100;  // OK：constinit 允许修改
```

## 典型用法

```cpp
// 全局对象的延迟初始化防护
constinit std::atomic<bool> initialized{false};  // 编译期初始化

void init() {
    if (!initialized.exchange(true, std::memory_order_acqrel)) {
        // 初始化...
    }
}

// 防止静态初始化顺序灾难
// file1.cpp
constinit int global_value = 42;  // 编译期初始化，不受其他静态变量影响

// file2.cpp
extern constinit int global_value;
int use() { return global_value; }  // 保证已经初始化
```

## 关键要点

> `constinit` 解决的核心问题是**静态初始化顺序灾难**——它保证变量在编译期初始化，不受其他运行时初始化的全局变量影响。

> `constinit` ≠ `const`——`constinit` 保证初始化时机，`const` 保证不修改。

## 相关模式 / 关联

- [[cpp-const与constexpr]] — const 和 constexpr
- [[cpp-编译期计算与constexpr深入]] — constexpr/consteval/constinit
