---
title: 多态容器与类型擦除容器
tags: [cpp, polymorphic-container, any-vector, type-erased-container, runtime]
aliases: [多态容器, any vector, 类型擦除容器, 异构容器, runtime多态]
created: 2026-04-04
updated: 2026-04-04
---

# 多态容器与类型擦除容器

C++ 的 vector 是同构的——所有元素必须是同一类型。需要存储不同类型时，有几种方案。

## 方案对比

```cpp
// 方案 1：variant
using Value = std::variant<int, double, std::string>;
std::vector<Value> values;
values.push_back(42);
values.push_back(3.14);
values.push_back("hello");
// 类型安全，编译期知道所有类型，性能好

// 方案 2：any
std::vector<std::any> anything;
anything.push_back(42);
anything.push_back(3.14);
anything.push_back(std::string("hello"));
// 完全动态，运行时检查，性能一般

// 方案 3：基类指针（传统 OOP）
std::vector<std::unique_ptr<Base>> objects;
objects.push_back(std::make_unique<Derived1>());
objects.push_back(std::make_unique<Derived2>());
// 虚函数调用，堆分配

// 方案 4：type erasure（自定义）
class AnyDrawable {
    struct Concept { virtual void draw() const = 0; virtual ~Concept() = default; };
    template <typename T> struct Model : Concept {
        T val;
        void draw() const override { val.draw(); }
    };
    std::unique_ptr<Concept> self_;
public:
    template <typename T> AnyDrawable(T v) : self_(new Model<T>{std::move(v)}) {}
    void draw() const { self_->draw(); }
};
std::vector<AnyDrawable> drawables;
```

## 选择指南

```
类型集合编译期已知      → variant
类型完全动态            → any
有公共接口（虚函数）    → unique_ptr<Base>
需要零开销              → type erasure
性能关键                → variant
```

## 关键要点

> `variant` 是首选——类型安全、栈分配、visit 模式。`any` 只在类型完全未知时使用。

> 传统 OOP（基类指针）仍有价值——当接口稳定且需要扩展新类型时。

## 相关模式 / 关联

- [[cpp-variant]] — variant 专题
- [[cpp-any]] — any 专题
- [[cpp-类型擦除]] — type erasure 原理
