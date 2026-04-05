---
title: SFINAE 表达式检测技巧
tags: [cpp, sfinae, detection, void_t, enable-if, type-detection]
aliases: [void_t 检测, 检测成员函数, 类型特征检测]
created: 2026-04-05
updated: 2026-04-05
---

# SFINAE 表达式检测技巧

**一句话概述：** `void_t` 是 C++17 的 SFINAE 利器——检测一个类型是否有某个成员、某个操作是否合法。配合 `decltype` 和 `std::declval`，可以检查任意复杂类型表达式。

## void_t 的魔力

```cpp
#include <type_traits>

template <typename, typename = void>
struct has_serialize : std::false_type {};

template <typename T>
struct has_serialize<T, std::void_t<
    decltype(std::declval<T>().serialize(std::declval<std::ostream&>()))
>> : std::true_type {};

// 使用
struct MyType { void serialize(std::ostream&) {} };
struct OtherType { void dump() {} };

static_assert(has_serialize<MyType>::value);      // true
static_assert(!has_serialize<OtherType>::value);   // false
static_assert(!has_serialize<int>::value);          // false
```

## 检测嵌套类型

```cpp
template <typename, typename = void>
struct has_value_type : std::false_type {};

template <typename T>
struct has_value_type<T, std::void_t<typename T::value_type>> : std::true_type {};

static_assert(has_value_type<std::vector<int>>::value);  // true
static_assert(!has_value_type<int>::value);               // false
```

## 关键要点

> C++20 的 requires 表达式是 void_t 的现代替代——更直观、报错更友好。新代码应该优先用 requires。

## 相关模式 / 关联

- [[cpp-sfinae与编译期多态]] — SFINAE 基础
- [[cpp-type-traits]] — 类型特征
- [[cpp-SFINAE的现代替代方案]] — concepts 替代
- [[cpp-concepts]] — C++20 concepts
