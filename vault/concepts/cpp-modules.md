---
title: C++20 Modules
tags: [cpp20, module, import, export, header-unit, compilation]
aliases: [modules, 模块, import, export, 编译单元替代, 头文件替代]
created: 2026-04-04
updated: 2026-04-04
---

# C++20 Modules

Modules 是 C++ 头文件系统的现代替代——更快的编译、更好的封装、消除了 include 的各种问题。

## 意图与场景

- 替代头文件+include guard 的传统模式
- 加速编译（模块只编译一次，import 不重复解析）
- 更好的封装（export 控制可见性）

## 基本语法

```cpp
// math.cppm（模块接口单元）
export module math;  // 声明模块

export int add(int a, int b) {
    return a + b;
}

export class Calculator {
public:
    int compute(int a, int b);
};

// 未 export 的内容对导入者不可见
int internal_helper(int x) {
    return x * 2;
}
```

```cpp
// main.cpp（模块使用者）
import math;  // 导入模块（替代 #include "math.h"）

int main() {
    int r = add(1, 2);            // OK
    Calculator calc;               // OK
    // internal_helper(5);         // 编译错误：未 export
}
```

## 模块分区

```cpp
// math-basic.cppm
export module math:basic;  // 分区 :basic

export int add(int a, int b);
```

```cpp
// math-advanced.cppm
export module math:advanced;

import :basic;  // 导入同模块的分区

export int factorial(int n);
```

```cpp
// math.cppm（主模块接口）
export module math;

export import :basic;     // 重新导出分区
export import :advanced;
```

## 头文件单元（过渡方案）

```cpp
// 将传统头文件作为模块导入
import <vector>;           // 标准库模块
import "my_legacy.h";     // 自定义头文件作为模块

// 编译器需要支持 header units
// 这是迁移到 module 的过渡方案
```

## 关键要点

> Modules 消除了 include 的问题：重复包含、宏泄漏、编译顺序依赖、解析开销。但截至 2024 年，编译器和构建系统的支持仍在成熟中。

> 标准库的模块化版本：`import std;`（C++23）——替代 `#include <vector>` 等全部标准头文件。

## 相关模式 / 关联

- [[cpp-编译模型与ODR]] — modules 消除了许多 ODR 问题
- [[cpp-预处理器]] — modules 替代了大部分预处理器用法
