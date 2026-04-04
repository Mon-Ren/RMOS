---
title: 类型擦除
tags: [cpp, type-erasure, any, function, variant, polymorphism]
aliases: [类型擦除, type erasure, 运行时多态替代, std::function原理]
created: 2026-04-04
updated: 2026-04-04
---

# 类型擦除

类型擦除隐藏具体类型，提供统一接口——`std::function`、`std::any`、`std::shared_ptr` 的实现核心。

## 原理

```cpp
// 类型擦除 = 多态 + 模板构造函数
class Drawable {
    // 抽象接口
    struct Concept {
        virtual ~Concept() = default;
        virtual void draw(std::ostream&) const = 0;
        virtual std::unique_ptr<Concept> clone() const = 0;
    };

    // 模板实现：捕获任意类型
    template <typename T>
    struct Model : Concept {
        T value_;
        explicit Model(T v) : value_(std::move(v)) {}
        void draw(std::ostream& os) const override { os << value_; }
        std::unique_ptr<Concept> clone() const override {
            return std::make_unique<Model>(value_);
        }
    };

    std::unique_ptr<Concept> self_;

public:
    // 模板构造函数：任何可 draw 的类型都能构造 Drawable
    template <typename T>
    Drawable(T value) : self_(std::make_unique<Model<T>>(std::move(value))) {}

    Drawable(const Drawable& other) : self_(other.self_->clone()) {}
    Drawable& operator=(const Drawable& other) {
        self_ = other.self_->clone();
        return *this;
    }

    void draw(std::ostream& os) const { self_->draw(os); }
};

// 使用：不同具体类型统一为 Drawable
std::vector<Drawable> items;
items.push_back(42);              // Model<int>
items.push_back(std::string("hi")); // Model<string>
items.push_back(3.14);            // Model<double>
for (const auto& d : items) d.draw(std::cout);
```

## std::function 的原理

```cpp
// std::function 类似上述 Drawable，但针对可调用对象
// 存储：虚函数表指针 + 小对象缓冲区或堆指针
// 小对象优化：lambda 小于一定大小时直接存缓冲区
```

## 关键要点

> 类型擦除的开销：虚函数调用（间接跳转）+ 可能的堆分配。模板构造函数在编译期生成具体实现，运行时通过虚函数分发。

> 类型擦除不同于 variant——variant 在编译期知道所有类型，类型擦除完全隐藏类型。

## 相关模式 / 关联

- [[cpp-variant]] — 编译期知道类型集合时的替代
- [[cpp-函数指针与function]] — std::function 的类型擦除
