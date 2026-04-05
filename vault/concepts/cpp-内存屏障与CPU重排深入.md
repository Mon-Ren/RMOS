---
title: 内存屏障与 CPU 重排深入
tags: [system, memory-barrier, cpu-reorder, store-buffer, tso]
aliases: [CPU 重排序, store buffer, 内存屏障硬件]
created: 2026-04-05
updated: 2026-04-05
---

# 内存屏障与 CPU 重排深入

**一句话概述：** 现代 CPU 会重排内存操作（乱序执行 + store buffer），编译器也会重排指令。内存屏障同时约束两者——硬件屏障阻止 CPU 重排，编译器屏障阻止编译器重排。x86 的 TSO 模型天然保证了很多顺序（store-load 除外）。

```
x86 TSO 模型的保证：
✅ Store-Store 不重排
✅ Load-Load 不重排
✅ Load-Store 不重排
❌ Store-Load 可以重排（通过 store buffer）

需要显式屏障的场景：
Store-Load：需要 mfence 或 lock 前缀
```

## 关键要点

> x86 上的优化提示：mfence 比 lfence/sfence 慢得多。如果只需要 Store-Store 屏障，用 SFENCE；如果需要全序，用 lock add（比 mfence 快）。

## 相关模式 / 关联

- [[cpp-memory-order实战剖析]] — 内存序实战
- [[cpp-atomic与内存序]] — 原子操作
- [[cpp-内存模型与数据竞争]] — C++ 内存模型
