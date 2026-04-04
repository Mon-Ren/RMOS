---
title: span（C++20）
tags: [cpp20, span, array-view, non-owning, contiguous]
aliases: [span, 数组视图, 非拥有引用, array_view]
created: 2026-04-04
updated: 2026-04-04
---

# std::span（C++20）

`span` 是连续数据的非拥有视图——函数参数的最优选择，接受数组、vector、array 而零拷贝。

## 意图与场景

- 函数接受连续数据片段而不关心容器类型
- 替代 `(pointer, size)` 参数对
- 子范围的零拷贝传递

## 基本用法

```cpp
#include <span>
#include <vector>
#include <array>

// span 不拥有数据，只是指向连续内存的视图
void process(std::span<const int> data) {
    for (int x : data) {
        std::cout << x << " ";
    }
}

int arr[] = {1, 2, 3, 4, 5};
std::vector<int> vec = {6, 7, 8};
std::array<int, 3> std_arr = {9, 10, 11};

process(arr);       // OK：从数组构造
process(vec);       // OK：从 vector 构造
process(std_arr);   // OK：从 array 构造
process({arr, 3});  // OK：指定大小

// 动态 span：大小运行时确定
std::span<int> dynamic = vec;

// 固定大小 span：编译期知道大小
std::span<int, 5> fixed = arr;  // 编译期检查大小
```

## 子范围操作

```cpp
std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
std::span<int> s = v;

auto first3 = s.first(3);      // {1, 2, 3}
auto last4 = s.last(4);        // {7, 8, 9, 10}
auto sub = s.subspan(2, 4);    // {3, 4, 5, 6}
auto rest = s.subspan(5);      // {6, 7, 8, 9, 10}

// span 支持范围操作
s.size();
s.empty();
s[0];
s.front();
s.back();
```

## 关键要点

> `span` 是函数参数中"接受连续数据"的最优解——它替代了 `(const T*, size_t)` 的传统写法，且自动从 vector/array/数组构造。

> `span` 不拥有数据——指向的数据必须在 span 生存期内存活。动态 span 的大小是 `size_t`，固定 span 的大小是编译期常量。

## 相关模式 / 关联

- [[cpp-string深入]] — `string_view` 是字符串版的 span
- [[cpp-vector深入]] — vector 是 span 最常见的数据源
