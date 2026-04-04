---
title: 类型擦除
tags: [cpp, idiom, type-erasure, polymorphism]
aliases: [Type Erasure, 类型擦除, Concept Wrapper, External Polymorphism]
created: 2026-04-04
updated: 2026-04-04
---

# 类型擦除

**一句话概述：** 将不同具体类型的对象统一为相同的接口类型，隐藏原始类型信息——`std::function`、`std::any`、`std::shared_ptr` 的核心实现技术。

## 意图与场景

Type Erasure 在不使用继承的情况下实现运行时多态：

- **统一接口，隐藏类型**：不同类型可以用相同接口操作
- **去除模板依赖**：避免模板在 API 中的传播
- **外部多态**：不修改原始类型即可为其添加接口

**适用场景：**
- 需要存储不同类型的同质容器
- 库的公共 API 需要隐藏模板
- 插件架构、回调系统
- 类型安全的 `void*` 替代（`std::any`）

## C++ 实现代码

### 手动实现类型擦除（std::function 原理）

```cpp
#include <memory>
#include <utility>
#include <iostream>
#include <vector>

class Drawable {
    // 类型擦除的核心：内部桥接接口
    struct Concept {
        virtual ~Concept() = default;
        virtual void draw() const = 0;
        virtual std::unique_ptr<Concept> clone() const = 0;
    };

    template <typename T>
    struct Model : Concept {
        T object_;
        explicit Model(T obj) : object_(std::move(obj)) {}
        
        void draw() const override {
            object_.draw();  // 鸭子类型：只要 T 有 draw() 方法
        }
        std::unique_ptr<Concept> clone() const override {
            return std::make_unique<Model>(object_);
        }
    };

    std::unique_ptr<Concept> impl_;

public:
    // 任意类型构造
    template <typename T>
    Drawable(T obj) : impl_(std::make_unique<Model<T>>(std::move(obj))) {}
    
    // 拷贝语义
    Drawable(const Drawable& other) : impl_(other.impl_->clone()) {}
    Drawable& operator=(const Drawable& other) {
        if (this != &other) impl_ = other.impl_->clone();
        return *this;
    }
    
    Drawable(Drawable&&) noexcept = default;
    Drawable& operator=(Drawable&&) noexcept = default;
    
    void draw() const { impl_->draw(); }
};

// 使用：完全不相关的类型
struct Circle { double r; 
    void draw() const { std::cout << "Circle r=" << r << '\n'; }
};
struct Label { std::string text; 
    void draw() const { std::cout << "Label: " << text << '\n'; }
};

void demo() {
    std::vector<Drawable> shapes;
    shapes.emplace_back(Circle{5.0});
    shapes.emplace_back(Label{"Hello"});
    
    for (const auto& s : shapes) {
        s.draw();  // 统一接口，原始类型已擦除
    }
}
```

### std::function 的简化实现

```cpp
#include <memory>
#include <utility>
#include <functional>

template <typename Signature>
class Function;

template <typename R, typename... Args>
class Function<R(Args...)> {
    struct CallableBase {
        virtual ~CallableBase() = default;
        virtual R invoke(Args... args) const = 0;
        virtual std::unique_ptr<CallableBase> clone() const = 0;
    };

    template <typename F>
    struct CallableImpl : CallableBase {
        F func_;
        explicit CallableImpl(F f) : func_(std::move(f)) {}
        
        R invoke(Args... args) const override {
            return func_(std::forward<Args>(args)...);
        }
        std::unique_ptr<CallableBase> clone() const override {
            return std::make_unique<CallableImpl>(func_);
        }
    };

    std::unique_ptr<CallableBase> callable_;

public:
    Function() = default;
    
    template <typename F>
    Function(F f) : callable_(std::make_unique<CallableImpl<F>>(std::move(f))) {}
    
    R operator()(Args... args) const {
        return callable_->invoke(std::forward<Args>(args)...);
    }
    
    explicit operator bool() const noexcept { return callable_ != nullptr; }
};
```

### C++17 std::any 简化实现

```cpp
#include <memory>
#include <typeinfo>

class Any {
    struct StorageBase {
        virtual ~StorageBase() = default;
        virtual const std::type_info& type() const = 0;
        virtual std::unique_ptr<StorageBase> clone() const = 0;
    };
    
    template <typename T>
    struct StorageImpl : StorageBase {
        T value_;
        explicit StorageImpl(T v) : value_(std::move(v)) {}
        const std::type_info& type() const override { return typeid(T); }
        std::unique_ptr<StorageBase> clone() const override {
            return std::make_unique<StorageImpl>(value_);
        }
    };
    
    std::unique_ptr<StorageBase> storage_;

public:
    Any() = default;
    
    template <typename T>
    Any(T value) : storage_(std::make_unique<StorageImpl<T>>(std::move(value))) {}
    
    const std::type_info& type() const { 
        return storage_ ? storage_->type() : typeid(void); 
    }
    
    bool has_value() const noexcept { return storage_ != nullptr; }
};

template <typename T>
T any_cast(const Any& a) {
    if (a.type() != typeid(T)) throw std::bad_cast();
    // 实际实现需 dynamic_cast ...
}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 不需要公共基类 | 间接调用有性能开销（虚函数 + 堆分配） |
| 类型安全（vs void*） | 实现复杂度高 |
| API 不暴露模板 | 每个操作增加一次间接调用 |
| 支持值语义（可拷贝） | 不支持子类特有方法 |

> [!tip] 关键要点
> 类型擦除是**编译时接口 + 运行时多态**的桥梁。`std::function<void()>` 可以存储 lambda、函数指针、bind 表达式——完全不同类型，相同接口。现代 C++ 趋势是用类型擦除替代虚继承，提供值语义的同时保持灵活性。性能敏感场景注意堆分配开销（小对象优化 SSO 可缓解）。

## 相关链接

- [[策略模式]] — 策略通常通过类型擦除实现
- [[Visitor 模式]] — 双重分派 vs 类型擦除
- [[cpp-智能指针详解]] — shared_ptr 的类型擦除删除器
- [[cpp-函数式编程模式]] — std::function 的使用
