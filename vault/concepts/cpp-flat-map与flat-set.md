---
title: C++23 flat_map 与 flat_set
tags: [cpp23, flat-map, flat-set, sorted-vector, associative]
aliases: [flat_map, flat_set, 有序vector容器, sorted container]
created: 2026-04-04
updated: 2026-04-04
---

# flat_map 与 flat_set（C++23）

`flat_map` 基于有序 `vector` 实现——查找 O(log n) 但遍历和 cache 访问比 `map` 快得多。

## 基本用法

```cpp
#include <flat_map>

std::flat_map<std::string, int> scores;
scores["Alice"] = 95;
scores["Bob"] = 87;
scores.insert({"Charlie", 92});

// 查找 O(log n)
auto it = scores.find("Alice");

// 遍历有序（与 map 一致）
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << "\n";
}
```

## 与 map 的对比

```
                map (红黑树)         flat_map (有序 vector)
查找            O(log n)             O(log n) (二分查找)
插入            O(log n)             O(n) (需要移动元素)
删除            O(log n)             O(n)
遍历            较慢（指针跳转）      快（连续内存）
内存开销        高（每个节点3个指针）  低（连续内存）
cache 友好      差                   好
适用场景        频繁插入删除          查找和遍历为主
```

## 关键要点

> `flat_map` 在查找和遍历为主的场景比 `map` 快——连续内存对 cache 友好。但插入删除更慢。

> 建好后不再修改的数据用 `flat_map`——构建一次，反复查找。

## 相关模式 / 关联

- [[cpp-map与set]] — map 的详细使用
- [[cpp-缓存友好设计]] — cache 友好的重要性
