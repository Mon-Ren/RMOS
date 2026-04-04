---
title: 模板模板参数
tags: [cpp, template, template-template-parameter, container-design]
aliases: [模板模板参数, template template, 容器模板参数]
created: 2026-04-04
updated: 2026-04-04
---

# 模板模板参数

模板模板参数让一个模板接受另一个模板作为参数——用来编写"适用于任何容器模板"的代码。

## 意图与场景

- 泛型容器包装：不限定具体容器，只限定容器模板
- 策略类模板化：策略本身是模板
- 编写真正容器无关的代码

## 基本语法

```cpp
// Container 是一个"模板参数"——它本身是一个模板
template <typename T, template <typename, typename> class Container>
class Stack {
    Container<T, std::allocator<T>> data_;  // 实例化 Container
public:
    void push(const T& val) { data_.push_back(val); }
    T pop() { T val = data_.back(); data_.pop_back(); return val; }
};

// 使用
Stack<int, std::vector> int_stack;   // 用 vector 存储
Stack<int, std::deque> int_deque;    // 用 deque 存储
```

## C++17 简化

```cpp
// C++17: template template parameter 的模板参数可以有默认值
template <template <typename, typename = std::allocator<int>> class Container>
class IntProcessor {
    Container<int> data_;  // 不需要手动指定 allocator
};

IntProcessor<std::vector> proc;  // OK
```

## C++20 Concepts 约束

```cpp
template <typename T>
concept SequenceContainer = requires(T t, typename T::value_type v) {
    t.push_back(v);
    t.pop_back();
    t.back();
    { t.size() } -> std::convertible_to<size_t>;
};

template <typename T, template <typename, typename> class Container>
    requires SequenceContainer<Container<T, std::allocator<T>>>
class SafeStack {
    Container<T, std::allocator<T>> data_;
};
```

## 关键要点

> 模板模板参数让模板接受"模板本身"而非"模板的实例"。语法上比普通模板参数复杂，但在泛型容器设计中非常有用。

> C++17 之前模板模板参数的参数列表必须精确匹配——C++17 允许参数数量不匹配时省略默认参数。

## 相关模式 / 关联

- [[cpp-模板编程基础]] — 模板基础
- [[cpp-concepts]] — C++20 的约束
