---
title: type_traits 类型萃取
tags: [cpp, template, type-traits, metaprogramming, type-predicate]
aliases: [type_traits, 类型萃取, 类型特征, 编译期类型查询]
created: 2026-04-04
updated: 2026-04-04
---

# type_traits 类型萃取

`<type_traits>` 是 C++ 编译期类型查询库——在模板中检查类型特征、变换类型、条件选择类型。

## 意图与场景

- 模板中根据类型特征选择实现
- 约束模板参数（配合 SFINAE 或 Concepts）
- 编译期类型变换

## 类型检查

```cpp
#include <type_traits>

// 类型谓词（返回 bool 的 constexpr）
std::is_integral<int>::value;           // true
std::is_floating_point<double>::value;  // true
std::is_pointer<int*>::value;           // true
std::is_same<int, int32_t>::value;      // true（通常）
std::is_base_of<Base, Derived>::value;  // true
std::is_convertible<int, double>::value;// true

// C++17 简写：_v 后缀
std::is_integral_v<int>;               // 等价于 ::value
std::is_same_v<int, int32_t>;
```

## 类型变换

```cpp
// 类型变换（返回新类型）
using T1 = std::remove_const<const int>::type;      // int
using T2 = std::remove_reference<int&>::type;        // int
using T3 = std::remove_pointer<int*>::type;          // int
using T4 = std::add_const<int>::type;                // const int
using T5 = std::decay<const int&>::type;             // int（去引用+去cv）
using T6 = std::conditional<true, int, double>::type; // int
using T7 = std::enable_if<true, int>::type;          // int

// C++17 简写：_t 后缀
using T8 = std::remove_const_t<const int>;           // 等价于 ::type
using T9 = std::conditional_t<sizeof(int) >= 4, int, long>;
```

## 实际应用

```cpp
// 条件返回类型
template <typename T>
auto safe_divide(T a, T b) -> std::conditional_t<std::is_floating_point_v<T>, T, double> {
    if constexpr (std::is_floating_point_v<T>) {
        return a / b;
    } else {
        return static_cast<double>(a) / b;
    }
}

// SFINAE 约束
template <typename T>
std::enable_if_t<std::is_arithmetic_v<T>> process(T val) {
    // 仅对算术类型启用
}

// 编译期静态断言
template <typename T>
void must_be_integral(T) {
    static_assert(std::is_integral_v<T>, "T must be integral");
}
```

## 自定义 type_trait

```cpp
// 检测类型是否有某个成员函数
template <typename T, typename = void>
struct has_size : std::false_type {};

template <typename T>
struct has_size<T, std::void_t<decltype(std::declval<T>().size())>>
    : std::true_type {};

template <typename T>
inline constexpr bool has_size_v = has_size<T>::value;

static_assert(has_size_v<std::vector<int>>);  // true
static_assert(!has_size_v<int>);              // false
```

## 关键要点

> `std::decay` 是最常用的类型变换——它模拟按值传参时的类型转换（去引用、去cv、数组转指针、函数转函数指针）。

> `std::void_t`（C++17）是 SFINAE 检测的核心工具——任意类型表达式列表的合法性检查。

## 相关模式 / 关联

- [[cpp-sfinae-与编译期多态]] — type_traits 的主要使用场景
- [[cpp-concepts]] — C++20 的更优替代
