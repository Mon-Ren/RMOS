---
title: Rule of Zero 与 Rule of Five
tags: [cpp, oop, rule-of-zero, rule-of-five, special-member-functions]
aliases: [Rule of Zero, Rule of Five, 零法则, 五法则, 特殊成员函数管理]
created: 2026-04-04
updated: 2026-04-04
---

# Rule of Zero 与 Rule of Five

这两个法则指导你何时需要自定义特殊成员函数——Rule of Zero 是默认选择，Rule of Five 是管理资源时的必须。

## Rule of Zero（优先）

> 如果类不直接管理资源（内存、句柄、锁），不要自定义任何特殊成员函数。让编译器生成。

```cpp
class Document {
    std::unique_ptr<Impl> impl_;   // unique_ptr 管理资源
    std::string title_;            // string 管理资源
    std::vector<Page> pages_;      // vector 管理资源
    // 不需要自定义析构/拷贝/移动——编译器生成的都正确
    // unique_ptr 抑制了拷贝，允许移动
    // string 和 vector 自己处理拷贝和移动
};
```

## Rule of Five（必须时）

> 如果类直接管理资源，需要自定义：析构函数、拷贝构造、拷贝赋值、移动构造、移动赋值。

```cpp
class Buffer {
    char* data_;
    size_t size_;
public:
    Buffer(size_t n) : data_(new char[n]), size_(n) {}

    // 1. 析构
    ~Buffer() { delete[] data_; }

    // 2. 拷贝构造
    Buffer(const Buffer& other) : data_(new char[other.size_]), size_(other.size_) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    // 3. 拷贝赋值
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            Buffer tmp(other);    // 拷贝构造临时对象
            std::swap(data_, tmp.data_);
            std::swap(size_, tmp.size_);
        }  // tmp 析构释放旧资源
        return *this;
    }

    // 4. 移动构造
    Buffer(Buffer&& other) noexcept : data_(other.data_), size_(other.size_) {
        other.data_ = nullptr;
        other.size_ = 0;
    }

    // 5. 移动赋值
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }
};
```

## Copy-and-Swap 惯用法

```cpp
// 用 swap 统一实现拷贝赋值和移动赋值
class SmartBuffer {
    char* data_;
    size_t size_;
public:
    void swap(SmartBuffer& other) noexcept {
        using std::swap;
        swap(data_, other.data_);
        swap(size_, other.size_);
    }

    // 拷贝赋值：按值传参（编译器选择拷贝或移动构造参数）
    SmartBuffer& operator=(SmartBuffer other) {  // 注意：按值传递
        swap(other);
        return *this;
    }
    // other 在函数结束时析构，释放旧资源
};
```

## 关键要点

> Rule of Zero 是默认选择——让 RAII 包装类管理资源。只有在直接管理资源（裸指针、文件句柄、socket）时才需要 Rule of Five。

> Copy-and-Swap 让拷贝赋值自动异常安全——如果拷贝构造失败，原对象不变。

## 相关模式 / 关联

- [[cpp-类与对象]] — 特殊成员函数
- [[cpp-右值引用与移动语义]] — 移动构造/赋值
- [[cpp-raii-惯用法]] — 资源管理
