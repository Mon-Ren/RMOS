---
title: 容器选择指南
tags: [cpp, stl, container, selection, performance, decision-tree]
aliases: [容器选择, 容器选型, container selection, decision tree, STL容器对比]
created: 2026-04-04
updated: 2026-04-04
---

# 容器选择指南

选对容器比优化代码更重要——错误的容器选择会让所有优化都徒劳。

## 决策流程

```
需要键值对？
  ├─ 需要有序遍历/范围查询 → map / multimap
  └─ 不需要有序 → unordered_map / unordered_set
需要有序集合？
  └─ set / multiset
不需要键值对？
  ├─ 需要随机访问？
  │   ├─ 大小固定 → array
  │   └─ 大小可变 → vector（默认选择！）
  ├─ 需要频繁头尾操作？
  │   └─ deque
  └─ 需要频繁中间插入删除？
      └─ list（但先试试 vector——cache 友好往往更快）
```

## 性能特性对比

```
容器              随机访问  头插入  尾插入  中间插入  内存布局
──────────────────────────────────────────────────────────
vector            O(1)     —       O(1)*   O(n)      连续
deque             O(1)     O(1)    O(1)    O(n)      分段连续
list              O(n)     O(1)    O(1)    O(1)      链式
forward_list      —        O(1)    —       O(1)*     单链
array             O(1)     —       —       —         连续
map               O(log n) —       —       O(log n)  红黑树
unordered_map     O(1)*    —       —       O(1)*     哈希桶
```

* = 摊还或平均

## 默认选择：vector

```cpp
// vector 几乎总是对的：
// 1. 连续内存 → cache 友好
// 2. 随机访问 O(1)
// 3. 尾部插入摊还 O(1)
// 4. 与 C API 互操作（data() 返回连续指针）
// 5. 内存紧凑

// 什么时候不用 vector：
// - 需要 O(1) 头插入 → deque
// - 需要稳定迭代器（插入删除不使迭代器失效）→ list
// - 需要有序查找 → set/map
// - 需要 O(1) 查找 → unordered_map
// - 大小编译期确定 → array
```

## 关键要点

> 默认用 vector，有明确需求时再换。不要因为"可能需要频繁中间插入"就选 list——实测 vector 往往更快（cache 效应）。

> 小数据量（< 1000）时容器选择影响不大，可以优先考虑代码清晰度。

## 相关模式 / 关联

- [[cpp-vector深入]] — 默认容器
- [[cpp-map与set]] — 有序容器
- [[cpp-unordered-map]] — 哈希容器
