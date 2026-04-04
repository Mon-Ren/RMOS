---
title: CRTP 应用场景汇总
tags: [cpp, crtp, static-polymorphism, mixin, compile-time, curiously-recurring]
aliases: [CRTP应用, 静态多态, mixin, 编译时多态, 奇异递归模板]
created: 2026-04-04
updated: 2026-04-04
---

# CRTP 应用场景汇总

CRTP（Curiously Recurring Template Pattern）的四种主要应用——每种解决不同的设计问题。

## 1. 静态多态（替代虚函数）

```cpp
template <typename Derived>
class Shape {
public:
    double area() const {
        return static_cast<const Derived*>(this)->area_impl();
    }
};

class Circle : public Shape<Circle> {
    double radius_;
public:
    double area_impl() const { return 3.14 * radius_ * radius_; }
};

// 调用：编译期绑定，可内联
Circle c{5.0};
Shape<Circle>& s = c;
s.area();  // 直接调用 Circle::area_impl()，无虚函数开销
```

## 2. Mixin 功能注入

```cpp
template <typename Derived>
class Printable {
public:
    void print() const {
        std::cout << static_cast<const Derived*>(this)->to_string() << "\n";
    }
};

template <typename Derived>
class Serializable {
public:
    std::string serialize() const {
        return static_cast<const Derived*>(this)->to_json();
    }
};

class Widget : public Printable<Widget>, public Serializable<Widget> {
public:
    std::string to_string() const { return "Widget{}"; }
    std::string to_json() const { return "{}"; }
};

Widget w;
w.print();     // 自动拥有 Printable 能力
w.serialize(); // 自动拥有 Serializable 能力
```

## 3. 计数器 / 追踪

```cpp
template <typename Derived>
class InstanceCounter {
    static inline int count_ = 0;
public:
    InstanceCounter() { ++count_; }
    InstanceCounter(const InstanceCounter&) { ++count_; }
    ~InstanceCounter() { --count_; }
    static int instance_count() { return count_; }
};

class Widget : public InstanceCounter<Widget> {};
class Gadget : public InstanceCounter<Gadget> {};

// Widget 和 Gadget 各自有独立的计数器
```

## 4. 启用特定操作

```cpp
template <typename Derived>
class EnableShared : public std::enable_shared_from_this<Derived> {
public:
    std::shared_ptr<Derived> shared() {
        return this->shared_from_this();
    }
};

class Node : public EnableShared<Node> {
    // 可以安全获取 shared_ptr<Node>
};
```

## 关键要点

> CRTP 的核心是"派生类把自己作为模板参数传给基类"——基类通过 `static_cast<Derived*>(this)` 调用派生类方法。

> C++23 的 `deducing this` 可以替代部分 CRTP 用法——更简洁，不需要继承。

## 相关模式 / 关联

- [[cpp-crtp-奇异递归模板模式]] — CRTP 基础
- [[cpp-继承与多态]] — 虚函数的对比
