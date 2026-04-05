---
title: benchmark 陷阱与正确方法
tags: [cpp, benchmark, google-benchmark, measurement, pitfalls]
aliases: [性能测试陷阱, 基准测试方法, benchmark 正确姿势]
created: 2026-04-05
updated: 2026-04-05
---

# benchmark 陷阱与正确方法

**一句话概述：** 性能测试最常见的错误：(1) 编译器优化掉了被测代码、(2) 没有预热 cache、(3) 样本量太小、(4) 在 debug 模式下测。用 Google Benchmark 并正确使用 `DoNotOptimize` 和 `KeepRunning`。

```cpp
#include <benchmark/benchmark.h>

// ❌ 错误：编译器可能把整个循环优化掉
void bad_bench() {
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 1000000; ++i) {
        int x = i * 2;  // 编译器：这个值没被使用 → 删掉
    }
    // 测到的是空循环
}

// ✅ 正确：用 Google Benchmark
static void BM_vector_push(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> v;
        for (int i = 0; i < state.range(0); ++i) {
            v.push_back(i);
        }
        benchmark::DoNotOptimize(v);  // 防止优化掉
    }
}
BENCHMARK(BM_vector_push)->Arg(1000)->Arg(10000)->Arg(100000);
```

## 关键要点

> 基准测试的黄金法则：(1) 用 Release 模式编译、(2) 热循环至少跑 1 秒、(3) 报告中位数而非平均值、(4) 用 DoNotOptimize 防止编译器优化。

## 相关模式 / 关联

- [[cpp-性能分析与基准测试]] — 性能分析
- [[cpp-性能优化速查]] — 优化清单
