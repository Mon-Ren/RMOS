---
title: 数据导向设计实战
tags: [cpp, data-oriented, SoA, AoS, cache, game-engine]
aliases: [DOD, SoA vs AoS, 数据布局优化]
created: 2026-04-05
updated: 2026-04-05
---

# 数据导向设计实战

**一句话概述：** 面向对象按"职责"组织数据（AoS），数据导向按"访问模式"组织数据（SoA）。游戏引擎和高性能计算用 SoA：处理位置时只加载位置数组，不加载不需要的其他字段。

```cpp
// AoS（Array of Structures）- OOP 风格
struct Particle { float x, y, z, vx, vy, vz, mass, life; };
Particle particles[100000];
// 更新位置：遍历时每次加载 32 字节（x,y,z,vx,vy,vz,mass,life）
// 但只需要 x,y,z,vx,vy,vz → 浪费 cache line 的 25%

// SoA（Structure of Arrays）- DOD 风格
struct Particles {
    float x[100000], y[100000], z[100000];
    float vx[100000], vy[100000], vz[100000];
    float mass[100000], life[100000];
};
// 更新位置：只遍历 x[], y[], z[], vx[], vy[], vz[]
// 每个数组连续 → cache 命中率 100%

// 性能差异：SoA 在遍历子集字段时快 2-5 倍
```

## 关键要点

> SoA 不是总是更好——如果总是访问所有字段，AoS 更简单且编译器优化更友好。SoA 的优势只在"只访问部分字段"时体现。

## 相关模式 / 关联

- [[cpp-缓存友好设计]] — cache 友好性
- [[cpp-SIMD-Intrinsics实战]] — SIMD 与 SoA 天然配合
- [[cpp-性能优化速查]] — 优化清单
