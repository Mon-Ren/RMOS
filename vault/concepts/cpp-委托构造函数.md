---
title: C++ 委托构造函数
tags: [cpp, delegating-constructor, constructor-chaining, cpp11]
aliases: [委托构造函数, 构造函数链, constructor chaining, 委托构造]
created: 2026-04-04
updated: 2026-04-04
---

# 委托构造函数（C++11）

委托构造函数让一个构造函数调用同一类的另一个构造函数——消除构造函数之间的重复代码。

## 基本用法

```cpp
class Connection {
    std::string host_;
    int port_;
    int timeout_;
public:
    // 主构造函数
    Connection(const std::string& host, int port, int timeout)
        : host_(host), port_(port), timeout_(timeout) {
        validate();
    }

    // 委托构造函数
    Connection() : Connection("localhost", 8080, 30) {}
    Connection(const std::string& host) : Connection(host, 8080, 30) {}
    Connection(const std::string& host, int port) : Connection(host, port, 30) {}
};
```

## 与默认参数的对比

```cpp
// 用默认参数（简洁但有限）
class Widget {
    int x_, y_;
public:
    Widget(int x = 0, int y = 0) : x_(x), y_(y) {}
};

// 用委托构造（更灵活）
class Widget {
    int x_, y_;
public:
    Widget(int x, int y) : x_(x), y_(y) { validate(); }
    Widget() : Widget(0, 0) {}
    Widget(int x) : Widget(x, x) {}  // 正方形——默认参数做不到
};
```

## 注意事项

```cpp
// ⚠️ 委托构造中不能用成员初始化列表
class Bad {
    int x_;
public:
    Bad() : Bad(0) {}
    Bad(int v) : Bad(), x_(v) {}  // 编译错误：不能同时委托和初始化成员
};

// ⚠️ 循环委托会导致运行时错误
class Bad2 {
public:
    Bad2() : Bad2(0) {}     // 委托给 Bad2(int)
    Bad2(int) : Bad2() {}   // 委托给 Bad2() → 循环！
};
```

## 关键要点

> 委托构造让多个构造函数共享初始化逻辑——代码更 DRY，维护更简单。

> 委托构造和成员初始化不能混用——要么委托，要么直接初始化成员。

## 相关模式 / 关联

- [[cpp-类与对象]] — 构造函数基础
- [[cpp-异常与构造函数]] — 构造函数中的异常
