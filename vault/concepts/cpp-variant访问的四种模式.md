---
title: variant 访问的四种模式
tags: [cpp17, variant, visit, pattern-matching, overload-set]
aliases: [variant 访问, std::visit 用法, 模式匹配模拟]
created: 2026-04-05
updated: 2026-04-05
---

# variant 访问的四种模式

**一句话概述：** `std::variant` 是类型安全的 union，但它没有 `.get<T>()` 的直接方式——`std::visit` 是主要的访问手段。四种模式从简单到优雅：裸 lambda、overload set、`if constexpr`、C++26 pattern matching。

## 模式 1：直接 visit + 单一 lambda

```cpp
#include <variant>
#include <string>
#include <iostream>

using Value = std::variant<int, double, std::string>;

// visit 接受一个能处理所有类型的 callable
Value v = 42;
std::visit([](auto&& val) {
    std::cout << val << "\n";  // int 42
}, v);
```

`auto&&` 是关键——lambda 的参数是泛型的，编译器为 variant 的每种类型都实例化一次。问题是：**所有分支的代码必须对所有类型都合法**。

```cpp
// ❌ 编译错误：std::string 没有 + int 操作
std::visit([](auto&& val) {
    std::cout << val + 1 << "\n";
}, v);  // v 可能是 std::string，val + 1 不合法
```

## 模式 2：Overload Set（推荐）

```cpp
// 辅助模板：组合多个 lambda 为 overload set
template <typename... Ts>
struct overloaded : Ts... { using Ts::operator()...; };
template <typename... Ts>
overloaded(Ts...) -> overloaded<Ts...>;  // C++17 推导指引

// 使用
std::visit(overloaded{
    [](int i)           { std::cout << "int: " << i << "\n"; },
    [](double d)        { std::cout << "double: " << d << "\n"; },
    [](const std::string& s) { std::cout << "string: " << s << "\n"; }
}, v);
```

**优点：** 每个分支只对对应的类型实例化，代码清晰，编译器能检查是否遗漏类型。`overloaded` 已经被提议进 C++ 标准库（P2891），但目前需要自己定义或用 Boost.Variant2 的版本。

## 模式 3：if constexpr + holds_alternative

```cpp
template <typename V>
void handle(V&& variant) {
    using T = std::decay_t<V>;

    if constexpr (std::is_same_v<T, int>) {
        std::cout << "处理整数: " << std::get<int>(variant) << "\n";
    } else if constexpr (std::is_same_v<T, double>) {
        std::cout << "处理浮点: " << std::get<double>(variant) << "\n";
    } else if constexpr (std::is_same_v<T, std::string>) {
        std::cout << "处理字符串: " << std::get<std::string>(variant) << "\n";
    }
}

// 或者在 visit 内用 if constexpr
std::visit([](auto&& val) {
    using T = std::decay_t<decltype(val)>;
    if constexpr (std::is_same_v<T, int>) {
        // 只对 int 类型编译这段代码
    }
}, v);
```

## 模式 4：C++26 Pattern Matching（未来）

```cpp
// P2688 提案语法（尚未标准化）
void handle(auto&& v) {
    inspect (v) {
        <int i> => std::cout << "int: " << i;
        <double d> => std::cout << "double: " << d;
        <std::string s> => std::cout << "string: " << s;
        __ => std::cout << "unknown";  // 兜底
    };
}
```

当前可用的近似方案：**用 `overloaded` + 带状态的 lambda** 模拟模式匹配：

```cpp
struct ProcessVisitor {
    int& total;

    void operator()(int i) {
        total += i;
    }
    void operator()(double d) {
        total += static_cast<int>(d);
    }
    void operator()(const std::string&) {
        // 字符串不计入总和
    }
};

int total = 0;
std::visit(ProcessVisitor{total}, v);
```

## 处理 variant 的"无值"状态

`std::variant` 在异常时可能进入 valueless_by_exception 状态：

```cpp
std::visit(overloaded{
    [](int i) { /*...*/ },
    [](const std::string& s) { /*...*/ },
    [](std::monostate) { /* 空状态 */ }
}, v);

// 检查
if (v.valueless_by_exception()) {
    // variant 处于无效状态（构造期间抛异常）
}

// std::monostate 作为第一个类型可以支持默认构造
using SafeVariant = std::variant<std::monostate, int, std::string>;
SafeVariant sv;  // 默认构造为 monostate
```

## visit 的性能

`std::visit` 的实现通常用跳转表（jump table）——O(1) 的索引分发，和虚函数调用一样快。编译器通常能内联整个 visit 调用。

```
visit 内部大致等价于：

switch (v.index()) {
    case 0: return callable(std::get<0>(v));
    case 1: return callable(std::get<1>(v));
    case 2: return callable(std::get<2>(v));
    // ...
}
```

## 关键要点

> `overloaded` 模式是最推荐的写法——编译器会检查是否覆盖了所有类型，漏掉一个就编译错误。这比 switch-case 安全得多。

> `std::variant` 的类型顺序有语义——同类型出现在不同位置算不同类型。`std::variant<int, int>` 是合法的（虽然不常见），`std::get<0>` 和 `std::get<1>` 区分它们。

> variant 替代继承体系（variant vs polymorphism）的决策点：variant 适合类型集合固定、性能敏感的场景（避免虚调用开销）；继承适合类型可扩展、运行时注册的场景。

## 相关模式 / 关联

- [[cpp-variant]] — variant 基础用法
- [[cpp-any与variant对比]] — variant vs any 选型
- [[cpp-optional]] — 可选值，variant 的特例
- [[cpp-访问者模式]] — visit 是访问者模式的 C++17 实现
- [[cpp-函数式编程模式]] — variant + visit 的函数式风格
