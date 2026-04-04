---
title: 构建系统与 CMake 基础
tags: [cpp, cmake, build-system, compilation, linking, target]
aliases: [CMake, 构建系统, build system, target, 编译配置]
created: 2026-04-04
updated: 2026-04-04
---

# 构建系统与 CMake 基础

CMake 是 C++ 事实标准的构建系统生成器——它不直接编译，而是生成 Makefile/Ninja/VS 项目。

## 基本 CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp LANGUAGES CXX)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 可执行文件
add_executable(myapp main.cpp utils.cpp)

# 库
add_library(mylib STATIC lib.cpp helper.cpp)     # 静态库
add_library(myshared SHARED lib.cpp)              # 动态库

# 链接
target_link_libraries(myapp PRIVATE mylib)
target_link_libraries(myapp PRIVATE Threads::Threads)  # 系统库

# 头文件路径
target_include_directories(mylib PUBLIC include/)
# PUBLIC：使用 mylib 的目标也获得此路径
# PRIVATE：仅 mylib 自身
```

## 现代 CMake（target-based）

```cmake
# ✅ 现代方式：以 target 为中心
add_executable(app main.cpp)
target_compile_features(app PRIVATE cxx_std_20)
target_compile_options(app PRIVATE -Wall -Wextra -O2)
target_include_directories(app PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_link_libraries(app PRIVATE mylib fmt::fmt)

# ❌ 旧方式：全局设置（不推荐）
set(CMAKE_CXX_FLAGS "-Wall -Wextra")
include_directories(include)
```

## 常用命令

```bash
# 配置
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake -B build -DCMAKE_BUILD_TYPE=Debug

# 编译
cmake --build build -j$(nproc)

# 安装
cmake --install build --prefix /usr/local

# 清理
cmake --build build --target clean
```

## 条件编译

```cmake
# 编译选项
option(ENABLE_TESTS "Build tests" ON)
if(ENABLE_TESTS)
    add_subdirectory(tests)
endif()

# 平台检测
if(WIN32)
    target_link_libraries(myapp PRIVATE ws2_32)
elseif(UNIX)
    target_link_libraries(myapp PRIVATE pthread)
endif()

# 编译器检测
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(myapp PRIVATE -Wall -Wextra)
elseif(MSVC)
    target_compile_options(myapp PRIVATE /W4)
endif()
```

## 关键要点

> 现代 CMake 以 target 为中心——`target_compile_options`、`target_link_libraries` 等设置只影响特定 target。

> `PRIVATE`/`PUBLIC`/`INTERFACE` 控制依赖传递：`PUBLIC` = 自己用 + 依赖者也用，`PRIVATE` = 仅自己用。

## 相关模式 / 关联

- [[cpp-编译模型与ODR]] — 编译链接基础
- [[cpp-modules]] — C++20 模块与构建系统
