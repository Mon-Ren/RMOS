---
title: C++ 模板特化与偏特化
tags: [cpp, template, specialization, partial-specialization, full-specialization]
aliases: [模板特化, 全特化, 偏特化, partial specialization, specialization]
created: 2026-04-04
updated: 2026-04-04
---

# 模板特化与偏特化

特化为特定类型提供定制实现——全特化针对完全匹配的类型，偏特化针对部分匹配的类型。

## 全特化

```cpp
// 主模板
template <typename T>
struct TypeName {
    static const char* get() { return "unknown"; }
};

// 全特化：为 int 提供定制
template <>
struct TypeName<int> {
    static const char* get() { return "int"; }
};

// 全特化：为 string 提供定制
template <>
struct TypeName<std::string> {
    static const char* get() { return "string"; }
};

TypeName<int>::get();        // "int"
TypeName<double>::get();     // "unknown"
```

## 偏特化

```cpp
// 主模板
template <typename T, typename U>
struct IsSame {
    static constexpr bool value = false;
};

// 偏特化：两个类型相同时
template <typename T>
struct IsSame<T, T> {
    static constexpr bool value = true;
};

IsSame<int, double>::value;  // false
IsSame<int, int>::value;     // true

// 指针偏特化
template <typename T>
struct TypeName<T*> {
    static const char* get() { return "pointer"; }
};

TypeName<int*>::get();       // "pointer"
```

## 函数模板只能全特化

```cpp
// 函数模板不能偏特化——用重载替代
template <typename T>
void process(T val) { /* 通用版本 */ }

// 全特化
template <>
void process<int>(int val) { /* int 版本 */ }

// 不能偏特化，但可以用重载模拟
template <typename T>
void process(T* ptr) { /* 指针版本（这是重载，不是偏特化） */ }
```

## 关键要点

> 类模板可以全特化和偏特化。函数模板只能全特化——用重载替代偏特化。

> 特化的选择规则：完全匹配的全特化 > 偏特化 > 主模板。

## 相关模式 / 关联

- [[cpp-模板编程基础]] — 模板基础
- [[cpp-type-traits]] — type_traits 中大量使用特化
