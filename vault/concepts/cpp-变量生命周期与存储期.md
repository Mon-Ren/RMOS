---
title: C++ 变量捕获与生命周期
tags: [cpp, variable, lifetime, capture, scope, dangling]
aliases: [变量生命周期, 作用域, 捕获, 自动存储期, 存储期]
created: 2026-04-04
updated: 2026-04-04
---

# 变量生命周期与存储期

理解 C++ 变量的四种存储期——自动、静态、线程、动态——是写出正确代码的基础。

## 四种存储期

```cpp
// 1. 自动存储期（局部变量）——离开作用域自动销毁
void foo() {
    int x = 42;              // 自动存储期
    std::string s = "hello";  // 自动存储期，析构时释放
}  // x 和 s 在这里销毁

// 2. 静态存储期——程序启动到结束
static int global = 0;       // 全局变量
void foo() {
    static int count = 0;    // 局部 static：首次调用初始化，程序结束销毁
    ++count;
}

// 3. 线程存储期——线程创建到结束
thread_local int tls_var = 0;  // 每个线程独立

// 4. 动态存储期——手动管理
void foo() {
    int* p = new int(42);     // 动态存储期
    delete p;                 // 手动释放
}
```

## 常见陷阱

```cpp
// 返回局部变量的引用
int& bad() {
    int x = 42;
    return x;  // 悬垂引用！
}

// Lambda 捕获局部变量后跨作用域使用
std::function<int()> make_counter() {
    int count = 0;
    return [&count]() { return ++count; };  // count 是局部变量！
}

// static 变量的析构顺序（跨编译单元）
// file1.cpp
static std::string s = "hello";
// file2.cpp
extern std::string s;
void use() { std::cout << s; }  // 可能在 s 析构后调用！
```

## 关键要点

> 自动变量的析构顺序与构造顺序相反（栈语义）。静态变量在 main 前初始化，main 后销毁。跨编译单元的静态变量析构顺序未定义。

> `thread_local` 变量在每个线程首次访问时初始化，线程退出时销毁。

## 相关模式 / 关联

- [[cpp-堆与栈内存]] — 栈和堆的区别
- [[cpp-call_once与thread_local]] — thread_local 详细
