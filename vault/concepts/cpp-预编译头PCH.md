---
title: C++ 预编译头（PCH）
tags: [cpp, PCH, precompiled-header, build-time, compilation]
aliases: [预编译头, PCH, precompiled header, 编译加速头文件]
created: 2026-04-04
updated: 2026-04-04
---

# 预编译头（PCH）

PCH 预先解析常用头文件——减少重复解析，加速大型项目的编译。

## 创建与使用

```cpp
// pch.h：列出频繁使用的头文件
#pragma once
#include <vector>
#include <string>
#include <memory>
#include <algorithm>
#include <iostream>
#include <map>
#include <functional>
#include <thread>
#include <mutex>

// 编译 PCH
// GCC/Clang:
// g++ -x c++-header pch.h -o pch.h.gch

// 使用 PCH
// g++ -include pch.h main.cpp
// 或在 CMake 中设置
```

## CMake 集成

```cmake
# CMake 3.16+
target_precompile_headers(myapp PRIVATE
    <vector>
    <string>
    <memory>
    <algorithm>
    <iostream>
)

# 共享 PCH（多个 target 共用）
add_library(pch_lib INTERFACE)
target_precompile_headers(pch_lib INTERFACE
    <vector>
    <string>
)
target_link_libraries(myapp PRIVATE pch_lib)
```

## 注意事项

```
PCH 的限制：
- 只对重复包含的头文件有效
- PCH 文件与编译器/选项绑定（不同选项需重新生成）
- 增量编译时 PCH 可能反而变慢（PCH 文件大，加载慢）
- 不适合头文件频繁变化的项目

最佳实践：
- 只放稳定的标准库头文件
- 不放项目自有头文件（变化频繁）
- 与 LTO 结合效果最佳
```

## 关键要点

> PCH 对大型项目（数百个源文件）有显著编译加速——标准库头文件解析一次，后续源文件直接使用。

> CMake 3.16+ 的 `target_precompile_headers` 是管理 PCH 的标准方式。

## 相关模式 / 关联

- [[cpp-编译时间优化]] — 编译加速
- [[cpp-modules]] — Modules 是 PCH 的现代替代
