---
title: 数值算法与归约
tags: [cpp, stl, accumulate, reduce, transform-reduce, partial-sum, inner-product]
aliases: [数值算法, accumulate, reduce, 归约, 前缀和, inner_product]
created: 2026-04-04
updated: 2026-04-04
---

# 数值算法与归约

STL 的数值算法做求和、乘积、前缀和、内积等计算——C++17 的 `reduce` 和 `transform_reduce` 支持并行执行。

## accumulate vs reduce

```cpp
#include <numeric>
#include <vector>
#include <execution>

std::vector<int> v = {1, 2, 3, 4, 5};

// accumulate：顺序归约，不保证浮点精度
int sum = std::accumulate(v.begin(), v.end(), 0);           // 15
int prod = std::accumulate(v.begin(), v.end(), 1, std::multiplies<>());  // 120

// reduce（C++17）：可并行，浮点精度更好
int sum2 = std::reduce(v.begin(), v.end(), 0);              // 15
int sum3 = std::reduce(std::execution::par, v.begin(), v.end(), 0);  // 并行归约

// transform_reduce：先变换再归约（省一次遍历）
int sq_sum = std::transform_reduce(v.begin(), v.end(), 0,
    std::plus<>(), [](int x) { return x * x; });  // 1²+2²+3²+4²+5² = 55
```

## 前缀和

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};
std::vector<int> result(v.size());

// partial_sum：inclusive scan（包含当前元素）
std::partial_sum(v.begin(), v.end(), result.begin());
// result = {1, 3, 6, 10, 15}

// inclusive_scan（C++17）：可并行版本
std::inclusive_scan(v.begin(), v.end(), result.begin());

// exclusive_scan（C++17）：不包含当前元素
std::exclusive_scan(v.begin(), v.end(), result.begin(), 0);
// result = {0, 1, 3, 6, 10}
```

## inner_product

```cpp
std::vector<int> a = {1, 2, 3};
std::vector<int> b = {4, 5, 6};

// 内积：1*4 + 2*5 + 3*6 = 32
int dot = std::inner_product(a.begin(), a.end(), b.begin(), 0);

// 自定义操作
int custom = std::inner_product(a.begin(), a.end(), b.begin(), 0,
    std::plus<>(), [](int x, int y) { return x * y + 1; });
```

## 关键要点

> `reduce` 比 `accumulate` 更适合浮点和并行场景——`accumulate` 顺序执行可能导致浮点精度累积误差。

> `transform_reduce` 一步完成变换和归约——比分开两次遍历更快（一次遍历，cache 友好）。

## 相关模式 / 关联

- [[cpp-stl算法总览]] — STL 算法全景
- [[cpp-atomic与内存序]] — 并行算法的底层支持
