---
title: lambda 闭包对象的内存布局
tags: [cpp, lambda, closure, capture, memory-layout, compiler]
aliases: [lambda 内部实现, 闭包对象布局, lambda 捕获的底层]
created: 2026-04-05
updated: 2026-04-05
---

# lambda 闭包对象的内存布局

**一句话概述：** Lambda 是编译器帮你生成的一个匿名类（闭包类型），捕获的变量变成类的数据成员，`operator()` 变成成员函数。捕获 by-value 的 lambda 大小 = 捕获变量的总大小；捕获 by-reference 的 lambda 大小固定（一个指针大小）。

## 编译器做了什么

```cpp
// 你写的代码
int x = 42;
auto lambda = [x, &y](int z) { return x + y + z; };

// 编译器生成的等价代码：
class __lambda_unique_name_001 {
    int x_;           // by-value 捕获 → 数据成员
    int& y_;          // by-reference 捕获 → 引用成员

public:
    __lambda_unique_name_001(int x, int& y) : x_(x), y_(y) {}

    auto operator()(int z) const {  // 无 mutable 时是 const
        return x_ + y_ + z;
    }
};

auto lambda = __lambda_unique_name_001(x, y);
```

## 不同捕获方式的内存布局

```cpp
int a = 10;
int b = 20;

// ─── 无捕获 ───
auto f1 = []() { return 42; };
static_assert(sizeof(f1) == 1);  // 空类，通常 1 字节
// 编译器可以隐式转换为函数指针
int (*fp)() = f1;  // ✅

// ─── 捕获一个 int by value ───
auto f2 = [a]() { return a; };
static_assert(sizeof(f2) == sizeof(int));  // 4 字节
// 内存布局：[ int a_ ]
// int (*fp)() = f2;  // ❌ 不能转为函数指针

// ─── 捕获两个 int by value ───
auto f3 = [a, b]() { return a + b; };
static_assert(sizeof(f3) == 2 * sizeof(int));  // 8 字节
// 内存布局：[ int a_, int b_ ]

// ─── 捕获 by reference ───
auto f4 = [&a, &b]() { return a + b; };
static_assert(sizeof(f4) == 2 * sizeof(int*));  // 16 字节（64位）
// 内存布局：[ int* a_ptr, int* b_ptr ]

// ─── 混合捕获 ───
auto f5 = [a, &b]() { return a + b; };
static_assert(sizeof(f5) == sizeof(int) + sizeof(int*));  // 12 字节（64位，对齐后 16）
// 内存布局：[ int a_, int* b_ptr ]

// ─── 捕获大量数据 ───
std::array<int, 1000> big;
auto f6 = [big]() { return big[0]; };
static_assert(sizeof(f6) == sizeof(big));  // 4000 字节！
// 内存布局：[ int big_[1000] ]
// ⚠️ 大 lambda 会很"胖"
```

## this 捕获的特殊性

```cpp
class Widget {
    int value_ = 42;

    void method() {
        // [this] 捕获 this 指针，不是 value_ 本身
        auto f = [this]() { return value_; };
        // 等价于：
        // class Closure {
        //     Widget* this_;
        //     auto operator()() const { return this_->value_; }
        // };
        // sizeof(f) == 8（64位上一个指针）

        // C++17: [*this] 捕获 this 的拷贝（值语义）
        auto g = [*this]() { return value_; };
        // 等价于：
        // class Closure {
        //     Widget widget_copy_;  // 整个 Widget 的拷贝
        //     auto operator()() const { return widget_copy_.value_; }
        // };
        // sizeof(g) == sizeof(Widget)  // 可能很大！
    }
};
```

## init capture（C++14 广义捕获）

```cpp
// init capture：在捕获时创建新变量
auto f = [ptr = std::make_unique<int>(42)]() {
    return *ptr;
};
// 编译器生成：
// class Closure {
//     std::unique_ptr<int> ptr_;
//     Closure(std::unique_ptr<int> p) : ptr_(std::move(p)) {}
//     auto operator()() const { return *ptr_; }
// };

// 这是移动 lambda（move-only lambda）的基础
std::thread t([data = std::move(big_vector)]() {
    process(data);
});
// big_vector 被移动到 lambda 的闭包对象里，再跟着线程走
```

## mutable lambda 的实现

```cpp
int count = 0;
auto f = [count]() mutable { return ++count; };
f();  // 1
f();  // 2

// 编译器生成：
// class Closure {
//     int count_;
//     Closure(int c) : count_(c) {}
//     auto operator()() { return ++count_; }  // 注意：非 const！
// };
// 没有 mutable → operator() 是 const → 不能修改成员
// 有 mutable    → operator() 非 const → 可以修改成员
```

## Lambda 与 std::function 的交互

```cpp
auto lambda = [x, &y](int z) { return x + y + z; };
// sizeof(lambda) 可能是 16（两个 int/int&）

std::function<int(int)> f = lambda;
// lambda 被类型擦除，存入 std::function 的 SBO 缓冲区
// 如果 lambda 太大 → 堆分配

// 性能对比：
// 直接调用 lambda：~0-1 ns（内联后零开销）
// 通过 std::function 调用：~3-5 ns（虚调用 + 可能的 cache miss）
```

## 关键要点

> lambda 的 `sizeof` 等于所有 by-value 捕获变量的总大小（加上对齐）。by-reference 捕获只增加一个指针大小。大捕获会导致 lambda 对象变大，在 std::function 中可能触发堆分配。

> 编译器可以（也确实会）优化掉不必要的 lambda 对象成员——如果某个捕获的 by-value 变量在函数体中从未使用，编译器可能不存储它（虽然标准要求可寻址的捕获变量必须存在）。

> Lambda 可以有模板参数（C++20 的 template lambda）：
> ```cpp
> auto f = []<typename T>(T a, T b) { return a + b; };
> f(1, 2);      // int
> f(1.0, 2.0);  // double
> ```
> 这比 `auto` 参数更精确，因为 `T` 在两次使用中必须是同一类型。

## 相关模式 / 关联

- [[cpp-lambda表达式]] — lambda 基础语法
- [[cpp-lambda捕获深入]] — 捕获模式详解
- [[cpp-function与lambda性能对比]] — 调用开销
- [[cpp-类型擦除]] — std::function 的类型擦除
- [[cpp-函数对象]] — functor vs lambda
