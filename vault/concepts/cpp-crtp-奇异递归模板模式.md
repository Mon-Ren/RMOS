---
title: CRTP 奇异递归模板模式
tags: [cpp, idiom, CRTP, template, static-polymorphism]
aliases: [CRTP, Curiously Recurring Template Pattern, 静态多态]
created: 2026-04-04
updated: 2026-04-04
---

# CRTP 奇异递归模板模式

**一句话概述：** 子类将自身作为模板参数传递给基类，实现编译时多态——零虚函数开销的"静态多态"。

## 意图与场景

CRTP（Curiously Recurring Template Pattern）的核心机制：

- **子类 → 基类的模板参数**：`class Derived : public Base<Derived>`
- **基类通过 `static_cast` 调用子类方法**：编译时决议，无 vtable 开销
- **Mixin 功能注入**：基类模板为子类提供通用实现

**适用场景：**
- 性能关键路径上需要多态但不接受虚函数开销
- 实现公共接口的模板代码（如单例基类）
- 编译时接口检查（静态断言替代运行时检查）
- Mixin 功能注入（计数、日志、序列化等）

## C++ 实现代码

### 基本 CRTP：静态多态

```cpp
#include <iostream>
#include <vector>
#include <memory>

// 基类模板
template <typename Derived>
class Shape {
public:
    void draw() const {
        // 编译时调用子类的实现
        static_cast<const Derived*>(this)->draw_impl();
    }
    
    double area() const {
        return static_cast<const Derived*>(this)->area_impl();
    }
};

class Circle : public Shape<Circle> {
    double radius_;
public:
    explicit Circle(double r) : radius_(r) {}
    
    void draw_impl() const {
        std::cout << "Circle(r=" << radius_ << ")\n";
    }
    double area_impl() const {
        return 3.14159265 * radius_ * radius_;
    }
};

class Rectangle : public Shape<Rectangle> {
    double w_, h_;
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    
    void draw_impl() const {
        std::cout << "Rectangle(" << w_ << "x" << h_ << ")\n";
    }
    double area_impl() const {
        return w_ * h_;
    }
};

// 通用接口，无虚函数
template <typename T>
void render(const Shape<T>& shape) {
    shape.draw();  // 静态派发
}
```

### CRTP 单例基类

```cpp
template <typename T>
class Singleton {
public:
    static T& instance() {
        static T inst;
        return inst;
    }
    
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    
protected:
    Singleton() = default;
    ~Singleton() = default;
};

class Logger : public Singleton<Logger> {
    friend class Singleton<Logger>;  // 允许基类构造
public:
    void log(const std::string& msg) { /* ... */ }
private:
    Logger() = default;  // 只能通过 instance() 创建
};

// 使用：Logger::instance().log("hello");
```

### CRTP Mixin：功能注入

```cpp
// 注入"计数"功能
template <typename Derived, typename CounterType = int>
class Counted {
    static inline CounterType count_ = 0;
protected:
    Counted() { ++count_; }
    Counted(const Counted&) { ++count_; }
    ~Counted() { --count_; }
public:
    static CounterType instance_count() { return count_; }
};

// 注入"可打印"功能
template <typename Derived>
class Printable {
public:
    void print() const {
        std::cout << static_cast<const Derived*>(this)->to_string() << '\n';
    }
};

// 组合多个 Mixin
class Document : public Counted<Document>, 
                 public Printable<Document> {
    std::string name_;
public:
    explicit Document(std::string name) : name_(std::move(name)) {}
    
    std::string to_string() const {
        return "Document: " + name_;
    }
};
```

### CRTP 接口约束（编译时 duck typing）

```cpp
template <typename Derived>
class Serializable {
public:
    std::string serialize() const {
        // 编译时检查 Derived 是否有 to_bytes() 方法
        return static_cast<const Derived*>(this)->to_bytes();
    }
    
    void save(const std::string& path) const {
        auto data = serialize();
        // 写入文件...
    }
};
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 零运行时开销，无 vtable 查找 | 编译时绑定，无法运行时替换实现 |
| 子类接口错误在编译时暴露 | 代码膨胀（每个子类生成独立模板实例） |
| 可作为 Mixin 组合 | 调试信息更复杂 |
| 基类可访问子类成员 | 不能用于异构容器（类型不同） |

> [!tip] 关键要点
> CRTP 本质是**用编译时多态替代运行时多态**。当你确定类型在编译时已知、且需要极致性能时选择 CRTP。但要注意：需要异构容器存储不同子类时，虚函数仍是正确选择。C++20 的 Concepts 在某些场景下可以替代 CRTP 的接口检查功能。

> [!example] std::enable_shared_from_this
> 标准库中的 `enable_shared_from_this<T>` 就是 CRTP 的经典应用：
> ```cpp
> class Widget : public std::enable_shared_from_this<Widget> {
> public:
>     void process() {
>         auto self = shared_from_this();  // 获取自身的 shared_ptr
>         // 安全地传递给异步操作...
>     }
> };
> ```

## 相关链接

- [[模板方法模式]] — CRTP 是模板方法的编译时版本
- [[cpp-策略设计]] — 都使用模板参数化行为
- [[cpp-sfinae-与编译期多态]] — 编译时约束的另一种方式
- [[设计模式-cpp-选型指南]] — 运行时多态 vs 编译时多态
