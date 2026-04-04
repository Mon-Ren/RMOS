---
title: C++ 编译期控制流
tags: [cpp, compile-time, if-constexpr, template-recursion, consteval]
aliases: [编译期控制流, 编译期循环, 编译期if, 递归模板]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 编译期控制流

C++ 中实现编译期"循环"和"分支"有多种方式——从 C++98 的递归模板到 C++20 的 consteval。

## if constexpr（C++17）

```cpp
template <typename T>
auto to_string(T val) {
    if constexpr (std::is_same_v<T, int>) {
        return std::to_string(val);
    } else if constexpr (std::is_same_v<T, double>) {
        return std::to_string(val);
    } else if constexpr (std::is_same_v<T, bool>) {
        return val ? "true" : "false";
    } else {
        static_assert(sizeof(T) == 0, "Unsupported type");
    }
}
```

## constexpr 函数中的循环（C++14）

```cpp
constexpr int sum_1_to_n(int n) {
    int total = 0;
    for (int i = 1; i <= n; ++i) {  // 编译期可执行
        total += i;
    }
    return total;
}
static_assert(sum_1_to_n(100) == 5050);
```

## 递归模板（C++98 方式）

```cpp
// 编译期阶乘——递归模板
template <int N> struct Factorial {
    static constexpr int value = N * Factorial<N-1>::value;
};
template <> struct Factorial<0> {
    static constexpr int value = 1;
};
static_assert(Factorial<10>::value == 3628800);
```

## consteval（C++20）

```cpp
// consteval 函数保证编译期执行
consteval int must_be_ct(int n) {
    int result = 0;
    for (int i = 0; i < n; ++i) {
        result += i * i;
    }
    return result;
}
constexpr auto val = must_be_ct(10);  // OK
```

## 编译期整数序列展开

```cpp
// 用 index_sequence 展开循环
template <size_t... Is>
void print_all_impl(std::index_sequence<Is...>) {
    (std::cout << ... << Is);  // 折叠表达式展开
}

template <size_t N>
void print_all() {
    print_all_impl(std::make_index_sequence<N>{});
}
// print_all<5>() 输出 01234
```

## 关键要点

> C++14 后 `constexpr` 函数可以写循环和分支——递归模板作为"编译期循环"的方式已过时。

> `if constexpr` 替代了大量模板特化分支。`consteval` 保证函数一定在编译期执行。

## 相关模式 / 关联

- [[cpp-if-constexpr]] — 编译期 if
- [[cpp-编译期计算与constexpr深入]] — constexpr 演进
