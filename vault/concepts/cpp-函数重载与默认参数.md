---
title: 函数重载与默认参数
tags: [cpp, fundamentals, function, overload, default-argument]
aliases: [函数重载, 默认参数, 函数签名, 重载决议]
created: 2026-04-04
updated: 2026-04-04
---

# 函数重载与默认参数

函数重载让同名函数根据参数类型分发调用，是 C++ 静态多态的基本形式。

## 意图与场景

- 同一操作针对不同类型有不同的实现
- 提供默认值减少调用者的代码量
- 提高接口的可用性和表达力

## 函数重载

```cpp
void print(int x)               { std::cout << "int: " << x << "\n"; }
void print(double x)            { std::cout << "double: " << x << "\n"; }
void print(const std::string& s){ std::cout << "string: " << s << "\n"; }

print(42);          // int 版本
print(3.14);        // double 版本
print("hello");     // string 版本（const char* → std::string 隐式转换）

// 重载决议优先级：
// 1. 精确匹配
// 2. 提升匹配（char/short → int，float → double）
// 3. 标准转换（int → double，Derived* → Base*）
// 4. 用户定义转换（通过转换运算符/构造函数）
// 5. 如果多个函数在同一层级匹配 → 歧义，编译错误
```

## 重载与 const

```cpp
class Text {
    std::string content_;
public:
    // const 重载：const 和非 const 版本可以共存
    char& operator[](size_t i)       { return content_[i]; }
    const char& operator[](size_t i) const { return content_[i]; }

    // const 对象调用 const 版本
    // 非 const 对象优先调用非 const 版本
};

Text t;
t[0] = 'A';             // 非 const 版本

const Text& ct = t;
char c = ct[0];         // const 版本
// ct[0] = 'B';          // 编译错误：返回 const char&
```

## 默认参数

```cpp
void log(const std::string& msg,
         Level level = Level::Info,
         const std::string& file = __FILE__,
         int line = __LINE__) {
    // ...
}

log("started");                         // 全部用默认值
log("error", Level::Error);             // 只覆盖 level
log("debug", Level::Debug, "main.cpp"); // 覆盖前两个

// 默认参数在声明处指定，不在定义处
void foo(int x, int y = 10);  // 声明
void foo(int x, int y) { }    // 定义不写默认值

// 陷阱：默认参数在编译时绑定，不是运行时
void f(int x = 10) { }
void f(int);           // 第二次声明不能重复默认值（C++ 中多次声明同一参数的默认值是错误）
```

## 重载 vs 默认参数

```cpp
// 重载：每种组合一个函数，类型安全
void connect(const std::string& host);
void connect(const std::string& host, int port);
void connect(const std::string& host, int port, int timeout);

// 默认参数：一个函数，但所有默认值必须兼容
void connect(const std::string& host, int port = 8080, int timeout = 30);

// 选择原则：
// - 默认参数只改变"量"（数值、标志）→ 默认参数
// - 默认参数改变"质"（类型、算法）→ 重载
// - 需要在默认值中创建对象 → 重载
```

## 关键要点

> 重载决议基于参数类型而非返回类型。两个函数仅返回类型不同不能重载。

> 虚函数可以重载，但派生类的重载会隐藏基类同名函数（除非用 `using` 引入）。

## 相关模式 / 关联

- [[cpp-运算符重载]] — 运算符也是函数重载
- [[cpp-类与对象]] — 构造函数重载与委托构造
