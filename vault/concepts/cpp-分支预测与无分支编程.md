---
title: 分支预测与无分支编程
tags: [cpp, branch-prediction, branchless, cmov, optimization]
aliases: [无分支代码, 分支预测失败, CMOV 优化]
created: 2026-04-05
updated: 2026-04-05
---

# 分支预测与无分支编程

**一句话概述：** CPU 分支预测器猜对了就快（流水线继续），猜错了就慢（冲刷流水线，~15-20 周期代价）。无分支编程用 CMOV、位运算、查表消除条件跳转，在分支不可预测时显著提升性能。

```cpp
// 有分支（分支不可预测时慢）
int abs_branch(int x) {
    if (x < 0) return -x;
    return x;
}

// 无分支（无分支预测惩罚）
int abs_branchless(int x) {
    int mask = x >> 31;  // x < 0 → 0xFFFFFFFF, x >= 0 → 0x00000000
    return (x ^ mask) - mask;  // x < 0 → ~x + 1 = -x, x >= 0 → x
}

// 编译器通常自动优化简单 if 为 CMOV
int max_cmov(int a, int b) {
    return a > b ? a : b;  // -O2 下通常编译为 CMOV 指令
}
```

## 关键要点

> 无分支不总是更快——如果分支可预测（比如 99% 走同一路径），分支预测器几乎 100% 命中，普通 if 更快。无分支只在分支随机时有优势。

## 相关模式 / 关联

- [[cpp-条件传送-cmovcc]] — CMOV 汇编指令
- [[cpp-性能优化速查]] — 优化速查
- [[cpp-位运算深入]] — 位运算技巧
