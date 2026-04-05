---
title: deque 分段连续内存剖析
tags: [cpp, stl, deque, segmented-memory, push-front]
aliases: [deque 实现, 分段连续, 双端队列原理]
created: 2026-04-05
updated: 2026-04-05
---

# deque 分段连续内存剖析

**一句话概述：** deque 是"分段连续"的双端队列——中控器（map）管理多个固定大小的数据块，首尾都能 O(1) 插入。代价是随机访问比 vector 慢（需要两次间接寻址），迭代器更复杂（4 个指针）。

```
deque 的分段结构：
map_（中控指针数组）:
  [0] → [块: 4个元素]
  [1] → [块: 4个元素]  ← start_ 在这里
  [2] → [块: 4个元素]
  [3] → [块: 4个元素]  ← finish_ 在这里

随机访问 operator[](i):
  1. 计算在哪个块：block = (start_offset + i) / block_size
  2. 计算块内偏移：offset = (start_offset + i) % block_size
  3. 两次间接：map_[block][offset]
  → 比 vector 多一次间接，cache 友好性差
```

## 关键要点

> deque 的适用场景：需要频繁在首尾插入删除（如 BFS 的队列、滑动窗口）。如果只在尾部操作，vector 更好。

## 相关模式 / 关联

- [[cpp-vector深入]] — vector 对比
- [[cpp-栈队列与优先队列]] — queue 默认用 deque
- [[cpp-容器选择指南]] — 选型指南
