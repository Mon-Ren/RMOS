---
title: 预处理器
tags: [cpp, preprocessor, macro, include, define, pragma]
aliases: [预处理器, 宏, macro, #define, #include, #pragma, 条件编译]
created: 2026-04-04
updated: 2026-04-04
---

# 预处理器

预处理器在编译之前处理源代码——它是 C 遗留下来的能力，现代 C++ 尽量用语言特性替代，但在 include guard、条件编译、调试宏等场景仍不可替代。

## include

```cpp
#include <vector>         // 系统头文件：搜索系统路径
#include "myheader.h"     // 用户头文件：先搜索当前目录

// 包含保护
#ifndef MY_HEADER_H       // 方式一：传统 guard
#define MY_HEADER_H
// ... 内容 ...
#endif

#pragma once              // 方式二：pragma once（非标准但广泛支持）
// ... 内容 ...
```

## 宏定义

```cpp
// 对象式宏
#define MAX_SIZE 1024
#define PI 3.14159

// 函数式宏（⚠️ 容易出错）
#define SQUARE(x) ((x) * (x))    // 必须加括号！
int r = SQUARE(1 + 2);           // ((1+2)*(1+2)) = 9 ✓
// ⚠️ SQUARE(i++) 展开为 ((i++)*(i++)) → 未定义行为！

// 多行宏
#define LOG(msg) \
    std::cerr << __FILE__ << ":" << __LINE__ << " " << msg << "\n"

// 可变参数宏
#define DEBUG(fmt, ...) \
    fprintf(stderr, fmt, ##__VA_ARGS__)

// 字符串化和连接
#define STRINGIFY(x) #x             // 转字符串
#define CONCAT(a, b) a##b           // 连接标识符
STRINGIFY(hello)    // "hello"
CONCAT(foo, bar)    // foobar
```

## 条件编译

```cpp
#ifdef DEBUG
    #define LOG(msg) std::cerr << msg
#else
    #define LOG(msg)
#endif

#if defined(_WIN32)
    // Windows 特有代码
#elif defined(__linux__)
    // Linux 特有代码
#elif defined(__APPLE__)
    // macOS 特有代码
#endif

// 特性测试（C++20）
#if __has_include(<optional>)
    #include <optional>
#endif
```

## 预定义宏

```cpp
__FILE__        // 当前文件名
__LINE__        // 当前行号
__func__        // 当前函数名（C++11）
__DATE__        // 编译日期
__TIME__        // 编译时间
__cplusplus     // C++ 标准版本（201703L = C++17）
__COUNTER__     // 每次使用递增（非标准但广泛支持）
```

## 现代替代

```cpp
// ❌ 函数式宏 → ✅ constexpr 函数或 inline 函数
#define SQUARE(x) ((x) * (x))
constexpr int square(int x) { return x * x; }  // 更安全，有类型检查

// ❌ 调试宏 → ✅ if constexpr
#ifdef DEBUG
    #define LOG(x) std::cerr << x
#endif
// 改为：
if constexpr (is_debug) { std::cerr << x; }

// ❌ 头文件保护 → #pragma once（或传统 guard，仍可接受）
```

## 关键要点

> 宏没有作用域、不参与类型检查、展开时可能产生意外副作用。现代 C++ 中尽可能用 `constexpr`、`inline`、`if constexpr` 替代。

> 唯一不可替代的预处理器用法：`#include`、条件编译（平台/配置切换）、`#pragma once`。

## 相关模式 / 关联

- [[cpp-const与constexpr]] — constexpr 替代宏常量
- [[cpp-if-constexpr]] — if constexpr 替代条件编译宏
