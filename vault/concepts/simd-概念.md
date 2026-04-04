---
title: SIMD 概念
tags: [assembly, simd, parallel, performance]
aliases: [SIMD, 单指令多数据, 数据级并行]
created: 2026-04-04
updated: 2026-04-04
---

SIMD（Single Instruction, Multiple Data）是一种**数据级并行**范式——一条指令同时处理多个数据元素，是现代 CPU 高性能计算的核心机制。

## 基本思想

```
标量运算：                          SIMD 运算：
  for i in 0..3:                      一条指令：
    c[i] = a[i] + b[i]               [c0,c1,c2,c3] = [a0,a1,a2,a3] + [b0,b1,b2,b3]
  (4 条 ADD 指令)                     (1 条 ADDPS 指令)
```

**关键洞察**：如果多个数据元素执行相同操作，将它们"打包"到宽寄存器中一次性处理。

## 数据级并行 vs 线程级并行

| 维度 | SIMD (数据级) | 多线程 (线程级) |
|------|--------------|----------------|
| 并行粒度 | 指令级 | 线程级 |
| 开销 | 几乎为零 | 线程创建/同步 |
| 适用范围 | 紧密循环、同构运算 | 任务并行 |
| 硬件 | ALU 宽度 | 多核 |
| 工具 | SSE/AVX/NEON | pthreads/OMP |
| 编译器 | auto-vectorize / 内联 | 编译指令 |

## 打包运算 vs 标量运算

```c
// 标量版本
void add_scalar(float *c, float *a, float *b, int n) {
    for (int i = 0; i < n; i++)
        c[i] = a[i] + b[i];
}

// SIMD 版本（SSE，每次处理 4 个）
void add_simd(float *c, float *a, float *b, int n) {
    for (int i = 0; i < n; i += 4) {
        __m128 va = _mm_load_ps(&a[i]);    // 加载 4 个 float
        __m128 vb = _mm_load_ps(&b[i]);
        __m128 vc = _mm_add_ps(va, vb);    // 一条指令加 4 个
        _mm_store_ps(&c[i], vc);           // 存回
    }
}

// AVX 版本（每次处理 8 个）
void add_avx(float *c, float *a, float *b, int n) {
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_store_ps(&c[i], vc);
    }
}
```

## x86 SIMD 演进

```
MMX (1997)     → 64 位，8 个 MM 寄存器，整数 SIMD
SSE (1999)     → 128 位，8 个 XMM，单精度浮点
SSE2 (2001)    → 双精度浮点 + 整数 SIMD
SSE3 (2004)    → 水平加减、数据移动
SSSE3 (2006)   → 洗牌、绝对值
SSE4 (2007)    → 点积、字符串操作
AVX (2011)     → 256 位 YMM，VEX 前缀
AVX2 (2013)    → 整数 256 位 SIMD
FMA3 (2013)    → 融合乘加
AVX-512 (2017) → 512 位 ZMM，掩码寄存器

ARM:
NEON (2005)    → 128 位 Q 寄存器
SVE (2016)     → 可变长度向量
```

## 应用场景

```c
// 1. 图像处理 — 像素逐元素运算
// 反色：pixel = 255 - pixel
__m128i pixels = _mm_load_si128(ptr);
__m128i maxval = _mm_set1_epi8(255);
__m128i result = _mm_sub_epi8(maxval, pixels);  // 16 个字节同时反色

// 2. 矩阵运算 — 点积
float dot_product(float *a, float *b, int n) {
    __m256 sum = _mm256_setzero_ps();
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);
        __m256 vb = _mm256_load_ps(&b[i]);
        sum = _mm256_fmadd_ps(va, vb, sum);  // sum += va * vb
    }
    // 水平归约
    float result[8];
    _mm256_store_ps(result, sum);
    return result[0]+result[1]+result[2]+result[3]+result[4]+result[5]+result[6]+result[7];
}

// 3. 字符串搜索 — 每次比较 16 个字符
// memchr 的 SIMD 优化版本

// 4. 密码学 — AES-NI 指令
// vaesenc — AES 轮加密，一条指令
```

## 性能分析

### 理论加速比

```
SSE (128-bit, float): 128/32 = 4x
AVX (256-bit, float): 256/32 = 8x
AVX-512 (512-bit, float): 512/32 = 16x
```

### 实际限制

```
1. 内存带宽 — 瓶颈往往不在计算
   - CPU 计算快于从内存读取
   - 缓存命中率是关键

2. 数据依赖 — 不是所有运算都可并行
   - 归约操作（sum, max）需要水平合并
   - 交叉依赖打破向量化

3. 数据对齐 — 非对齐访问有惩罚
   - 16/32 字节对齐的数组才能高效处理

4. SIMD/SSE/AVX 切换惩罚
   - 混用不同指令集需要 vzeroupper
```

## 编译器自动向量化

```c
// 编译器通常能自动向量化简单循环
// gcc -O3 -march=native -ftree-vectorize

void scale(float *a, float k, int n) {
    for (int i = 0; i < n; i++)
        a[i] *= k;  // 编译器会自动使用 SIMD
}

// 查看是否向量化成功
// gcc -fopt-info-vec -O3 ...
```

## 关键要点

> **SIMD = 一条指令处理 N 个数据**：128 位处理 4 个 float，256 位处理 8 个。本质上是用更宽的 ALU 实现数据级并行。

> **与多线程互补**：SIMD 是单核内的并行（ALU 宽度），多线程是多核间的并行。两者可以叠加。

> **内存带宽是实际瓶颈**：理论 8 倍加速并不意味着 8 倍提速——如果你受限于内存读取，SIMD 帮助有限。

> **对齐 + 避免标量尾巴**：数据需要对齐到 SIMD 寄存器宽度；尾部不足一次处理量的元素需标量处理。

## 关联

- [[SSE 指令集]]
- [[AVX 指令集]]
- [[汇编优化技巧]]
- [[缓存与缓存行]]
