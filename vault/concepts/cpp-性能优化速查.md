---
title: C++ 性能优化速查
tags: [cpp, performance, optimization, quick-reference, tips]
aliases: [性能优化, 优化速查, performance tips, 快速参考]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 性能优化速查

性能优化的优先级：先对，再清晰，最后才快。

## 算法层面

```
O(n²) → O(n log n)    用排序代替嵌套循环
O(n)  → O(log n)      用哈希或二分查找
O(n)  → O(1)          用预计算/查表
```

## 数据结构

```
链表 → vector            连续内存，cache 友好
map → unordered_map      O(1) vs O(log n) 查找
vector → array           大小已知时避免动态分配
多态 → variant           避免虚函数调用
```

## 内存

```
频繁小分配 → 内存池/arena
指针追踪 → 连续数据结构
深拷贝 → 移动语义
string 拼接 → ostringstream 或预分配
```

## 函数调用

```
虚函数 → CRTP / if constexpr
std::function → auto lambda
小函数 → inline / 编译器自动内联
回调 → Lambda（可内联）
```

## 并发

```
锁争用 → 减小临界区
细粒度锁 → atomic
伪共享 → alignas(64)
线程创建 → 线程池
```

## 编译器

```
-O2          标准优化
-flto        链接时优化
-fprofile-generate/use  PGO
-march=native  利用目标 CPU 特性
```

## 关键要点

> 优化的黄金法则：先测量，再优化。90% 时间花在 10% 代码上——用 profiler 找瓶颈。

> 算法改进（O(n²)→O(n log n)）的收益永远大于微观优化。

## 相关模式 / 关联

- [[cpp-性能分析与基准测试]] — 测量方法
- [[cpp-缓存友好设计]] — cache 优化
