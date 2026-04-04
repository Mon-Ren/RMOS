---
title: C++ 与 C 互操作
tags: [cpp, c-interop, extern-C, ABI, linkage, name-mangling]
aliases: [C互操作, extern C, ABI兼容, 名称修饰, name mangling, 链接规范]
created: 2026-04-04
updated: 2026-04-04
---

# C++ 与 C 互操作

`extern "C"` 是 C++ 与 C 代码互操作的桥梁——它使用 C 的链接规范，不做名称修饰。

## extern "C"

```cpp
// 在 C++ 中声明 C 函数
extern "C" {
    #include <sqlite3.h>    // C 库头文件
    void legacy_function(int x, const char* s);
}

// 让 C++ 函数可被 C 调用
extern "C" void my_api(int x) {
    // 不能重载、不能使用 C++ 特性在接口层
}
```

## 头文件中的 extern "C"

```cpp
// mylib.h：同时兼容 C 和 C++ 编译器
#ifdef __cplusplus
extern "C" {
#endif

int add(int a, int b);
void process(const char* data);

#ifdef __cplusplus
}
#endif

// C 编译器看到：int add(int, int);
// C++ 编译器看到：extern "C" { int add(int, int); }
```

## 限制

```cpp
// extern "C" 函数不能：
// 1. 重载
extern "C" void foo(int);
extern "C" void foo(double);  // 链接冲突！

// 2. 使用 C++ 特性作为参数/返回值
extern "C" void bar(std::string s);  // 不可以：string 不是 POD

// 3. 是成员函数
// extern "C" void Widget::method();  // 不可以

// 安全做法：用 POD 类型做接口
extern "C" {
    struct CPoint { double x, y; };  // POD 类型
    double distance(CPoint a, CPoint b);
}
```

## 关键要点

> `extern "C"` 告诉编译器用 C 的链接规范——不做名称修饰（name mangling），使得 C 代码能找到 C++ 编译的符号。

> 互操作的接口层只用 POD 类型（无构造函数、无虚函数、无引用成员），避免 ABI 问题。

## 相关模式 / 关联

- [[cpp-编译模型与ODR]] — 链接与名称修饰
- [[cpp-sizeof与内存对齐]] — POD 类型的布局保证
