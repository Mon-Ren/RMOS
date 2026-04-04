---
title: 位运算深入
tags: [cpp, bit-manipulation, bitwise, bitmask, set, clear]
aliases: [位运算, 位操作, bitmask, 位掩码, set bit, clear bit, toggle]
created: 2026-04-04
updated: 2026-04-04
---

# 位运算深入

位运算是底层编程的基本工具——标志位管理、位集合、位图、哈希组合都离不开它。

## 基本运算符

```cpp
// & 与：两位都为1则1
// | 或：任一位为1则1
// ^ 异或：不同则1
// ~ 取反：0变1，1变0
// << 左移：高位丢弃，低位补0
// >> 右移：低位丢弃，高位补符号位（有符号）或0（无符号）

unsigned int a = 0b1010;
unsigned int b = 0b1100;

a & b   // 0b1000 (8)
a | b   // 0b1100 (12)
a ^ b   // 0b0100 (4)
~a      // 0xFFFFFFF5
a << 2  // 0b101000 (40)
a >> 1  // 0b0101 (5)
```

## 常用位操作技巧

```cpp
// 设置第 n 位
flags |= (1u << n);

// 清除第 n 位
flags &= ~(1u << n);

// 切换第 n 位
flags ^= (1u << n);

// 检查第 n 位
bool is_set = (flags >> n) & 1;
bool is_set2 = flags & (1u << n);

// 检查是否为 2 的幂
bool is_pow2 = n && !(n & (n - 1));

// 计算最低位的 1（lowbit）
int lowbit = n & (-n);  // 或 n & (~n + 1)

// 去掉最低位的 1
n &= (n - 1);

// 统计 1 的个数
int popcount = __builtin_popcount(n);  // GCC/Clang
int popcount2 = std::popcount(n);      // C++20

// 枚举所有子集
int mask = 0b1011;
int subset = mask;
do {
    // process subset
    subset = (subset - 1) & mask;
} while (subset != mask);
```

## std::bitset

```cpp
#include <bitset>

std::bitset<32> flags;
flags.set(3);          // 设置第3位
flags.reset(3);        // 清除第3位
flags.flip(3);         // 切换第3位
flags.test(3);         // 检查第3位
flags.count();         // 统计1的个数
flags.to_ulong();      // 转为 unsigned long
flags.to_string();     // 转为字符串 "00000000..."
```

## 关键要点

> 位运算是零开销的标志位管理方式。`std::bitset` 提供安全的封装，`std::popcount`（C++20）提供跨平台的 1 计数。

> 有符号整数的右移是实现定义的（算术右移 vs 逻辑右移）。用 `unsigned` 类型做位操作避免歧义。

## 相关模式 / 关联

- [[cpp-基本数据类型]] — 整数类型
- [[cpp-枚举类型]] — 位标志枚举
