---
title: C++17 主要特性汇总
tags: [cpp17, features, structured-bindings, if-constexpr, fold, filesystem, optional]
aliases: [C++17, 特性汇总, structured bindings, if constexpr, 折叠表达式]
created: 2026-04-04
updated: 2026-04-04
---

# C++17 主要特性汇总

C++17 是实用性大幅提升的一批改进——没有颠覆性变化，但每一项都让日常编码更舒服。

## 语言特性

```cpp
// 结构化绑定
auto [key, value] = *map.begin();

// if constexpr
if constexpr (std::is_integral_v<T>) { /* ... */ }

// 折叠表达式
(auto... args) { return (args + ...); }

// 类模板参数推导（CTAD）
std::pair p{1, 2.0};              // deduced as pair<int, double>
std::vector v = {1, 2, 3};        // deduced as vector<int>
std::mutex mtx;
std::lock_guard lock(mtx);        // deduced as lock_guard<mutex>

// inline 变量
inline int global_count = 0;       // 头文件中定义，ODR-safe
inline std::string name = "test";

// 嵌套命名空间
namespace A::B::C { }  // 等价于 namespace A { namespace B { namespace C { } } }

// if 初始化语句
if (auto it = map.find(key); it != map.end()) {
    // it 在这里可用
}

// switch 初始化语句
switch (auto val = compute(); val) {
    case 1: /* ... */ break;
}

// [[nodiscard]], [[maybe_unused]], [[fallthrough]] 属性

// constexpr lambda
auto square = [](int x) constexpr { return x * x; };
constexpr int s = square(5);

// 模板参数的 auto
template <auto N> struct C { };  // C<42> N 的类型是 int
```

## 库特性

```cpp
// std::optional
std::optional<int> find(int key);

// std::variant
std::variant<int, double, std::string> val;

// std::any
std::any anything = 42;

// std::string_view
void process(std::string_view sv);

// std::filesystem
namespace fs = std::filesystem;
fs::path p = "/home/user/file.txt";

// std::byte
std::byte b{0xFF};

// std::execution（并行算法）
#include <execution>
std::sort(std::execution::par, v.begin(), v.end());

// std::reduce, std::exclusive_scan, std::inclusive_scan

// std::scoped_lock（多 mutex）
std::scoped_lock lock(mtx1, mtx2);

// 结构化绑定 + std::map
for (const auto& [k, v] : my_map) { }
```

## 关键要点

> C++17 最实用的五项：`if constexpr`、结构化绑定、`std::optional`、`std::string_view`、`std::filesystem`。

> CTAD（类模板参数推导）让模板类不需要手写 `make_*` 函数——`std::pair p{1, 2}` 比 `std::make_pair(1, 2)` 更直观。

## 相关模式 / 关联

- [[cpp-optional]] — optional 专题
- [[cpp-variant]] — variant 专题
- [[cpp-filesystem]] — filesystem 专题
