---
title: 运算符重载
tags: [cpp, oop, operator-overloading, overload]
aliases: [运算符重载, 操作符重载, operator overload]
created: 2026-04-04
updated: 2026-04-04
---

# 运算符重载

运算符重载让自定义类型能像内置类型一样使用运算符——好的重载让代码直观，坏的重载让代码变成天书。

## 意图与场景

- 让自定义数值类型支持 `+` `-` `*` `/`
- 实现比较运算符用于排序和容器
- 重载 `<<` 用于流输出
- 重载 `[]` 用于容器下标访问

## 通用规则

```cpp
// 1. 不能创造新运算符，只能重载已有的
// 2. 不能改变运算符的优先级和结合性
// 3. 不能改变运算符的操作数个数
// 4. 不能重载 ::  .  .*  ?:
// 5. 重载应该保持直觉语义
```

## 成员函数 vs 非成员函数

```cpp
class Vec2 {
    double x_, y_;
public:
    Vec2(double x, double y) : x_(x), y_(y) {}

    // 成员函数：左操作数是 *this
    Vec2 operator+(const Vec2& rhs) const {
        return {x_ + rhs.x_, y_ + rhs.y_};
    }

    Vec2& operator+=(const Vec2& rhs) {
        x_ += rhs.x_;
        y_ += rhs.y_;
        return *this;
    }

    // 下标运算符
    double& operator[](size_t i) { return (i == 0) ? x_ : y_; }
    const double& operator[](size_t i) const { return (i == 0) ? x_ : y_; }

    // 非成员友元：支持左操作数不是 this 的情况
    friend Vec2 operator*(double s, const Vec2& v) {
        return {s * v.x_, s * v.y_};
    }
    friend std::ostream& operator<<(std::ostream& os, const Vec2& v) {
        return os << "(" << v.x_ << ", " << v.y_ << ")";
    }
};

// 非成员版本支持对称性：
Vec2 v{1, 2};
auto a = v + Vec2{3, 4};   // 成员函数 OK
auto b = 2.0 * v;          // 非成员友元 OK
// auto c = v * 2.0;       // 如果只定义了 double * Vec2，这行不编译
```

## 比较运算符（C++20）

```cpp
// C++20：spaceship operator 自动生成所有比较
#include <compare>

class Point {
    int x_, y_;
public:
    auto operator<=>(const Point&) const = default;
    // 自动生成 ==, !=, <, <=, >, >=（按成员字典序比较）
};

// C++20 之前：
bool operator==(const Point& lhs, const Point& rhs) {
    return lhs.x_ == rhs.x_ && lhs.y_ == rhs.y_;
}
bool operator!=(const Point& lhs, const Point& rhs) {
    return !(lhs == rhs);  // 用 == 实现 !=
}
```

## 常见陷阱

```cpp
// 陷阱1：赋值运算符返回 *this 以支持链式调用
Widget& operator=(const Widget& other) {
    // ...
    return *this;  // 不是返回 void
}

// 陷阱2：后置 ++ 应返回旧值
class Counter {
    int n_;
public:
    Counter& operator++()     { ++n_; return *this; }      // 前置
    Counter  operator++(int)  { auto old = *this; ++n_; return old; }  // 后置
};

// 陷阱3：不要重载 && || ，会失去短路求值语义
// 陷阱4：operator== 和 operator!= 应该一致
// 陷阱5：如果定义了 <，也应该定义 ==（C++20 前）
```

## 关键要点

> 运算符重载的黄金法则：保持直觉语义。`+` 应该做加法相关的事，不应该做文件操作。如果语义不明确，用命名函数代替。

> 二元算术运算符通常实现为非成员函数以支持对称性，复合赋值运算符实现为成员函数。

## 相关模式 / 关联

- [[cpp-类与对象]] — 特殊成员函数
- [[cpp-流与IO]] — `operator<<` 和 `operator>>` 的使用
