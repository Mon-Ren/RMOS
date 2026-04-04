---
title: 性能分析与基准测试
tags: [cpp, performance, profiling, benchmark, optimization, perf]
aliases: [性能分析, profiling, benchmark, 基准测试, perf, 性能优化]
created: 2026-04-04
updated: 2026-04-04
---

# 性能分析与基准测试

"过早优化是万恶之源"——但不做分析就优化更糟糕。先测量，再优化。

## 基准测试

```cpp
#include <chrono>

// 基本计时
auto start = std::chrono::high_resolution_clock::now();
// ... 被测代码 ...
auto end = std::chrono::high_resolution_clock::now();

auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
std::cout << "Time: " << duration.count() << " ns\n";

// Google Benchmark（推荐）
// #include <benchmark/benchmark.h>
// static BM_VectorPush(benchmark::State& state) {
//     for (auto _ : state) {
//         std::vector<int> v;
//         for (int i = 0; i < state.range(0); ++i)
//             v.push_back(i);
//     }
// }
// BENCHMARK(BM_VectorPush)->Range(8, 1<<20);
```

## 常用工具

```
Linux：
- perf stat：CPU 计数器统计
- perf record/report：采样分析
- valgrind/cachegrind：缓存行为分析
- heaptrack：内存分配跟踪
- callgrind/kcachegrind：调用图分析

macOS：
- Instruments（Xcode）
- dtrace

通用：
- Google Benchmark：C++ 基准测试框架
- Tracy：实时帧分析器
- VTune：Intel 性能分析器
```

## 性能瓶颈定位

```
常见瓶颈（按概率排序）：
1. 不必要的拷贝 → 用移动语义、引用
2. 缓存不友好 → 连续内存、数据局部性
3. 频繁小分配 → 内存池、reserve
4. 虚函数开销 → CRTP、if constexpr
5. 算法复杂度 → 换算法
6. 锁争用 → 无锁结构、减少临界区
7. 分支预测失败 → 查找表、cmov
```

## 关键要点

> 先用分析工具找瓶颈（通常 90% 时间花在 10% 代码上），再针对性优化。不要凭直觉优化。

> 基准测试要稳定：固定环境、多次运行取中位数、避免冷启动。Google Benchmark 自动处理这些。

## 相关模式 / 关联

- [[cpp-编译优化与链接优化]] — 编译器优化
- [[缓存与缓存行]] — cache 友好设计
