---
title: 移动语义
tags: [cpp, idiom, move-semantics, rvalue, performance]
aliases: [Move Semantics, 移动语义, 右值引用, rvalue reference, 完美转发, perfect forwarding]
created: 2026-04-04
updated: 2026-04-04
---

# Move Semantics 与移动语义

**一句话概述：** 通过右值引用（`&&`）和 `std::move`，将资源（如堆内存、文件句柄）从一个对象"窃取"到另一个对象，避免昂贵的深拷贝。

## 意图与场景

C++11 引入的移动语义解决了"临时对象只能被拷贝"的问题：

- **右值引用 `&&`**：绑定到即将销毁的临时对象
- **`std::move`**：将左值转为右值引用（实际不移动任何东西）
- **移动构造/赋值**：接管源对象的资源，源对象进入"有效但未指定"状态
- **完美转发 `std::forward`**：保持参数的值类别转发

**适用场景：**
- 大对象（vector、string）的返回值优化
- 容器操作（push_back、emplace、排序）
- 资源转移（unique_ptr 所有权转移）
- 泛型编程中的参数转发

## C++ 实现代码

### 移动构造与移动赋值

```cpp
#include <algorithm>
#include <cstring>
#include <utility>
#include <iostream>

class Buffer {
    char* data_;
    std::size_t size_;

public:
    // 构造
    explicit Buffer(std::size_t n) 
        : data_(new char[n]), size_(n) {}
    
    // 拷贝构造：深拷贝
    Buffer(const Buffer& other) 
        : data_(new char[other.size_]), size_(other.size_) {
        std::memcpy(data_, other.data_, size_);
    }
    
    // 移动构造：窃取资源
    Buffer(Buffer&& other) noexcept 
        : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;  // 源对象置空
        other.size_ = 0;
    }
    
    // 拷贝赋值
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            Buffer tmp(other);  // copy-and-swap
            swap(tmp);
        }
        return *this;
    }
    
    // 移动赋值
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;      // 释放自己的资源
            data_ = other.data_; // 窃取
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }
    
    ~Buffer() { delete[] data_; }
    
    void swap(Buffer& other) noexcept {
        std::swap(data_, other.data_);
        std::swap(size_, other.size_);
    }
};
```

### 5/3/0 法则

```cpp
// Rule of 5：管理资源的类需要实现全部 5 个特殊成员函数
class ResourceHolder {
    int* ptr_;
    
public:
    ResourceHolder() : ptr_(new int(0)) {}               // 默认构造
    
    ResourceHolder(const ResourceHolder& o)               // 拷贝构造
        : ptr_(new int(*o.ptr_)) {}
    
    ResourceHolder(ResourceHolder&& o) noexcept           // 移动构造
        : ptr_(o.ptr_) { o.ptr_ = nullptr; }
    
    ResourceHolder& operator=(const ResourceHolder& o) {  // 拷贝赋值
        if (this != &o) { delete ptr_; ptr_ = new int(*o.ptr_); }
        return *this;
    }
    
    ResourceHolder& operator=(ResourceHolder&& o) noexcept { // 移动赋值
        if (this != &o) { delete ptr_; ptr_ = o.ptr_; o.ptr_ = nullptr; }
        return *this;
    }
    
    ~ResourceHolder() { delete ptr_; }                    // 析构
};

// Rule of 0：优先使用标准库容器和智能指针，不需要手动写任何特殊成员函数
class ModernHolder {
    std::unique_ptr<int> ptr_;     // RAII 管理
    std::vector<int> data_;        // 标准库容器
    // 编译器自动生成所有特殊成员函数（正确的行为）
};
```

### 完美转发

```cpp
#include <utility>
#include <string>
#include <memory>

// 工厂函数：完美转发所有参数
template <typename T, typename... Args>
std::unique_ptr<T> make(Args&&... args) {
    // std::forward 保持参数的值类别
    // 左值传入 → 转发为左值
    // 右值传入 → 转发为右值
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

// 通用引用 + 完美转发
template <typename T>
void wrapper(T&& arg) {          // 通用引用：T 推导决定左/右值
    target(std::forward<T>(arg)); // 保持原始值类别
}

// emplace 的完美转发
template <typename Container, typename... Args>
void emplace_back_example(Container& c, Args&&... args) {
    // 原地构造，避免临时对象的创建和移动
    c.emplace_back(std::forward<Args>(args)...);
}
```

### std::move 的正确使用

```cpp
#include <vector>
#include <string>

void correct_move_usage() {
    std::vector<std::string> src = {"hello", "world", "cpp"};
    
    // ✅ 正确：转移所有权
    std::vector<std::string> dst = std::move(src);
    // src 现在处于"有效但未指定"状态
    
    // ✅ 正确：作为返回值（编译器通常自动 move）
    // return local_vec;  // 不需要 std::move（RVO）
    
    // ✅ 正确：push_back 移动
    std::string name = "large_string_...";
    dst.push_back(std::move(name));
    // name 现在处于"有效但未指定"状态
    
    // ❌ 错误：不要对 const 对象 move（会退化为拷贝）
    // const std::string cs = "hello";
    // auto x = std::move(cs);  // 实际调用拷贝构造！
}
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 避免不必要的深拷贝 | 理解门槛高（值类别、引用折叠） |
| 返回大对象零开销 | 移动后源对象状态需小心处理 |
| 支持独占所有权（unique_ptr） | 完美转发写法繁琐 |
| 容器操作性能大幅提升 | const 对象 move 静默退化为 copy |

> [!tip] 关键要点
> `std::move` **不移动任何东西**——它只是一个到右值引用的 `static_cast`。真正的"移动"发生在移动构造/赋值函数中。记住三个原则：(1) 返回局部变量**不要** `std::move`（RVO 比 move 更优）；(2) 函数参数**永远不要** `std::move` 传入（除非明确要转移所有权）；(3) const 对象的 `std::move` 会调用拷贝而非移动。

> [!info] 值类别速查
> - **左值 (lvalue)**：有名字、有地址（变量）
> - **纯右值 (prvalue)**：临时对象（字面量、函数返回值）
> - **亡值 (xvalue)**：被 move 过的对象
> - `T&` 绑定左值；`T&&` 绑定右值；`T&&` 在模板中是**通用引用**

## 相关链接

- [[cpp-raii-惯用法]] — 移动语义使 RAII 对象可转移所有权
- [[cpp-智能指针详解]] — unique_ptr 依赖移动语义
- [[cpp-对象池模式]] — 移动语义在对象池中的应用
