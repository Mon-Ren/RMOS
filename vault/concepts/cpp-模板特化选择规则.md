---
title: C++ 模板特化选择规则
tags: [cpp, template, specialization, overload-resolution, partial-ordering]
aliases: [特化选择, 偏序规则, 模板重载决议, 特化优先级]
created: 2026-04-04
updated: 2026-04-04
---

# 模板特化选择规则

当有多个模板候选时，编译器按规则选择最匹配的一个——理解这个规则是写出正确模板的关键。

## 选择顺序

```
1. 非模板函数/类（普通函数）
2. 模板函数的特化/重载
3. 主模板

全特化 vs 偏特化 vs 主模板：
- 完全匹配的全特化 > 偏特化 > 主模板
- 多个偏特化：更"特化"的胜出（偏序规则）
```

## 偏序规则

```cpp
// 主模板
template <typename T, typename U>
struct IsSame { static constexpr bool value = false; };

// 偏特化 1：两个类型相同
template <typename T>
struct IsSame<T, T> { static constexpr bool value = true; };

// IsSame<int, double> → 用主模板（T=int, U=double）→ false
// IsSame<int, int> → 用偏特化（T=int）→ true

// 偏序规则：更"特化"的胜出
template <typename T>
struct Foo { static constexpr int v = 0; };

template <typename T>
struct Foo<T*> { static constexpr int v = 1; };  // 偏特化：指针

template <>
struct Foo<int*> { static constexpr int v = 2; }; // 全特化：int*

// Foo<int*> → 全特化（v=2）
// Foo<double*> → 指针偏特化（v=1）
// Foo<int> → 主模板（v=0）
```

## 函数模板重载

```cpp
// 函数模板：重载决议而非特化
template <typename T> void foo(T);        // #1
template <typename T> void foo(T*);       // #2 重载（不是特化）
template <> void foo<int>(int);           // #1 的全特化

foo(42);       // 选 #1 的全特化（int 精确匹配）
foo(&x);       // 选 #2（T* 更特化）
foo(3.14);     // 选 #1（T=double）
```

## 关键要点

> 类模板用特化，函数模板用重载——函数模板的特化容易出错（特化不参与重载决议）。

> 偏序规则的核心：编译器选择"最特化"的候选。全特化 > 偏特化 > 主模板。

## 相关模式 / 关联

- [[cpp-模板特化与偏特化]] — 特化的写法
- [[cpp-模板编程基础]] — 模板基础
