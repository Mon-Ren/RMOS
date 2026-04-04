---
title: const 与 constexpr
tags: [cpp, fundamentals, const, constexpr, compile-time]
aliases: [常量, 编译期常量, const正确性, constexpr函数]
created: 2026-04-04
updated: 2026-04-04
---

# const 与 constexpr

`const` 承诺"不修改"，`constexpr` 承诺"编译期可知"——两者语义不同，用途不同。

## 意图与场景

- `const`：运行时常量，保护数据不被意外修改
- `constexpr`：编译期常量，启用编译期计算和模板参数
- `consteval`（C++20）：强制编译期求值

## const：运行时不变性

```cpp
const int x = 42;           // 初始化后不可修改
const int* p = &x;          // 指向 const int 的指针（指针本身可变）
int* const q = &someInt;    // const 指针（指向的内容可变）
const int* const r = &x;    // 指针和内容都不可变

// const 成员函数：承诺不修改对象状态
class Widget {
    int value_;
public:
    int getValue() const { return value_; }  // 不能修改 value_
    // void set(int v) const { value_ = v; } // 编译错误
};

// mutable：在 const 成员函数中仍可修改
class Cache {
    mutable int cachedResult_;
    mutable bool cacheValid_;
public:
    int compute() const {  // const 函数
        if (!cacheValid_) {
            cachedResult_ = expensiveCalc();  // mutable 允许修改
            cacheValid_ = true;
        }
        return cachedResult_;
    }
};
```

## constexpr：编译期求值

```cpp
// constexpr 变量隐含 const
constexpr int maxSize = 1024;

// constexpr 函数：参数合适时编译期求值
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

constexpr int fact5 = factorial(5);  // 编译期计算，值 120

int runtime_val = 10;
int runtime_result = factorial(runtime_val);  // 运行时也可以调用

// constexpr if（C++17）：编译期分支
template <typename T>
auto get_value(const T& t) {
    if constexpr (std::is_pointer_v<T>) {
        return *t;           // T 是指针时编译这段
    } else {
        return t;            // T 不是指针时编译这段
    }
}
```

## consteval（C++20）

```cpp
// consteval：必须在编译期求值，否则报错
consteval int compile_time_only(int n) {
    return n * n;
}

constexpr int a = compile_time_only(5);  // OK，编译期

int x = 10;
// int b = compile_time_only(x);  // 编译错误！x 不是常量表达式
```

## const 与指针的组合

```cpp
// 从右往左读：
const int*       p1;  // pointer to const int（内容不可通过 p1 修改）
int const*       p2;  // 同上（const 在 * 左边，两种写法等价）
int* const       p3;  // const pointer to int（指针本身不可变）
const int* const p4;  // const pointer to const int

// 顶层 const vs 底层 const
// 顶层 const：指针本身是 const（p3, p4）
// 底层 const：指向的内容是 const（p1, p2, p4）
```

## 关键要点

> `const` 是运行时承诺——"我不会修改这个"；`constexpr` 是编译期能力——"这个值可以在编译时确定"。

> `constexpr` 函数并非"只能编译期调用"，它在运行时也可用，只是参数为常量表达式时会被编译器求值。

## 相关模式 / 关联

- [[cpp-模板元编程]] — constexpr 在模板中的威力
- [[cpp-auto-与类型推导]] — auto 与 const 的交互
