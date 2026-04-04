---
title: 继承与多态
tags: [cpp, oop, inheritance, polymorphism, virtual-function]
aliases: [继承, 多态, 虚函数, 虚函数表, vtable, 运行时多态]
created: 2026-04-04
updated: 2026-04-04
---

# 继承与多态

继承建立类型层次，虚函数实现运行时多态——这是 C++ 面向对象的核心机制，也是最容易被滥用的机制。

## 意图与场景

- 接口抽象：通过基类指针/引用操作不同派生类
- 代码复用：派生类继承基类实现（但优先组合而非继承）
- 策略扩展：用户通过继承自定义行为

## 虚函数与 vtable

```cpp
class Shape {
public:
    virtual double area() const = 0;       // 纯虚函数：必须实现
    virtual void draw() const { /* 默认实现 */ }
    virtual ~Shape() = default;            // 虚析构！否则通过基类指针 delete 派生类是 UB
};

class Circle : public Shape {
    double radius_;
public:
    explicit Circle(double r) : radius_(r) {}
    double area() const override { return 3.14159265 * radius_ * radius_; }
    void draw() const override { /* 圆形绘制 */ }
};

class Rectangle : public Shape {
    double w_, h_;
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; }
    void draw() const override { /* 矩形绘制 */ }
};

// 多态使用
void printArea(const Shape& s) {
    std::cout << s.area() << "\n";  // 运行时绑定到正确的 area()
}

// vtable 机制：
// - 每个有虚函数的类有一张虚函数表（vtable），存储虚函数地址
// - 每个对象有一个隐藏的 vptr 指向其类的 vtable
// - 调用虚函数时：通过 vptr → vtable → 函数地址（间接调用）
```

## 继承方式

```cpp
class Base {
public:    int pub;
protected: int prot;
private:   int priv;
};

class Pub : public Base {
    // pub → public
    // prot → protected
    // priv → 不可访问
};

class Prot : protected Base {
    // pub → protected
    // prot → protected
    // priv → 不可访问
};

class Priv : private Base {
    // pub → private
    // prot → private
    // priv → 不可访问
};
```

## override 与 final

```cpp
class Base {
public:
    virtual void foo() const;
    virtual void bar();
};

class Derived : public Base {
    void foo() const override;  // override：编译器检查确实覆盖了基类虚函数
    // void foo() override;      // 编译错误：const 不匹配，override 帮助发现

    void bar() final;           // final：禁止进一步覆盖
};

class MoreDerived : public Derived {
    // void bar() override;      // 编译错误：bar 已被声明为 final
};

// final 也可以用于类：禁止继承
class Sealed final : public Base { };
// class Sub : public Sealed { };  // 编译错误
```

## 虚析构函数规则

```cpp
// 通过基类指针删除派生类对象时，基类必须有虚析构
Base* p = new Derived();
delete p;  // 如果 Base::~Base() 不是 virtual → UB（只调用基类析构）

// 有虚函数的类应该有虚析构函数
// 作为接口的抽象类必须有虚析构函数（或 protected 非虚析构）
```

## 关键要点

> 虚函数调用有间接跳转开销（通常 2-3 倍于普通调用），在热路径上可能影响性能。但现代 CPU 分支预测通常能很好地处理。

> 继承建立"is-a"关系——如果不确定是否满足里氏替换原则，就用组合而非继承。

## 相关模式 / 关联

- [[cpp-crtp-奇异递归模板模式]] — 编译时多态替代方案
- [[cpp-nvi-非虚接口]] — 公有非虚 + 私有虚函数的设计
- [[设计模式-策略模式]] — 运行时多态策略选择
