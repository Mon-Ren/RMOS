---
title: 迭代器类别与适配器
tags: [cpp, stl, iterator, iterator-category, adapter]
aliases: [迭代器, 迭代器类别, 迭代器适配器, reverse_iterator, back_inserter]
created: 2026-04-04
updated: 2026-04-04
---

# 迭代器类别与适配器

迭代器是 STL 算法与容器之间的桥梁——不同类别的迭代器决定了哪些算法可用。

## 迭代器类别

```
能力递增链（C++17 前）：

Input ──→ Forward ──→ Bidirectional ──→ RandomAccess
读一次     可多次读      可双向移动         可随机跳跃

C++20 新增：
Contiguous（连续迭代器）= RandomAccess + 内存连续
  vector, array, string 的迭代器是 Contiguous
```

```cpp
// 各类别支持的操作：
// Input:       *it, ++it, it++
// Forward:     上面 + it++, 可多次遍历同一范围
// Bidirectional: 上面 + --it, it--
// RandomAccess: 上面 + it[n], it + n, it - n, it1 - it2, <, >, <=, >=
// Contiguous:   上面 + 内存连续保证
```

## 容器与迭代器类别

```
容器              迭代器类别
───────────────────────────
vector           RandomAccess (C++20: Contiguous)
array            RandomAccess (C++20: Contiguous)
deque            RandomAccess
list             Bidirectional
set/map          Bidirectional
forward_list     Forward
unordered_*      Forward
istream_iterator Input
ostream_iterator Output
```

## 迭代器适配器

```cpp
#include <iterator>

// reverse_iterator：反向遍历
std::vector<int> v = {1, 2, 3, 4, 5};
for (auto it = v.rbegin(); it != v.rend(); ++it) {
    std::cout << *it << " ";  // 5 4 3 2 1
}

// 插入迭代器
std::vector<int> src = {1, 2, 3};
std::vector<int> dst;
std::copy(src.begin(), src.end(), std::back_inserter(dst));   // push_back
std::copy(src.begin(), src.end(), std::front_inserter(dst));  // push_front（需 deque/list）
std::copy(src.begin(), src.begin() + 2, std::inserter(dst, dst.begin()));  // insert

// move_iterator：移动元素而非拷贝
std::vector<std::string> src_s = {"hello", "world"};
std::vector<std::string> dst_s;
std::copy(std::make_move_iterator(src_s.begin()),
          std::make_move_iterator(src_s.end()),
          std::back_inserter(dst_s));
// src_s 现在处于 moved-from 状态

// count_iterator（C++20）
auto n = std::distance(v.begin(), std::find(v.begin(), v.end(), 3));
```

## 自定义迭代器（C++20 简化）

```cpp
#include <iterator>

// C++20 只需满足特定 concept
class RangeIter {
    int current_;
public:
    using iterator_category = std::forward_iterator_tag;
    using value_type = int;
    using difference_type = std::ptrdiff_t;

    explicit RangeIter(int start) : current_(start) {}
    int operator*() const { return current_; }
    RangeIter& operator++() { ++current_; return *this; }
    RangeIter operator++(int) { auto old = *this; ++current_; return old; }
    bool operator==(const RangeIter& other) const { return current_ == other.current_; }
};
```

## 关键要点

> 算法要求的迭代器类别决定了它能用于哪些容器。`std::sort` 需要 RandomAccess，所以不能用于 `list`（`list` 有自己的 `sort()` 方法）。

> 插入迭代器是算法输出到容器的桥梁——`back_inserter` 让你不用预分配大小。

## 相关模式 / 关联

- [[cpp-stl算法总览]] — 算法与迭代器的配合
- [[cpp-vector深入]] — Contiguous 迭代器
