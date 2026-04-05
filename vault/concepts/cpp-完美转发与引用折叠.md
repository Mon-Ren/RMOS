---
title: 完美转发与引用折叠
tags: [cpp, perfect-forwarding, reference-collapsing, universal-reference, forwarding-reference]
aliases: [完美转发, 引用折叠规则, 万能引用, 转发引用]
created: 2026-04-05
updated: 2026-04-05
---

# 完美转发与引用折叠

**一句话概述：** `T&&` 在模板中不是"右值引用"——它是转发引用，能接受左值也能接受右值，通过引用折叠规则（`T& && → T&`，`T&& && → T&&`）保留原始的值类别，配合 `std::forward` 实现"原样转发"。

## 引用折叠规则

C++ 禁止"引用的引用"（`int& &`），但模板实例化时会产生这种情况。编译器用四条规则消除：

```
T&  &   → T&    （左值引用 + 左值引用 = 左值引用）
T&  &&  → T&    （左值引用 + 右值引用 = 左值引用）
T&& &   → T&    （右值引用 + 左值引用 = 左值引用）
T&& &&  → T&&   （右值引用 + 右值引用 = 右值引用）
```

记忆：**只要有一个左值引用，结果就是左值引用**。只有两个都是右值引用，结果才是右值引用。

## 转发引用 vs 右值引用

```cpp
// 情况 1：右值引用（确定的类型）
void foo(int&& x);          // 只接受右值
void foo(std::string&& s);  // 只接受右值

// 情况 2：转发引用（模板参数 + &&）
template <typename T>
void bar(T&& x);            // T 可以是 int、int&、int&&
                            // x 的类型随传入参数变化

// 区别关键：转发引用必须满足
// 1. 必须是函数模板参数（或类模板的成员函数模板参数）
// 2. 形式必须是 T&&（T 是模板参数）
// 3. T 必须是被推导出来的
```

```cpp
template <typename T>
void f(T&& param);           // ✅ 转发引用

template <typename T>
void g(std::vector<T>&& v);  // ❌ 不是转发引用，是右值引用（&& 在 vector 后面）

template <typename T>
void h(const T&& param);     // ❌ 不是转发引用，有 const 限定

template <typename T>
struct S {
    void m(T&& param);       // ❌ T 在类模板上已经确定，不是推导的
};
```

## 转发引用的推导规则

```cpp
template <typename T>
void f(T&& param);

int x = 42;
f(x);   // T 推导为 int&（传入左值）
        // 引用折叠：int& && → int&
        // param 的类型是 int&

f(42);  // T 推导为 int（传入右值）
        // param 的类型是 int&&

const int cx = 10;
f(cx);  // T 推导为 const int&
        // 引用折叠：const int& && → const int&
        // param 的类型是 const int&

f(std::move(x));  // T 推导为 int
                  // param 的类型是 int&&
```

## std::forward 的实现

```cpp
// std::forward 的本质：有条件地转换为右值引用
template <typename T>
T&& forward(std::remove_reference_t<T>& arg) noexcept {
    return static_cast<T&&>(arg);
}

// 当 T = int&（传入左值时推导出的）
// forward<int&>(arg) → int& && → int&  → 返回左值引用

// 当 T = int（传入右值时推导出的）
// forward<int>(arg)  → int&&         → 返回右值引用
```

## 实战：写一个完美转发的工厂函数

```cpp
#include <memory>
#include <utility>

template <typename T, typename... Args>
std::unique_ptr<T> make(Args&&... args) {
    //                 ^^^^^^^^^^^^
    //                 Args 是参数包，每个元素独立推导
    //                 每个都是转发引用

    return std::unique_ptr<T>(
        new T(std::forward<Args>(args)...)
        //              ^^^^^^^^^^^^^^^^
        //              保持每个参数原始的值类别
        //              左值传入 → 左值转发
        //              右值传入 → 右值转发
    );
}

// 使用
std::string s = "hello";
auto p1 = make<std::string>(s);          // 拷贝构造（s 是左值）
auto p2 = make<std::string>(std::move(s)); // 移动构造（move 后是右值）
auto p3 = make<std::string>("world");    // 移动构造（字面量是右值）
```

## 常见错误

### 错误 1：忘记 std::forward

```cpp
template <typename T>
void wrapper(T&& arg) {
    // ❌ 错误：arg 是左值（有名字的右值引用是左值！）
    target(arg);

    // ✅ 正确：转发值类别
    target(std::forward<T>(arg));
}
```

**为什么有名字的右值引用是左值？**

```cpp
void process(std::string&& s) {
    // s 有名字 → 在函数体内 s 是左值
    // 如果要移动，必须显式 std::move(s)
    // 如果要转发，用 std::forward<std::string&&>(s)
}
```

### 错误 2：对非转发引用用 std::forward

```cpp
void foo(int&& x) {
    std::forward<int&&>(x);  // 可以但不常见，这里 x 明确是右值引用
    std::move(x);            // 更清晰：明确表示"我要移动它"
}
```

**规则：**
- 转发引用（`T&&`）→ 用 `std::forward<T>(arg)`
- 右值引用（`int&&`）→ 用 `std::move(arg)`
- 左值引用（`int&`）→ 不移动也不转发

## 关键要点

> 转发引用只在模板参数推导时出现。`auto&&` 也是转发引用（`auto` 扮演模板参数的角色）。`for (auto&& item : range)` 中的 `auto&&` 能同时正确处理左值和右值范围。

> 引用折叠是 C++ 的"逃生舱"——它让模板能够保留参数的值类别，而不是在传递过程中丢失信息。没有引用折叠，完美转发不可能实现。

> `std::forward` 应该只用在转发引用（`T&&`）上。对普通右值引用用 `std::move`。混淆两者会导致难以追踪的 bug。

## 相关模式 / 关联

- [[cpp-右值引用与移动语义]] — 移动语义基础
- [[cpp-可变参数模板]] — 参数包 + 转发引用
- [[cpp-emplace操作]] — 原地构造中的完美转发
- [[cpp-移动语义与异常安全]] — noexcept 移动
- [[cpp-auto与类型推导]] — auto 推导规则
