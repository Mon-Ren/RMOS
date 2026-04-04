---
title: 标签分发与标签派发
tags: [cpp, template, tag-dispatch, dispatch, compile-time-selection]
aliases: [标签分发, tag dispatch, 编译期分发, 重载决议选择]
created: 2026-04-04
updated: 2026-04-04
---

# 标签分发（Tag Dispatch）

标签分发利用重载决议在编译期选择函数实现——在 `if constexpr` 和 Concepts 之前，这是做编译期分发的主流方式。

## 基本原理

```cpp
// 标签类型（空类型，仅用于区分重载）
struct fast_tag {};
struct safe_tag {};

// 实现函数用标签区分
void do_work_impl(int val, fast_tag) {
    std::cout << "Fast path: " << val << "\n";
}

void do_work_impl(int val, safe_tag) {
    std::cout << "Safe path: " << val << "\n";
}

// 分发函数
void do_work(int val, bool use_fast) {
    if (use_fast)
        do_work_impl(val, fast_tag{});
    else
        do_work_impl(val, safe_tag{});
}
```

## STL 中的应用

```cpp
// std::advance 的经典实现（简化版）
namespace detail {
    template <typename It>
    void advance_impl(It& it, typename std::iterator_traits<It>::difference_type n,
                      std::random_access_iterator_tag) {
        it += n;  // 随机访问：O(1)
    }

    template <typename It>
    void advance_impl(It& it, typename std::iterator_traits<It>::difference_type n,
                      std::input_iterator_tag) {
        while (n--) ++it;  // 输入迭代器：O(n)
    }
}

template <typename It>
void advance(It& it, typename std::iterator_traits<It>::difference_type n) {
    detail::advance_impl(it, n,
        typename std::iterator_traits<It>::iterator_category{});
}
// 根据迭代器类别自动选择高效实现
```

## 现代替代

```cpp
// C++17: if constexpr
template <typename It>
void advance(It& it, std::iter_difference_t<It> n) {
    if constexpr (std::random_access_iterator<It>) {
        it += n;
    } else {
        while (n--) ++it;
    }
}

// C++20: Concepts + 重载
void advance(std::random_access_iterator auto& it, auto n) { it += n; }
void advance(std::input_iterator auto& it, auto n) { while (n--) ++it; }
```

## 关键要点

> 标签分发的核心是利用空类型的重载决议——编译器选择最匹配的重载，运行时零开销。`std::integral_constant` 和 `std::true_type`/`std::false_type` 是常用的标签。

> C++17 的 `if constexpr` 和 C++20 的 Concepts 已经大幅取代了标签分发，但理解它有助于读懂标准库源码。

## 相关模式 / 关联

- [[cpp-if-constexpr]] — 现代替代
- [[cpp-concepts]] — 更现代的替代
- [[cpp-stl算法总览]] — STL 中的标签分发
