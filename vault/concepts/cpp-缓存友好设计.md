---
title: 缓存友好设计
tags: [cpp, cache, cache-line, false-sharing, locality, prefetch]
aliases: [cache友好, 缓存行, false sharing, 数据局部性, prefetch, cache优化]
created: 2026-04-04
updated: 2026-04-04
---

# 缓存友好设计

现代 CPU 的性能瓶颈往往不在计算而在内存访问——缓存友好设计让数据访问模式匹配 CPU 缓存。

## 缓存层次

```
L1 缓存：~32KB，~1ns
L2 缓存：~256KB，~3ns
L3 缓存：~8MB，~10ns
主内存：~GB，~100ns

缓存行：通常 64 字节——一次读取的最小单位
```

## 数据局部性

```cpp
// ❌ 缓存不友好：链表遍历
std::list<int> lst;
for (auto it = lst.begin(); it != lst.end(); ++it)
    sum += *it;  // 每个节点可能在不同缓存行 → 频繁 cache miss

// ✅ 缓存友好：连续遍历
std::vector<int> vec;
for (auto x : vec)
    sum += x;  // 连续内存 → 预取有效 → 极少 cache miss

// 实测：遍历 1000 万元素
// vector：~1ms
// list：~10ms（10倍差距来自缓存）
```

## 避免 False Sharing

```cpp
// ❌ False sharing：不同线程访问同一缓存行的不同变量
struct Bad {
    std::atomic<int> counter1;  // 线程 1 写
    std::atomic<int> counter2;  // 线程 2 写
    // 在同一缓存行 → 互相干扰 → 性能灾难
};

// ✅ 缓存行对齐
struct alignas(64) Good {
    std::atomic<int> counter1;  // 独占缓存行
};
struct alignas(64) Good2 {
    std::atomic<int> counter2;  // 独占缓存行
};

// C++17: hardware_destructive_interference_size
struct Best {
    alignas(std::hardware_destructive_interference_size) std::atomic<int> counter1;
    alignas(std::hardware_destructive_interference_size) std::atomic<int> counter2;
};
```

## SoA vs AoS

```cpp
// AoS（Array of Structures）：对象数组
struct Particle { float x, y, z, vx, vy, vz; };
std::vector<Particle> particles;  // x,y,z 相邻

// SoA（Structure of Arrays）：数组结构
struct Particles {
    std::vector<float> x, y, z;    // 所有 x 相邻
    std::vector<float> vx, vy, vz;
};
// SoA 对 SIMD 和只访问部分字段的场景更 cache 友好
```

## 关键要点

> 连续内存（vector、array）比链式结构（list、tree）对 cache 友好——差距可达 10 倍。

> False sharing 是多线程性能的隐形杀手——用 `alignas(64)` 让不同线程的热数据在不同缓存行。

## 相关模式 / 关联

- [[cpp-vector深入]] — 连续内存的 cache 友好性
- [[cpp-sizeof与内存对齐]] — 对齐
