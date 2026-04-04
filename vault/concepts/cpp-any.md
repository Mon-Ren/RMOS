---
title: std::any（C++17）
tags: [cpp17, any, type-erasure, dynamic-type]
aliases: [any, 任意类型, type-erased, 动态类型容器]
created: 2026-04-04
updated: 2026-04-04
---

# std::any（C++17）

`std::any` 是类型擦除的值容器——可以持有任意类型的单个值，运行时检查类型。

## 意图与场景

- 配置系统中存储不同类型的值
- 插件系统传递不透明数据
- 替代 `void*`（类型安全）

## 基本用法

```cpp
#include <any>
#include <string>

std::any val;

val = 42;                    // 持有 int
val = std::string("hello");  // 现在持有 string（之前的 int 被销毁）
val = 3.14;                  // 现在持有 double

// 检查
val.has_value();             // true
val.type();                  // 返回 std::type_info

// 安全获取
try {
    int n = std::any_cast<int>(val);  // 类型不对抛 std::bad_any_cast
} catch (const std::bad_any_cast&) { }

// 指针版本（安全）
int* p = std::any_cast<int>(&val);   // 类型不对返回 nullptr
if (p) std::cout << *p;

// 原地构造
val.emplace<std::string>("world");
```

## 与 variant 的对比

```
                    any                    variant<int, string, double>
类型集合            任意类型                编译期固定
访问方式            any_cast（运行时）       get<>/visit（编译期+运行时）
内存开销            可能堆分配              栈上分配（大小=最大类型）
性能                较慢（类型擦除）        较快
适用场景            完全未知类型            类型集合已知
```

## 关键要点

> `any` 适用于类型完全未知的场景，但有性能代价。如果类型集合在编译期已知，`variant` 是更好的选择。

> `any` 的小对象优化（SSO）——小于一定大小的类型直接在栈上存储，避免堆分配。

## 相关模式 / 关联

- [[cpp-variant]] — 类型集合已知时的替代方案
- [[cpp-类型擦除]] — any 的实现原理
