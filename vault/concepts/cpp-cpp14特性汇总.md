---
title: C++14 主要特性汇总
tags: [cpp14, features, generic-lambda, variable-template, constexpr, return-type]
aliases: [C++14, 泛型lambda, 变量模板, constexpr增强, 返回类型推导]
created: 2026-04-04
updated: 2026-04-04
---

# C++14 主要特性汇总

C++14 是 C++11 的完善——没有颠覆性变化，但填补了实际编码中的许多小缺口。

## 语言特性

```cpp
// 泛型 lambda
auto add = [](auto a, auto b) { return a + b; };
add(1, 2);       // int
add(1.0, 2.0);   // double

// 返回类型推导（auto 返回类型）
auto square(int x) { return x * x; }
// 编译器从 return 语句推导返回类型

// 变量模板
template <typename T>
constexpr T pi = T(3.14159265358979323846);
// pi<int> → 3, pi<double> → 3.14159...

// lambda 初始化捕获
auto ptr = std::make_unique<int>(42);
auto l = [p = std::move(ptr)]() { return *p; };

// 二进制字面量
int flags = 0b1010'1100;  // 数字分隔符

// constexpr 增强（循环、变量、if/switch）
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) result *= i;
    return result;
}

// deprecated 属性
[[deprecated("Use new_func instead")]]
void old_func();

// std::make_unique
auto p = std::make_unique<Widget>(args);
```

## 库特性

```cpp
// std::make_unique（C++11 没有提供）
auto p = std::make_unique<int>(42);

// std::integer_sequence
template <std::size_t... Is>
void process(std::index_sequence<Is...>);

// std::quoted（带引号的字符串 IO）
std::string s = "hello world";
std::cout << std::quoted(s);  // 输出 "hello world"

// 异构查找（std::map/set）
std::map<std::string, int> m;
auto it = m.find("key"s);  // C++14: std::less<> 支持异构查找
```

## 关键要点

> C++14 的泛型 lambda 和 auto 返回类型让模板代码更简洁。`make_unique` 填补了 `make_shared` 的对称性缺失。

> C++14 的 constexpr 增强让编译期计算从"只能写表达式"变成"可以写循环和分支"。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — 泛型 lambda
- [[cpp-auto与类型推导]] — 返回类型推导
