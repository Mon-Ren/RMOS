---
title: 字符串字面量与原始字符串
tags: [cpp, string-literal, raw-string, u8, u, U, constexpr-string]
aliases: [字符串字面量, 原始字符串, raw string, u8字面量, R"()"语法]
created: 2026-04-04
updated: 2026-04-04
---

# 字符串字面量与原始字符串

C++ 的字符串字面量有多种前缀和语法——从普通 ASCII 到 UTF-8/16/32，再到无需转义的原始字符串。

## 字面量前缀

```cpp
auto s1 = "hello";         // const char[6]，普通字符串
auto s2 = L"hello";        // const wchar_t[6]，宽字符
auto s3 = u8"hello";       // const char8_t[6]，UTF-8（C++20 起是 char8_t）
auto s4 = u"hello";        // const char16_t[6]，UTF-16
auto s5 = U"hello";        // const char32_t[6]，UTF-32

// C++20: char8_t 明确区分 UTF-8
const char8_t* utf8 = u8"中文";  // UTF-8 编码
// const char* raw = u8"中文";    // C++20 前可以，C++20 不行（类型不同）
```

## 原始字符串（C++11）

```cpp
// R"(...)"：无需转义引号、反斜杠
auto path = R"(C:\Users\name\file.txt)";        // 不需要转义反斜杠
auto json = R"({"key": "value", "num": 42})";   // 不需要转义引号
auto regex = R"(\d+\.\d+\.\d+\.\d+)";           // 正则表达式不用双重转义

// 自定义分隔符：R"delimiter(...)delimiter"
auto s = R"abc(This contains )" and )" too)abc";
// 可以包含 )" 组合
```

## 字面量后缀

```cpp
// 用户定义字面量
auto dist = 100km;      // 使用 using namespace std::literals
auto time = 30s;
auto name = "hello"s;   // std::string（需要 using namespace std::literals）
auto sv = "hello"sv;    // std::string_view（需要 using namespace std::string_view_literals）

// 编译期字符串哈希（自定义字面量）
constexpr size_t operator""_hash(const char* str, size_t len) {
    size_t h = 0;
    for (size_t i = 0; i < len; ++i)
        h = h * 31 + str[i];
    return h;
}
constexpr auto key = "config"_hash;  // 编译期计算哈希
```

## 关键要点

> `u8` 前缀在 C++20 产生 `char8_t`（不再是 `const char*`）——与旧代码兼容时需要注意。

> 原始字符串 `R"(...)"` 让包含反斜杠和引号的字符串不需要转义——正则表达式和 JSON 文本中特别有用。

## 相关模式 / 关联

- [[cpp-string深入]] — string 操作
- [[cpp-const与constexpr]] — constexpr 字符串
