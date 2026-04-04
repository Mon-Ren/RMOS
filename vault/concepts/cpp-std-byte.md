---
title: C++ std::byte（C++17）
tags: [cpp17, byte, raw-memory, type-safe, bitwise]
aliases: [std::byte, 原始字节, 字节类型, byte操作]
created: 2026-04-04
updated: 2026-04-04
---

# std::byte（C++17）

`std::byte` 是表示原始内存的类型——不做算术、不隐式转换为整数，只支持位操作。

## 基本用法

```cpp
#include <cstddef>

std::byte b{0xFF};  // 从整数字面量初始化
std::byte b2{0b1010'0101};

// 位操作
auto result = b & b2;    // 位与
auto result2 = b | b2;   // 位或
auto result3 = b ^ b2;   // 异或
auto result4 = ~b;       // 取反

// 移位
auto shifted = b << 3;   // 左移
auto shifted2 = b >> 1;  // 右移

// ❌ 不支持算术
// b + b2;  // 编译错误
// b * 2;   // 编译错误

// ❌ 不隐式转换为整数
// int n = b;  // 编译错误
int n = std::to_integer<int>(b);  // 必须显式转换

// 与 unsigned char 互转
unsigned char uc = 0x42;
auto b = std::byte{uc};
auto uc2 = std::to_integer<unsigned char>(b);
```

## 使用场景

```cpp
// 原始内存操作
std::byte buffer[1024];
std::memset(buffer, 0, sizeof(buffer));  // OK：byte 可以传给 memset

// 位标志
std::byte flags{0};
flags |= std::byte{1} << 0;  // 设置第 0 位
flags |= std::byte{1} << 3;  // 设置第 3 位
bool bit3 = (flags & (std::byte{1} << 3)) != std::byte{0};
```

## 关键要点

> `std::byte` 的设计意图：表达"这是原始数据，不做算术"——比 `unsigned char` 或 `uint8_t` 更有语义。

> 需要算术时用整数类型，需要原始字节操作时用 `std::byte`。

## 相关模式 / 关联

- [[cpp-基本数据类型]] — 类型选择
- [[cpp-位运算深入]] — 位操作
