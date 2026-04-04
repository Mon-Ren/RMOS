---
title: 模板编程基础
tags: [cpp, template, generic, function-template, class-template]
aliases: [模板, 函数模板, 类模板, 泛型编程, template]
created: 2026-04-04
updated: 2026-04-04
---

# 模板编程基础

模板是 C++ 泛型编程的核心——编译器根据使用时的类型参数，为每种类型实例化一份独立的代码。

## 意图与场景

- 编写与类型无关的通用算法和数据结构
- STL 的基础（容器、算法、迭代器全部基于模板）
- 编译期计算和类型操作

## 函数模板

```cpp
// 函数模板
template <typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

// 使用
int x = maximum(3, 5);           // T 推导为 int
double y = maximum(3.14, 2.71);  // T 推导为 double

// 显式指定类型
auto z = maximum<double>(3, 2.71);  // T = double，3 被隐式转换

// 多参数模板
template <typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}
auto r = add(1, 2.5);  // T=int, U=double, 返回 double
```

## 类模板

```cpp
template <typename T, size_t N>
class FixedArray {
    T data_[N];
public:
    T& operator[](size_t i) { return data_[i]; }
    const T& operator[](size_t i) const { return data_[i]; }
    constexpr size_t size() const { return N; }

    // 迭代器
    T* begin() { return data_; }
    T* end() { return data_ + N; }
};

FixedArray<int, 10> arr;        // N 是非类型模板参数，编译期确定
FixedArray<std::string, 5> strs;
```

## 模板特化

```cpp
// 主模板
template <typename T>
class Printer {
public:
    static void print(const T& val) {
        std::cout << val << "\n";
    }
};

// 全特化：针对特定类型
template <>
class Printer<std::string> {
public:
    static void print(const std::string& val) {
        std::cout << "\"" << val << "\"\n";  // 加引号
    }
};

// 偏特化：针对部分类型特征
template <typename T>
class Printer<T*> {
public:
    static void print(T* ptr) {
        std::cout << "ptr: " << ptr << "\n";
    }
};

Printer<int>::print(42);       // 用主模板
Printer<std::string>::print("hi");  // 用全特化
int x = 10;
Printer<int>::print(&x);       // 用偏特化（T*版本）
```

## SFINAE 初识

```cpp
#include <type_traits>

// SFINAE：Substitution Failure Is Not An Error
// 模板参数替换失败时，不报错，只是从重载集中移除

// 只对有 .size() 的类型启用
template <typename T>
auto get_size(const T& container) -> decltype(container.size()) {
    return container.size();
}

// 对指针类型特化
template <typename T>
std::enable_if_t<std::is_pointer_v<T>, size_t>
get_size(T ptr) {
    return 1;
}

std::vector<int> v{1, 2, 3};
get_size(v);     // 调用第一个版本

int* p = nullptr;
get_size(p);     // 调用指针版本
```

## 关键要点

> 模板在编译期实例化，每种类型参数生成独立的代码。优点是零开销抽象，缺点是编译时间长和代码膨胀。

> 非类型模板参数（如 `size_t N`）必须是编译期常量，这使得模板可以用于编译期计算。

## 相关模式 / 关联

- [[cpp-sfinae-与编译期多态]] — SFINAE 的深入应用
- [[cpp-variadic-模板]] — 可变参数模板
- [[cpp-constexpr-元编程]] — 编译期计算
