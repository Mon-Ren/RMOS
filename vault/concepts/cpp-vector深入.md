---
title: std::vector 深入
tags: [cpp, stl, vector, container, dynamic-array]
aliases: [vector, 动态数组, 向量, push_back, emplace_back]
created: 2026-04-04
updated: 2026-04-04
---

# std::vector 深入

`vector` 是 C++ 最常用的容器——连续内存、自动扩容、cache 友好。理解它的扩容策略和迭代器失效规则是写出正确高效代码的前提。

## 意图与场景

- 默认选择的序列容器（除非有明确理由选别的）
- 需要随机访问（O(1)）和尾部插入（摊还 O(1)）
- 数据需要连续存储（与 C API 互操作、cache 优化）

## 内存模型

```
vector 内部布局：
┌──────────────────────────────────────────┐
│  [start]──→  [  data  ][  data  ][...][  ]  │
│                       ↑              ↑       │
│                     begin()        end()     │
│                       ↑                      │
│              [size = 3, capacity = 5]        │
└──────────────────────────────────────────┘

size：已使用元素数
capacity：已分配内存能容纳的元素数
data()：返回底层数组指针
```

## 扩容策略

```cpp
std::vector<int> v;
// 大多数实现：capacity 按 1.5x 或 2x 增长

v.push_back(1);  // capacity: 1
v.push_back(2);  // capacity: 2（需要扩容：分配新内存、拷贝/移动、释放旧内存）
v.push_back(3);  // capacity: 4
v.push_back(4);  // capacity: 4
v.push_back(5);  // capacity: 8

// reserve 预分配避免多次扩容
v.reserve(1000);  // 一次性分配 1000 个元素的空间

// shrink_to_fit 释放多余容量（不保证）
v.shrink_to_fit();  // 建议释放，非强制
```

## 迭代器失效

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

// push_back：如果触发扩容，所有迭代器、指针、引用失效
//            如果不触发扩容，end() 之前的迭代器仍有效

// insert：插入点及之后的迭代器失效
auto it = v.begin() + 2;
v.insert(it, 99);  // it 现在无效！

// erase：被删点及之后的迭代器失效
auto it2 = v.begin();
while (it2 != v.end()) {
    if (*it2 % 2 == 0)
        it2 = v.erase(it2);  // erase 返回下一个有效迭代器
    else
        ++it2;
}

// clear：所有迭代器失效，但 capacity 不变
v.clear();  // size = 0, capacity 不变
```

## emplace_back vs push_back

```cpp
std::vector<std::pair<int, int>> v;

v.push_back({1, 2});          // 创建临时 pair，然后移动进 vector
v.emplace_back(1, 2);         // 在 vector 内存中直接构造 pair，省一次移动

// emplace 优势明显的场景：构造开销大的对象
std::vector<Widget> widgets;
widgets.emplace_back(arg1, arg2, arg3);  // 直接构造，不创建临时对象
```

## 关键要点

> vector 的 `data()` 返回连续内存指针，可以直接传给 C API（`memcpy`, `fread` 等）。迭代器失效规则必须牢记——扩容时所有迭代器、指针、引用全部失效。

> 已知大小时用 `reserve` 预分配避免多次扩容，已知大小时用 `resize` 或初始化列表。

## 相关模式 / 关联

- [[cpp-堆与栈内存]] — vector 的堆分配
- [[cpp-右值引用与移动语义]] — emplace_back 的原理
