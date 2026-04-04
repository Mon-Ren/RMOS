---
title: 堆与栈内存
tags: [cpp, fundamentals, stack, heap, memory, allocation]
aliases: [堆内存, 栈内存, 动态分配, new, delete, stack vs heap]
created: 2026-04-04
updated: 2026-04-04
---

# 堆与栈内存

栈由编译器自动管理，堆由程序员显式管理——理解两者的区别是理解 C++ 性能和内存安全的基础。

## 意图与场景

- 局部变量用栈：快速、自动释放
- 大对象或动态大小用堆：生命周期不受作用域限制
- 性能敏感场景需要理解分配开销的差异

## 栈（Stack）

```cpp
void foo() {
    int x = 42;           // 栈分配——移动栈指针即可，极快
    int arr[100];         // 栈数组——大小必须编译期已知
    Widget w;             // 栈对象——离开作用域自动析构

    // 栈大小有限（通常 1-8 MB）
    // int huge[1000000];  // 可能栈溢出（Stack Overflow）
}
// 离开作用域，栈自动释放——无需手动管理
```

## 堆（Heap）

```cpp
// C++ 方式：new/delete（不推荐直接使用）
int* p = new int(42);           // 堆分配
int* arr = new int[100];        // 堆数组
delete p;                        // 释放单个对象
delete[] arr;                    // 释放数组（必须用 delete[]）

// 现代 C++ 方式：智能指针（推荐）
auto p = std::make_unique<int>(42);           // 自动释放
auto arr = std::make_unique<int[]>(100);      // 自动释放数组

// 堆分配开销：
// 1. 系统调用（brk/mmap 或 HeapAlloc）
// 2. 内存对齐处理
// 3. 碎片管理
// 比栈分配慢 10-100 倍
```

## 性能对比

```cpp
#include <chrono>

void benchmark() {
    auto start = std::chrono::high_resolution_clock::now();

    // 栈分配：约 1ns
    for (int i = 0; i < 1000000; ++i) {
        int x = i;
        (void)x;
    }

    auto mid = std::chrono::high_resolution_clock::now();

    // 堆分配：约 100ns/次
    for (int i = 0; i < 1000000; ++i) {
        auto p = std::make_unique<int>(i);
    }

    auto end = std::chrono::high_resolution_clock::now();
    // 栈 vs 堆：数量级差异
}
```

## 常见陷阱

```cpp
// ❌ 返回栈变量的指针/引用
int* bad() {
    int x = 42;
    return &x;  // 悬垂指针！x 已被销毁
}

// ❌ 内存泄漏
void leak() {
    int* p = new int(42);
    // 忘记 delete → 内存泄漏
}

// ❌ 双重释放
void double_free() {
    int* p = new int(42);
    delete p;
    delete p;  // 未定义行为！
}

// ❌ 数组 delete 不匹配
void mismatch() {
    int* arr = new int[100];
    delete arr;  // 应该是 delete[] arr
}
```

## 关键要点

> 栈分配接近零开销，但空间有限且生命周期受作用域限制。堆分配灵活但开销大且需要管理。现代 C++ 用智能指针消除手动管理。

> 性能敏感代码优先考虑栈分配或内存池，避免频繁的小块堆分配。

## 相关模式 / 关联

- [[cpp-智能指针详解]] — 堆内存的安全管理
- [[cpp-对象池模式]] — 避免频繁堆分配的方案
- [[cpp-new与delete]] — 自定义内存管理
