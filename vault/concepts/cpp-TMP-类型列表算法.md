---
title: TMP 类型列表算法
tags: [cpp, template, typelist, metaprogramming, type-computation]
aliases: [TypeList 算法, 编译期类型操作, 类型列表变换]
created: 2026-04-05
updated: 2026-04-05
---

# TMP 类型列表算法

**一句话概述：** TypeList 是模板元编程的"数组"——PushFront、PopFront、Find、Filter、Map 等操作在编译期对类型进行变换。C++11 的变参模板让 TypeList 的实现简洁了很多。

## 实现

```cpp
// TypeList 定义
template <typename... Ts>
struct TypeList {};

// Head（取第一个类型）
template <typename List>
struct Head;

template <typename T, typename... Ts>
struct Head<TypeList<T, Ts...>> { using type = T; };

// Tail（去掉第一个类型）
template <typename List>
struct Tail;

template <typename T, typename... Ts>
struct Tail<TypeList<T, Ts...>> { using type = TypeList<Ts...>; };

// PushFront
template <typename List, typename T>
struct PushFront;

template <typename... Ts, typename T>
struct PushFront<TypeList<Ts...>, T> { using type = TypeList<T, Ts...>; };

// Size
template <typename List>
struct Size;

template <typename... Ts>
struct Size<TypeList<Ts...>>
    : std::integral_constant<size_t, sizeof...(Ts)> {};

// IndexOf（查找类型在列表中的位置）
template <typename List, typename T>
struct IndexOf;

template <typename T, typename... Ts>
struct IndexOf<TypeList<T, Ts...>, T>
    : std::integral_constant<size_t, 0> {};

template <typename T, typename U, typename... Ts>
struct IndexOf<TypeList<U, Ts...>, T>
    : std::integral_constant<size_t, 1 + IndexOf<TypeList<Ts...>, T>::value> {};

// 使用
using MyTypes = TypeList<int, double, char, float>;
static_assert(Head<MyTypes>::type{} == typeid(int));
static_assert(Size<MyTypes>::value == 4);
static_assert(IndexOf<MyTypes, char>::value == 2);
```

## 关键要点

> TypeList 的核心价值：编译期类型验证。比如检查某类型是否在允许的类型列表中，不在就编译错误。

> C++20 concepts 让很多 TypeList 场景变得不需要了——直接用 requires 表达式检查类型特征。

## 相关模式 / 关联

- [[cpp-可变参数模板]] — 参数包
- [[cpp-模板元编程]] — TMP 基础
- [[cpp-concepts]] — 现代替代
- [[cpp-variant]] — 运行时类型列表
