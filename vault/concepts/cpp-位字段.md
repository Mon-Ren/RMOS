---
title: C++ 位字段
tags: [cpp, bitfield, struct-bitfield, packed, memory-layout]
aliases: [位字段, bitfield, 位域, struct位域, 比特字段]
created: 2026-04-04
updated: 2026-04-04
---

# 位字段（Bitfield）

位字段让结构体的成员只占用指定数量的位——用于硬件寄存器映射和紧凑存储。

## 基本用法

```cpp
struct Flags {
    unsigned int read    : 1;  // 1 位
    unsigned int write   : 1;  // 1 位
    unsigned int execute : 1;  // 1 位
    unsigned int mode    : 4;  // 4 位
    unsigned int reserved : 25; // 25 位
};

Flags f = {1, 0, 1, 3, 0};
f.read = 1;
f.mode = 7;  // 超出范围时行为是实现定义的

sizeof(Flags);  // 通常 4 字节（32位刚好放得下）
```

## 命名位字段（C++20）

```cpp
// C++20: 匿名位字段用于对齐
struct Packet {
    unsigned int type : 4;
    unsigned int      : 4;  // 填充 4 位
    unsigned int data : 8;
    unsigned int      : 0;  // 强制对齐到下一个存储单元边界
    unsigned int seq  : 16;
};
```

## 与 std::bitset 对比

```
                位字段                    std::bitset
定义方式        struct 成员                独立类型
大小            编译期确定                 编译期确定
可变大小        不支持                     支持（模板参数）
运算            逐成员访问                 位运算、count、to_string
移植性          实现定义的布局             保证一致
```

## 关键要点

> 位字段的内存布局是实现定义的——不同编译器、不同平台可能不同。用于硬件映射时要查阅编译器文档。

> 大部分场景用 `std::bitset` 或枚举位标志更安全——位字段只在需要精确控制内存布局时使用。

## 相关模式 / 关联

- [[cpp-位运算深入]] — 位操作
- [[cpp-sizeof与内存对齐]] — 内存布局
