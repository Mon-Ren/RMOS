---
title: 友元模板与 Barton-Nackman 技巧
tags: [cpp, template, friend, barton-nackman, operator, ADL]
aliases: [Barton-Nackman, 友元函数注入, 非成员运算符]
created: 2026-04-05
updated: 2026-04-05
---

# 友元模板与 Barton-Nackman 技巧

**一句话概述：** Barton-Nackman 技巧：在模板类内定义友元函数，利用"注入类名"和 ADL 让运算符在不需要显式声明的情况下被找到。这是模板类定义 `operator==`、`operator<` 等非成员运算符的标准方式。

## 实现

```cpp
template <typename T>
class Rational {
    T num_, den_;
public:
    Rational(T n, T d) : num_(n), den_(d) {}

    // 友元函数定义在类内 → ADL 能找到它
    friend bool operator==(const Rational& a, const Rational& b) {
        return a.num_ * b.den_ == b.num_ * a.den_;
    }

    friend bool operator<(const Rational& a, const Rational& b) {
        return a.num_ * b.den_ < b.num_ * a.den_;
    }

    // 自动从 == 和 < 生成其他运算符（C++20）
    // friend auto operator<=>(const Rational&, const Rational&) = default;
};

// 使用：不需要全局声明
Rational<int> a(1, 2), b(2, 4);
bool eq = (a == b);  // ADL 在 Rational<int> 的关联命名空间中找到 operator==
```

## 关键要点

> 类内定义的友元函数只有通过 ADL 才能被找到——不能通过普通名字查找。`using std::operator==;` 或显式调用 `operator==(a, b)` 可能找不到它。

> C++20 的 `operator<=>` 让比较运算符的定义大幅简化——一个 `<=>` 自动生成所有六种比较运算符。

## 相关模式 / 关联

- [[cpp-ADL参数依赖查找]] — ADL 原理
- [[cpp-运算符重载]] — 运算符重载规则
- [[cpp-模板友元]] — 模板友元声明
- [[cpp-spaceship运算符]] — C++20 <=>
