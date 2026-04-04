---
title: map 与 set（关联容器）
tags: [cpp, stl, map, set, tree, ordered, red-black-tree]
aliases: [map, set, multimap, multiset, 有序容器, 红黑树]
created: 2026-04-04
updated: 2026-04-04
---

# map 与 set

`std::map` 和 `std::set` 基于红黑树实现，有序存储，查找/插入/删除都是 O(log n)。

## 意图与场景

- 需要有序遍历的键值映射（map）或唯一集合（set）
- 需要范围查询（lower_bound / upper_bound）
- 键类型可以比较但不适合哈希时

## std::map

```cpp
#include <map>

std::map<std::string, int> scores;

// 插入
scores["Alice"] = 95;              // 下标：不存在则插入默认值再赋值
scores.insert({"Bob", 87});        // insert：已存在则不覆盖
scores.insert_or_assign("Bob", 90); // C++17：存在则覆盖
scores.emplace("Charlie", 92);     // 原地构造

// 查找
auto it = scores.find("Alice");    // O(log n)
if (it != scores.end()) {
    std::cout << it->second;       // 用迭代器访问
}

// ⚠️ 下标 vs find 的区别
int val = scores["Unknown"];       // 插入 {"Unknown", 0}！不想要这个行为用 find

// 范围查询
auto lo = scores.lower_bound("B"); // 第一个 >= "B" 的
auto hi = scores.upper_bound("D"); // 第一个 > "D" 的
// 遍历 [lo, hi) 得到范围内的所有元素

// 遍历（有序！按 key 升序）
for (const auto& [key, value] : scores) {
    std::cout << key << ": " << value << "\n";
}
```

## std::set

```cpp
#include <set>

std::set<int> nums = {3, 1, 4, 1, 5};  // {1, 3, 4, 5} — 自动去重排序

nums.insert(2);        // 插入
nums.erase(3);         // 删除
bool exists = nums.contains(4);  // C++20: O(log n) 查找

// lower_bound / upper_bound 用于范围
auto it = nums.lower_bound(3);
```

## 自定义比较

```cpp
// 自定义排序
std::set<int, std::greater<int>> desc = {1, 2, 3};  // {3, 2, 1}

// 自定义类型作为 key
struct Person {
    std::string name;
    int age;
};

struct PersonLess {
    bool operator()(const Person& a, const Person& b) const {
        return a.name < b.name;
    }
};

std::set<Person, PersonLess> people;
// C++20: 也可以用 lambda（需要捕获时）
auto cmp = [](const Person& a, const Person& b) { return a.name < b.name; };
std::set<Person, decltype(cmp)> people2(cmp);
```

## multimap / multiset

```cpp
std::multimap<std::string, int> grades;
grades.insert({"Alice", 95});
grades.insert({"Alice", 88});  // 允许重复 key

auto range = grades.equal_range("Alice");  // 返回 [begin, end) 范围
for (auto it = range.first; it != range.second; ++it) {
    std::cout << it->second << "\n";  // 95, 88
}
```

## 关键要点

> map 的 `operator[]` 在 key 不存在时会插入默认值——这是最常见的陷阱。只读访问用 `find()` 或 C++20 的 `contains()`。

> 需要有序遍历或范围查询用 map/set，不需要有序用 unordered_map/unordered_set（通常更快）。

## 相关模式 / 关联

- [[cpp-unordered-map]] — 无序版本，通常 O(1)
- [[算法-红黑树]] — map/set 的底层实现
