---
title: SIMD Intrinsics 实战
tags: [cpp, simd, intrinsics, sse, avx, vectorization]
aliases: [SIMD 内联函数, AVX intrinsics, 向量化编程]
created: 2026-04-05
updated: 2026-04-05
---

# SIMD Intrinsics 实战

**一句话概述：** SIMD intrinsics 是 CPU 向量指令的直接映射——`_mm256_add_ps` 对应 AVX 的 8 个 float 并行加法。比自动向量化更可控，比汇编更可读。性能提升可达 4-8 倍。

```cpp
#include <immintrin.h>

// 8 个 float 并行加法
float a[8], b[8], c[8];
__m256 va = _mm256_load_ps(a);   // 加载 8 个 float
__m256 vb = _mm256_load_ps(b);
__m256 vc = _mm256_add_ps(va, vb);  // 8 个加法同时执行
_mm256_store_ps(c, vc);             // 存回

// 数组求和（SSE/AVX 归约）
float sum_array(const float* data, size_t n) {
    __m256 sum = _mm256_setzero_ps();
    for (size_t i = 0; i + 8 <= n; i += 8) {
        __m256 v = _mm256_loadu_ps(data + i);
        sum = _mm256_add_ps(sum, v);
    }
    // 归约：8 个 float → 1 个
    float result[8];
    _mm256_storeu_ps(result, sum);
    float total = 0;
    for (int i = 0; i < 8; ++i) total += result[i];
    // 处理剩余元素
    for (size_t i = n & ~7; i < n; ++i) total += data[i];
    return total;
}
```

## 关键要点

> 数据必须对齐到 32 字节（AVX）或 16 字节（SSE）才能用 `_mm256_load_ps`（对齐加载）。不对齐时用 `_mm256_loadu_ps`（可能慢 1-2 周期，但现代 CPU 差异很小）。

> SIMD 优化的核心瓶颈通常是内存带宽而非计算。如果数据不在 cache 中，SIMD 的计算优势被内存延迟掩盖。

## 相关模式 / 关联

- [[cpp-缓存友好设计]] — 数据局部性
- [[cpp-并行算法]] — std::execution
- [[cpp-位运算深入]] — 位操作优化
