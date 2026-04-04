---
title: C++ 编译期整数序列
tags: [cpp, integer-sequence, index-sequence, make-index-sequence, compile-time]
aliases: [integer_sequence, index_sequence, 整数序列, 编译期序列展开]
created: 2026-04-04
updated: 2026-04-04
---

# 编译期整数序列（C++14）

`std::index_sequence` 是编译期的整数列表——用于展开参数包、生成索引序列。

## 基本用法

```cpp
#include <utility>

// index_sequence<0, 1, 2, 3, 4>
using seq = std::index_sequence<0, 1, 2, 3, 4>;

// make_index_sequence<N> 生成 0 到 N-1
using seq5 = std::make_index_sequence<5>;  // index_sequence<0,1,2,3,4>
```

## 展开参数包

```cpp
// 用索引展开 tuple
template <typename Tuple, size_t... Is>
void print_tuple_impl(const Tuple& t, std::index_sequence<Is...>) {
    ((std::cout << std::get<Is>(t) << " "), ...);
    std::cout << "\n";
}

template <typename... Args>
void print_tuple(const std::tuple<Args...>& t) {
    print_tuple_impl(t, std::make_index_sequence<sizeof...(Args)>{});
}

auto t = std::make_tuple(1, 3.14, "hello");
print_tuple(t);  // 1 3.14 hello
```

## 数组展开

```cpp
template <typename T, size_t N, size_t... Is>
auto array_to_tuple_impl(const std::array<T, N>& arr, std::index_sequence<Is...>) {
    return std::make_tuple(arr[Is]...);
}

template <typename T, size_t N>
auto array_to_tuple(const std::array<T, N>& arr) {
    return array_to_tuple_impl(arr, std::make_index_sequence<N>{});
}

auto arr = std::array<int, 3>{1, 2, 3};
auto t = array_to_tuple(arr);  // std::tuple<int, int, int>{1, 2, 3}
```

## 关键要点

> `index_sequence` 是展开参数包的核心工具——`make_index_sequence<N>` 生成编译期索引 0 到 N-1。

> C++17 的折叠表达式已经替代了部分 `index_sequence` 场景，但 tuple/数组展开仍需要它。

## 相关模式 / 关联

- [[cpp-可变参数模板]] — 参数包
- [[cpp-折叠表达式]] — 折叠表达式替代部分场景
