---
title: deque 与 list
tags: [cpp, stl, deque, list, forward_list, linked-list, double-ended-queue]
aliases: [deque, list, forward_list, 双端队列, 链表, 双向链表]
created: 2026-04-04
updated: 2026-04-04
---

# deque 与 list

`deque` 和 `list` 是 vector 之外的两种序列容器——理解它们的内存模型和操作复杂度才能选对容器。

## std::deque

```cpp
#include <deque>

// deque：双端队列，分段连续内存
// - O(1) 头尾插入删除
// - O(1) 随机访问
// - 内存不连续（分段数组，中控数组管理）

std::deque<int> dq;
dq.push_back(1);    // O(1) 尾部插入
dq.push_front(0);   // O(1) 头部插入（vector 做不到）
dq.pop_back();      // O(1)
dq.pop_front();     // O(1)
dq[2];               // O(1) 随机访问

// 迭代器失效规则比 vector 宽松：
// - push_front/push_back 不会使已有迭代器失效（除非重新分配中控数组）
// - 首尾之外的 insert/erase 使所有迭代器失效
```

## std::list

```cpp
#include <list>

// list：双向链表
// - O(1) 任意位置插入删除（有迭代器时）
// - O(n) 随机访问
// - 每个元素额外存储两个指针

std::list<int> lst = {3, 1, 4, 1, 5};
lst.push_back(9);
lst.push_front(0);

// list 特有操作（O(1)，因为不移动元素）
auto it = std::next(lst.begin(), 2);
lst.splice(it, other_lst);    // 将 other_lst 的元素移到 it 前面
lst.remove(1);                // 删除所有值为 1 的元素
lst.unique();                 // 删除连续重复元素（先排序）
lst.sort();                   // list 专用排序（不支持 std::sort，因无随机访问迭代器）
lst.merge(other);             // 合并两个有序链表
lst.reverse();                // 反转

// ⚠️ list 的迭代器在 insert/splice 后仍然有效
auto it = lst.begin();
lst.insert(it, 99);  // it 仍然指向原来的元素
```

## std::forward_list（C++11）

```cpp
#include <forward_list>

// forward_list：单向链表，比 list 更省内存
// - 每个元素只存一个 next 指针
// - 无 size() 方法（保持 O(1) 实现）
// - 用 before_begin() 返回首元素前的"哨兵"迭代器

std::forward_list<int> flst = {1, 2, 3};
flst.push_front(0);           // O(1) 头部插入
flst.insert_after(flst.begin(), 99);  // 在第一个元素后插入
flst.erase_after(flst.begin());       // 删除第一个元素后的元素
```

## 容器选择

```
场景                    → 容器
─────────────────────────────────
需要随机访问 + 尾部插入 → vector
需要头尾插入删除         → deque
需要任意位置频繁插入删除 → list（但 vector 往往仍然更快）
单向链表 + 省内存        → forward_list
```

## 关键要点

> 除非真的需要频繁的中间插入/删除，否则 vector 几乎总是比 list 好——连续内存对 cache 友好，实际运行更快。`list::sort()` 存在是因为 `std::sort` 需要随机访问迭代器。

> `deque` 看起来像 vector+list 的折中，但它的内存分段特性意味着迭代器更复杂、常数因子更大。

## 相关模式 / 关联

- [[cpp-vector深入]] — 序列容器对比
- [[缓存与缓存行]] — 容器性能与 cache 的关系
