---
title: SFINAE 与编译期多态
tags: [cpp, template, SFINAE, enable_if, type-detection, compile-time]
aliases: [SFINAE, enable_if, 编译期多态, substitution failure, 模板约束]
created: 2026-04-04
updated: 2026-04-04
---

# SFINAE 与编译期多态

SFINAE（Substitution Failure Is Not An Error）——模板参数替换失败不是错误，只是从候选集中移除。这是 C++17 之前做模板约束的唯一机制。

## 核心原理

```cpp
// 编译器尝试所有模板，只要替换过程出错就静默跳过
template <typename T>
typename T::value_type get_first(const T& container) {
    return *container.begin();
}

int x = 42;
// get_first(x);  // 替换 T=int：int::value_type 不存在 → SFINAE，静默跳过
// 但如果没有其他重载 → 编译错误

std::vector<int> v = {1, 2, 3};
get_first(v);  // T=vector<int>：vector<int>::value_type 存在 → OK
```

## enable_if

```cpp
#include <type_traits>

// 仅对算术类型启用
template <typename T>
std::enable_if_t<std::is_arithmetic_v<T>>
process(T val) {
    std::cout << "Arithmetic: " << val << "\n";
}

// 返回值位置的 enable_if
template <typename T>
typename std::enable_if<std::is_integral_v<T>, T>::type
safe_negate(T val) {
    return -val;
}

// 模板参数位置的 enable_if（更常用）
template <typename T,
          typename = std::enable_if_t<std::is_integral_v<T>>>
T safe_negate2(T val) {
    return -val;
}
```

## void_t 检测惯用法

```cpp
#include <type_traits>

// 检测类型是否有 begin() 方法
template <typename T, typename = void>
struct has_begin : std::false_type {};

template <typename T>
struct has_begin<T, std::void_t<decltype(std::declval<T>().begin())>>
    : std::true_type {};

// 使用
static_assert(has_begin<std::vector<int>>::value);  // true
static_assert(!has_begin<int>::value);               // false
```

## 现代替代

```cpp
// C++17: if constexpr 替代大部分 SFINAE
template <typename T>
auto process(T val) {
    if constexpr (std::is_arithmetic_v<T>) {
        std::cout << "Arithmetic: " << val;
    } else {
        std::cout << "Other type";
    }
}

// C++20: Concepts 完全替代 SFINAE
template <typename T> requires std::is_arithmetic_v<T>
void process(T val) {
    std::cout << "Arithmetic: " << val;
}
```

## 关键要点

> SFINAE 只在"直接上下文"中生效——函数体内的错误不是 SFINAE，会直接编译失败。`decltype` 表达式在模板参数替换阶段求值，是 SFINAE 的核心工具。

> C++20 的 Concepts 是 SFINAE 的完全替代——更清晰的语法、更好的错误信息。

## 相关模式 / 关联

- [[cpp-concepts]] — C++20 的现代替代
- [[cpp-type-traits]] — SFINAE 依赖的类型检查
- [[cpp-if-constexpr]] — 运行分支的替代
