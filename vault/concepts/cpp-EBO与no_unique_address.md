---
title: 空基类优化与 [[no_unique_address]]
tags: [cpp, EBO, empty-base-optimization, no_unique_address, compressed-pair]
aliases: [空基类优化, EBO, no_unique_address, compressed_pair, 空类优化]
created: 2026-04-04
updated: 2026-04-04
---

# 空基类优化与 [[no_unique_address]]

C++ 允许空基类不占空间——让策略类、分配器等空类型零开销地"混入"类中。

## EBO（Empty Base Optimization）

```cpp
struct Empty {};  // sizeof(Empty) == 1（最小化）

struct Bad {
    int x;
    Empty e;       // sizeof(Bad) == 8（Empty 占 4 字节 padding）
};

struct Good : Empty {  // EBO：Empty 不占空间
    int x;
};
// sizeof(Good) == 4（与 int 一样大）

// 多个空基类的 EBO
struct A {};
struct B {};
struct C : A, B {
    int x;
};
// sizeof(C) == 4（A 和 B 都不占空间，但不能是相同类型的基类）
```

## [[no_unique_address]]（C++20）

```cpp
// 比 EBO 更灵活——不需要继承
struct Widget {
    [[no_unique_address]] Allocator alloc;  // 空类时不占空间
    [[no_unique_address]] Comparator cmp;   // 空类时不占空间
    int value;
};
// 如果 Allocator 和 Comparator 都是空类
// sizeof(Widget) == sizeof(int) == 4

// 标准库中的应用
template <typename T, typename Allocator = std::allocator<T>>
class vector {
    [[no_unique_address]] Allocator alloc_;
    T* data_;
    size_t size_, capacity_;
    // 默认 allocator 不额外占空间
};
```

## 关键要点

> EBO 是 C++ 长期支持的优化，但只对基类有效。C++20 的 `[[no_unique_address]]` 让成员也能享受空类优化，不再需要继承。

> `sizeof(空类) == 1` 是为了保证不同对象有不同的地址。EBO 和 `[[no_unique_address]]` 通过特殊规则避免了这个限制。

## 相关模式 / 关联

- [[cpp-sizeof与内存对齐]] — sizeof 与内存布局
- [[cpp-allocator与PMR]] — 分配器的空类优化
