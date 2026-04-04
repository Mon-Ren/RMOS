---
title: 编译期计算与 constexpr 函数深入
tags: [cpp, constexpr, compile-time, consteval, constinit, metaprogramming]
aliases: [编译期计算, constexpr函数, consteval, constinit, 编译期编程]
created: 2026-04-04
updated: 2026-04-04
---

# 编译期计算与 constexpr 函数深入

C++ 的编译期计算能力从 C++11 到 C++20 不断增强——从简单常量到循环、虚函数、try-catch，几乎可以在编译期做任何事。

## constexpr 演进

```
C++11：constexpr 函数只能有单条 return 语句
C++14：加入循环、变量、if、switch
C++17：加入 lambda、聚合类型的 constexpr
C++20：加入虚函数、try-catch、dynamic_cast、union 活跃状态管理
C++23：加入 static_assert、goto 之外的几乎所有语言特性
```

## C++14+ constexpr 函数

```cpp
constexpr int fibonacci(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

constexpr int fib10 = fibonacci(10);  // 编译期计算：55

// constexpr 可以运行时调用
int n = 10;
int result = fibonacci(n);  // 运行时调用
```

## constexpr 容器（C++20）

```cpp
#include <array>

constexpr auto make_lut() {
    std::array<int, 256> lut{};
    for (int i = 0; i < 256; ++i) {
        lut[i] = i * i;  // 编译期生成查找表
    }
    return lut;
}

constexpr auto SQUARE_LUT = make_lut();  // 编译期计算
// 运行时直接查表，零开销
```

## consteval（C++20）

```cpp
// consteval：必须在编译期求值
consteval int must_be_compile_time(int n) {
    return n * n;
}

constexpr int a = must_be_compile_time(5);   // OK
// int x = 10;
// int b = must_be_compile_time(x);           // 编译错误！
```

## constinit（C++20）

```cpp
// constinit：保证变量在编译期初始化（但不是 const）
constinit int global_count = 0;  // 编译期初始化
constinit std::string global_str = "hello";  // OK（string 的编译期初始化）

void increment() {
    global_count++;  // 可以修改！constinit ≠ const
}
```

## 关键要点

> `constexpr` 函数在参数为常量表达式时编译期求值，否则运行时执行。`consteval` 强制编译期。`constinit` 强制编译期初始化但允许后续修改。

> 编译期计算的限制：不能访问运行时状态、不能做 I/O、不能有 UB。

## 相关模式 / 关联

- [[cpp-const与constexpr]] — const 基础
- [[cpp-模板元编程]] — 另一种编译期计算方式
