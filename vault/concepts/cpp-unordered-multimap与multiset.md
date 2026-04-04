---
title: C++ unordered_multimap 与 multiset
tags: [cpp, unordered_multimap, multiset, duplicate-keys, equal-range]
aliases: [unordered_multimap, multiset, 多键容器, equal_range, 相同键]
created: 2026-04-04
updated: 2026-04-04
---

# unordered_multimap 与 multiset

`unordered_multimap` 允许重复键——一个键对应多个值，哈希实现，平均 O(1) 查找。

## unordered_multimap

```cpp
#include <unordered_map>

std::unordered_multimap<std::string, int> grades;
grades.insert({"Alice", 95});
grades.insert({"Alice", 88});   // 允许重复键
grades.insert({"Bob", 72});

// 查找所有相同键的值
auto range = grades.equal_range("Alice");
for (auto it = range.first; it != range.second; ++it) {
    std::cout << it->second << "\n";  // 95, 88
}

// 统计键出现次数
size_t count = grades.count("Alice");  // 2

// 删除所有相同键的元素
grades.erase("Alice");  // 删除所有 Alice
```

## multiset

```cpp
#include <set>

std::multiset<int> nums = {3, 1, 4, 1, 5, 1};  // 允许重复
// {1, 1, 1, 3, 4, 5} — 有序

nums.insert(1);  // 可以插入重复值
nums.count(1);   // 4

// equal_range 找所有相同值
auto range = nums.equal_range(1);
for (auto it = range.first; it != range.second; ++it) {
    std::cout << *it << "\n";  // 1, 1, 1, 1
}
```

## 关键要点

> `multimap`/`multiset` 允许重复键，用 `equal_range` 获取所有相同键的元素范围。`erase(key)` 删除所有相同键的元素。

> 如果每个键只需要一个值，用 `map`/`set`——更强的语义保证。

## 相关模式 / 关联

- [[cpp-map与set]] — map/set 详细
- [[cpp-unordered-map]] — unordered_map 详细
