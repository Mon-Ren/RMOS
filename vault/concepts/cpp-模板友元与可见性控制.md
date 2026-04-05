---
title: 模板友元与可见性控制
tags: [cpp, template, friend, visibility, access-control]
aliases: [模板友元声明, 类模板友元, 访问控制]
created: 2026-04-05
updated: 2026-04-05
---

# 模板友元与可见性控制

**一句话概述：** 模板类的友元声明有三种形式——友元函数模板、友元类模板、特定实例化的友元。选错形式会导致编译错误或意外的访问权限。

## 三种友元形式

```cpp
template <typename T> class Widget;

// 形式 1：所有 T 的 Widget<T> 都互为友元
template <typename T>
class Container {
    template <typename U>
    friend class Widget;  // Widget<int> 能访问 Container<double> 的私有成员
};

// 形式 2：同类型 T 的友元
template <typename T>
class Container {
    friend class Widget<T>;  // Widget<int> 只能访问 Container<int>
};

// 形式 3：非模板友元
class Helper {
    // ...
};
template <typename T>
class Container {
    friend class Helper;  // Helper 能访问所有 Container<T>
};
```

## 关键要点

> 形式 2（`friend class Widget<T>`）是最常用且最安全的——同类型配对，不会意外暴露给其他类型实例。形式 1 过于宽松，只在极少数场景需要。

## 相关模式 / 关联

- [[cpp-友元与静态成员]] — 友元基础
- [[cpp-模板编程基础]] — 模板基础
- [[cpp-友元模板与Barton-Nackman]] — Barton-Nackman
