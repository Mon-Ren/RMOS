---
title: vector 扩容策略与内存管理
tags: [cpp, stl, vector, capacity, growth-factor, reallocation]
aliases: [vector 扩容, capacity 管理, vector 内存策略]
created: 2026-04-05
updated: 2026-04-05
---

# vector 扩容策略与内存管理

**一句话概述：** vector 扩容时 capacity 的增长因子决定了性能特性——GCC/Clang 用 2x、MSVC 用 1.5x。2x 更少的重新分配次数但更多的内存浪费；1.5x 能复用之前释放的内存块（数学可证：1.5x 的累积分配永远不会超过 2 倍最终大小）。

## 扩容机制

```cpp
std::vector<int> v;
// 初始 capacity = 0

v.push_back(1);  // capacity = 1
v.push_back(2);  // capacity = 2 (翻倍)
v.push_back(3);  // capacity = 4 (翻倍)
v.push_back(4);  // capacity = 4 (够用)
v.push_back(5);  // capacity = 8 (翻倍)

// GCC 的增长策略：capacity *= 2
// MSVC：capacity = capacity * 3 / 2 (1.5x)

// 手动控制
v.reserve(100);   // 预分配，避免多次扩容
v.shrink_to_fit(); // 释放多余容量（非绑定请求）
```

## 关键要点

> vector 扩容时需要拷贝/移动所有元素 + 释放旧内存。如果元素的移动构造不是 noexcept，扩容时可能降级为拷贝（move_if_noexcept）。

> capacity 不会随元素减少自动缩小——erase 后 capacity 不变。需要手动 shrink_to_fit() 或 swap 技巧释放内存。

## 相关模式 / 关联

- [[cpp-vector深入]] — vector 更多细节
- [[cpp-容器选择指南]] — 容器选型
- [[cpp-move-if-noexcept与强异常保证]] — 扩容异常安全
- [[cpp-new与delete深入]] — 堆分配
