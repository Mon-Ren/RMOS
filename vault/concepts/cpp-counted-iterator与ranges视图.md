---
title: std::counted_iterator 与 std::ranges
tags: [cpp20, counted_iterator, ranges, iota-view, views]
aliases: [counted_iterator, iota_view, ranges视图, 惰性视图]
created: 2026-04-04
updated: 2026-04-04
---

# counted_iterator 与 ranges 视图

`counted_iterator` 把迭代器和计数打包——让不满足 sized_sentinel 的迭代器也能用 ranges 算法。

## counted_iterator

```cpp
#include <iterator>

int arr[] = {1, 2, 3, 4, 5};
// 将原生指针包装为 counted_iterator，限制遍历 3 个元素
auto it = std::counted_iterator(arr, 3);
// *it = 1, *++it = 2, *++it = 3, ++it 到达末尾

// 常用场景：配合 ranges 算法
auto counted = std::counted_iterator(v.begin(), 5);
auto last = std::default_sentinel;
auto result = std::ranges::find(counted, last, 42);
```

## 常用视图

```cpp
namespace rv = std::views;

// iota：惰性整数序列
for (int i : rv::iota(0, 10)) { /* 0,1,2,...,9 */ }
for (int i : rv::iota(0) | rv::take(5)) { /* 0,1,2,3,4 */ }

// repeat（C++23）：重复值
auto threes = rv::repeat(3) | rv::take(5);  // 3,3,3,3,3

// empty：空视图
auto ev = rv::empty<int>;

// single：单元素视图
auto sv = rv::single(42);

// 组合
auto squares = rv::iota(1)
    | rv::transform([](int n) { return n * n; })
    | rv::take(10);  // 1,4,9,16,...,100
```

## 关键要点

> `counted_iterator` + `default_sentinel` 组合让指针也能参与 ranges 算法——不需要知道范围大小的迭代器对也能表达有限遍历。

> `iota_view` 是惰性生成的整数序列——零内存开销，按需生成。

## 相关模式 / 关联

- [[cpp-range库]] — Ranges 管道
- [[cpp-迭代器类别与适配器]] — 迭代器基础
