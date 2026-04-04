---
title: Concepts（C++20）
tags: [cpp20, concepts, requires, constraints, template]
aliases: [concepts, 概念, requires子句, 模板约束, 概念约束]
created: 2026-04-04
updated: 2026-04-04
---

# Concepts（C++20）

Concepts 给模板参数加上可表达的约束——SFINAE 的噩梦结束了，编译错误终于能读了。

## 意图与场景

- 替代 SFINAE 约束模板参数
- 在编译期捕获类型不匹配问题，给出清晰错误信息
- 约束 auto 参数（C++20 简化语法）

## 基本用法

```cpp
#include <concepts>

// 定义 concept
template <typename T>
concept Numeric = std::is_arithmetic_v<T>;

// 使用 concept 约束模板
template <Numeric T>
T add(T a, T b) {
    return a + b;
}

// 等价写法
template <typename T> requires Numeric<T>
T add(T a, T b) { return a + b; }

// 约束 auto
Numeric auto x = 42;          // OK
// Numeric auto y = "hello";  // 编译错误：const char* 不满足 Numeric
```

## 标准库 concepts

```cpp
#include <concepts>

// 核心语言 concepts
std::same_as<int> auto a = 42;              // 类型必须精确为 int
std::convertible_to<double> auto b = 42;    // int 可转换为 double
std::derived_from<Derived, Base> auto c = d; // Derived 必须派生自 Base

// 比较 concepts
std::equality_comparable<int>;               // 支持 ==
std::totally_ordered<int>;                   // 支持 <, >, <=, >=

// 对象 concepts
std::copyable<std::string>;                  // 可拷贝
std::movable<std::unique_ptr<int>>;          // 可移动
std::default_initializable<Widget>;          // 可默认构造

// 可调用 concepts
std::invocable<void(int), int>;              // 可用 int 调用
std::predicate<std::function<bool(int)>, int>; // 返回 bool
```

## requires 表达式

```cpp
template <typename T>
concept HasSize = requires(T t) {
    { t.size() } -> std::convertible_to<size_t>;  // t.size() 可转换为 size_t
    typename T::value_type;                        // T 有 value_type 嵌套类型
    { t.begin() } -> std::input_or_output_iterator; // t.begin() 是迭代器
};

// 复合约束
template <typename T>
concept SortableContainer = HasSize<T> && requires(T t) {
    { std::sort(t.begin(), t.end()) };
    requires std::swappable<T>;
};
```

## 实际示例

```cpp
// 约束算法
template <std::ranges::range R, typename T>
    requires std::equality_comparable_with<std::ranges::range_value_t<R>, T>
auto find_in(R&& range, const T& value) {
    return std::ranges::find(range, value);
}

// 约束类模板
template <typename T>
    requires std::is_arithmetic_v<T>
class SafeNumber {
    T value_;
public:
    explicit SafeNumber(T v) : value_(v) {}
    // ...
};
```

## 关键要点

> Concepts 是编译期约束——不产生运行时开销。它让模板错误信息从"一堆模板实例化栈"变成"类型 X 不满足 concept Y"。

> C++20 标准库已经大量使用 concepts（`<concepts>` 头文件和 ranges 库），理解 concepts 是使用现代 C++ 的前提。

## 相关模式 / 关联

- [[cpp-sfinae-与编译期多态]] — Concepts 是 SFINAE 的替代
- [[cpp-模板编程基础]] — 模板约束的演进
