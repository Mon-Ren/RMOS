---
title: C++ 嵌套类与局部类
tags: [cpp, nested-class, local-class, inner-class, scope]
aliases: [嵌套类, 局部类, inner class, 成员类]
created: 2026-04-04
updated: 2026-04-04
---

# 嵌套类与局部类

C++ 支持在类内部或函数内部定义类——它们的作用域受限于外层。

## 嵌套类

```cpp
class Tree {
    struct Node {          // 嵌套类：只在 Tree 内可见
        int data;
        Node* left;
        Node* right;
    };
    Node* root_;
public:
    // Node 对外不可见——实现细节被隐藏
};

// 嵌套类可以访问外层类的 private 成员（C++11 起）
class Container {
    int value_ = 42;
public:
    class Iterator {
        Container* parent_;
    public:
        int get() const { return parent_->value_; }  // 可以访问 private
    };
    Iterator begin() { return {this}; }
};
```

## 局部类

```cpp
void process() {
    // 函数内定义的类——只在函数内可见
    struct Helper {
        int val;
        int compute() const { return val * 2; }
    };

    Helper h{21};
    std::cout << h.compute();  // 42

    // 局部类的限制：
    // - 不能有 static 成员
    // - 不能访问函数的局部变量（C++11 前）
    // - C++11 起可以捕获外层局部变量（作为构造函数参数）
    // - 不能用作模板参数（C++20 起允许）
}
```

## 使用场景

```cpp
// Pimpl 中嵌套 Impl
class Widget {
    struct Impl;  // 前向声明
    std::unique_ptr<Impl> impl_;
public:
    Widget();
    ~Widget();
};

// 迭代器作为嵌套类
class Container {
    struct Iterator {
        // ...
    };
public:
    Iterator begin();
    Iterator end();
};

// 局部类用作回调
void setup() {
    struct Callback {
        void operator()(int event) { handle(event); }
    };
    register_callback(Callback{});
}
```

## 关键要点

> 嵌套类是实现细节的隐藏手段——Pimpl 的 Impl、树的 Node、容器的 Iterator 都是典型用法。

> 局部类的使用较少——Lambda 几乎完全替代了局部类作为回调的场景。

## 相关模式 / 关联

- [[cpp-Pimpl惯用法]] — 嵌套 Impl
- [[cpp-lambda表达式]] — Lambda 替代局部类
