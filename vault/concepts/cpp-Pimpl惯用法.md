---
title: C++ Pimpl 惯用法
tags: [cpp, pimpl, compilation-firewall, opaque-pointer, bridge]
aliases: [Pimpl, 编译防火墙, 不透明指针, bridge pattern, pointer to implementation]
created: 2026-04-04
updated: 2026-04-04
---

# Pimpl 惯用法

Pimpl（Pointer to Implementation）把类的实现细节隐藏在 .cpp 文件中——减少头文件依赖、加速编译、实现二进制兼容。

## 实现

```cpp
// widget.h（轻量头文件）
#include <memory>
#include <string>

class Widget {
public:
    Widget();
    ~Widget();  // 必须在 .cpp 中定义
    Widget(Widget&&);
    Widget& operator=(Widget&&);

    void set_name(const std::string& name);
    std::string name() const;

private:
    struct Impl;                  // 前向声明
    std::unique_ptr<Impl> impl_;  // 指向实现
};

// widget.cpp（重实现）
#include "widget.h"
#include <vector>   // 重头文件只在这里包含
#include <mutex>

struct Widget::Impl {
    std::string name;
    std::vector<int> data;
    std::mutex mtx;
    // 所有私有成员和辅助函数
};

Widget::Widget() : impl_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;  // 必须在 Impl 定义后

void Widget::set_name(const std::string& n) { impl_->name = n; }
std::string Widget::name() const { return impl_->name; }
```

## 优势

```
1. 减少编译依赖：改 impl 不触发依赖重编译
2. 二进制兼容：添加/移除私有成员不改变类大小
3. 隐藏实现细节：头文件不暴露任何私有成员
4. 减少头文件传递：vector/mutex 等重头文件不暴露
```

## 代价

```
1. 一次间接访问（指针跳转）
2. 一次堆分配（make_unique）
3. unique_ptr 的移动操作
4. 代码量增加
```

## 关键要点

> Pimpl 的 `~Widget()` 必须在 .cpp 中定义——因为 `unique_ptr<Impl>` 的析构需要 Impl 的完整定义。

> 如果性能是关键且头文件变化不频繁，Pimpl 的间接开销可能不值得。大部分场景 Pimpl 的编译时间收益更重要。

## 相关模式 / 关联

- [[cpp-编译时间优化]] — Pimpl 是编译加速的关键技术
- [[cpp-类与对象]] — 特殊成员函数
