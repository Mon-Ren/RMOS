---
title: unordered_map 实现原理与扩容
tags: [cpp, stl, unordered-map, hash-table, rehash, bucket]
aliases: [哈希表扩容, rehash 机制, 桶管理]
created: 2026-04-05
updated: 2026-04-05
---

# unordered_map 实现原理与扩容

**一句话概述：** std::unordered_map 是链地址法哈希表——数组（桶）+ 链表（每个桶一个链表或开放寻址）。load factor 超过 max_load_factor 时触发 rehash：分配新的更大的桶数组，重新插入所有元素。rehash 的 O(n) 成本是性能抖动的根源。

## 内部结构

```
unordered_map<int, string>
buckets_:
[0] → (42,"a") → nullptr
[1] → nullptr
[2] → (7,"b") → (15,"c") → nullptr  ← hash 冲突，链表解决
[3] → nullptr
[4] → (9,"d") → nullptr

bucket_count = 5
size = 4
load_factor = 4/5 = 0.8
```

## rehash 触发条件

```cpp
std::unordered_map<int, int> m;
m.max_load_factor();  // 默认 1.0

// 触发 rehash 的场景：
// 1. insert 后 load_factor > max_load_factor
// 2. 显式调用 rehash(n) 或 reserve(n)

// 性能建议：提前 reserve
m.reserve(10000);  // 预分配桶，避免插入时反复 rehash
```

## 关键要点

> rehash 的性能影响：10 万个元素的 rehash 大约 1-5ms（取决于元素大小和哈希函数）。在延迟敏感的路径上，应该在热路径前调用 reserve()。

> 自定义哈希函数的质量直接影响性能。差的哈希函数导致元素集中到少数桶 → 链表变长 → O(1) 退化为 O(n)。

## 相关模式 / 关联

- [[cpp-算法-哈希表原理]] — 哈希表数据结构
- [[cpp-unordered容器的哈希与桶]] — 哈希函数设计
- [[cpp-map与set]] — 红黑树 vs 哈希表
- [[cpp-容器选择指南]] — 容器选型
