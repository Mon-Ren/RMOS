---
title: 多重继承与虚继承
tags: [cpp, oop, multiple-inheritance, virtual-inheritance, diamond-problem]
aliases: [多重继承, 虚继承, 菱形继承, diamond problem, virtual base]
created: 2026-04-04
updated: 2026-04-04
---

# 多重继承与虚继承

多重继承让一个类有多个基类——威力强大但容易制造复杂性。虚继承解决菱形继承的二义性问题。

## 意图与场景

- 实现多个接口（接口继承）
- Mixin 模式：组合多个功能片段
- 需要菱形继承时使用虚继承

## 基本多重继承

```cpp
class Reader {
public:
    virtual void read() = 0;
};

class Writer {
public:
    virtual void write() = 0;
};

class FileReader : public Reader {
public:
    void read() override { /* 读文件 */ }
};

class FileWriter : public Writer {
public:
    void write() override { /* 写文件 */ }
};

// 多重继承：同时实现读写
class FileIO : public FileReader, public FileWriter {
public:
    void read() override { /* 具体实现 */ }
    void write() override { /* 具体实现 */ }
};

FileIO io;
Reader* r = &io;   // OK
Writer* w = &io;   // OK
```

## 菱形继承问题

```cpp
class Animal {
public:
    int age_;
    void eat() { }
};

class Mammal : public Animal { };
class WingedAnimal : public Animal { };

// Bat 同时继承 Mammal 和 WingedAnimal
class Bat : public Mammal, public WingedAnimal { };

Bat b;
// b.eat();       // 编译错误：二义性——哪个 Animal::eat()?
// b.age_ = 5;    // 编译错误：二义性

// 必须显式指定
b.Mammal::eat();
b.Mammal::age_ = 5;
```

## 虚继承

```cpp
// 虚继承：确保只有一份基类子对象
class Animal {
public:
    int age_;
};

class Mammal : virtual public Animal { };      // virtual 继承
class WingedAnimal : virtual public Animal { }; // virtual 继承

class Bat : public Mammal, public WingedAnimal { };

Bat b;
b.age_ = 5;   // OK：只有一份 Animal
b.eat();      // OK：无二义性
```

## 虚继承的代价

```cpp
// 虚继承增加间接性：
// - 每个虚基类通过指针间接访问
// - 派生最深的类负责初始化虚基类
// - 构造顺序：虚基类 → 非虚基类 → 成员 → 自身

class A { public: A(int) {} };
class B : virtual public A { public: B() : A(0) {} };
class C : virtual public A { public: C() : A(0) {} };
class D : public B, public C {
public:
    D() : A(0), B(), C() {}  // D 必须直接初始化 A
};
```

## 关键要点

> 优先使用接口继承（纯虚函数的多重继承）而非实现继承。菱形继承用虚继承解决，但虚继承有性能开销和构造复杂性。

> 大部分"需要多重继承"的场景，组合（composition）+ 接口继承是更好的设计。

## 相关模式 / 关联

- [[cpp-继承与多态]] — 单继承基础
- [[cpp-nvi-非虚接口]] — 接口设计模式
