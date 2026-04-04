---
title: 编译器内建函数
tags: [cpp, builtin, compiler-intrinsic, gcc, clang, msvc, optimization]
aliases: [内建函数, compiler builtin, intrinsic, __builtin, 编译器扩展]
created: 2026-04-04
updated: 2026-04-04
---

# 编译器内建函数

编译器提供特殊内建函数——它们映射到硬件指令或提供标准库做不到的功能。

## GCC/Clang 内建

```cpp
// 位操作
__builtin_popcount(x);        // 统计 1 的位数（C++20: std::popcount）
__builtin_clz(x);             // 前导零个数
__builtin_ctz(x);             // 尾随零个数
__builtin_ffs(x);             // 最低 1 的位置（从 1 开始）

// 预期分支提示
if (__builtin_expect(condition, 1)) {  // 预期 condition 为 true
    // 热路径
}
// C++20: if (condition) [[likely]] { }

// 不可达代码标记
__builtin_unreachable();      // 告诉编译器此路径不可能执行
// 用于优化 switch 的 default 分支

// 类型特征
__builtin_types_compatible_p(T, U)  // 编译期检查类型兼容性
__builtin_constant_p(x)            // x 是否是编译期常量

// 内存操作
__builtin_memcpy(dst, src, n)      // 编译器可能优化为 SIMD 指令
__builtin_memset(dst, val, n)
```

## MSVC 内建

```cpp
// 位操作
__popcnt(x);                  // 统计 1 的位数
__lzcnt(x);                   // 前导零
__tzcnt(x);                   // 尾随零

// 字节序
_byteswap_ulong(x);           // 字节翻转

// 内存屏障
_ReadWriteBarrier();          // 编译器内存屏障
_mm_mfence();                 // CPU 内存屏障（需要 <intrin.h>）
```

## 跨平台封装

```cpp
// 封装内建函数为跨平台代码
inline int popcount(unsigned int x) {
#if defined(__GNUC__) || defined(__clang__)
    return __builtin_popcount(x);
#elif defined(_MSC_VER)
    return __popcnt(x);
#else
    // 纯 C++ 实现
    int count = 0;
    while (x) { x &= x - 1; ++count; }
    return count;
#endif
}
// C++20: std::popcount 替代上述所有
```

## 关键要点

> 内建函数让 C++ 能利用编译器特殊能力——位操作、分支预测、SIMD 等。C++20 的 `<bit>` 头文件替代了大部分位操作内建。

> 内建函数是编译器特定的——需要跨平台时封装为统一接口，用条件编译选择实现。

## 相关模式 / 关联

- [[cpp-位运算深入]] — 位操作
- [[cpp-编译优化与链接优化]] — 编译器优化
