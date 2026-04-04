---
title: C++ ABI 与二进制兼容
tags: [cpp, ABI, binary-compatibility, name-mangling, vtable-layout]
aliases: [ABI, 二进制兼容, name mangling, ABI稳定, 接口兼容]
created: 2026-04-04
updated: 2026-04-04
---

# ABI 与二进制兼容

ABI（Application Binary Interface）定义了编译后代码的约定——name mangling、调用约定、vtable 布局、数据结构布局。

## 什么是 ABI

```
ABI 包含：
- 函数调用约定（参数如何传递、返回值如何返回）
- Name mangling（函数名/类型名的编码规则）
- 数据类型大小和对齐
- vtable 布局（虚函数表的结构）
- 异常处理机制（表格式、栈展开）
- RTTI 格式
```

## 二进制兼容问题

```cpp
// ❌ 以下操作会破坏二进制兼容：
// 1. 给类添加虚函数（改变 vtable 布局）
// 2. 改变类的成员布局
// 3. 改变函数签名
// 4. 改变 inline 函数的实现
// 5. 改变模板的实现

// ✅ 兼容的操作：
// 1. 添加非虚成员函数
// 2. 添加 static 成员函数
// 3. 修改非 inline 函数的实现（在 .cpp 中）
// 4. 添加新的非虚类
```

## 确保 ABI 稳定

```cpp
// Pimpl 模式：私有成员变化不影响 ABI
class Widget {
    struct Impl;
    std::unique_ptr<Impl> impl_;  // 大小始终是指针大小
public:
    void method();  // 新增方法不影响 ABI
};

// 虚函数接口固定：用纯虚接口类
class IService {
public:
    virtual ~IService() = default;
    virtual void do_work() = 0;
    // 不添加新虚函数 → vtable 布局稳定
};
```

## 关键要点

> C++ 的 ABI 不稳定——添加虚函数、改变成员布局、改变 inline 函数都会破坏二进制兼容。Pimpl 和纯虚接口是维护 ABI 稳定的标准手段。

> 跨编译单元的 inline 函数是 ABI 隐患——改了实现但没重编译依赖方会导致 ODR 违反。

## 相关模式 / 关联

- [[cpp-Pimpl惯用法]] — ABI 稳定的核心技术
- [[cpp-与C互操作]] — extern "C" 的稳定 ABI
