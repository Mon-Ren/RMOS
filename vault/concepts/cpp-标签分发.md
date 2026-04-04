---
title: Tag Dispatch 标签分发
tags: [cpp, idiom, tag-dispatch, template]
aliases: [Tag Dispatch, 标签分发, tag dispatching, 编译期分支]
created: 2026-04-04
updated: 2026-04-04
---

# Tag Dispatch 标签分发

**一句话概述：** 利用空类型标签（tag types）和函数重载决议，在编译时将调用分派到正确的实现——标准库中 `std::advance`、`std::copy` 等函数的核心技术。

## 意图与场景

Tag Dispatch 利用 C++ 重载决议规则做编译期分支：

- **标签类型**：空类仅作为"类型标签"，不存储数据
- **重载决议**：编译器选择最匹配的重载
- **零开销分支**：运行时无 if/switch，编译时确定

**适用场景：**
- 根据迭代器类别选择最优算法
- 根据类型特征选择实现
- 编译时策略选择
- 替代 `if constexpr`（在某些旧代码中）

## C++ 实现代码

### std::advance 的实现原理

```cpp
#include <iterator>
#include <type_traits>
#include <iostream>
#include <list>
#include <vector>

// 标签类型（来自标准库）
// struct input_iterator_tag {};
// struct forward_iterator_tag : input_iterator_tag {};
// struct bidirectional_iterator_tag : forward_iterator_tag {};
// struct random_access_iterator_tag : bidirectional_iterator_tag {};

// 内部实现：通过标签分派
namespace detail {
    template <typename InputIt, typename Distance>
    void advance_impl(InputIt& it, Distance n, std::input_iterator_tag) {
        // 输入迭代器：只能逐个前进
        for (Distance i = 0; i < n; ++i) ++it;
    }
    
    template <typename BidirIt, typename Distance>
    void advance_impl(BidirIt& it, Distance n, std::bidirectional_iterator_tag) {
        // 双向迭代器：可以前进或后退
        if (n >= 0) while (n--) ++it;
        else         while (n++) --it;
    }
    
    template <typename RandIt, typename Distance>
    void advance_impl(RandIt& it, Distance n, std::random_access_iterator_tag) {
        // 随机访问迭代器：O(1) 直接跳转
        it += n;
    }
}

// 公有接口：提取标签并分派
template <typename InputIt, typename Distance>
void my_advance(InputIt& it, Distance n) {
    using category = typename std::iterator_traits<InputIt>::iterator_category;
    detail::advance_impl(it, n, category{});
    //                                         ^^^^^^^^^ 创建标签对象
}
```

### 自定义 Tag Dispatch 示例

```cpp
#include <type_traits>
#include <cstring>
#include <algorithm>

// 自定义标签
struct trivially_copyable_tag {};
struct non_trivially_copyable_tag {};

// 检测并分派
namespace detail {
    template <typename T>
    void optimized_copy(const T* src, T* dst, std::size_t count, 
                        trivially_copyable_tag) {
        // POD 类型：用 memcpy 最快
        std::memcpy(dst, src, count * sizeof(T));
    }
    
    template <typename T>
    void optimized_copy(const T* src, T* dst, std::size_t count,
                        non_trivially_copyable_tag) {
        // 非平凡类型：必须调用拷贝构造
        for (std::size_t i = 0; i < count; ++i) {
            new (&dst[i]) T(src[i]);  // placement new
        }
    }
}

template <typename T>
void fast_copy(const T* src, T* dst, std::size_t count) {
    using tag = std::conditional_t<
        std::is_trivially_copyable_v<T>,
        trivially_copyable_tag,
        non_trivially_copyable_tag
    >;
    detail::optimized_copy(src, dst, count, tag{});
}
```

### integral_constant 与 true_type/false_type

```cpp
#include <type_traits>

// true_type / false_type 本质是 integral_constant 的别名
// template <bool B>
// using bool_constant = integral_constant<bool, B>;
// using true_type  = bool_constant<true>;
// using false_type = bool_constant<false>;

// 利用 true_type / false_type 做 tag dispatch
namespace detail {
    template <typename T>
    T abs_impl(T val, std::true_type) {  // signed
        return val < 0 ? -val : val;
    }
    
    template <typename T>
    T abs_impl(T val, std::false_type) { // unsigned
        return val;  // 无符号不需要 abs
    }
}

template <typename T>
T my_abs(T val) {
    return detail::abs_impl(val, std::is_signed<T>{});
    //                                    ^^^^^^^^^^^^^^ 创建 tag 对象
}
```

### C++17 编译期 if 替代

```cpp
// 现代 C++17 风格：if constexpr 替代 tag dispatch
template <typename InputIt, typename Distance>
void advance_modern(InputIt& it, Distance n) {
    using cat = typename std::iterator_traits<InputIt>::iterator_category;
    
    if constexpr (std::is_same_v<cat, std::random_access_iterator_tag>) {
        it += n;  // O(1)
    } else if constexpr (std::is_same_v<cat, std::bidirectional_iterator_tag>) {
        if (n >= 0) while (n--) ++it;
        else        while (n++) --it;
    } else {
        for (Distance i = 0; i < n; ++i) ++it;  // O(n)
    }
}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 编译时零开销分支 | C++17 前写法略显迂回 |
| 利用类型层次自动选择最优 | 需要定义标签类型层级 |
| 标准库广泛使用，成熟可靠 | 调试时不易追踪分派逻辑 |
| 与重载决议自然结合 | if constexpr 在多数场景更直观 |

> [!tip] 关键要点
> Tag Dispatch 的本质是**用类型系统表达编译时分支**。标签类型（如 `random_access_iterator_tag`）本身不携带数据，仅用于引导编译器选择正确的重载。C++17 的 `if constexpr` 已经能覆盖大部分 tag dispatch 场景，但标准库底层仍然使用 tag dispatch，理解它对阅读标准库源码至关重要。

## 相关链接

- [[cpp-sfinae-与编译期多态]] — SFINAE 与 tag dispatch 是互补技术
- [[cpp-策略设计]] — 两者都用于编译时行为选择
- [[cpp-crtp-奇异递归模板模式]] — 另一种编译时分派机制
