---
title: std::format（C++20）
tags: [cpp20, format, string-formatting, printf, type-safe]
aliases: [format, 格式化, string formatting, 类型安全格式化]
created: 2026-04-04
updated: 2026-04-04
---

# std::format（C++20）

`std::format` 是 Python f-string 风格的类型安全格式化——替代 `printf` 的类型不安全和 `std::stringstream` 的冗长。

## 意图与场景

- 替代 `printf`（类型安全）和 `stringstream`（简洁）
- 日志、错误消息、UI 文本的字符串构建
- 性能敏感的格式化场景

## 基本用法

```cpp
#include <format>
#include <iostream>
#include <string>

// 基本格式化
std::string msg = std::format("Hello, {}! You are {} years old.", "Alice", 25);
// "Hello, Alice! You are 25 years old."

// 位置参数
std::string s = std::format("{1} before {0}", "second", "first");
// "first before second"

// 格式说明符
std::format("{:d}", 42);         // "42" — 十进制
std::format("{:x}", 255);        // "ff" — 十六进制
std::format("{:08b}", 42);       // "00101010" — 二进制，8位补零
std::format("{:.2f}", 3.14159);  // "3.14" — 浮点2位精度
std::format("{:>10}", "hi");     // "        hi" — 右对齐10位宽
std::format("{:*<10}", "hi");    // "hi********" — 左对齐，*填充
std::format("{:^10}", "hi");     // "    hi    " — 居中

// C++23: 输出到 ostream
std::print("Value: {}\n", 42);            // 直接打印
std::println("Value: {}", 42);            // 自动换行
std::print(stderr, "Error: {}\n", msg);   // 输出到 stderr
```

## 自定义类型格式化

```cpp
struct Point {
    double x, y;
};

// 特化 std::formatter
template <>
struct std::formatter<Point> {
    constexpr auto parse(std::format_parse_context& ctx) {
        return ctx.begin();
    }

    auto format(const Point& p, std::format_context& ctx) const {
        return std::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};

std::string s = std::format("{}", Point{1.0, 2.0});  // "(1, 2)"
```

## 关键要点

> `std::format` 编译期检查格式字符串的语法（C++23 起也检查参数类型），比 `printf` 安全。性能通常优于 `stringstream`。

> C++23 的 `std::print` 直接输出到流，是替代 `printf` 和 `cout` 的现代选择。

## 相关模式 / 关联

- [[cpp-string深入]] — string 的构建方式
- [[cpp-可变参数模板]] — format 的实现原理
