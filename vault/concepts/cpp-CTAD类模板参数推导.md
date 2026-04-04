---
title: 模板参数推导（CTAD）
tags: [cpp17, CTAD, class-template-argument-deduction, deduction-guide]
aliases: [CTAD, 类模板参数推导, deduction guide, 推导指引]
created: 2026-04-04
updated: 2026-04-04
---

# 类模板参数推导（CTAD，C++17）

CTAD 让类模板从构造函数参数自动推导模板参数——不再需要 `make_*` 辅助函数。

## 基本用法

```cpp
// C++17 前：必须指定类型或用 make_*
std::pair<int, double> p1(1, 3.14);          // 显式指定
auto p2 = std::make_pair(1, 3.14);           // 辅助函数

// C++17：自动推导
std::pair p(1, 3.14);                        // 推导为 pair<int, double>
std::vector v = {1, 2, 3};                   // 推导为 vector<int>
std::mutex mtx;
std::lock_guard lock(mtx);                   // 推导为 lock_guard<mutex>
std::array a = {1, 2, 3};                    // 推导为 array<int, 3>
```

## 自定义推导指引

```cpp
template <typename T>
class Buffer {
    T* data_;
    size_t size_;
public:
    Buffer(T* data, size_t size) : data_(data), size_(size) {}
};

// 推导指引：从指针类型推导 T
template <typename T>
Buffer(T*, size_t) -> Buffer<T>;

int arr[10];
Buffer buf(arr, 10);  // 推导为 Buffer<int>

// 常见场景：容器从迭代器推导
std::vector<int> v = {1, 2, 3};
std::set s(v.begin(), v.end());  // 推导为 set<int>
```

## 关键要点

> CTAD 让类模板的使用像普通类一样简洁——`std::pair p{1, 2.0}` 比 `std::make_pair(1, 2.0)` 更直接。

> 自定义类可以通过推导指引控制 CTAD 行为——标准库的大部分容器和适配器都提供了推导指引。

## 相关模式 / 关联

- [[cpp-auto与类型推导]] — auto 的类型推导
- [[cpp-模板编程基础]] — 模板基础
