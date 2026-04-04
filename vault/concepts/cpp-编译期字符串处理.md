---
title: C++ 编译期字符串处理
tags: [cpp, constexpr, string, compile-time, string-view, fixed-string]
aliases: [编译期字符串, constexpr string, 编译期字符串处理, fixed_string]
created: 2026-04-04
updated: 2026-04-04
---

# 编译期字符串处理

C++20 起可以在编译期创建和操作字符串——`std::string` 的构造函数可以是 constexpr。

## C++20 constexpr string

```cpp
#include <string>

constexpr std::string make_greeting(const std::string& name) {
    std::string result = "Hello, ";
    result += name;
    result += "!";
    return result;
}

constexpr auto msg = make_greeting("World");  // 编译期计算
// msg == "Hello, World!"
```

## constexpr string_view

```cpp
#include <string_view>

constexpr size_t count_chars(std::string_view sv, char target) {
    size_t count = 0;
    for (char c : sv) {
        if (c == target) ++count;
    }
    return count;
}

static_assert(count_chars("hello world", 'o') == 2);
static_assert(count_chars("aaa", 'a') == 3);
```

## 编译期字符串查找

```cpp
constexpr bool contains(std::string_view haystack, std::string_view needle) {
    if (needle.size() > haystack.size()) return false;
    for (size_t i = 0; i <= haystack.size() - needle.size(); ++i) {
        if (haystack.substr(i, needle.size()) == needle) return true;
    }
    return false;
}

static_assert(contains("hello world", "world"));
static_assert(!contains("hello", "xyz"));
```

## 编译期哈希

```cpp
constexpr uint32_t fnv1a_hash(std::string_view sv) {
    uint32_t hash = 2166136261u;
    for (char c : sv) {
        hash ^= static_cast<uint32_t>(c);
        hash *= 16777619u;
    }
    return hash;
}

static_assert(fnv1a_hash("hello") != fnv1a_hash("world"));
```

## 关键要点

> C++20 起 `std::string` 的构造、拼接、查找等操作都可以是 `constexpr`——编译期字符串处理不再是难题。

> 编译期字符串处理的实际应用：编译期哈希、编译期 JSON 解析、编译期配置验证。

## 相关模式 / 关联

- [[cpp-编译期计算与constexpr深入]] — constexpr 演进
- [[cpp-string深入]] — string 操作
