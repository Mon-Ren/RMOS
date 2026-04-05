---
title: TMP 编译期状态机
tags: [cpp, template, metaprogramming, state-machine, compile-time]
aliases: [编译期状态机, 模板状态机, 编译期自动机]
created: 2026-04-05
updated: 2026-04-05
---

# TMP 编译期状态机

**一句话概述：** 用模板特化在编译期定义状态和转移规则，编译器在编译时验证状态转移的合法性。非法的状态转移直接编译错误——把运行时的状态机 bug 消灭在编译阶段。

## 实现

```cpp
// 状态定义
struct Closed {};
struct Listening {};
struct Connected {};
struct Error {};

// 事件定义
struct Open {};
struct Accept {};
struct Close {};
struct Data {};

// 转移规则：当前状态 × 事件 → 新状态
template <typename State, typename Event>
struct Transition;  // 未定义 = 不允许的转移

// 合法转移
template <> struct Transition<Closed, Open>     { using type = Listening; };
template <> struct Transition<Listening, Accept>{ using type = Connected; };
template <> struct Transition<Connected, Data>  { using type = Connected; };
template <> struct Transition<Connected, Close> { using type = Closed; };
template <> struct Transition<Connected, Open>  { using type = Error; };

// 状态机
template <typename State>
class Machine {
public:
    template <typename Event>
    auto on(Event) {
        using NewState = typename Transition<State, Event>::type;
        return Machine<NewState>{};
    }
};

// 使用
auto m = Machine<Closed>{};
auto m2 = m.on(Open{});      // Closed → Listening ✅
auto m3 = m2.on(Accept{});   // Listening → Connected ✅
auto m4 = m3.on(Close{});    // Connected → Closed ✅
// auto bad = m.on(Accept{}); // Closed → Accept → 编译错误！（未定义 Transition）
```

## 关键要点

> 编译期状态机的价值在于**非法转移的编译期捕获**。在协议实现中，比如 TCP 状态机，不可能的转移直接报错。

> 局限性：状态数多时编译时间增长。更适合状态数有限（< 20）的协议。

## 相关模式 / 关联

- [[cpp-模板元编程]] — TMP 基础
- [[cpp-设计模式-状态模式]] — 运行时状态机
- [[cpp-编译期校验与static_assert]] — 编译期断言
