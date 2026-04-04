---
title: C++ 移动语义与异常安全
tags: [cpp, move, exception-safety, noexcept, strong-guarantee]
aliases: [移动与异常安全, noexcept移动, vector扩容异常安全]
created: 2026-04-04
updated: 2026-04-04
---

# 移动语义与异常安全

`noexcept` 移动构造函数影响 STL 容器的行为——vector 扩容时选择移动还是拷贝取决于此。

## vector 扩容的移动决策

```cpp
class Widget {
public:
    // 标记 noexcept：vector 扩容时会移动
    Widget(Widget&& other) noexcept { /* 移动资源 */ }

    // 未标记 noexcept：vector 扩容时会拷贝（为了强异常安全）
    // Widget(Widget&& other) { /* 移动资源 */ }
};

// vector 扩容时的决策：
// 1. 如果移动构造是 noexcept → 移动元素（快）
// 2. 如果移动构造不是 noexcept → 拷贝元素（安全）
// 3. 如果不可移动也不可拷贝 → 编译错误
```

## 为什么需要 noexcept 移动

```cpp
// 没有 noexcept：扩容时必须拷贝以保证强异常安全
// 如果移动到一半抛异常 → 部分元素已移动，部分未移动 → 状态不一致

// 有了 noexcept：扩容可以安全地移动所有元素
// 移动不会抛异常 → 任何时刻中断都安全
```

## 最佳实践

```cpp
class Resource {
    int* data_;
    size_t size_;
public:
    // ✅ 移动构造标记 noexcept
    Resource(Resource&& other) noexcept
        : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;
        other.size_ = 0;
    }

    // ✅ 移动赋值标记 noexcept
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }

    // swap 也标记 noexcept
    friend void swap(Resource& a, Resource& b) noexcept {
        using std::swap;
        swap(a.data_, b.data_);
        swap(a.size_, b.size_);
    }
};
```

## 关关键要点

> 移动操作应标记 `noexcept`——这不仅是一个承诺，它直接影响 STL 容器（vector、deque 等）扩容时的性能。

> 如果移动操作可能抛异常（比如需要分配内存），不要标记 `noexcept`——STL 会回退到拷贝以保证异常安全。

## 相关模式 / 关联

- [[cpp-右值引用与移动语义]] — 移动语义基础
- [[cpp-异常安全深入]] — 异常安全级别
