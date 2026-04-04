---
title: SFINAE 与编译期多态
tags: [cpp, idiom, SFINAE, template, metaprogramming]
aliases: [SFINAE, Substitution Failure Is Not An Error, 编译期多态, enable_if, type_traits]
created: 2026-04-04
updated: 2026-04-04
---

# SFINAE 与编译期多态

**一句话概述：** 模板参数替换失败不是错误——利用这一规则在编译时根据类型特征选择不同的重载或特化，实现编译期多态。

## 意图与场景

SFINAE（Substitution Failure Is Not An Error）是 C++ 模板元编程的基石：

- **重载决议中的候选过滤**：替换失败的模板从候选集中静默移除
- **类型特征检测**：编译时判断类型是否具有某种特性
- **条件编译**：根据类型能力选择不同实现

**适用场景：**
- 函数模板根据参数类型选择不同实现
- 类型安全的编译期分支
- 约束模板参数（C++20 Concepts 的前身）
- 库开发中的通用工具函数

## C++ 实现代码

### std::enable_if 约束模板

```cpp
#include <type_traits>
#include <iostream>
#include <string>
#include <vector>

// 只接受整数类型
template <typename T>
std::enable_if_t<std::is_integral_v<T>, T>
safe_divide(T a, T b) {
    if (b == 0) throw std::invalid_argument("Division by zero");
    return a / b;
}

// 只接受浮点类型
template <typename T>
std::enable_if_t<std::is_floating_point_v<T>, T>
safe_divide(T a, T b) {
    if (std::abs(b) < 1e-10) throw std::invalid_argument("Near-zero division");
    return a / b;
}

// 使用
void demo() {
    auto x = safe_divide(10, 3);      // 整数版本
    auto y = safe_divide(10.0, 3.0);  // 浮点版本
    // safe_divide("a", "b");          // 编译错误：无匹配重载
}
```

### 类型特征检测

```cpp
#include <type_traits>

// 检测类型是否有 size() 方法
template <typename T, typename = void>
struct has_size : std::false_type {};

template <typename T>
struct has_size<T, std::void_t<decltype(std::declval<T>().size())>> 
    : std::true_type {};

template <typename T>
inline constexpr bool has_size_v = has_size<T>::value;

// 根据类型能力选择实现
template <typename T>
auto get_size(const T& container) {
    if constexpr (has_size_v<T>) {
        return container.size();
    } else {
        return std::distance(std::begin(container), std::end(container));
    }
}
```

### C++17 if constexpr 替代 SFINAE

```cpp
#include <type_traits>
#include <string>
#include <concepts>

// C++17: if constexpr 替代 SFINAE 分支
template <typename T>
std::string to_debug_string(const T& value) {
    if constexpr (std::is_same_v<T, std::string>) {
        return "\"" + value + "\"";
    } else if constexpr (std::is_integral_v<T>) {
        return std::to_string(value) + " (int)";
    } else if constexpr (std::is_pointer_v<T>) {
        return "ptr: " + to_debug_string(*value);
    } else {
        return "<unknown>";
    }
}

// C++20: Concepts 版本（更清晰）
template <std::integral T>
T gcd(T a, T b) {
    while (b) { a %= b; std::swap(a, b); }
    return a;
}

template <std::floating_point T>
T safe_sqrt(T x) {
    if (x < 0) throw std::domain_error("Negative sqrt");
    return std::sqrt(x);
}
```

### 编译时特性检测

```cpp
#include <type_traits>

// 检测是否可默认构造
template <typename T, typename = void>
struct is_default_constructible : std::false_type {};

template <typename T>
struct is_default_constructible<T, std::void_t<decltype(T())>> 
    : std::true_type {};

// 检测是否有特定成员函数
template <typename T, typename = void>
struct has_serialize : std::false_type {};

template <typename T>
struct has_serialize<T, std::void_t<decltype(std::declval<T>().serialize())>> 
    : std::true_type {};

// 使用
template <typename T>
void process(const T& obj) {
    if constexpr (has_serialize<T>::value) {
        auto data = obj.serialize();
        // 发送数据...
    } else {
        static_assert(has_serialize<T>::value, 
                      "T must have a serialize() method");
    }
}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 编译时多态，零运行时开销 | 错误信息极其冗长和晦涩 |
| 类型安全（vs 宏条件编译） | 学习曲线陡峭 |
| 可对任意类型操作 | C++17 之前写法繁琐 |
| if constexpr 大幅简化代码 | 编译时间增加 |

> [!tip] 关键要点
> **C++17 之后优先使用 `if constexpr`**，替代 `enable_if` SFINAE 技巧——代码更清晰，错误信息更友好。**C++20 进一步用 Concepts 替代**，使意图表达更直接。SFINAE 仍然重要，因为理解它才能理解标准库的约束机制和旧代码。

> [!info] SFINAE 演进路线
> C++11: `std::enable_if` + `void_t` → C++17: `if constexpr` + `type_traits` → C++20: `concepts` + `requires`。每一步都在让编译期编程更易读、更安全。

## 相关链接

- [[cpp-crtp-奇异递归模板模式]] — 另一种编译时多态技术
- [[cpp-策略设计]] — SFINAE 约束策略模板
- [[cpp-标签分发]] — SFINAE 的补充：利用重载决议分支
