---
title: C++23 std::mdspan
tags: [cpp23, mdspan, multidimensional, array-view, extents]
aliases: [mdspan, 多维数组视图, 多维span, extents]
created: 2026-04-04
updated: 2026-04-04
---

# std::mdspan（C++23）

`mdspan` 是多维数组的非拥有视图——把一维连续内存解释为多维数组，零开销。

## 基本用法

```cpp
#include <mdspan>

// 将一维数据解释为 3x4 矩阵
std::vector<int> data(12);
std::mdspan<int, std::extents<int, 3, 4>> matrix(data.data());

matrix[1, 2] = 42;   // 访问 [1][2]
int val = matrix[0, 3];

// 动态维度
std::mdspan<int, std::extents<int, std::dynamic_extent, 4>> dyn(data.data(), 3);
// 第一维运行时确定，第二维编译期确定为 4
```

## layout 策略

```cpp
// layout_right（C 风格）：最后一维连续
std::mdspan<int, std::extents<int, 3, 4>,
    std::layout_right> row_major(data.data());

// layout_left（Fortran 风格）：第一维连续
std::mdspan<int, std::extents<int, 3, 4>,
    std::layout_left> col_major(data.data());

// layout_stride：自定义步长
```

## 关键要点

> `mdspan` 不拥有数据——底层数据必须连续且存活。它是 `span` 的多维版本。

> 固定维度在编译期已知时，编译器可以优化循环。动态维度通过 `dynamic_extent` 支持。

## 相关模式 / 关联

- [[cpp-span]] — 一维版本
- [[cpp-vector深入]] — 底层数据容器
