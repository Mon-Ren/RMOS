---
title: 并行算法（execution policy）
tags: [cpp17, parallel, execution-policy, par, par-unseq, algorithm]
aliases: [并行算法, execution policy, par, par_unseq, SIMD并行, std::execution]
created: 2026-04-04
updated: 2026-04-04
---

# 并行算法（C++17）

C++17 为 STL 算法添加了执行策略——一行代码让算法在多线程甚至 SIMD 上并行执行。

## 执行策略

```cpp
#include <execution>

// seq：顺序执行（默认）
std::sort(std::execution::seq, v.begin(), v.end());

// par：并行（多线程）
std::sort(std::execution::par, v.begin(), v.end());

// par_unseq：并行 + 向量化（SIMD）
// 可能更激进的重排，禁止同步
std::transform(std::execution::par_unseq, src.begin(), src.end(), dst.begin(),
    [](int x) { return x * x; });

// unseq：向量化（单线程，SIMD）
std::for_each(std::execution::unseq, v.begin(), v.end(),
    [](int& x) { x *= 2; });
```

## 支持并行策略的算法

```cpp
// 排序
std::sort, std::stable_sort

// 查找
std::find, std::find_if, std::count, std::count_if

// 归约
std::reduce, std::transform_reduce

// 变换
std::transform, std::for_each

// 填充
std::fill, std::generate

// 集合
std::merge, std::includes

// 更多...
// 但不是所有算法都支持并行策略
```

## 注意事项

```cpp
// ⚠️ 并行算法有额外要求：
// 1. 函数对象必须线程安全（不能有共享可变状态）
// 2. 迭代器必须满足更严格的随机访问要求
// 3. 数据不能有别名（par_unseq 时）

// ❌ 非线程安全的函数对象
int sum = 0;
std::for_each(std::execution::par, v.begin(), v.end(),
    [&sum](int x) { sum += x; });  // 数据竞争！

// ✅ 用 reduce 替代
int sum = std::reduce(std::execution::par, v.begin(), v.end(), 0);
```

## 关键要点

> 并行算法对大数据量（> 10000 元素）才有收益——小数据的线程管理开销超过并行收益。

> `par_unseq` 最激进但限制最多——函数对象不能有同步，数据不能有别名。

## 相关模式 / 关联

- [[cpp-stl算法总览]] — 算法基础
- [[cpp-数值算法与归约]] — 并行归约
