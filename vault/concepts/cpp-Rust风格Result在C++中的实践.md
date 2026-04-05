---
title: Rust 风格 Result 在 C++ 中的实践
tags: [cpp, expected, result, error-handling, monadic, rust-like]
aliases: [Result 模式, 错误处理函数式, expected 链式调用]
created: 2026-04-05
updated: 2026-04-05
---

# Rust 风格 Result 在 C++ 中的实践

**一句话概述：** C++23 的 `std::expected` 终于给了我们 Rust `Result` 的等价物——返回值要么是正确结果，要么是错误信息，不需要异常也不需要错误码配对。配合 `and_then`/`transform`/`or_else` 链式操作，可以写出不含任何 if 检查的错误传播代码。

## 从错误码到 expected

```cpp
// ─── 方案 1：错误码（C 风格）───
ErrorCode read_config(Config& out) {
    auto file = fopen("config.json", "r");
    if (!file) return ErrorCode::FileNotFound;
    // ... 解析 ...
    if (parse_failed) { fclose(file); return ErrorCode::ParseError; }
    fclose(file);
    return ErrorCode::Ok;
}
// 问题：调用者必须检查返回值，忘记检查 = bug

// ─── 方案 2：异常 ──
Config read_config() {
    auto file = fopen("config.json", "r");
    if (!file) throw FileError("not found");
    // ... 解析 ...
}
// 问题：异常开销大（微秒级），控制流不显式

// ─── 方案 3：expected（推荐）───
std::expected<Config, std::string> read_config() {
    auto file = fopen("config.json", "r");
    if (!file) return std::unexpected("config.json not found");
    // ... 解析 ...
    if (parse_failed) return std::unexpected("invalid JSON");
    fclose(file);
    return config;
}
// 返回值强制调用者处理错误情况
// 没有堆分配，没有异常开销
```

## 链式操作：消灭 if 检查

```cpp
#include <expected>
#include <string>
#include <fstream>
#include <sstream>

// 基础操作
std::expected<std::string, std::string> read_file(const std::string& path) {
    std::ifstream f(path);
    if (!f) return std::unexpected("Cannot open: " + path);
    std::ostringstream ss;
    ss << f.rdbuf();
    return ss.str();
}

std::expected<int, std::string> parse_int(const std::string& s) {
    try { return std::stoi(s); }
    catch (...) { return std::unexpected("Not an integer: " + s); }
}

// ─── 传统 if 检查链 ───
auto result1 = read_file("port.txt");
if (!result1) { /* handle error */ return; }
auto result2 = parse_int(*result1);
if (!result2) { /* handle error */ return; }
int port = *result2;

// ─── 链式调用（C++23）───
auto port = read_file("port.txt")
    .and_then(parse_int)               // 文件内容 → 整数
    .transform([](int p) { return p > 0 ? p : 8080; })  // 修正非正数
    .or_else([](const std::string& err) -> std::expected<int, std::string> {
        std::cerr << "Warning: " << err << ", using default\n";
        return 8080;  // 所有错误都用默认值
    });
// port 是 std::expected<int, std::string>，没有一层 if
```

## and_then / transform / or_else 的语义

```cpp
// Rust        → C++23
// .map()      → .transform()  // 成功时变换值，失败时透传错误
// .and_then() → .and_then()   // 成功时返回新 expected，失败时透传错误
// .or_else()  → .or_else()    // 失败时处理错误，成功时透传值

// 类型变化：
expected<int, E>
    .transform([](int v) { return std::to_string(v); })  // → expected<string, E>
    .and_then([](string s) -> expected<double, E> {      // → expected<double, E>
        return std::stod(s);
    })
    .or_else([](E err) -> expected<double, E> {          // → expected<double, E>
        return 0.0;  // 提供默认值
    });
```

## 实战：文件处理管道

```cpp
#include <expected>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

struct AppError {
    std::string message;
    int code;
};

std::expected<std::string, AppError> load_input(const std::string& path) {
    std::ifstream f(path);
    if (!f) return std::unexpected(AppError{"File not found: " + path, 1});
    std::ostringstream ss;
    ss << f.rdbuf();
    return ss.str();
}

std::expected<std::vector<int>, AppError> parse_numbers(const std::string& text) {
    std::vector<int> nums;
    std::istringstream iss(text);
    int n;
    while (iss >> n) nums.push_back(n);
    if (nums.empty()) return std::unexpected(AppError{"No numbers found", 2});
    return nums;
}

std::expected<std::vector<int>, AppError> filter_positive(std::vector<int> nums) {
    nums.erase(std::remove_if(nums.begin(), nums.end(),
        [](int x) { return x <= 0; }), nums.end());
    if (nums.empty()) return std::unexpected(AppError{"No positive numbers", 3});
    return nums;
}

// 完整管道：零 if 检查
auto result = load_input("data.txt")
    .and_then(parse_numbers)
    .and_then(filter_positive)
    .transform([](std::vector<int> v) {
        std::sort(v.begin(), v.end());
        return v;
    });

if (result) {
    for (int x : *result) std::cout << x << "\n";
} else {
    std::cerr << "Error " << result.error().code
              << ": " << result.error().message << "\n";
}
```

## expected vs 其他方案

| 特性 | 错误码 | 异常 | expected |
|------|--------|------|----------|
| 强制检查 | ❌ | ❌（可以不 catch） | ✅（必须检查才能取值） |
| 正常路径开销 | 极低 | 零 | 极低 |
| 错误路径开销 | 极低 | 高（~微秒） | 极低 |
| 代码侵入性 | 高（每层检查） | 低（自动传播） | 中（链式传播） |
| 错误信息丰富度 | 低（int） | 高（exception 类） | 高（任意类型） |
| 多线程安全 | ✅ | ✅ | ✅ |
| ABI 兼容 | ✅ | ❌ | ✅ |

## 自定义 expected 类型（C++17/20 向后兼容）

```cpp
// 如果没有 C++23，可以用 tl::expected（单头文件库）
// 或自己实现简化版
// https://github.com/TartanLlama/expected

// 简化版核心思路：
template <typename T, typename E>
class Result {
    union {
        T value_;
        E error_;
    };
    bool has_value_;

public:
    // ... 构造、析构、访问、转换 ...
    // 和 std::expected 接口一致
};
```

## 关键要点

> `std::expected` 的值和错误存储在同一对象中（union 语义），大小 = max(sizeof(T), sizeof(E))。没有堆分配，没有虚函数调用。这就是它比异常快的原因。

> `and_then` 和 `transform` 的区别：`and_then` 的回调返回 `expected<U, E>`（可能失败），`transform` 的回调返回 `U`（不失败）。选择哪个取决于回调是否可能失败。

> expected 适合"预期可能失败"的操作（文件找不到、解析失败、网络超时）。对于"不应该发生"的逻辑错误（断言失败、不可达代码），还是应该用异常或 `std::terminate`。

## 相关模式 / 关联

- [[cpp-expected]] — std::expected 基础
- [[cpp-optional]] — optional（expected 的特例，没有错误信息）
- [[cpp-异常vs错误码]] — 错误处理策略对比
- [[cpp-异常处理]] — 异常机制
- [[cpp-函数式编程模式]] — monadic 操作风格
