---
title: sizeof 与内存对齐
tags: [cpp, fundamentals, sizeof, alignment, padding, alignof]
aliases: [sizeof, 内存对齐, padding, 对齐, alignof, alignas]
created: 2026-04-04
updated: 2026-04-04
---

# sizeof 与内存对齐

内存对齐是硬件效率的要求——CPU 读取对齐的数据比未对齐的快数倍，结构体中的 padding 就是为了满足对齐要求。

## 意图与场景

- 理解结构体的实际内存占用（比成员大小之和大）
- 性能优化：合理排列成员减少 padding
- 与硬件/网络协议交互时精确控制内存布局

## sizeof 基础

```cpp
// sizeof 返回对象或类型占用的字节数（编译期常量）
sizeof(int);           // 通常 4
sizeof(double);        // 通常 8
sizeof(char);          // 总是 1

// sizeof 不评估表达式（不调用函数）
int x = 0;
sizeof(++x);           // x 仍为 0，++x 未执行
sizeof(x++);           // x 仍为 0

// 数组
int arr[10];
sizeof(arr);           // 40（10 * sizeof(int)）

// 指针
int* p = arr;
sizeof(p);             // 8（64位系统上的指针大小）
```

## 对齐规则

```cpp
// 每个类型有对齐要求（alignment requirement）
alignof(int);          // 通常 4
alignof(double);       // 通常 8
alignof(char);         // 1

// 结构体的对齐 = 最大成员的对齐要求
struct Example {
    char  a;    // 1 字节 + 3 字节 padding
    int   b;    // 4 字节（对齐到 4）
    char  c;    // 1 字节 + 7 字节 padding
    double d;   // 8 字节（对齐到 8）
};
// sizeof(Example) = 24，不是 1+4+1+8=14

// 合理排列可以减少 padding：
struct Packed {
    double d;   // 8 字节
    int    b;   // 4 字节
    char   a;   // 1 字节
    char   c;   // 1 字节 + 2 字节 padding
};
// sizeof(Packed) = 16，比 Example 更紧凑
```

## alignas（C++11）

```cpp
// 强制指定对齐
alignas(16) int aligned_int;       // 16 字节对齐
alignas(64) struct CacheLine {     // 64 字节对齐（缓存行）
    int data[16];
};

// 对齐到另一个类型的对齐值
struct alignas(double) MyStruct {
    int x;  // 结构体整体按 double 对齐
};
```

## 关键要点

> 结构体大小 >= 各成员大小之和，多出的部分是 padding。成员按声明顺序从低地址排列，每个成员的地址必须是其对齐值的倍数。

> 大成员在前、小成员在后的排列方式能最小化 padding——这是 cache 友好的基本技巧。

## 相关模式 / 关联

- [[cpp-基本数据类型]] — 各类型的大小和对齐
- [[缓存与缓存行]] — 缓存行对齐的性能意义
