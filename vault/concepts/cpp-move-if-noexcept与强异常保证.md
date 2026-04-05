---
title: move_if_noexcept 与强异常保证
tags: [cpp, move-if-noexcept, exception-safety, strong-guarantee, vector]
aliases: [move_if_noexcept, vector 扩容异常安全, 条件移动]
created: 2026-04-05
updated: 2026-04-05
---

# move_if_noexcept 与强异常保证

**一句话概述：** `std::move_if_noexcept` 在移动构造函数是 `noexcept` 时返回右值引用（触发移动），否则返回左值引用（触发拷贝）。这是 `std::vector::push_back` 实现强异常保证的关键——如果移动可能抛异常，扩容时宁可慢（拷贝）也不冒险（移动到一半抛异常导致状态不一致）。

## vector 扩容的异常安全困境

```cpp
std::vector<Widget> v;
v.push_back(w);  // 触发扩容：分配新内存，迁移旧元素

// 扩容时需要把旧元素迁移到新内存
// 用移动还是拷贝？

// 方案 A：逐个移动
for (size_t i = 0; i < old_size; ++i) {
    new (&new_buffer[i]) Widget(std::move(old_buffer[i]));
    // 如果第 3 个元素的移动构造抛异常：
    // - 元素 0,1,2 已经移动（旧对象处于"被移动"状态，不可用）
    // - 元素 3+ 还在旧位置（未移动）
    // - 新内存中的元素 0,1 需要析构
    // - 旧内存中移动后的"尸体"也需要处理
    // → vector 状态不一致 → 没有强异常保证！
}

// 方案 B：逐个拷贝
for (size_t i = 0; i < old_size; ++i) {
    new (&new_buffer[i]) Widget(old_buffer[i]);  // 拷贝构造
    // 如果第 3 个元素的拷贝构造抛异常：
    // - 新内存中的元素 0,1,2 需要析构（已构造的）
    // - 释放新内存
    // - 旧内存完全没动 → vector 状态不变 → 强异常保证 ✅
}
```

## std::move_if_noexcept 的实现

```cpp
#include <type_traits>
#include <utility>

template <typename T>
constexpr auto move_if_noexcept(T& x) noexcept {
    // 如果移动构造是 noexcept，返回 T&&（移动）
    // 否则，返回 const T&（拷贝）
    if constexpr (std::is_nothrow_move_constructible_v<T> ||
                  !std::is_copy_constructible_v<T>) {
        return std::move(x);
    } else {
        return static_cast<const T&>(x);
    }
}
```

**逻辑：**
1. 如果移动不会抛异常 → 用移动（快）
2. 如果没有拷贝构造函数（move-only 类型）→ 用移动（没得选）
3. 如果移动可能抛异常且有拷贝构造 → 用拷贝（安全）

## vector::push_back 的实际行为

```cpp
// vector 扩容的简化实现
template <typename T>
void vector<T>::push_back(const T& value) {
    if (size_ == capacity_) {
        // 需要扩容
        size_t new_cap = growth_factor(size_);
        T* new_buf = alloc_.allocate(new_cap);

        size_t constructed = 0;
        try {
            for (size_t i = 0; i < size_; ++i) {
                // 关键：move_if_noexcept 决定用移动还是拷贝
                ::new (&new_buf[i]) T(std::move_if_noexcept(data_[i]));
                ++constructed;
            }
            // 放入新元素
            ::new (&new_buf[size_]) T(value);
            ++constructed;
        } catch (...) {
            // 异常安全：析构已构造的新元素，释放新内存
            for (size_t i = 0; i < constructed; ++i)
                new_buf[i].~T();
            alloc_.deallocate(new_buf, new_cap);
            throw;  // 重新抛出
        }

        // 成功：析构旧元素，释放旧内存，更新指针
        for (size_t i = 0; i < size_; ++i)
            data_[i].~T();
        alloc_.deallocate(data_, capacity_);
        data_ = new_buf;
        capacity_ = new_cap;
    }
    // ... 放入新元素
}
```

## 实际效果

```cpp
struct FastMover {
    FastMover(FastMother&&) noexcept { /* O(1) 移动指针 */ }
    FastMover(const FastMother&) { /* O(n) 深拷贝 */ }
    // vector 扩容时 → move_if_noexcept 返回右值引用 → 移动 → 快 ✅
};

struct SlowMover {
    SlowMover(SlowMover&&) { /* 可能抛异常 */ }
    SlowMover(const SlowMover&) { /* 深拷贝 */ }
    // vector 扩容时 → move_if_noexcept 返回左值引用 → 拷贝 → 慢但安全 ✅
};

struct MoveOnly {
    MoveOnly(MoveOnly&&) { /* 没有拷贝构造 */ }
    // vector 扩容时 → move_if_noexcept 返回右值引用 → 移动（没得选） ✅
};
```

## 性能影响

```
100 万个元素的 vector 扩容（1x → 2x）：

有 noexcept 移动构造：
  移动 100 万个元素：~5 ms（只移动指针）

没有 noexcept（退化为拷贝）：
  拷贝 100 万个元素：~50 ms（深拷贝 10 倍数据）

→ noexcept 移动构造的性能收益是 10 倍！
```

## 关键要点

> `noexcept` 不只是"告诉编译器不抛异常"——它是性能优化信号。标准库根据 `noexcept` 来决定使用移动还是拷贝，直接影响运行时性能。

> `std::move_if_noexcept` 的名字有误导性——它不只是检查移动是否 noexcept，而是综合判断"用移动还是拷贝更安全"。对于 move-only 类型，即使移动可能抛异常，也会用移动（因为没有拷贝选项）。

> Rule of Five 中，如果你的移动构造函数不会抛异常（99% 的情况如此），一定要标记 `noexcept`。不标 `noexcept` 的移动构造在标准库中会被降级为拷贝。

## 相关模式 / 关联

- [[cpp-右值引用与移动语义]] — 移动语义基础
- [[cpp-异常安全深入]] — 异常安全保证级别
- [[cpp-Rule-of-Zero与Rule-of-Five]] — 特殊成员函数
- [[cpp-拷贝省略与RVO]] — 其他优化机制
- [[cpp-copy-and-swap惯用法]] — 异常安全赋值
