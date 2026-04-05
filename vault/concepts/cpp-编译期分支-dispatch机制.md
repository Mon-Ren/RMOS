---
title: 编译期分支与 dispatch 机制
tags: [cpp, compile-time, dispatch, if-constexpr, tag-dispatch, overload]
aliases: [编译期分发, 函数分发机制, 编译期选择]
created: 2026-04-05
updated: 2026-04-05
---

# 编译期分支与 dispatch 机制

**一句话概述：** C++ 提供三种编译期分支机制——标签分发（tag dispatch）、SFINAE/enable_if、if constexpr。if constexpr 是最简洁的现代选择，但标签分发在某些场景仍然不可替代（比如跨多个函数的分发）。

## 三种机制对比

```cpp
// ─── 标签分发（C++98+）───
template <typename T>
void do_impl(T val, std::true_type)  { /* 快速路径 */ }
template <typename T>
void do_impl(T val, std::false_type) { /* 通用路径 */ }
template <typename T>
void do_dispatch(T val) {
    do_impl(val, std::is_integral<T>{});  // 编译期选择
}
// 优点：分发逻辑可以跨函数传递
// 缺点：需要额外的函数重载

// ─── if constexpr（C++17）───
template <typename T>
void do_dispatch(T val) {
    if constexpr (std::is_integral_v<T>) {
        /* 快速路径 */
    } else {
        /* 通用路径 */
    }
}
// 优点：简洁、直观
// 缺点：分支逻辑必须在一个函数内

// ─── requires（C++20）───
template <typename T> requires std::is_integral_v<T>
void do_dispatch(T val) { /* 快速路径 */ }
template <typename T> requires (!std::is_integral_v<T>)
void do_dispatch(T val) { /* 通用路径 */ }
// 优点：概念约束清晰
// 缺点：需要多个函数签名
```

## 关键要点

> 选择规则：同一函数体内分支用 if constexpr，跨函数/类级别分发用 tag dispatch 或 concepts。现代 C++ 优先用 if constexpr。

## 相关模式 / 关联

- [[cpp-if-constexpr]] — 编译期分支
- [[cpp-标签分发]] — tag dispatch
- [[cpp-concepts]] — concepts 约束
- [[cpp-SFINAE的现代替代方案]] — SFINAE 替代
