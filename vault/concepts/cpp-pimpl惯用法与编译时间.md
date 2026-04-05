---
title: Pimpl 惯用法与编译时间
tags: [cpp, pimpl, compilation, forward-declaration, build-time]
aliases: [Pimpl 编译防火墙, 编译时间优化, 降低编译依赖]
created: 2026-04-05
updated: 2026-04-05
---

# Pimpl 惯用法与编译时间

**一句话概述：** Pimpl（Pointer to Implementation）把类的私有成员移到一个单独的 Impl 类，头文件只保留前向声明和 unique_ptr。改 Impl 的成员不需要重新编译依赖该头文件的代码——这就是"编译防火墙"。

```cpp
// widget.h
class Widget {
public:
    Widget();
    ~Widget();
    void do_something();
private:
    struct Impl;  // 前向声明
    std::unique_ptr<Impl> pimpl_;
};

// widget.cpp
struct Widget::Impl {
    std::vector<int> data;
    std::string name;
    // 私有成员全在这里
};
Widget::Widget() : pimpl_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;  // 必须在 cpp 中定义（Impl 完整类型可见）
void Widget::do_something() { pimpl_->data.push_back(42); }
```

## 关键要点

> Pimpl 的代价：一次间接调用（虚调用级别的开销）、一次堆分配、阻止内联。对于性能关键的热路径，可能需要权衡。

## 相关模式 / 关联

- [[cpp-pimpl-惯用法]] — Pimpl 基础
- [[cpp-前向声明与减少依赖]] — 前向声明
- [[cpp-编译时间优化]] — 编译加速
