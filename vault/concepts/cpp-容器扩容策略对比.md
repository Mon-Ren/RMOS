---
title: 容器扩容策略对比
tags: [cpp, stl, growth, reserve, capacity, strategy]
aliases: [容器预分配, reserve 策略, 容量管理]
created: 2026-04-05
updated: 2026-04-05
---

# 容器扩容策略对比

**一句话概述：** 不同容器的扩容策略不同——vector 翻倍、deque 分块分配、unordered_map 按素数增长。预分配（reserve）是消除扩容开销的最有效手段。

```cpp
// 10 万个元素的性能对比
std::vector<int> v;
v.reserve(100000);     // 1 次 malloc
for (int i = 0; i < 100000; ++i) v.push_back(i);

// vs 不 reserve
std::vector<int> v2;
for (int i = 0; i < 100000; ++i) v2.push_back(i);
// ~17 次扩容（2^17 = 131072 > 100000）
// 每次扩容：分配新内存 + 移动所有旧元素
// 总开销约比 reserve 版慢 5-10 倍
```

## 关键要点

> 如果能预估大小，永远先 reserve。在构造时直接传大小更好：`vector<int> v(100000);` 同时分配内存和初始化。

## 相关模式 / 关联

- [[cpp-vector-扩容策略与内存管理]] — vector 扩容
- [[cpp-容器选择指南]] — 选型
- [[cpp-new与delete深入]] — 内存分配
