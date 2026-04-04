---
title: this 指针与成员指针
tags: [cpp, oop, this, member-pointer, member-function-pointer]
aliases: [this指针, 成员指针, 成员函数指针, pointer to member]
created: 2026-04-04
updated: 2026-04-04
---

# this 指针与成员指针

`this` 是成员函数中指向当前对象的隐式指针。成员指针是指向类成员（数据或函数）的特殊指针类型。

## this 指针

```cpp
class Widget {
    int x_;
public:
    // this 的类型：
    // 非 const 成员函数：Widget* const
    // const 成员函数：const Widget* const

    void set(int x) {
        this->x_ = x;    // 显式使用 this（通常省略）
    }

    Widget& chain_set(int x) {
        this->x_ = x;
        return *this;    // 返回自身引用，支持链式调用
    }

    // 显式捕获 this 的 lambda
    auto make_callback() {
        return [this]() { return x_; };  // 捕获 this 指针
    }
};

// C++23: deducing this（显式对象参数）
struct Widget2 {
    template <typename Self>
    auto&& get_x(this Self&& self) {
        return std::forward<Self>(self).x_;
        // const Widget 调用 → const int&
        // Widget 调用 → int&
        // 减少 const/non-const 重载
    }
};
```

## 成员指针

```cpp
class Widget {
public:
    int x;
    double y;
    void print() const { std::cout << x << ", " << y << "\n"; }
    int compute(int z) const { return x + z; }
};

// 数据成员指针
int Widget::* px = &Widget::x;       // 指向 Widget::x
double Widget::* py = &Widget::y;    // 指向 Widget::y

Widget w{10, 3.14};
w.*px = 42;                          // 通过成员指针访问
int val = w.*px;                     // 42

Widget* p = &w;
p->*px = 100;                        // 通过对象指针访问

// 成员函数指针
void (Widget::*pf)() const = &Widget::print;
(w.*pf)();                           // 调用成员函数

int (Widget::*pf2)(int) const = &Widget::compute;
int result = (w.*pf2)(5);            // 调用带参数的成员函数
```

## 成员指针的实际应用

```cpp
// 通用序列化（基于成员指针）
template <typename T, typename M>
void serialize(std::ostream& os, const T& obj, M T::*member) {
    os << obj.*member;
}

Widget w{10, 3.14};
serialize(std::cout, w, &Widget::x);  // 输出 10

// 成员指针 → 函数对象（C++17）
auto x_accessor = std::mem_fn(&Widget::x);
x_accessor(w) = 50;  // 等价于 w.x = 50
```

## 关键要点

> C++23 的 `deducing this` 让 `this` 成为显式参数，消除了 const/non-const 成员函数重载的需要，同时支持 CRTP 和 mixin 的更简洁写法。

> 成员指针不同于普通指针——它存储的是成员在对象中的偏移量，而非绝对地址。

## 相关模式 / 关联

- [[cpp-类与对象]] — 类的基础
- [[cpp-crtp-奇异递归模板模式]] — deducing this 的简化版
