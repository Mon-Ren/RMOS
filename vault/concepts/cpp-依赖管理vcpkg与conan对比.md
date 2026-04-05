---
title: 依赖管理 vcpkg 与 Conan 对比
tags: [cpp, vcpkg, conan, package-manager, dependency]
aliases: [C++ 包管理, vcpkg 使用, Conan 使用]
created: 2026-04-05
updated: 2026-04-05
---

# 依赖管理 vcpkg 与 Conan 对比

**一句话概述：** vcpkg 更简单（微软维护、CMake 原生集成、manifest 模式）；Conan 更灵活（自定义 recipe、支持多种构建系统、私有仓库更好）。小团队用 vcpkg，大项目/企业用 Conan。

```
vcpkg:
  安装: apt install vcpkg 或 git clone
  使用: vcpkg.json manifest + CMake 集成
  优势: 零配置、Microsoft 维护、库数量多
  劣势: 不支持自定义 recipe、版本控制弱

Conan:
  安装: pip install conan
  使用: conanfile.py + conan install
  优势: 灵活的 recipe、版本管理好、私有仓库
  劣势: 学习曲线陡、配置多
```

## 关键要点

> 如果只是想用第三方库而不折腾，vcpkg 是更好的选择。如果需要发布自己的库、管理多个版本、或有私有依赖，Conan 更适合。

## 相关模式 / 关联

- [[cpp-CMake现代实践]] — CMake 构建
- [[cpp-编译缓存ccache使用]] — 编译加速
