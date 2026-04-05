---
title: 内存对齐与结构体布局优化
tags: [cpp, alignment, struct-layout, padding, cache-line]
aliases: [结构体对齐, 字段排序优化, alignas]
created: 2026-04-05
updated: 2026-04-05
---

# 内存对齐与结构体布局优化

**一句话概述：** 结构体字段的声明顺序直接影响大小——按对齐要求从大到小排列字段可以最小化 padding。`alignas` 可强制对齐到 cache line 以避免 false sharing。

```cpp
// ❌ 差的布局（16 字节，4 字节 padding）
struct Bad {
    char a;     // 1 字节
    // 3 字节 padding
    int b;      // 4 字节
    char c;     // 1 字节
    // 3 字节 padding
    int d;      // 4 字节
};  // sizeof = 16

// ✅ 好的布局（12 字节）
struct Good {
    int b;      // 4 字节
    int d;      // 4 字节
    char a;     // 1 字节
    char c;     // 1 字节
    // 2 字节 padding
};  // sizeof = 12

// 对齐到 cache line
struct alignas(64) Padded {
    std::atomic<int> counter;
    // 60 字节 padding → 独占一个 cache line
};
```

## 关键要点

> 编译器不会帮你重排字段（因为 C++ 保证字段按声明顺序布局）。手动排序是你的责任。工具如 pahole 可以分析结构体布局。

## 相关模式 / 关联

- [[cpp-sizeof与内存对齐]] — 对齐规则
- [[cpp-缓存友好设计]] — cache 优化
- [[cpp-伪共享与填充]] — false sharing
