---
title: 数组与 std::array
tags: [cpp, array, std::array, C-array, fixed-size, aggregate]
aliases: [std::array, 数组, C数组, 固定大小数组, aggregate]
created: 2026-04-04
updated: 2026-04-04
---

# 数组与 std::array

C 数组裸露而危险，`std::array` 安全而零开销——固定大小场景用 `std::array`，动态大小用 `vector`。

## C 数组 vs std::array

```cpp
// C 数组：裸指针退化、无边界信息
int arr[5] = {1, 2, 3, 4, 5};
int* p = arr;              // 数组退化为指针，丢失大小
sizeof(arr);               // 20（知道大小）
void foo(int a[]);         // 实际是 int* a，丢失大小

// std::array：类型安全、零开销
#include <array>
std::array<int, 5> arr = {1, 2, 3, 4, 5};
// arr 不会退化为指针
arr.size();                // 5（编译期已知）
arr[0];                    // 带边界信息的访问
// arr.at(10);              // 抛异常（带边界检查）

// 零开销：std::array 的内存布局与 C 数组完全一致
static_assert(sizeof(std::array<int, 5>) == 5 * sizeof(int));
```

## std::array 的用法

```cpp
std::array<int, 10> a = {1, 2, 3, 4, 5};  // 其余为 0

a.fill(0);              // 全部填 0
a.front();              // 第一个元素
a.back();               // 最后一个元素
a.data();               // 返回底层数组指针（兼容 C API）

// 迭代
for (auto& x : a) { x *= 2; }

// 解构
auto [a1, a2, a3, a4, a5, r1, r2, r3, r4, r5] = a;

// 比较（C++20 隐式生成 spaceship）
std::array<int, 3> x = {1, 2, 3};
std::array<int, 3> y = {1, 2, 4};
x < y;  // true（字典序比较）
```

## 与 vector 的选择

```
场景                      选择
大小编译期已知且固定     → std::array
大小运行时确定           → std::vector
需要连续内存             → 两者都满足
与 C API 互操作          → 两者都可（data() 返回指针）
栈上分配                 → std::array
大数组（> 1MB）          → std::vector（避免栈溢出）
```

## 关键要点

> `std::array` 是 C 数组的安全替代——零运行时开销、支持 STL 接口、保留大小信息。优先用 `std::array` 替代 C 数组。

> 大数组用 `std::vector`（堆分配）或全局 `std::array`，避免栈溢出。

## 相关模式 / 关联

- [[cpp-vector深入]] — 动态数组
- [[cpp-span]] — array/vector 的视图
