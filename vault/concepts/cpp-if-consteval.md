---
title: C++23 if consteval
tags: [cpp23, if-consteval, consteval, compile-time, runtime]
aliases: [if consteval, consteval分支, 编译期/运行时分支]
created: 2026-04-04
updated: 2026-04-04
---

# if consteval（C++20/23）

`if consteval` 在编译期和运行时选择不同实现——编译期走优化路径，运行时走通用路径。

## 基本用法

```cpp
constexpr int factorial(int n) {
    if consteval {
        // 编译期执行：可以用更高效的实现
        int result = 1;
        for (int i = 2; i <= n; ++i) result *= i;
        return result;
    } else {
        // 运行时执行：可以用运行时特性（如查表）
        static const int table[] = {1, 1, 2, 6, 24, 120, /*...*/};
        if (n < 12) return table[n];
        // fallback
        int result = 1;
        for (int i = 2; i <= n; ++i) result *= i;
        return result;
    }
}
```

## 与 if constexpr 的区别

```cpp
// if constexpr：编译期选择分支（不满足的分支不编译）
template <typename T>
void process(T val) {
    if constexpr (std::is_integral_v<T>) {
        // 整数分支
    } else {
        // 非整数分支
    }
}

// if consteval：同一函数根据是否编译期求值选择分支
// 两个分支都编译，但只执行一个
constexpr int compute(int n) {
    if consteval {
        return n * n;  // 编译期
    } else {
        return n * n + 1;  // 运行时
    }
}
```

## 关键要点

> `if consteval` 的两个分支都会被编译——它不是编译期分支，而是运行时检查"当前是否在编译期求值上下文中"。

> `consteval` 函数内部不能有 `if consteval`——因为 `consteval` 函数永远在编译期执行。

## 相关模式 / 关联

- [[cpp-if-constexpr]] — 编译期分支
- [[cpp-编译期计算与constexpr深入]] — 编译期计算
