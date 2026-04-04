---
title: STL 算法总览
tags: [cpp, stl, algorithm, sort, find, transform, for-each]
aliases: [STL算法, 算法库, algorithm, 排序, 查找, 变换]
created: 2026-04-04
updated: 2026-04-04
---

# STL 算法总览

STL 算法是 C++ 泛型编程的精髓——操作迭代器范围而非特定容器，一套算法适用于所有容器。

## 意图与场景

- 对容器做排序、查找、变换、过滤、归约等操作
- 用命名算法替代手写循环——意图更清晰、bug 更少

## 查找算法

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// 单元素查找
auto it = std::find(v.begin(), v.end(), 5);         // 查找值
auto it2 = std::find_if(v.begin(), v.end(),         // 条件查找
    [](int x) { return x > 5; });
auto it3 = std::find_if_not(v.begin(), v.end(),     // 找第一个不满足条件的
    [](int x) { return x < 5; });

// 统计
int count = std::count(v.begin(), v.end(), 1);       // 统计值出现次数
int count2 = std::count_if(v.begin(), v.end(),       // 条件计数
    [](int x) { return x % 2 == 0; });

// 范围查找
bool has = std::binary_search(v.begin(), v.end(), 5);  // 有序范围中查找
auto lb = std::lower_bound(v.begin(), v.end(), 5);     // 第一个 >= 5
auto ub = std::upper_bound(v.begin(), v.end(), 5);     // 第一个 > 5

// 谓词检查
bool all_pos = std::all_of(v.begin(), v.end(), [](int x) { return x > 0; });
bool any_neg = std::any_of(v.begin(), v.end(), [](int x) { return x < 0; });
bool none_zero = std::none_of(v.begin(), v.end(), [](int x) { return x == 0; });
```

## 排序与重排

```cpp
std::sort(v.begin(), v.end());                          // 升序
std::sort(v.begin(), v.end(), std::greater<>());        // 降序
std::stable_sort(v.begin(), v.end());                   // 稳定排序

std::partial_sort(v.begin(), v.begin() + 3, v.end());   // 前3个最小
std::nth_element(v.begin(), v.begin() + 3, v.end());    // 第3小的在正确位置

std::reverse(v.begin(), v.end());                       // 反转
std::rotate(v.begin(), v.begin() + 2, v.end());         // 旋转
std::shuffle(v.begin(), v.end(), rng);                  // 随机打乱

// 去重（先排序）
std::sort(v.begin(), v.end());
auto end = std::unique(v.begin(), v.end());             // 移动重复到末尾
v.erase(end, v.end());                                  // 真正删除
```

## 变换与归约

```cpp
std::vector<int> src = {1, 2, 3, 4, 5};
std::vector<int> dst(src.size());

// 变换
std::transform(src.begin(), src.end(), dst.begin(),
    [](int x) { return x * x; });                      // dst = {1, 4, 9, 16, 25}

// 归约（C++17）
int sum = std::reduce(src.begin(), src.end(), 0);      // 并行友好
int prod = std::accumulate(src.begin(), src.end(), 1,
    [](int a, int b) { return a * b; });               // C++11 方式

// 前缀和
std::partial_sum(src.begin(), src.end(), dst.begin());  // dst = {1, 3, 6, 10, 15}

// 填充
std::fill(v.begin(), v.end(), 0);                       // 全部设为 0
std::iota(v.begin(), v.end(), 1);                       // {1, 2, 3, 4, 5}
```

## 集合操作（需有序范围）

```cpp
std::vector<int> a = {1, 2, 3, 4, 5};
std::vector<int> b = {3, 4, 5, 6, 7};
std::vector<int> result;

std::set_union(a.begin(), a.end(), b.begin(), b.end(),
    std::back_inserter(result));         // {1, 2, 3, 4, 5, 6, 7}

std::set_intersection(a.begin(), a.end(), b.begin(), b.end(),
    std::back_inserter(result));         // {3, 4, 5}

std::set_difference(a.begin(), a.end(), b.begin(), b.end(),
    std::back_inserter(result));         // {1, 2}（a 有 b 没有的）
```

## 关键要点

> 优先使用命名算法而非手写循环——`std::find` 比 `for` 循环意图更明确，且编译器优化得更好。

> 大部分算法接受自定义比较函数（谓词），最后一个参数通常是 `pred`。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — 算法中 Lambda 的使用
- [[cpp-range库]] — C++20 管道风格算法
