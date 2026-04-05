---
title: CMake 现代实践
tags: [cpp, cmake, build, target, package, modern]
aliases: [现代 CMake, target-based, CMake 最佳实践]
created: 2026-04-05
updated: 2026-04-05
---

# CMake 现代实践

**一句话概述：** 现代 CMake（3.x+）的核心是 target——一切属性附着在 target 上，用 target_link_libraries 传播依赖。抛弃 include_directories/add_definitions 等全局命令，用 target_xxx 替代。

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 创建 target
add_library(mylib src/lib.cpp)
target_include_directories(mylib PUBLIC include)  # 传播给依赖者
target_compile_options(mylib PRIVATE -Wall -Wextra)

add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib)  # 自动传播 include 路径

# 查找包
find_package(fmt REQUIRED)
target_link_libraries(mylib PUBLIC fmt::fmt)
```

## 关键要点

> PUBLIC/PRIVATE/INTERFACE 的区别：PRIVATE 只影响当前 target，PUBLIC 影响当前 target 和依赖者，INTERFACE 只影响依赖者。

## 相关模式 / 关联

- [[cpp-CMake基础]] — CMake 基础
- [[cpp-编译优化与链接优化]] — 编译选项
