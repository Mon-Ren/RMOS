---
title: 右值引用与移动语义
tags: [cpp, move-semantics, rvalue-reference, perfect-forwarding, cpp11]
aliases: [移动语义, 右值引用, 完美转发, move, forward, 5-3-0法则]
created: 2026-04-04
updated: 2026-04-04
---

# 右值引用与移动语义

移动语义允许"窃取"临时对象的资源而非深拷贝——这是 C++11 最重要的性能特性。

## 意图与场景

- 大对象（容器、字符串）从函数返回时避免拷贝
- 容器扩容时移动元素而非拷贝
- 实现移动构造函数和移动赋值运算符
- 完美转发保持参数的值类别

## 左值 vs 右值

```cpp
int x = 42;      // x 是左值（有名字，有地址）
int& lref = x;   // 左值引用

int foo() { return 42; }
// foo() 的返回值是纯右值（prvalue）——没有名字，即将消亡

int&& rref = 42;       // 右值引用绑定到临时量
int&& rref2 = foo();   // 右值引用延长临时量的生命周期

// 关键：右值引用本身是左值！
// rref 有名字，所以它是左值
int&& rref3 = std::move(rref);  // 需要 move 才能再次转移
```

## std::move

```cpp
// std::move 什么也不移动，只是做 static_cast<T&&>
// 它将左值转为右值引用，允许移动操作发生

std::string s = "hello";
std::string s2 = std::move(s);  // 移动构造，s 变为 valid but unspecified
// s 现在处于有效但未指定的状态，不应假设其内容
// 可以安全地做的：赋新值、销毁、与空字符串比较

// 典型的移动构造函数
class Buffer {
    char* data_;
    size_t size_;
public:
    // 移动构造
    Buffer(Buffer&& other) noexcept
        : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;  // 源对象置空，防止析构时释放
        other.size_ = 0;
    }

    // 移动赋值
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;          // 释放自身资源
            data_ = other.data_;     // 窃取对方资源
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }
};
```

## 5/3/0 法则

```
如果类需要：
  - 自定义析构函数
  - 自定义拷贝构造
  - 自定义拷贝赋值
  那么可能也需要移动构造和移动赋值（5法则）

或者：
  - 什么都不自定义，依赖编译器生成（0法则）
  - 只管理资源时使用 RAII 包装（unique_ptr 等）
```

```cpp
// 0 法则示例：让成员管理资源
class Document {
    std::unique_ptr<Impl> impl_;   // unique_ptr 自动处理移动
    std::string name_;             // string 自动处理移动
    std::vector<Page> pages_;      // vector 自动处理移动
    // 不需要自定义析构/拷贝/移动——编译器生成的都正确
};
```

## 完美转发

```cpp
template <typename T>
void wrapper(T&& arg) {               // 转发引用
    target(std::forward<T>(arg));     // 保持 arg 原始的值类别
}

// forward 的作用：
// 如果 T 推导为左值引用 → forward 返回左值引用
// 如果 T 推导为非引用类型 → forward 返回右值引用
```

## 关键要点

> `std::move` 不移动任何东西，它只是授权移动。真正的"移动"发生在移动构造/赋值中——通常是指针的复制和源指针置空。

> 移动后的对象处于"有效但未指定"状态，只可以安全地赋新值或析构。

## 相关模式 / 关联

- [[cpp-引用与指针]] — 左值引用与右值引用的区别
- [[cpp-智能指针详解]] — unique_ptr 是移动语义的典型应用
- [[cpp-移动语义]] — 更详细的移动语义讨论
