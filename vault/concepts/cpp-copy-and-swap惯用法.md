---
title: copy-and-swap 惯用法
tags: [cpp, exception-safety, copy-swap, copy-assignment, swap]
aliases: [copy-and-swap, 拷贝并交换, 异常安全赋值]
created: 2026-04-05
updated: 2026-04-05
---

# copy-and-swap 惯用法

**一句话概述：** 赋值运算符的异常安全写法：先在参数里拷贝一份（可能抛异常），然后用 `noexcept` swap 交换（不会抛异常）——拷贝失败则原对象不变（强异常保证），swap 永远成功。

## 问题：朴素赋值的异常安全

```cpp
class Widget {
    int* data_;
    size_t size_;
public:
    // ❌ 朴素赋值：没有强异常保证
    Widget& operator=(const Widget& other) {
        if (this == &other) return *this;
        delete[] data_;                    // ① 释放旧资源
        size_ = other.size_;
        data_ = new int[size_];            // ② 分配新资源 ← 可能抛异常！
        std::copy(other.data_, other.data_ + size_, data_);
        return *this;
        // 问题：如果 ② 抛异常，data_ 已经被 delete 了，对象处于无效状态
    }
};
```

## 解法：copy-and-swap

```cpp
class Widget {
    int* data_;
    size_t size_;

public:
    // 拷贝构造函数（已实现）
    Widget(const Widget& other)
        : data_(new int[other.size_]), size_(other.size_) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    // 析构函数
    ~Widget() { delete[] data_; }

    // swap：noexcept，只交换指针和大小
    friend void swap(Widget& a, Widget& b) noexcept {
        using std::swap;
        swap(a.data_, b.data_);
        swap(a.size_, b.size_);
    }

    // ✅ copy-and-swap 赋值运算符
    // 参数 by-value：调用拷贝构造函数（可能抛异常，但在参数构造阶段）
    Widget& operator=(Widget other) {  // ← 按值传参 = 拷贝
        swap(*this, other);             // ← noexcept 交换
        return *this;
        // other 析构时会释放旧资源（RAII）
    }
};
```

## 异常保证分析

```
调用 a = b;

① Widget other = b;  ← 拷贝构造 other
   │
   ├── 成功：other 持有 b 的副本
   └── 失败（new 抛异常）：a 完全没被修改 → 强异常保证 ✅

② swap(a, other);    ← noexcept，不可能失败
   │
   └── a 现在持有 b 的副本
       other 持有 a 的旧资源

③ return *this;
   │
   └── other 析构 → 释放 a 的旧资源 → RAII 自动清理 ✅
```

**结果：要么完全成功（a = b），要么完全不变（a 保持原样）。** 这就是强异常保证。

## 与 Rule of Five 的关系

```cpp
class Widget {
    // Rule of Three/Five 的简洁写法：
    // 1. 拷贝构造函数（深拷贝）
    Widget(const Widget& other)
        : data_(new int[other.size_]), size_(other.size_) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    // 2. 析构函数
    ~Widget() { delete[] data_; }

    // 3. 赋值运算符 = 按值传参 + swap（统一了拷贝赋值和移动赋值！）
    Widget& operator=(Widget other) {
        swap(*this, other);
        return *this;
    }

    // 如果还需要移动构造函数：
    Widget(Widget&& other) noexcept
        : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;
        other.size_ = 0;
    }

    friend void swap(Widget& a, Widget& b) noexcept {
        using std::swap;
        swap(a.data_, b.data_);
        swap(a.size_, b.size_);
    }

    int* data_;
    size_t size_;
};
```

**注意：** `operator=(Widget other)` 同时处理了拷贝赋值和移动赋值：
- `a = b;` → other 由拷贝构造 → 拷贝赋值
- `a = std::move(b);` → other 由移动构造 → 移动赋值

## 什么时候不应该用 copy-and-swap

### 1. 自赋值频繁时

```cpp
a = a;  // 自赋值

// copy-and-swap：先拷贝一份 a（多余的开销），再 swap
// 朴素实现：if (this == &other) return *this; → 直接返回

// 现代观点：自赋值极其罕见，copy-and-swap 的额外开销可忽略
// 但标准库实现（如 string）通常还是会检测自赋值
```

### 2. 需要移动赋值优化时

```cpp
// copy-and-swap 的移动赋值：
a = std::move(b);
// → other 由移动构造（开销：转移指针）
// → swap（开销：交换指针）
// → other 析构（开销：释放 a 的旧资源）

// 直接移动赋值：
a = std::move(b);
// → 释放 a 的旧资源
// → 转移 b 的指针
// → 开销更少（少了移动构造 + swap + 析构）
```

### 3. 基类赋值

```cpp
class Base {
public:
    Base& operator=(Base other) { swap(*this, other); return *this; }
};

class Derived : public Base {
public:
    Derived& operator=(Derived other) {
        // 不能用 Base::operator= 了，因为参数类型不匹配
        Base::operator=(std::move(other));  // 需要特殊处理
        swap(derived_members_, other.derived_members_);
        return *this;
    }
};
```

## 关键要点

> copy-and-swap 的价值不在于性能，而在于**异常安全的正确性证明**——构造阶段可能失败但不影响原对象，swap 阶段不会失败。这种分离让正确性更容易论证。

> 现代 C++ 的 Rule of Zero 倾向于完全不写特殊成员函数（用 `unique_ptr`/`shared_ptr` 管理资源）。只有手动管理资源时才需要 copy-and-swap。

> swap 函数应该是非成员函数（`friend` 声明 + 非成员定义），并且应该支持 ADL（参数依赖查找）。标准库的 `std::swap` 会通过 ADL 找到你的自定义 `swap`。

## 相关模式 / 关联

- [[cpp-异常安全深入]] — 异常安全保证级别
- [[cpp-Rule-of-Zero与Rule-of-Five]] — 特殊成员函数管理
- [[cpp-深拷贝与浅拷贝]] — 拷贝语义
- [[cpp-右值引用与移动语义]] — 移动赋值优化
- [[cpp-智能指针详解]] — 自动资源管理替代手动管理
