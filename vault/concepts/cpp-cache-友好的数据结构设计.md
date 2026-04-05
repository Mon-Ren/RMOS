---
title: cache 友好的数据结构设计
tags: [cpp, cache, locality, data-structure, hot-cold-split]
aliases: [缓存友好设计, 数据结构 cache 优化, 冷热分离]
created: 2026-04-05
updated: 2026-04-05
---

# cache 友好的数据结构设计

**一句话概述：** cache 友好的核心原则：热数据连续存放、减少间接寻址、避免指针追踪。链表的每个节点可能在不同的 cache line → 遍历链表比遍历数组慢 10 倍以上。flat_map 用有序数组替代红黑树就是 cache 优化的典型案例。

```cpp
// ❌ 链表：每个节点独立分配，cache 命中率低
std::list<int> lst;

// ✅ 向量：连续内存，cache 命中率 100%
std::vector<int> vec;

// hot-cold 分离：频繁访问的字段放前面
struct Player {
    // hot：每帧都访问
    float x, y, z;
    float vx, vy, vz;
    // cold：偶尔访问
    std::string name;
    int player_id;
    std::vector<Achievement> achievements;
};
```

## 关键要点

> B-树比红黑树更 cache 友好——每个节点存多个键（填满一个 cache line），一次内存加载比较多个键。这就是数据库索引用 B-树而不是红黑树的原因。

## 相关模式 / 关联

- [[cpp-缓存友好设计]] — 缓存基础
- [[cpp-数据导向设计实战]] — DOD 设计
- [[cpp-flat-map与flat-set]] — flat 容器
- [[cpp-性能优化速查]] — 优化清单
