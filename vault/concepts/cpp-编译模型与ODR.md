---
title: 编译模型与 ODR
tags: [cpp, fundamentals, compilation, ODR, translation-unit, linker]
aliases: [编译模型, ODR, 单一定义规则, 编译单元, 链接, header]
created: 2026-04-04
updated: 2026-04-04
---

# 编译模型与 ODR

理解 C++ 的编译模型是解决"为什么编译出错"和"为什么链接出错"的根本。ODR（One Definition Rule）是贯穿整个编译链接过程的核心规则。

## 意图与场景

- 理解为什么头文件需要 include guard
- 理解声明与定义的区别
- 解决链接错误（multiple definition / undefined reference）

## 编译过程

```
源文件 (.cpp)
    ↓  预处理器（展开 #include, #define, #ifdef）
翻译单元（translation unit）
    ↓  编译器（语法分析、代码生成）
目标文件 (.o / .obj)
    ↓  链接器（解析符号引用）
可执行文件 / 库
```

## 声明 vs 定义

```cpp
// 声明：告诉编译器这个名字存在
extern int global_count;          // 变量声明
void foo(int x);                  // 函数声明
class Widget;                     // 前向声明（不完整类型）

// 定义：提供实体的完整信息
int global_count = 0;             // 变量定义
void foo(int x) { /* ... */ }     // 函数定义
class Widget { int x_; };         // 类定义
```

## ODR（单一定义规则）

```
1. 任何翻译单元中，一个变量/函数/类/模板/枚举只能有一个定义
2. 整个程序中，一个变量/函数/类只能有一个定义（ODR-use 的情况下）
3. 类型、模板、inline 函数/变量允许在多个翻译单元中有相同定义
```

```cpp
// header.h
#pragma once              // 或 #ifndef HEADER_H / #define HEADER_H

// OK：类定义可以在多个 TU 中重复（但必须完全一致）
class Widget {
    int x_;
public:
    void method();        // 声明
};

// OK：inline 函数可以在多个 TU 中定义
inline int square(int x) { return x * x; }

// OK：模板可以在多个 TU 中定义
template <typename T>
T maximum(T a, T b) { return (a > b) ? a : b; }

// ❌ 非 inline 函数定义不能放头文件
void Widget::method() { /* ... */ }  // 如果被多个 .cpp 包含 → 链接错误

// ❌ 全局变量定义不能放头文件
int global_var = 42;  // 多次 include → multiple definition
// 应改为：
inline int global_var = 42;  // C++17 inline variable
```

## include guard

```cpp
// 方式一：传统 guard
#ifndef MY_HEADER_H
#define MY_HEADER_H
// ... 内容 ...
#endif

// 方式二：pragma once（非标准但广泛支持）
#pragma once
// ... 内容 ...

// pragma once 更简洁，但某些边缘情况（符号链接、硬链接）可能失效
// 实践中两者都行，#pragma once 更常用
```

## 关键要点

> ODR 的核心：一个实体在整个程序中只能有一份定义（某些例外：类、模板、inline 函数/变量允许多份相同定义）。

> 链接错误通常源于违反 ODR：要么找不到定义（undefined reference），要么定义了多次（multiple definition）。

## 相关模式 / 关联

- [[cpp-命名空间]] — 命名空间与符号可见性
- [[cpp-模板编程基础]] — 模板的 ODR 例外
