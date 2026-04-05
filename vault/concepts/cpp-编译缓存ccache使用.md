---
title: 编译缓存 ccache 使用
tags: [cpp, ccache, build, cache, compilation, ci]
aliases: [ccache 加速编译, 编译缓存配置, 构建加速]
created: 2026-04-05
updated: 2026-04-05
---

# 编译缓存 ccache 使用

**一句话概述：** ccache 缓存编译结果（基于编译命令 + 源文件的 hash），相同输入直接返回缓存的 .o 文件。CI 中配合缓存存储，编译速度提升 3-10 倍。

```bash
# 安装
apt install ccache

# 使用：设置环境变量
export CC="ccache gcc"
export CXX="ccache g++"

# 或 CMake
cmake -DCMAKE_C_COMPILER_LAUNCHER=ccache \
      -DCMAKE_CXX_COMPILER_LAUNCHER=ccache ..

# 查看统计
ccache -s
# cache hit: 1542
# cache miss: 312
# hit rate: 83%
```

## 关键要点

> ccache 的缓存 key 包括：源文件内容、编译器路径、编译选项、包含的头文件内容。改任何头文件都会导致缓存失效——这就是前向声明和 Pimpl 减少编译依赖的价值。

## 相关模式 / 关联

- [[cpp-编译时间优化]] — 编译加速
- [[cpp-pimpl惯用法与编译时间]] — 编译防火墙
- [[cpp-CMake现代实践]] — CMake 配置
