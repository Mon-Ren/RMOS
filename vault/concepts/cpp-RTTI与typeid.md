---
title: RTTI 与 typeid
tags: [cpp, oop, RTTI, typeid, type_info, dynamic_type]
aliases: [RTTI, typeid, type_info, 运行时类型识别, dynamic_cast]
created: 2026-04-04
updated: 2026-04-04
---

# RTTI 与 typeid

RTTI（Run-Time Type Information）让程序在运行时查询对象的实际类型——它是 `dynamic_cast` 和 `typeid` 的基础。

## 意图与场景

- 运行时检查对象的实际类型
- 调试和日志中输出类型名
- 序列化/反序列化中根据类型分发

## typeid

```cpp
#include <typeinfo>
#include <iostream>

class Base { virtual ~Base() = default; };
class Derived : public Base {};

Base* p = new Derived();

// typeid 获取运行时类型（需要多态类型）
const std::type_info& ti = typeid(*p);
std::cout << ti.name() << "\n";  // 输出派生类名（名称因编译器而异）

// 类型比较
if (typeid(*p) == typeid(Derived)) {
    std::cout << "It's a Derived\n";
}

// 非多态类型：typeid 返回静态类型
int x = 42;
typeid(x).name();  // int（编译期确定）
```

## type_info

```cpp
const std::type_info& ti1 = typeid(int);
const std::type_info& ti2 = typeid(double);

ti1 == ti2;            // false
ti1 != ti2;            // true
ti1.before(ti2);       // 排序序（用于 map 键）
ti1.hash_code();       // 哈希值（用于 unordered_map）
ti1.name();            // 类型名字符串（不可移植）
```

## type_index（C++11）

```cpp
#include <typeindex>
#include <unordered_map>

// type_index 可以做哈希容器的键
std::unordered_map<std::type_index, std::string> type_names;
type_names[typeid(int)] = "int";
type_names[typeid(double)] = "double";

// 运行时类型到字符串的映射
auto name = type_names[typeid(*p)];
```

## RTTI 的代价

```cpp
// RTTI 有开销：
// 1. 每个有多态的类增加 type_info 对象
// 2. vtable 中存储指向 type_info 的指针
// 3. typeid 和 dynamic_cast 的运行时比较

// 禁用 RTTI（编译选项 -fno-rtti）
// 禁用后 typeid 和 dynamic_cast 不可用
// 用自定义类型标签替代
class Base {
    virtual const char* type_name() const { return "Base"; }
};
```

## 关键要点

> `typeid` 对多态类型返回动态类型，对非多态类型返回静态类型。`type_info::name()` 的结果不可移植（不同编译器格式不同）。

> 需要 RTTI 意味着设计可能有问题——优先用虚函数实现多态行为，而非在外部检查类型。

## 相关模式 / 关联

- [[cpp-继承与多态]] — RTTI 的基础
- [[cpp-类型转换]] — dynamic_cast 依赖 RTTI
