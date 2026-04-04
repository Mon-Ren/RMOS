---
title: C++ 编译器特定扩展
tags: [cpp, compiler-extension, gcc, clang, msvc, attribute, builtin]
aliases: [编译器扩展, gcc扩展, clang扩展, msvc扩展, __attribute__, __declspec]
created: 2026-04-04
updated: 2026-04-04
---

# 编译器特定扩展

编译器提供非标准扩展——用条件编译封装以保持跨平台兼容。

## GCC/Clang 扩展

```cpp
// 函数属性
__attribute__((always_inline))    // 强制内联
__attribute__((noinline))         // 禁止内联
__attribute__((deprecated("msg"))) // 标记弃用
__attribute__((pure))             // 无副作用（只读全局状态）
__attribute__((const))            // 无副作用（不读全局状态）
__attribute__((hot))              // 标记热函数
__attribute__((cold))             // 标记冷函数
__attribute__((aligned(64)))      // 对齐
__attribute__((packed))           // 紧凑排列

// 变量属性
int x __attribute__((aligned(64)));
int arr[10] __attribute__((section(".data")));

// 预定义宏
__GNUC__, __GNUC_MINOR__         // GCC 版本
__clang__, __clang_major__       // Clang 版本
__has_builtin(x)                 // 检查内建函数
__has_include(<header>)          // 检查头文件
```

## MSVC 扩展

```cpp
__declspec(dllexport)     // 导出 DLL 符号
__declspec(dllimport)     // 导入 DLL 符号
__declspec(align(64))     // 对齐
__declspec(noinline)      // 禁止内联
__forceinline             // 强制内联
__debugbreak()            // 调试断点
__pragma(...)             // _Pragma 等价
```

## 跨平台封装

```cpp
// 统一属性宏
#if defined(__GNUC__) || defined(__clang__)
    #define FORCE_INLINE __attribute__((always_inline)) inline
    #define NO_INLINE __attribute__((noinline))
    #define ALIGNED(x) __attribute__((aligned(x)))
    #define PACKED __attribute__((packed))
    #define LIKELY(x) __builtin_expect(!!(x), 1)
    #define UNLIKELY(x) __builtin_expect(!!(x), 0)
#elif defined(_MSC_VER)
    #define FORCE_INLINE __forceinline
    #define NO_INLINE __declspec(noinline)
    #define ALIGNED(x) __declspec(align(x))
    #define PACKED  // MSVC 用 #pragma pack
    #define LIKELY(x) (x)
    #define UNLIKELY(x) (x)
#else
    #define FORCE_INLINE inline
    #define NO_INLINE
    #define ALIGNED(x) alignas(x)
    #define PACKED
    #define LIKELY(x) (x)
    #define UNLIKELY(x) (x)
#endif
```

## 关键要点

> 编译器扩展只在特定编译器下有效——跨平台代码必须用条件编译封装。C++20 的 `[[likely]]`、`[[nodiscard]]` 等属性正在替代部分扩展。

> `__attribute__((pure))` 和 `__attribute__((const))` 帮助编译器优化——可以做公共子表达式消除。

## 相关模式 / 关联

- [[cpp-属性]] — C++ 标准属性
- [[cpp-编译器内建函数]] — 内建函数
