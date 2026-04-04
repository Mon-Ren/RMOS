---
title: C++ Lambda 与递归
tags: [cpp, lambda, recursion, std-function, Y-combinator, deducing-this]
aliases: [lambda递归, 递归lambda, Y组合子, 自递归]
created: 2026-04-04
updated: 2026-04-04
---

# Lambda 与递归

Lambda 不能直接引用自己（类型不完整时不知道自己名字）——有几种方式实现递归。

## 方式 1：std::function（最简单）

```cpp
#include <functional>

std::function<int(int)> fib = [&fib](int n) -> int {
    return (n <= 1) ? n : fib(n-1) + fib(n-2);
};

// ⚠️ fib 按引用捕获自身——循环引用风险
// ⚠️ std::function 有类型擦除开销
```

## 方式 2：传参递归（零开销）

```cpp
auto fib = [](auto self, int n) -> int {
    return (n <= 1) ? n : self(self, n-1) + self(self, n-2);
};
int result = fib(fib, 10);

// 配合辅助函数更简洁
auto call = [](auto f, auto... args) {
    return f(f, std::forward<decltype(args)>(args)...);
};
int result = call(fib, 10);
```

## 方式 3：C++23 deducing this

```cpp
auto fib = [](this auto self, int n) -> int {
    return (n <= 1) ? n : self(n-1) + self(n-2);
};
int result = fib(10);  // 最简洁！不需要传自己
```

## 方式 4：Y 组合子

```cpp
// Y 组合子：从非递归函数构造递归函数
auto Y = [](auto f) {
    return [f](auto&&... args) {
        return f(f, std::forward<decltype(args)>(args)...);
    };
};

auto fib_impl = [](auto self, int n) -> int {
    return (n <= 1) ? n : self(self, n-1) + self(self, n-2);
};
auto fib = Y(fib_impl);
int result = fib(10);
```

## 关键要点

> C++23 的 `deducing this` 是递归 lambda 的最佳方案——语法最简洁，无额外开销。

> `std::function` 方案最简单但有开销和循环引用风险。传参方案零开销但语法稍复杂。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — Lambda 基础
- [[cpp-deducing-this]] — C++23 显式对象参数
