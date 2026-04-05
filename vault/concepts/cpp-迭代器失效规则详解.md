---
title: 迭代器失效规则详解
tags: [cpp, stl, iterator, invalidation, dangling-iterator]
aliases: [迭代器失效, 悬垂迭代器, iterator 失效规则]
created: 2026-04-05
updated: 2026-04-05
---

# 迭代器失效规则详解

**一句话概述：** 修改容器可能使迭代器失效——继续使用失效的迭代器是未定义行为。规则因容器而异：vector 的插入/扩容使所有迭代器失效，list 的插入不使任何迭代器失效，map 的插入不使任何迭代器失效。

## 各容器规则

```
vector:
  push_back: 未触发扩容→不失效；扩容→全部失效
  insert:    位置之后全部失效
  erase:     位置之后全部失效

deque:
  push_front/back: 全部失效
  insert:    全部失效
  erase:     全部失效

list/forward_list:
  insert:    不失效
  erase:     仅被删元素失效

map/set/multimap/multiset:
  insert:    不失效
  erase:     仅被删元素失效

unordered_*:
  insert:    可能触发 rehash→全部失效；不触发→不失效
  erase:     仅被删元素失效
```

## 关键要点

> 迭代器失效的常见陷阱：在 for 循环中 erase 时，erase 返回的是下一个有效迭代器，必须用 `it = v.erase(it)` 而非 `v.erase(it++)`。

## 相关模式 / 关联

- [[cpp-vector深入]] — vector 操作
- [[cpp-容器选择指南]] — 选择依据
- [[cpp-迭代器类别与适配器]] — 迭代器分类
