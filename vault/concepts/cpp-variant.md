---
title: std::variant（C++17）
tags: [cpp17, variant, union, type-safe, visit, std-visit]
aliases: [variant, 类型安全联合体, tagged union, sum type, visit]
created: 2026-04-04
updated: 2026-04-04
---

# std::variant（C++17）

`variant` 是类型安全的联合体——在编译期确定能持有的类型集合，运行时持有其中之一，访问时类型安全。

## 意图与场景

- 替代 C 风格 union（类型安全）
- 实现可辨识联合体（tagged union）
- AST 节点、状态机状态、配置值等多态场景
- 替代继承层次较浅的多态（variant + visit）

## 基本用法

```cpp
#include <variant>
#include <string>

std::variant<int, double, std::string> val;

val = 42;          // 持有 int
val = 3.14;        // 持有 double
val = "hello";     // 持有 string

// 访问
std::cout << std::get<int>(val);        // 安全访问，类型不对抛异常
std::cout << std::get<0>(val);          // 按索引访问

// 检查
std::holds_alternative<int>(val);       // 是否持有 int
auto* p = std::get_if<int>(&val);       // 安全获取指针，类型不对返回 nullptr
if (p) std::cout << *p;

// 当前索引
val.index();  // 0=int, 1=double, 2=string
```

## visit

```cpp
// visit：对 variant 的值调用对应的重载
std::variant<int, double, std::string> val = 42;

// 方式一：重载 lambda
auto visitor = overloaded {
    [](int i) { std::cout << "int: " << i; },
    [](double d) { std::cout << "double: " << d; },
    [](const std::string& s) { std::cout << "string: " << s; },
};
std::visit(visitor, val);

// 辅助模板（需要自己定义或用 Boost）
template <typename... Ts> struct overloaded : Ts... { using Ts::operator()...; };
template <typename... Ts> overloaded(Ts...) -> overloaded<Ts...>;

// C++20 简化：可以用 lambda + 模板参数
auto visitor2 = []<typename T>(const T& val) {
    if constexpr (std::is_same_v<T, int>) { /* ... */ }
    else if constexpr (std::is_same_v<T, double>) { /* ... */ }
    else { /* string */ }
};
```

## 实际应用

```cpp
// JSON 值表示
using JsonValue = std::variant<
    std::nullptr_t,
    bool,
    double,
    std::string,
    std::vector<JsonValue>,     // 递归需要 std::vector<variant<...>>
    std::map<std::string, JsonValue>
>;

// 状态机
struct Idle {};
struct Running { int progress; };
struct Done { std::string result; };
struct Failed { std::string error; };

using State = std::variant<Idle, Running, Done, Failed>;

State handle_event(const State& current, const Event& event) {
    return std::visit(overloaded {
        [](const Idle&, const StartEvent&) { return State{Running{0}}; },
        [](const Running& r, const ProgressEvent& p) {
            return State{Running{r.progress + p.delta}};
        },
        // ...
    }, current, event);
}
```

## 关键要点

> `variant` 不允许持有引用类型和数组。第一个类型必须可默认构造（`std::monostate` 可用作占位）。

> `variant` 在栈上分配，大小等于最大类型的大小加上标签开销——比继承层次的虚函数表更快。

## 相关模式 / 关联

- [[cpp-optional]] — 可选值
- [[设计模式-访问者模式]] — visit 是访问者的函数式实现
