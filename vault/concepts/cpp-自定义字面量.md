---
title: 字符串字面量后缀与自定义字面量
tags: [cpp, literal, user-defined-literal, operator, suffix, chrono]
aliases: [自定义字面量, user-defined literal, 字面量后缀, operator"", 后缀]
created: 2026-04-04
updated: 2026-04-04
---

# 自定义字面量（C++11）

自定义字面量让用户定义 `42_km`、`"hello"_hash` 这样的语法——标准库用它实现 `std::chrono` 的 `30s`、`100ms`。

## 标准库字面量

```cpp
using namespace std::literals;

auto dur = 30s;              // std::chrono::seconds
auto ms = 100ms;             // std::chrono::milliseconds
auto str = "hello"s;         // std::string
auto sv = "hello"sv;         // std::string_view（using namespace std::string_view_literals）

// 注意：不引入命名空间时不会生效
// auto x = 30s;  // 编译错误：s 被当作变量名
using namespace std::chrono_literals;
auto y = 30s;  // OK
```

## 自定义字面量

```cpp
// 编译期字符串哈希
constexpr size_t operator""_hash(const char* str, size_t len) {
    size_t h = 5381;
    for (size_t i = 0; i < len; ++i)
        h = ((h << 5) + h) + str[i];  // djb2 哈希
    return h;
}

constexpr auto key = "config"_hash;  // 编译期计算
// switch(key) 也可以用
switch ("setting"_hash) {
    case "config"_hash: break;
    case "debug"_hash: break;
}

// 整数字面量
constexpr long double operator""_km(long double v) { return v * 1000.0; }
auto dist = 5.0_km;  // 5000.0

// 自定义类型
struct Time {
    int hours, minutes;
};

constexpr Time operator""_h(unsigned long long h) {
    return Time{static_cast<int>(h), 0};
}

auto t = 3_h;  // Time{3, 0}
```

## 注意事项

```cpp
// 字面量运算符的参数类型有规定：
// 整数字面量：unsigned long long
// 浮点字面量：long double
// 字符字面量：char, wchar_t, char16_t, char32_t
// 字符串字面量：const char*, size_t

// 不能重载内置字面量的含义
// 不能自定义 0x、0b 等前缀

// 用户定义字面量必须以下划线开头（避免与标准库冲突）
constexpr int operator""_myval(unsigned long long);  // ✅ 下划线开头
// constexpr int operator""myval(unsigned long long);  // ❌ 可能与标准冲突
```

## 关键要点

> 自定义字面量让代码更表达意图——`30s` 比 `std::chrono::seconds(30)` 更直观。

> 编译期字符串哈希是自定义字面量的经典应用——`"key"_hash` 在编译期计算，零运行时开销。

## 相关模式 / 关联

- [[cpp-字符串字面量与原始字符串]] — 字符串字面量基础
- [[cpp-constexpr与constexpr深入]] — 编译期计算
