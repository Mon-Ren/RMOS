---
title: 编译时间优化
tags: [cpp, build-time, compilation, precompiled-header, forward-declaration, modules]
aliases: [编译时间, build time, 编译加速, 前向声明, 预编译头, 编译优化]
created: 2026-04-04
updated: 2026-04-04
---

# 编译时间优化

C++ 的长编译时间是大型项目的痛点——前向声明、减少模板实例化、PCH 都能显著改善。

## 减少头文件依赖

```cpp
// ❌ 头文件包含实现依赖
// widget.h
#include <vector>
#include <string>
#include <memory>
#include <mutex>
#include "database.h"
#include "cache.h"

// ✅ 前向声明 + 指针/引用
// widget.h
#include <memory>  // 只需要 unique_ptr
class Database;    // 前向声明
class Cache;

class Widget {
    std::unique_ptr<Database> db_;   // Pimpl 或 unique_ptr
    void process(Cache& cache);      // 引用参数只需前向声明
};
```

## Pimpl 模式

```cpp
// widget.h（轻量头文件）
class Widget {
    struct Impl;
    std::unique_ptr<Impl> impl_;
public:
    Widget();
    ~Widget();  // 必须在 .cpp 中定义（Impl 不完整时不能析构）
    void do_work();
};

// widget.cpp（重实现放这里，改了不影响其他文件）
#include "widget.h"
#include <vector>   // 只在 .cpp 中包含重头文件
#include "database.h"

struct Widget::Impl {
    std::vector<int> data;
    Database db;
    void helper() { /* ... */ }
};

Widget::Widget() : impl_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;  // 必须在 Impl 定义后
void Widget::do_work() { impl_->helper(); }
```

## 模板实例化控制

```cpp
// 显式实例化：避免每个 TU 重复实例化
// widget.cpp 中显式实例化常用类型
template class std::vector<int>;
template class std::map<std::string, int>;

// 其他 TU 声明为 extern（C++11 起支持）
extern template class std::vector<int>;  // 不实例化，使用别处的
```

## 预编译头（PCH）

```cpp
// pch.h：频繁使用的头文件
#include <vector>
#include <string>
#include <memory>
#include <algorithm>
#include <iostream>

// 编译：
// g++ -x c++-header pch.h -o pch.h.gch
// g++ -include pch.h main.cpp  # 自动使用 PCH
```

## 关键要点

> Pimpl 把重头文件从 .h 移到 .cpp——改 .cpp 不触发依赖重编译。前向声明减少头文件包含。

> 显式实例化 + extern template 避免模板在每个 TU 重复实例化，是模板库的编译加速关键。

## 相关模式 / 关联

- [[cpp-pimpl-惯用法]] — Pimpl 的详细讨论
- [[cpp-modules]] — C++20 的终极方案
