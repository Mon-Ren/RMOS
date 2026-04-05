---
title: 自定义 allocator 实战
tags: [cpp, allocator, memory, pool, monotonic, pmr]
aliases: [自定义分配器, 内存分配器, PMR 分配器]
created: 2026-04-05
updated: 2026-04-05
---

# 自定义 allocator 实战

**一句话概述：** 自定义 allocator 让你控制 STL 容器的内存分配——monotonic allocator（一次性分配、批量释放）、pool allocator（固定大小块复用）、tracking allocator（监控分配量）。C++17 的 PMR 让切换分配器更方便。

## Monotonic Buffer Allocator（C++17 PMR）

```cpp
#include <memory_resource>
#include <vector>

// 栈上缓冲区
char buffer[1024 * 1024];  // 1MB 栈上空间
std::pmr::monotonic_buffer_resource pool{buffer, sizeof(buffer)};

// vector 使用栈上内存
std::pmr::vector<int> v{&pool};
for (int i = 0; i < 10000; ++i) v.push_back(i);
// 零 malloc 调用——所有内存来自 buffer
// pool 析构时一次性释放，不用逐个 free
```

## 关键要点

> PMR 的价值：不改容器类型（还是 vector<int>），只换分配器。适合临时计算、帧内分配等"用完即弃"的场景。

## 相关模式 / 关联

- [[cpp-allocator与PMR]] — PMR 基础
- [[cpp-内存池分配器]] — 内存池设计
- [[cpp-placement-new与内存管理分层]] — 内存分层
- [[cpp-容器选择指南]] — 容器选型
