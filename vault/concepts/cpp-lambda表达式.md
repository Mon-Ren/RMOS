---
title: Lambda 表达式
tags: [cpp, lambda, closure, functional, cpp11]
aliases: [lambda, 闭包, 匿名函数, closure]
created: 2026-04-04
updated: 2026-04-04
---

# Lambda 表达式

Lambda 是一个编译器为你生成的匿名函数对象（闭包类），捕获列表就是它的构造函数参数。

## 意图与场景

- 作为回调传递给算法（`std::sort`, `std::find_if`）
- 替代简单的函数对象（functor）
- 异步任务、事件处理中定义内联逻辑
- 需要捕获局部变量的场景

## 语法结构

```cpp
[捕获列表](参数列表) mutable(可选) noexcept(可选) -> 返回类型 { 函数体 }
```

### 捕获方式

```cpp
int x = 10, y = 20;

auto l1 = []()      { /* 不捕获任何外部变量 */ };
auto l2 = [x]()     { return x; };        // 按值捕获 x（拷贝）
auto l3 = [&x]()    { x = 100; };         // 按引用捕获 x
auto l4 = [=]()     { return x + y; };    // 按值捕获所有使用的变量
auto l5 = [&]()     { x = 1; y = 2; };    // 按引用捕获所有使用的变量
auto l6 = [x, &y]() { return x + y; };    // 混合捕获

// C++14：初始化捕获（广义 lambda 捕获）
auto l7 = [ptr = std::make_unique<int>(42)]() { return *ptr; };
auto l8 = [ref = std::as_const(x)]() { return ref; };  // C++17
```

### mutable 与 const

```cpp
// 默认情况下 operator() 是 const 的——按值捕获的变量不可修改
int x = 10;
auto l = [x]() mutable { x++; return x; };  // 需要 mutable 才能修改捕获的拷贝
l();  // 返回 11，但外部 x 仍为 10

// 按引用捕获不需要 mutable 即可修改
auto l2 = [&x]() { x++; };  // OK，修改外部 x
```

## 泛型 Lambda（C++14）

```cpp
// auto 参数 → 编译器生成模板 operator()
auto print = [](const auto& item) {
    std::cout << item << "\n";
};

print(42);           // operator()<int>
print("hello");      // operator()<const char*>

// C++14：auto 用于参数
auto add = [](auto a, auto b) { return a + b; };
add(1, 2);           // int
add(1.0, 2.0);       // double
```

## Lambda 与 std::function

```cpp
#include <functional>

// Lambda 可以存储到 std::function 中（有类型擦除开销）
std::function<int(int, int)> op = [](int a, int b) { return a + b; };

// 但如果类型已知，直接用 auto 保存 lambda 避免开销
auto op2 = [](int a, int b) { return a + b; };  // 没有类型擦除
```

## 递归 Lambda（C++14+）

```cpp
// 通过 std::function 实现递归
std::function<int(int)> fib = [&fib](int n) -> int {
    return (n <= 1) ? n : fib(n - 1) + fib(n - 2);
};

// 更高效：使用 auto + 传参实现自递归
auto fib2 = [](auto self, int n) -> int {
    return (n <= 1) ? n : self(self, n - 1) + self(self, n - 2);
};
int result = fib2(fib2, 10);
```

## 关键要点

> Lambda 是编译器生成的函数对象，捕获列表决定了闭包类的成员变量。按值捕获产生拷贝，按引用捕获产生引用成员——注意悬垂引用。

> 捕获 `this` 指针时（`[this]` 或 `[=]`），lambda 持有的是裸指针，对象销毁后调用会导致 UB。C++17 的 `[*this]` 可以按值捕获整个对象。

## 相关模式 / 关联

- [[cpp-函数式编程模式]] — Lambda 在函数式风格中的应用
- [[设计模式-策略模式]] — Lambda 替代策略类
