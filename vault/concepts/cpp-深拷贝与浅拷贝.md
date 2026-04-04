---
title: 深拷贝与浅拷贝
tags: [cpp, deep-copy, shallow-copy, copy-constructor, copy-semantics]
aliases: [深拷贝, 浅拷贝, copy constructor, 拷贝语义, copy semantics]
created: 2026-04-04
updated: 2026-04-04
---

# 深拷贝与浅拷贝

深拷贝复制所有间接资源，浅拷贝只复制指针值——默认生成的是浅拷贝，管理资源时必须自定义深拷贝。

## 浅拷贝（编译器默认）

```cpp
// 编译器生成的拷贝是逐成员拷贝（浅拷贝）
struct Shallow {
    int* data;
    size_t size;
};

Shallow a{new int[10], 10};
Shallow b = a;  // 浅拷贝：b.data == a.data

// ⚠️ 问题：
// 1. 两个对象共享同一块内存
// 2. a 析构后 b.data 成为悬垂指针
// 3. 最后 b 析构时 double delete
```

## 深拷贝（自定义）

```cpp
class DeepCopy {
    int* data_;
    size_t size_;
public:
    // 深拷贝构造函数：分配新内存并复制内容
    DeepCopy(const DeepCopy& other)
        : data_(new int[other.size_]), size_(other.size_) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    // 深拷贝赋值
    DeepCopy& operator=(const DeepCopy& other) {
        if (this != &other) {
            DeepCopy tmp(other);  // 先拷贝（可能抛异常）
            std::swap(data_, tmp.data_);
            std::swap(size_, tmp.size_);
        }
        return *this;
    }

    ~DeepCopy() { delete[] data_; }
};

DeepCopy a(10);
DeepCopy b = a;  // 深拷贝：b 有自己的 data_
```

## 指针语义 vs 值语义

```cpp
// 值语义：拷贝 = 独立副本
std::vector<int> a = {1, 2, 3};
std::vector<int> b = a;  // 深拷贝，修改 b 不影响 a

// 指针语义：拷贝 = 共享同一对象
std::shared_ptr<Widget> a = std::make_shared<Widget>();
std::shared_ptr<Widget> b = a;  // 引用计数 +1，修改 b 影响 a

// 设计选择：类应该明确自己的拷贝语义
// 值语义：string, vector, unique_ptr(移动)
// 指针语义：shared_ptr, weak_ptr
```

## 关键要点

> 编译器默认生成浅拷贝（逐成员拷贝）。管理资源（堆内存、文件句柄、socket）的类必须自定义深拷贝或禁止拷贝。

> 优先用值语义——让 RAII 类型管理资源。需要共享所有权时用 shared_ptr。

## 相关模式 / 关联

- [[cpp-Rule-of-Zero与Rule-of-Five]] — 拷贝控制的规则
- [[cpp-智能指针对比与最佳实践]] — 指针语义
