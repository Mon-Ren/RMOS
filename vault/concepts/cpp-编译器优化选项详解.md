---
title: 编译器优化选项详解
tags: [cpp, compiler, optimization, gcc, clang, flags]
aliases: [编译优化级别, GCC 优化选项, 编译器 flags]
created: 2026-04-05
updated: 2026-04-05
---

# 编译器优化选项详解

**一句话概述：** -O2 是生产环境的标准选择（平衡优化和编译时间）。-O3 激进优化（循环展开、向量化）可能增大代码体积。-Os 优化体积。-Ofast 牺牲标准合规换速度（可能改变浮点行为）。

```
-O0: 不优化，调试用（默认）
-O1: 基础优化
-O2: 推荐生产用（含内联、循环优化、向量化提示）
-O3: 激进（更多内联、循环展开、SIMD、函数合并）
-Os: 优化体积
-Ofast: -O3 + 违反 IEEE 浮点标准（-ffast-math）
-Og: 调试友好的优化（保留变量、控制流）
-flto: 链接时优化（跨编译单元内联）
-fprofile-generate/-fprofile-use: PGO
```

## 关键要点

> -Ofast 的 -ffast-math 会打破 NaN/Inf 的 IEEE 行为、改变浮点结合律。科学计算和金融代码应该避免。

## 相关模式 / 关联

- [[cpp-编译优化与链接优化]] — 编译优化
- [[cpp-Link-Time-Optimization]] — LTO
- [[cpp-PGO-Profile-Guided]] — PGO
