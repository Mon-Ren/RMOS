---
title: 编译期单元测试
tags: [cpp, constexpr, static-assert, compile-time-test, testing]
aliases: [编译期测试, constexpr 测试, static_assert 测试]
created: 2026-04-05
updated: 2026-04-05
---

# 编译期单元测试

**一句话概述：** 用 static_assert 在编译期验证函数的正确性——测试不通过直接编译失败，零运行时开销。配合 constexpr 函数，可以把大量逻辑的正确性验证放在编译阶段。

```cpp
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) result *= i;
    return result;
}

// 编译期测试
static_assert(factorial(0) == 1);
static_assert(factorial(1) == 1);
static_assert(factorial(5) == 120);
static_assert(factorial(10) == 3628800);
// 如果任何一行失败 → 编译错误，代码无法通过编译
```

## 关键要点

> 编译期测试只适用于 constexpr 函数。对于涉及 IO、多线程、运行时状态的代码，仍需要运行时测试。

## 相关模式 / 关联

- [[cpp-编译期校验与static_assert]] — static_assert
- [[cpp-constexpr-分配与编译期容器]] — 编译期计算
- [[cpp-测试基础]] — 测试概览
