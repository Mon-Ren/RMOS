---
title: C++ std::pair 与 std::tuple
tags: [cpp, pair, tuple, structured-binding, multi-value, get]
aliases: [pair, tuple, get, make_pair, make_tuple, 多元组]
created: 2026-04-04
updated: 2026-04-04
---

# std::pair 与 std::tuple

`pair` 是固定两个值的组合，`tuple` 是任意多个值的组合——结构化绑定让它们的使用更自然。

## std::pair

```cpp
#include <utility>

std::pair<std::string, int> p1{"Alice", 25};
auto p2 = std::make_pair("Bob", 30);     // C++11
std::pair p3{"Charlie", 35};             // C++17 CTAD

p1.first;   // "Alice"
p1.second;  // 25

auto [name, age] = p1;  // 结构化绑定
```

## std::tuple

```cpp
#include <tuple>

std::tuple<int, double, std::string> t1{42, 3.14, "hello"};
auto t2 = std::make_tuple(1, 2.0, "world");  // C++11
std::tuple t3{1, 2.0, std::string("hi")};   // C++17 CTAD

// 访问
std::get<0>(t1);         // 42（按索引）
std::get<double>(t1);    // 3.14（按类型，不能有重复类型）

// 结构化绑定
auto [n, d, s] = t1;

// 修改
std::get<0>(t1) = 100;

// tie：将 tuple 解包到已有变量
int x; double y; std::string z;
std::tie(x, y, z) = t1;

// 忽略某些值
auto [a, _, c] = t1;  // 忽略第二个
```

## 常用操作

```cpp
// tuple 连接
auto t = std::tuple_cat(std::make_tuple(1), std::make_tuple(2.0, "hi"));
// (1, 2.0, "hi")

// tuple 比较（C++20 自动生成 <=>）
std::tuple<int, int> a{1, 2};
std::tuple<int, int> b{1, 3};
a < b;  // true（字典序）

// tuple 大小
std::tuple_size_v<decltype(t1)>;  // 3

// tuple_element
std::tuple_element_t<0, decltype(t1)>;  // int
```

## 关键要点

> pair 适合两个相关值（map 的键值对、find 的结果），tuple 适合三个以上值。但超过三个值时，考虑用 struct——更自文档化。

> `std::tie` 可以将 tuple 解包到已有变量，也可以创建"左值 tuple"用于比较。

## 相关模式 / 关联

- [[cpp-结构化绑定]] — 解构 pair/tuple
- [[cpp-函数返回多个值]] — 用 pair/tuple 返回多值
