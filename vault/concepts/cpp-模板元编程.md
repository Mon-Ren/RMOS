---
title: 模板元编程
tags: [cpp, template, metaprogramming, compile-time, type-computation]
aliases: [模板元编程, compile-time programming, 类型计算, TMP]
created: 2026-04-04
updated: 2026-04-04
---

# 模板元编程

模板元编程是在编译期用模板系统做计算——C++ 的"第二语言"，编译器就是解释器。

## 编译期计算

```cpp
// 经典示例：编译期阶乘
template <int N>
struct Factorial {
    static constexpr int value = N * Factorial<N - 1>::value;
};

template <>
struct Factorial<0> {
    static constexpr int value = 1;
};

static_assert(Factorial<5>::value == 120);  // 编译期计算

// 现代替代：constexpr 函数更简洁
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}
```

## 类型计算

```cpp
// 编译期类型列表
template <typename... Ts>
struct TypeList {};

// 取第一个类型
template <typename List>
struct Front;

template <typename T, typename... Rest>
struct Front<TypeList<T, Rest...>> {
    using type = T;
};

using MyList = TypeList<int, double, char>;
using First = Front<MyList>::type;  // int

// 类型判断
template <typename T, typename U>
struct IsSame : std::false_type {};

template <typename T>
struct IsSame<T, T> : std::true_type {};

static_assert(IsSame<int, int>::value);
```

## if constexpr 替代大部分元编程

```cpp
// 旧方式：模板特化 + 类型选择
template <bool Cond, typename T, typename F>
struct If;

template <typename T, typename F>
struct If<true, T, F> { using type = T; };

template <typename T, typename F>
struct If<false, T, F> { using type = F; };

using Selected = If<sizeof(int) == 4, int, long>::type;

// 现代方式：if constexpr + std::conditional_t
using Selected2 = std::conditional_t<sizeof(int) == 4, int, long>;

// 甚至直接用 if constexpr
template <typename T>
auto process(T val) {
    if constexpr (std::is_integral_v<T>) { /* 整数处理 */ }
    else { /* 其他处理 */ }
}
```

## 关键要点

> C++11 的模板元编程是图灵完备的——但代码难以阅读。C++17 的 `if constexpr` 和 C++20 的 Concepts/consteval 已经替代了大部分 TMP 场景。

> 需要做编译期计算时，优先用 `constexpr` 函数；需要做类型操作时，优先用 `<type_traits>`。

## 相关模式 / 关联

- [[cpp-if-constexpr]] — 编译期分支
- [[cpp-type-traits]] — 类型操作库
- [[cpp-concepts]] — 模板约束
