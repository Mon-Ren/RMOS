---
title: Pimpl 惯用法
tags: [cpp, idiom, pimpl, compilation]
aliases: [Pimpl, Pointer to Implementation, 编译防火墙, Cheshire Cat, Handle Body]
created: 2026-04-04
updated: 2026-04-04
---

# Pimpl 惯用法

**一句话概述：** 通过指针将类的实现细节隐藏在一个前向声明的结构体中，大幅减少头文件依赖和编译时间。

## 意图与场景

Pimpl（Pointer to Implementation）又称 Handle-Body 或 Cheshire Cat 模式，核心目标：

- **减少编译依赖**：头文件不再包含实现细节的头文件
- **隐藏实现细节**：用户只看到公共接口
- **ABI 稳定性**：实现变更不影响头文件，无需重新编译客户端代码
- **编译防火墙**：修改 `.cpp` 文件后，只重编译该文件本身

**适用场景：**
- 大型项目减少编译时间
- 库的 ABI 稳定性要求
- 需要隐藏专有实现细节
- 实现频繁变更但接口稳定

## C++ 实现代码

### 标准 Pimpl 实现

```cpp
// widget.h —— 公共头文件
#pragma once
#include <memory>
#include <string>

class Widget {
public:
    Widget();
    ~Widget();  // 必须在 .cpp 中定义
    
    // 支持移动
    Widget(Widget&&) noexcept;
    Widget& operator=(Widget&&) noexcept;
    
    // 禁止拷贝（或实现深拷贝）
    Widget(const Widget&) = delete;
    Widget& operator=(const Widget&) = delete;
    
    void draw() const;
    void set_name(std::string name);

private:
    struct Impl;                    // 前向声明
    std::unique_ptr<Impl> pimpl_;   // 唯一拥有者
};
```

```cpp
// widget.cpp —— 实现文件
#include "widget.h"
#include <iostream>
#include <vector>

// 实现细节完全隐藏在此
struct Widget::Impl {
    std::string name;
    std::vector<int> data;
    int width = 0, height = 0;
    
    void do_draw() const {
        std::cout << "Drawing: " << name 
                  << " (" << width << "x" << height << ")\n";
    }
};

Widget::Widget() : pimpl_(std::make_unique<Impl>()) {}
Widget::~Widget() = default;  // 必须在此定义，因为 Impl 此处完整

Widget::Widget(Widget&&) noexcept = default;
Widget& Widget::operator=(Widget&&) noexcept = default;

void Widget::draw() const {
    pimpl_->do_draw();
}

void Widget::set_name(std::string name) {
    pimpl_->name = std::move(name);
}
```

### 带默认删除器的 Pimpl

```cpp
// 如果 Impl 需要特殊清理
class Handler {
    struct Impl;
    struct ImplDeleter {
        void operator()(Impl* p) const;  // 在 .cpp 中定义
    };
    std::unique_ptr<Impl, ImplDeleter> pimpl_;
public:
    Handler();
    // unique_ptr 的析构函数自动调用 ImplDeleter
};
```

### 拷贝支持的 Pimpl

```cpp
class CopyableWidget {
    struct Impl;
    std::unique_ptr<Impl> pimpl_;
public:
    CopyableWidget();
    ~CopyableWidget();
    
    // 深拷贝
    CopyableWidget(const CopyableWidget& other);
    CopyableWidget& operator=(const CopyableWidget& other);
    
    CopyableWidget(CopyableWidget&&) noexcept = default;
    CopyableWidget& operator=(CopyableWidget&&) noexcept = default;
};

// .cpp 中
CopyableWidget::CopyableWidget(const CopyableWidget& other)
    : pimpl_(other.pimpl_ ? std::make_unique<Impl>(*other.pimpl_) : nullptr) {}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 减少头文件依赖，加快编译 | 多一次间接寻址，轻微性能开销 |
| ABI 稳定，接口变更不需重编 | 必须在 .cpp 中定义析构函数 |
| 隐藏实现细节 | 拷贝需要深拷贝实现 |
| 改善模块化 | 调试时多了一层间接性 |

> [!tip] 关键要点
> Pimpl 的核心是**编译时间换运行时间**。现代构建系统（ccache、分布式编译）已大幅降低重编译成本，因此 Pimpl 在新项目中使用频率下降。但在**库开发**和 **ABI 稳定性**要求高的场景仍然很有价值。析构函数**必须**在 `.cpp` 文件中定义（`= default` 即可），否则 `unique_ptr<Impl>` 会在不完整类型上 `static_assert` 失败。

> [!warning] 常见陷阱
> Pimpl 类中 `unique_ptr<Impl>` 的析构函数要求 `Impl` 是完整类型。因此**析构函数不能 inline 在头文件中**，即使是 `= default` 也要写在 `.cpp` 里。移动操作同样需要 `Impl` 完整（除非显式 `= default` 在 .cpp 中）。

## 相关链接

- [[桥接模式]] — Pimpl 是桥接模式的特例
- [[cpp-raii-惯用法]] — unique_ptr 管理 Impl 生命周期
- [[cpp-智能指针详解]] — unique_ptr 的详细用法
