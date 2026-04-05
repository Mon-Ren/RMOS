---
title: 红黑树与有序容器实现
tags: [cpp, stl, map, set, red-black-tree, balanced-bst]
aliases: [map 红黑树实现, set 底层结构, 有序容器原理]
created: 2026-04-05
updated: 2026-04-05
---

# 红黑树与有序容器实现

**一句话概述：** std::map/set 底层是红黑树——自平衡 BST，保证 O(log n) 查找/插入/删除。五条着色规则保证最长路径不超过最短路径的 2 倍。迭代器是中序遍历，天然有序。

## 红黑树五条性质

```
1. 每个节点要么红要么黑
2. 根节点是黑
3. 叶子节点（NIL）是黑
4. 红节点的两个子节点必须是黑（不能连续红）
5. 从任一节点到叶子的每条路径包含相同数目的黑节点

→ 最长路径 ≤ 2 × 最短路径 → O(log n)
```

## 关键要点

> map 的 O(log n) 查找在小数据集（<100）上可能比 unordered_map 的 O(1) 更快——因为红黑树的节点在内存中更紧凑（只需一个指针），cache 命中率高。

## 相关模式 / 关联

- [[cpp-map与set]] — map/set 用法
- [[cpp-算法-红黑树]] — 红黑树算法
- [[cpp-unordered-map]] — 哈希表对比
- [[cpp-flat-map与flat-set]] — flat 替代
