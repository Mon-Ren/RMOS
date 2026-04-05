---
title: 虚表布局与多重继承
tags: [cpp, vtable, virtual-function, multiple-inheritance, abi]
aliases: [vtable 布局, 虚表内部结构, 多重继承 vtable, vptr 偏移]
created: 2026-04-05
updated: 2026-04-05
---

# 虚表布局与多重继承

**一句话概述：** 虚表（vtable）是编译器为每个多态类生成的函数指针数组，每个对象头部隐藏一个 vptr 指向它。多重继承时一个对象会有多个 vptr（每个基类一个），`dynamic_cast` 和 `typeid` 的运行时成本就来自 vtable 查找和偏移计算。

## 单继承的虚表

```cpp
class Base {
public:
    virtual void foo() { }
    virtual void bar() { }
    virtual ~Base() = default;
    int x;
};

class Derived : public Base {
public:
    void foo() override { }  // 覆盖 Base::foo
    virtual void baz() { }   // 新增虚函数
    int y;
};
```

内存布局（Itanium ABI，GCC/Clang）：

```
Base 对象：                    Derived 对象：
┌──────────────┐              ┌──────────────┐
│ vptr ──────────────┐        │ vptr ─────────────────┐
├──────────────┤     │        ├──────────────┤         │
│ x (int)      │     │        │ x (int)      │         │
└──────────────┘     │        ├──────────────┤         │
                     │        │ y (int)      │         │
                     │        └──────────────┘         │
                     │                                 │
                     ▼                                 ▼
Base 的 vtable:               Derived 的 vtable:
┌────────────────────┐        ┌────────────────────┐
│ typeinfo for Base  │        │ typeinfo for Derived│
├────────────────────┤        ├────────────────────┤
│ &Base::foo         │        │ &Derived::foo      │  ← 覆盖了
├────────────────────┤        ├────────────────────┤
│ &Base::bar         │        │ &Base::bar         │  ← 继承未覆盖
├────────────────────┤        ├────────────────────┤
│ &Base::~Base       │        │ &Derived::~Derived │
├────────────────────┤        ├────────────────────┤
│                    │        │ &Derived::baz      │  ← 新增的
└────────────────────┘        └────────────────────┘
```

**Itanium ABI 的 vtable 布局规则：**
1. 偏移 -2：typeinfo 指针（用于 `typeid` 和 `dynamic_cast`）
2. 偏移 -1：到对象起始的偏移（多重继承时非零）
3. 偏移 0+：虚函数指针，按声明顺序排列

## 多重继承：多个 vptr

```cpp
class Base1 {
public:
    virtual void foo() { }
    virtual ~Base1() = default;
    int a;
};

class Base2 {
public:
    virtual void bar() { }
    virtual ~Base2() = default;
    int b;
};

class Derived : public Base1, public Base2 {
public:
    void foo() override { }
    void bar() override { }
    virtual void qux() { }
    int c;
};
```

```
Derived 对象内存布局：
┌──────────────────────┐
│ Base1 子对象           │
│   vptr₁ ──────────────────────┐
│   a                    │      │
├──────────────────────┤      │
│ Base2 子对象           │      │
│   vptr₂ ──────────────────┐  │
│   b                    │  │  │
├──────────────────────┤  │  │
│ Derived 自身成员       │  │  │
│   c                    │  │  │
└──────────────────────┘  │  │
                          │  │
vptr₁ 指向的 vtable:      │  │
┌────────────────────┐    │  │
│ typeinfo Derived   │    │  │
├────────────────────┤    │  │
│ offset = 0         │ ───┘  │  ← 到对象起始的偏移
├────────────────────┤       │
│ &Derived::foo      │       │
├────────────────────┤       │
│ &Base1::~Base1     │       │
├────────────────────┤       │
│ &Derived::qux      │       │
└────────────────────┘       │
                             │
vptr₂ 指向的 vtable:         │
┌────────────────────┐       │
│ typeinfo Derived   │       │
├────────────────────┤       │
│ offset = -16       │ ─── Derived* = Base2* - 16  ← 调整指针
├────────────────────┤
│ &Derived::bar      │       │  ← 注意：thunk，不是直接指向 bar
├────────────────────┤
│ &Base2::~Base2     │       │
└────────────────────┘
```

**关键点：**
- Derived 对象有两个 vptr（来自两个基类子对象）
- Base2 子对象的 vptr 偏移不为 0（offset = -16），因为它在对象内部偏移了 16 字节
- 从 `Base2*` 转换到 `Derived*` 时需要减去这个偏移

## dynamic_cast 的实现

```cpp
Base2* b2 = get_some_object();
Derived* d = dynamic_cast<Derived*>(b2);

// 编译器生成的伪代码：
// 1. 通过 vptr₂ 读取 typeinfo
// 2. 查找 typeinfo 的派生类图，看 Derived 是否在其中
// 3. 如果是，计算偏移：Derived* = b2 + offset_of_base2_in_derived
// 4. 如果不是，返回 nullptr

// 为什么 dynamic_cast 慢？
// typeinfo 是一个树形结构，查找需要遍历（特别是跨 so 时可能涉及字符串比较）
// 代价通常是 ~10-50ns（比虚调用的 ~1-2ns 高一个数量级）
```

## 虚继承的虚表（菱形继承）

```cpp
class Base {
public:
    virtual void foo() { }
    int x;
};

class A : virtual public Base {  // 虚继承
public:
    void foo() override { }
    virtual void a_only() { }
};

class B : virtual public Base {  // 虚继承
public:
    void foo() override { }
    virtual void b_only() { }
};

class C : public A, public Base { ... };
// 这里 B 没出现，只是说明虚继承
```

虚继承时，Base 子对象的位置在编译期不确定（取决于最派生类），所以：
- A 的 vtable 增加一个偏移条目：**vbase offset**（到虚基类的偏移）
- 构造最派生类 C 时，编译器填入正确的偏移值
- 这就是为什么虚继承有额外开销

## 关键要点

> vtable 在编译期由编译器生成，存储在只读段（`.rodata`）。每个包含虚函数的类有一张 vtable，同类的所有对象共享同一张 vtable（通过 vptr 指向它）。

> 虚调用的成本：一次间接内存访问（读 vptr）+ 一次间接跳转（读 vtable 中的函数指针）= 两次 cache miss 的风险。现代 CPU 的分支预测对此帮助不大（间接跳转目标不确定）。但实际性能影响通常很小（<2ns），除非在极热循环中。

> 构造函数中调用虚函数不会多态分发——构造基类子对象时，vptr 指向基类的 vtable（派生类部分还没构造），所以调用的是基类版本。这是 C++ 的设计：构造期间对象类型逐渐"变完整"。

## 相关模式 / 关联

- [[cpp-继承与多态]] — 虚函数基础
- [[cpp-多重继承与虚继承]] — 菱形问题、虚基类
- [[cpp-RTTI与typeid]] — 运行时类型识别
- [[cpp-类型擦除]] — 类型擦除 vs 虚函数
- [[cpp-CRTP奇异递归模板模式]] — 编译时多态替代虚函数
