---
title: unordered_map 与 unordered_set
tags: [cpp, stl, hash, unordered_map, unordered_set, hashtable]
aliases: [unordered_map, unordered_set, 哈希表, 哈希容器, hash map]
created: 2026-04-04
updated: 2026-04-04
---

# unordered_map 与 unordered_set

基于哈希表实现，平均 O(1) 查找——比 map 快得多，但无序且需要哈希函数。

## 意图与场景

- 需要快速查找/插入/删除（平均 O(1)）
- 不需要有序遍历
- 大多数"查表"场景的默认选择

## 基本用法

```cpp
#include <unordered_map>
#include <unordered_set>

std::unordered_map<std::string, int> word_count;

// 插入与更新
word_count["hello"] = 1;                  // 下标访问
word_count.insert({"world", 2});          // insert
word_count.insert_or_assign("hello", 3);  // C++17
word_count.emplace("foo", 4);             // 原地构造

// 查找
auto it = word_count.find("hello");       // O(1) 平均
if (it != word_count.end()) {
    it->second = 5;                       // 修改值
}

// C++20
bool has = word_count.contains("hello");  // 简洁的包含检查

// 遍历（无序！顺序取决于哈希桶）
for (const auto& [key, val] : word_count) { }
```

## 自定义哈希

```cpp
struct Point {
    int x, y;
    bool operator==(const Point&) const = default;  // C++20
};

// 自定义哈希函数
struct PointHash {
    size_t operator()(const Point& p) const {
        auto h1 = std::hash<int>{}(p.x);
        auto h2 = std::hash<int>{}(p.y);
        return h1 ^ (h2 << 1);  // 组合哈希
    }
};

std::unordered_set<Point, PointHash> points;
points.insert({1, 2});
```

## 性能与桶管理

```cpp
std::unordered_map<int, int> m;

// 查看内部状态
m.bucket_count();        // 桶数
m.load_factor();         // 负载因子 = size / bucket_count
m.max_load_factor();     // 最大负载因子（默认 1.0）

// 负载因子 > max 时自动 rehash
m.reserve(1000);         // 预留空间，避免 rehash
m.rehash(1000);          // 直接设置桶数

// 高负载因子 → 冲突多 → 性能下降
// 保持负载因子 < 0.7 最佳
```

## 关键要点

> unordered_map 在大多数场景下比 map 快（O(1) vs O(log n)），但最坏情况是 O(n)（所有元素落入同一桶）。对用户自定义类型必须提供哈希函数。

> 需要有序遍历或范围查询时用 map；纯粹查表用 unordered_map。小数据量（< 100）时 map 可能更快（常数因子优势）。

## 相关模式 / 关联

- [[cpp-map与set]] — 有序版本
- [[算法-哈希表]] — 哈希表原理
