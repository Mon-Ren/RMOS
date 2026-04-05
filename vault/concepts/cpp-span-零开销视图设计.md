---
title: span 零开销视图设计
tags: [cpp20, span, view, array-view, zero-overhead]
aliases: [std::span, array_view, 连续内存视图]
created: 2026-04-05
updated: 2026-04-05
---

# span 零开销视图设计

**一句话概述：** std::span<T> 是连续内存的非拥有视图——一个指针 + 一个大小（16 字节），不拷贝数据、不分配内存。用它替代 `const T* data, size_t len` 参数对，或者替代 `const vector<T>&`（避免耦合到 vector 类型）。

```cpp
#include <span>
#include <vector>
#include <array>

// 接受任何连续内存
void process(std::span<const int> data) {
    for (int x : data) { /* ... */ }
}

std::vector<int> v = {1, 2, 3};
std::array<int, 3> a = {4, 5, 6};
int raw[] = {7, 8, 9};

process(v);    // ✅
process(a);    // ✅
process(raw);  // ✅
process(std::span<const int>{v.data() + 1, 2});  // ✅ 子范围
```

## 关键要点

> span 的危险：指向的内存可能被释放。span 不延长底层数据的生命周期——和 string_view 一样的悬垂引用风险。

> 固定大小的 span：`std::span<int, 3>` 编译期已知大小，不存储 size 字段，更省内存且允许编译器优化。

## 相关模式 / 关联

- [[cpp-span]] — span 基础
- [[cpp-string_view注意事项]] — 类似的非拥有视图
- [[cpp-容器选择指南]] — 参数传递选择
- [[cpp-range库]] — ranges 视图
