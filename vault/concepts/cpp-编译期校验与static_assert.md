---
title: C++ 编译期校验与 static_assert
tags: [cpp, static_assert, compile-time, constraint, verification]
aliases: [static_assert, 编译期校验, 编译期断言, concept检查]
created: 2026-04-04
updated: 2026-04-04
---

# 编译期校验与 static_assert

`static_assert` 是编译期的断言——不满足条件直接编译失败，零运行时开销。

## 基本用法

```cpp
// 验证类型大小
static_assert(sizeof(int) == 4, "int must be 4 bytes");
static_assert(sizeof(void*) == 8, "must be 64-bit");

// 验证类型特征
static_assert(std::is_integral_v<int>);
static_assert(std::is_base_of_v<Base, Derived>);

// C++17: 消息可选
static_assert(sizeof(int) == 4);  // C++17 起不需要消息
```

## 模板中的 static_assert

```cpp
template <typename T>
T safe_negate(T val) {
    static_assert(std::is_arithmetic_v<T>, "T must be arithmetic");
    return -val;
}

// 当用户传入不支持的类型时，编译错误信息清晰
safe_negate("hello");  // 编译错误：T must be arithmetic

// 与 requires 配合（C++20）
template <typename T> requires std::integral<T>
T gcd(T a, T b) {
    static_assert(sizeof(T) <= 8, "T too large for this implementation");
    // ...
}
```

## 禁止模板实例化

```cpp
// 永远失败的 static_assert（依赖模板参数）
template <typename T>
void unsupported() {
    static_assert(sizeof(T) == 0, "This type is not supported");
}
// sizeof(T) == 0 永远不成立，但编译器在模板未实例化时不报错
// 只有实例化时才报错

template <>
void unsupported<int>() { /* int 的特殊处理 */ }
```

## 关键要点

> `static_assert` 在编译期检查条件——用于验证类型假设、大小约束、平台特性等。不满足条件则编译失败，提供清晰的错误信息。

> 在模板中用 `static_assert` 给出比模板实例化错误更友好的错误信息。

## 相关模式 / 关联

- [[cpp-调试技术与断言]] — 运行时 assert
- [[cpp-concepts]] — C++20 的概念约束
