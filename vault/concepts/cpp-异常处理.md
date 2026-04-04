---
title: 异常处理
tags: [cpp, fundamentals, exception, try-catch, noexcept]
aliases: [异常, try-catch, throw, noexcept, RAII异常安全]
created: 2026-04-04
updated: 2026-04-04
---

# 异常处理

异常是 C++ 的错误报告机制——正常路径和错误路径分离，RAII 保证资源在栈展开时正确释放。

## 意图与场景

- 不可恢复的错误需要传播到调用者
- 构造函数中发生错误（构造函数无法返回错误码）
- 嵌套调用深层的错误需要向上传播

## 基本语法

```cpp
#include <stdexcept>
#include <string>

// 抛出异常
void openFile(const std::string& path) {
    if (!file_exists(path)) {
        throw std::runtime_error("File not found: " + path);
    }
}

// 捕获异常
void process() {
    try {
        openFile("config.txt");
    } catch (const std::runtime_error& e) {    // 按 const 引用捕获
        std::cerr << "Error: " << e.what() << "\n";
    } catch (const std::exception& e) {        // 基类兜底
        std::cerr << "General error: " << e.what() << "\n";
    } catch (...) {                             // 捕获所有异常
        std::cerr << "Unknown error\n";
    }
}
```

## 异常安全级别

```
1. 无异常安全（No guarantee）  — 泄露资源或破坏不变量
2. 基本安全（Basic guarantee） — 不泄露资源，对象处于有效但不确定状态
3. 强安全（Strong guarantee）  — 操作要么成功，要么状态不变（commit-or-rollback）
4. 不抛异常（Nothrow guarantee）— 保证不抛异常
```

```cpp
class Vector {
    int* data_;
    size_t size_, capacity_;
public:
    // 强异常安全：push_back
    void push_back(int val) {
        if (size_ < capacity_) {
            data_[size_++] = val;  // 不可能失败
            return;
        }
        // 需要扩容——先在新内存上操作
        auto new_cap = capacity_ * 2;
        auto new_data = std::make_unique<int[]>(new_cap);  // 如果失败，原对象不变

        for (size_t i = 0; i < size_; ++i)
            new_data[i] = std::move(data_[i]);  // 如果失败，原对象不变
        new_data[size_++] = val;

        // 以下操作不抛异常
        data_.reset(new_data.release());
        capacity_ = new_cap;
    }
};
```

## noexcept

```cpp
// noexcept 说明符：承诺不抛异常
void swap(Widget& a, Widget& b) noexcept {
    using std::swap;
    swap(a.data_, b.data_);
}

// noexcept 运算符：编译期查询表达式是否 noexcept
static_assert(noexcept(swap(a, b)));  // 编译期检查

// 移动操作应标记 noexcept（否则 vector 等容器会回退到拷贝）
// 析构函数默认 noexcept
```

## 自定义异常

```cpp
class ValidationError : public std::runtime_error {
    int errorCode_;
public:
    ValidationError(int code, const std::string& msg)
        : std::runtime_error(msg), errorCode_(code) {}
    int code() const { return errorCode_; }
};

// 使用
try {
    validate(input);
} catch (const ValidationError& e) {
    log(e.code(), e.what());
}
```

## 关键要点

> 异常的核心价值是将错误处理从正常逻辑中分离。RAII 是异常安全的基石——没有 RAII，异常处理几乎不可能写对。

> `noexcept` 不仅是承诺，它影响代码生成——编译器可以生成更高效的代码，且 STL 在 `noexcept` 条件下会使用移动而非拷贝。

## 相关模式 / 关联

- [[cpp-raii-惯用法]] — 异常安全的资源管理基础
- [[cpp-类与对象]] — 构造函数中的异常处理
