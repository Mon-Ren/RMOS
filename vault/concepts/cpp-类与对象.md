---
title: 面向对象基础——类与对象
tags: [cpp, oop, class, object, constructor, destructor]
aliases: [类, 对象, 构造函数, 析构函数, 特殊成员函数]
created: 2026-04-04
updated: 2026-04-04
---

# 面向对象基础——类与对象

类是 C++ 用户自定义类型的机制，构造函数控制初始化，析构函数控制清理——两者共同定义了对象的生命周期。

## 意图与场景

- 封装数据与行为，建立不变量
- 精确控制对象的创建、复制、移动和销毁
- 实现 RAII——C++ 资源管理的基石

## 特殊成员函数

C++ 有 6 个特殊成员函数，编译器可能自动生成：

```cpp
class Widget {
public:
    Widget();                              // 默认构造
    Widget(const Widget&);                 // 拷贝构造
    Widget& operator=(const Widget&);      // 拷贝赋值
    Widget(Widget&&);                      // 移动构造 (C++11)
    Widget& operator=(Widget&&);           // 移动赋值 (C++11)
    ~Widget();                             // 析构
};
```

### 编译器生成规则

```cpp
// 如果你没有声明：
// - 没有拷贝操作 → 编译器生成（逐成员拷贝）
// - 没有移动操作 → 如果没有用户声明的析构/拷贝，编译器生成
// - 没有析构 → 编译器生成（默认 public）

// 声明了任何一个 → 抑制其他自动生成（部分）
// 声明了移动操作 → 抑制拷贝操作的隐式生成
// 声明了析构 → 不抑制移动操作的生成（C++11 修正）

// =default 和 =delete 可以精确控制
class RuleOfFive {
public:
    RuleOfFive() = default;
    RuleOfFive(const RuleOfFive&) = default;
    RuleOfFive& operator=(const RuleOfFive&) = default;
    RuleOfFive(RuleOfFive&&) = default;
    RuleOfFive& operator=(RuleOfFive&&) = default;
    ~RuleOfFive() = default;
};
```

## 构造函数技巧

```cpp
class Config {
    int timeout_;
    std::string host_;
    int port_;
public:
    // 委托构造函数（C++11）
    Config() : Config(30, "localhost", 8080) {}
    Config(int t, const std::string& h, int p)
        : timeout_(t), host_(h), port_(p) {}

    // 列表初始化（C++11）——防止窄化
    // Config c{3.14};  // 编译错误：double 到 int 窄化

    // explicit 防止隐式转换
    explicit Config(int timeout) : timeout_(timeout), host_("localhost"), port_(8080) {}
    // Config c = 30;  // 编译错误：explicit 阻止隐式转换
    Config c(30);      // OK：直接初始化
};
```

## 初始化列表

```cpp
class Rectangle {
    int width_, height_;
public:
    // 成员初始化列表：在构造函数体执行前初始化
    Rectangle(int w, int h) : width_(w), height_(h) {
        // 此时成员已经初始化完毕
        // 这里是赋值，不是初始化
    }
};

// 初始化顺序由声明顺序决定，与初始化列表顺序无关
class Foo {
    int a_;
    int b_;
public:
    // 警告：b_ 先于 a_ 声明，但这里 a_ 写在前面
    Foo(int x) : b_(x), a_(b_) { }  // UB！a_ 用未初始化的 b_ 初始化
};
```

## 关键要点

> 遵循 Rule of Zero：如果能用标准库 RAII 类型管理资源，就不要自定义特殊成员函数。需要自定义时遵循 Rule of Five。

> 成员初始化列表的顺序由成员声明顺序决定，务必保持一致。

## 相关模式 / 关联

- [[cpp-raii-惯用法]] — 构造/析构的核心应用
- [[cpp-右值引用与移动语义]] — 移动构造/赋值
