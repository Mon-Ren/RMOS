---
title: C++ 中的 ADL（参数依赖查找）
tags: [cpp, ADL, argument-dependent-lookup, name-lookup, operator-overload]
aliases: [ADL, 参数依赖查找, argument dependent lookup, Koenig查找]
created: 2026-04-04
updated: 2026-04-04
---

# ADL（参数依赖查找）

ADL 让编译器在参数类型的命名空间中查找函数——这是 `std::cout << x` 和 `swap` 能正常工作的原因。

## 基本原理

```cpp
namespace MyLib {
    struct Widget {};

    // 这个函数在 MyLib 命名空间中
    void print(const Widget& w) {
        std::cout << "MyLib::Widget\n";
    }
}

// 调用处：没有 using namespace MyLib
MyLib::Widget w;
print(w);  // 编译器通过 ADL 在 MyLib 中找到 print！
// 因为参数 w 的类型 Widget 在 MyLib 中，编译器查找 MyLib 命名空间
```

## swap 与 ADL

```cpp
// 经典的 swap 惯用法
template <typename T>
void my_swap(T& a, T& b) {
    using std::swap;        // 引入 std::swap 作为备选
    swap(a, b);             // ADL 优先查找 T 命名空间中的 swap
    // 如果 T 的命名空间有自定义 swap → 用自定义版本
    // 否则 fallback 到 std::swap
}

// 这就是为什么自定义类型应该在同命名空间中定义 swap
namespace MyLib {
    struct Widget { int* data; size_t size; };

    void swap(Widget& a, Widget& b) noexcept {
        using std::swap;
        swap(a.data, b.data);
        swap(a.size, b.size);
    }
}
```

## ADL 的限制

```cpp
// ADL 只查找参数类型的"关联命名空间"
// 不查找：模板参数、默认参数、成员函数

// ADL 不会找到类的成员函数
struct Foo { void method(); };
Foo f;
// method();  // 编译错误：ADL 不查找成员

// 使用 using 时的陷阱
using std::swap;  // 引入所有 std::swap 重载
swap(a, b);       // ADL + std::swap 都在候选集中

using namespace std;  // 引入 std 中所有名字（不推荐）
swap(a, b);           // 可能与 ADL 结果冲突
```

## 关键要点

> ADL 是 C++ 查找机制的核心部分——它让运算符重载、`swap` 惯用法、`begin`/`end` 等全局函数能自动找到自定义类型的实现。

> 自定义类型的运算符和 `swap` 应该定义在与类型相同的命名空间中——ADL 会自动找到它们。

## 相关模式 / 关联

- [[cpp-运算符重载]] — 运算符通过 ADL 找到
- [[cpp-命名空间]] — 命名空间与查找
