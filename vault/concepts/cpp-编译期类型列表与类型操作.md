---
title: C++ 编译期类型列表与类型操作
tags: [cpp, metaprogramming, type-list, type-operations, compile-time]
aliases: [类型列表, TypeList, 类型操作, 编译期类型计算]
created: 2026-04-04
updated: 2026-04-04
---

# 编译期类型列表与类型操作

类型列表是模板元编程的基础数据结构——在编译期操作类型集合。

## TypeList

```cpp
template <typename... Ts>
struct TypeList {};

// 基本操作
using MyList = TypeList<int, double, std::string>;

// 获取长度
template <typename List>
struct Length;

template <typename... Ts>
struct Length<TypeList<Ts...>> {
    static constexpr size_t value = sizeof...(Ts);
};

static_assert(Length<MyList>::value == 3);
```

## Head / Tail

```cpp
// 取第一个类型
template <typename List>
struct Head;

template <typename T, typename... Rest>
struct Head<TypeList<T, Rest...>> {
    using type = T;
};

// 取剩余类型
template <typename List>
struct Tail;

template <typename T, typename... Rest>
struct Tail<TypeList<T, Rest...>> {
    using type = TypeList<Rest...>;
};

using MyList = TypeList<int, double, char>;
using First = Head<MyList>::type;         // int
using Rest = Tail<MyList>::type;          // TypeList<double, char>
```

## IndexOf

```cpp
// 查找类型在列表中的位置
template <typename T, typename List>
struct IndexOf;

template <typename T, typename... Rest>
struct IndexOf<T, TypeList<T, Rest...>> {
    static constexpr size_t value = 0;  // 找到了
};

template <typename T, typename U, typename... Rest>
struct IndexOf<T, TypeList<U, Rest...>> {
    static constexpr size_t value = 1 + IndexOf<T, TypeList<Rest...>>::value;
};

static_assert(IndexOf<double, MyList>::value == 1);
```

## 关键要点

> 类型列表让编译期可以操作类型集合——variant、tuple 的实现都依赖类似的类型操作。

> C++17 的 `if constexpr` 和折叠表达式已经替代了大部分类型列表递归操作。

## 相关模式 / 关联

- [[cpp-模板元编程]] — 元编程基础
- [[cpp-variant]] — variant 的实现涉及类型列表
