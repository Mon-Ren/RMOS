---
title: ABI 稳定性与版本管理
tags: [cpp, abi, binary-compatibility, symbol-versioning, library]
aliases: [ABI 兼容性, 二进制兼容, SONAME]
created: 2026-04-05
updated: 2026-04-05
---

# ABI 稳定性与版本管理

**一句话概述：** C++ 没有稳定的 ABI——添加虚函数改变 vtable 布局、改变类大小影响内存布局、改 inline 函数需要重编译。库的版本管理用 SONAME 控制 ABI 版本，SOVERSION 控制链接。

```
libfoo.so.1.2.3
├── libfoo.so.1    ← SONAME（ABI 版本，程序链接时用）
├── libfoo.so      ← 开发用符号链接
└── .1.2.3         ← 实际文件

规则：ABI 兼容 = 相同 SONAME
  添加虚函数 → ABI 不兼容 → SONAME 版本 +1
  添加非虚成员函数（在末尾）→ ABI 兼容
  改变类大小 → ABI 不兼容
  改变 inline 函数 → 需重编译但 ABI 可能兼容
```

## 关键要点

> Pimpl 是保持 ABI 公开稳定的最佳实践——Impl 类的所有变化都不影响公开头文件的二进制布局。

## 相关模式 / 关联

- [[cpp-ABI与二进制兼容]] — ABI 基础
- [[cpp-pimpl-惯用法]] — 编译防火墙
- [[cpp-动态链接与PLT-GOT]] — 动态链接
