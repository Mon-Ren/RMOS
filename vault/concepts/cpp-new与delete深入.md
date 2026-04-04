---
title: new 与 delete 深入
tags: [cpp, memory, new, delete, placement-new, operator-new]
aliases: [new, delete, placement new, operator new, 自定义分配器, 内存分配]
created: 2026-04-04
updated: 2026-04-04
---

# new 与 delete 深入

`new` 和 `delete` 是 C++ 的内存管理运算符——它们做两件事：分配内存和调用构造/析构。理解它们的机制才能编写自定义内存管理。

## 两步操作

```cpp
// new 表达式做了两件事：
Widget* p = new Widget(args);
// 1. 调用 operator new(sizeof(Widget)) 分配原始内存
// 2. 在分配的内存上调用 Widget(args) 构造对象

// delete 表达式也做两件事：
delete p;
// 1. 调用 p->~Widget() 析构对象
// 2. 调用 operator delete(p) 释放内存

// new[] 和 delete[]
int* arr = new int[100];  // 分配 + 默认构造 100 个 int
delete[] arr;              // 析构 100 个 + 释放
// 必须匹配！new[] 用 delete[]，new 用 delete
```

## placement new

```cpp
#include <new>

// placement new：在已有内存上构造对象
alignas(Widget) char buffer[sizeof(Widget)];
Widget* p = new (buffer) Widget(args);  // 在 buffer 上构造，不分配新内存

// 必须手动析构
p->~Widget();  // 手动调用析构函数
// 不要调用 operator delete——buffer 不是 operator new 分配的

// 常见用法：内存池
void* raw = pool.allocate(sizeof(Widget));
Widget* w = new (raw) Widget(args);
// ... 使用 ...
w->~Widget();
pool.deallocate(raw);
```

## 重载 operator new/delete

```cpp
class Widget {
public:
    // 类专属 operator new
    static void* operator new(size_t size) {
        std::cout << "Custom new: " << size << " bytes\n";
        return ::operator new(size);  // 委托给全局 operator new
    }

    static void operator delete(void* ptr) {
        std::cout << "Custom delete\n";
        ::operator delete(ptr);
    }

    // 数组版本
    static void* operator new[](size_t size);
    static void operator delete[](void* ptr);

    // placement 版本
    static void* operator new(size_t size, void* ptr) {
        return ptr;  // 直接返回，不分配
    }
};
```

## 关键要点

> placement new 在已有内存上构造对象，用完必须手动调用析构函数，但不能调用 `delete`（因为内存不是 `operator new` 分配的）。

> 现代 C++ 几乎不需要直接用 `new/delete`——`make_unique`/`make_shared` 自动处理。

## 相关模式 / 关联

- [[cpp-智能指针详解]] — 替代手动 new/delete
- [[cpp-对象池模式]] — placement new 的典型应用
