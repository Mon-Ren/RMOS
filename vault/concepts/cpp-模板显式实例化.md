---
title: C++ 模板的导出与显式实例化
tags: [cpp, template, explicit-instantiation, extern-template, export]
aliases: [显式实例化, extern template, 模板导出, 模板实例化控制]
created: 2026-04-04
updated: 2026-04-04
---

# 模板的显式实例化与 extern template

控制模板在何处实例化——避免每个编译单元重复实例化相同类型。

## 显式实例化

```cpp
// widget.cpp：显式实例化常用类型
template class std::vector<int>;
template class std::vector<std::string>;
template class std::map<std::string, int>;

// 告诉编译器：在这里生成这些类型的代码
// 其他编译单元可以用 extern template 避免重复生成
```

## extern template（C++11）

```cpp
// header.h
template <typename T>
class Widget { /* ... */ };

// main.cpp
#include "header.h"
extern template class Widget<int>;  // 不实例化，使用别处的定义

Widget<int> w;  // 链接时使用 widget.cpp 中的实例
```

## 函数模板的显式实例化

```cpp
// 显式实例化定义
template int add<int>(int, int);  // 在此编译单元生成 add<int>
template double add<double>(double, double);

// extern 声明
extern template int add<int>(int, int);  // 不在此生成
```

## 关键要点

> 显式实例化把模板实例化集中到一个编译单元——避免重复实例化、减少编译时间、减小二进制体积。

> `extern template` 是"不要再实例化这个"的声明——链接器会使用其他编译单元中的实例。

## 相关模式 / 关联

- [[cpp-编译时间优化]] — 编译加速
- [[cpp-模板编程基础]] — 模板基础
