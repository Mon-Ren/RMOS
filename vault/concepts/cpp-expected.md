---
title: std::expected（C++23）
tags: [cpp23, expected, error-handling, monadic, result-type]
aliases: [expected, 错误处理, result类型, monadic error handling]
created: 2026-04-04
updated: 2026-04-04
---

# std::expected（C++23）

`expected` 是值或错误的类型安全表示——Rust 的 `Result` 在 C++ 中的实现，让错误处理显式而优雅。

## 意图与场景

- 替代异常进行错误处理（无异常开销）
- 链式操作中自动传播错误
- 明确区分成功值和错误值

## 基本用法

```cpp
#include <expected>
#include <string>

// 返回 expected<值类型, 错误类型>
std::expected<int, std::string> parse_int(const std::string& s) {
    try {
        return std::stoi(s);
    } catch (...) {
        return std::unexpected("parse error: " + s);
    }
}

// 使用
auto result = parse_int("42");
if (result) {
    std::cout << *result << "\n";     // 42
} else {
    std::cerr << result.error() << "\n";  // 错误信息
}

// value_or 默认值
int n = parse_int("abc").value_or(0);  // 解析失败返回 0
```

## 单子操作

```cpp
std::expected<int, std::string> double_it(int n) {
    if (n > 1000) return std::unexpected("too large");
    return n * 2;
}

// 链式调用：任何一步失败则短路
auto result = parse_int("42")
    .and_then(double_it)           // 返回 expected
    .transform([](int n) {         // 返回值变换
        return std::to_string(n);
    })
    .or_else([](const std::string& err) {  // 处理错误
        std::cerr << err;
        return std::expected<std::string, std::string>("default");
    });
```

## 与异常的对比

```
                异常                expected
性能开销        有（栈展开）        无（值语义）
错误传播        自动但隐式          链式但显式
调用栈          自动展开            需手动传播
适用场景        不可恢复错误        预期的失败
```

## 关键要点

> `expected` 让错误成为类型系统的一部分——函数签名直接告诉你可能失败。链式操作让错误传播零样板代码。

> 与异常互补而非替代：`expected` 用于预期的、可恢复的失败；异常用于意外的、不可恢复的错误。

## 相关模式 / 关联

- [[cpp-optional]] — 无错误信息的"可能无值"
- [[cpp-异常处理]] — 异常 vs expected 的选择
