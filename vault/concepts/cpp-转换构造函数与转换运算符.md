---
title: 转换构造函数与转换运算符
tags: [cpp, oop, conversion, explicit, operator-type]
aliases: [转换构造函数, 转换运算符, explicit, 隐式转换, 用户定义转换]
created: 2026-04-04
updated: 2026-04-04
---

# 转换构造函数与转换运算符

用户定义的类型转换——可以让自定义类型和其它类型之间自然转换，也可能制造隐蔽的 bug。

## 意图与场景

- 让类型从其他类型自然构造（如 string 从 const char*）
- 让类型可以转换为其他类型（如智能指针转 bool）
- 精确控制隐式转换的行为

## 转换构造函数

```cpp
class Rational {
    int num_, den_;
public:
    // 转换构造函数：可以从 int 构造
    Rational(int num, int den = 1) : num_(num), den_(den) {}

    // ⚠️ 允许隐式转换：
    Rational r = 42;          // OK：Rational(42, 1)
    void foo(Rational r);
    foo(10);                   // OK：隐式构造 Rational(10)
};

// explicit：禁止隐式转换
class SafeRational {
public:
    explicit SafeRational(int num, int den = 1) : num_(num), den_(den) {}
};

SafeRational r1(42);          // OK：直接初始化
// SafeRational r2 = 42;      // 编译错误：不允许隐式转换
// foo(10);                    // 编译错误
foo(SafeRational(10));        // OK：显式构造
```

## 转换运算符

```cpp
class SmartPtr {
    Widget* ptr_;
public:
    // 转换为 bool
    explicit operator bool() const { return ptr_ != nullptr; }
    // 用 explicit 避免意外转换到 int 等

    // 使用
    SmartPtr p(new Widget);
    if (p) { }           // OK：bool 上下文（if/while/for 条件）
    // int n = p;         // 编译错误：explicit 阻止隐式转换
};

// C++11 之前的经典问题：
class OldBool {
    int val_;
public:
    operator bool() const { return val_ != 0; }  // 非 explicit
    // 危险！
    // if (a < b < c)   ← bool 和 int 混用
    // int n = a + b    ← bool 隐式转 int
};

// C++11: explicit 转换运算符 + bool 上下文特殊规则
```

## 关键要点

> 单参数构造函数默认是隐式转换构造函数——可能带来意外的隐式转换。除非明确需要隐式转换，否则标记 `explicit`。

> 转换运算符同理——`operator bool()` 应标记 `explicit`，否则会隐式转换到整数类型。

## 相关模式 / 关联

- [[cpp-运算符重载]] — 运算符重载基础
- [[cpp-类型转换]] — 四种命名转换
