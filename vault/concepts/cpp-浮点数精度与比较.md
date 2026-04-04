---
title: C++ 浮点数精度与比较
tags: [cpp, float, double, precision, comparison, epsilon, IEEE-754]
aliases: [浮点精度, 浮点比较, epsilon, IEEE-754, 浮点误差]
created: 2026-04-04
updated: 2026-04-04
---

# 浮点数精度与比较

浮点数不是精确的——直接用 `==` 比较浮点数是 bug 的常见来源。

## 精度问题

```cpp
// 浮点数不是精确的
double a = 0.1 + 0.2;
double b = 0.3;
a == b;  // false！a ≈ 0.30000000000000004

// 误差累积
double sum = 0.0;
for (int i = 0; i < 100; ++i) sum += 0.1;
sum == 10.0;  // false！
```

## 安全比较

```cpp
// 方式 1：相对误差
bool nearly_equal(double a, double b, double epsilon = 1e-9) {
    if (a == b) return true;  // 精确相等或都是 0
    double diff = std::abs(a - b);
    double largest = std::max(std::abs(a), std::abs(b));
    return diff <= largest * epsilon;
}

// 方式 2：绝对误差（值较小时）
bool close(double a, double b, double tolerance = 1e-9) {
    return std::abs(a - b) <= tolerance;
}

// 方式 3：ULP 比较（Units in the Last Place）
#include <cmath>
bool ulp_equal(float a, float b, int max_ulps = 4) {
    return std::abs(std::bit_cast<int32_t>(a) - std::bit_cast<int32_t>(b)) <= max_ulps;
}

// Google Test 的方式
EXPECT_FLOAT_EQ(0.1f + 0.2f, 0.3f);   // 允许 4 ULP 误差
EXPECT_DOUBLE_EQ(a, b);                 // 允许 4 ULP 误差
EXPECT_NEAR(a, b, 0.001);              // 绝对误差 <= 0.001
```

## 关键要点

> 永远不要用 `==` 直接比较浮点数——用相对误差、绝对误差或 ULP 比较。

> IEEE-754 浮点数有特殊值：`NaN`、`+Inf`、`-Inf`、`-0.0`。`NaN != NaN`（永远为 false），任何与 NaN 的比较都是 false。

## 相关模式 / 关联

- [[cpp-基本数据类型]] — float/double 类型
- [[cpp-调试技术与断言]] — EXPECT_FLOAT_EQ
