---
title: C++23 print 与格式化增强
tags: [cpp23, print, println, format, std-print, output]
aliases: [print, println, std::print, C++23输出, 格式化输出]
created: 2026-04-04
updated: 2026-04-04
---

# C++23 std::print 与 println

`std::print` 是 `std::format` 的自然延伸——直接输出到流，替代 `printf` 和 `cout` 的所有场景。

## 基本用法

```cpp
#include <print>

// 输出到 stdout
std::print("Hello, {}!\n", name);
std::println("Hello, {}!", name);  // 自动加换行

// 输出到指定流
std::print(std::cerr, "Error: {}\n", msg);

// 格式化语法与 std::format 一致
std::println("Pi: {:.4f}", 3.14159265);       // "Pi: 3.1416"
std::println("Hex: {:08x}", 255);              // "Hex: 000000ff"
std::println("Pad: {:>10}", "hello");          // "Pad:      hello"
std::println("Name: {}, Age: {}", name, age);  // 模板式
```

## 与 printf / cout 的对比

```
                printf          cout              std::print
类型安全        ✗（格式串不匹配  ✓                 ✓
                → UB）
性能            快               慢（stream开销）   快（format 缓冲）
语法            %d, %s          << 连接            {} 占位符
自定义类型      ✗               operator<< 重载    formatter 特化
可变参数        va_list         多个 <<            直接参数包
Unicode         有限支持         有限支持           良好支持
```

## 自定义类型格式化

```cpp
struct Point { double x, y; };

template <>
struct std::formatter<Point> {
    constexpr auto parse(auto& ctx) { return ctx.begin(); }
    auto format(const Point& p, auto& ctx) const {
        return std::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};

Point p{1.0, 2.0};
std::println("Point: {}", p);  // "Point: (1, 2)"
```

## 关键要点

> `std::println` 是 C++23 中最实用的特性——类型安全、高性能、语法简洁。它应该成为新代码的默认输出方式。

> `print` 不刷新缓冲区（与 `cout` 一致），`println` 同理。需要强制刷新时用 `std::flush`。

## 相关模式 / 关联

- [[cpp-format]] — format 是 print 的基础
- [[cpp-流与IO基础]] — 传统 IO
