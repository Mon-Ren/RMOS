---
title: 引用与指针
tags: [cpp, fundamentals, reference, pointer]
aliases: [引用, 指针, lvalue reference, rvalue reference, 左值引用, 右值引用]
created: 2026-04-04
updated: 2026-04-04
---

# 引用与指针

引用是别名，指针是地址——看似相似，语义完全不同。理解两者的区别是写出安全 C++ 的基础。

## 意图与场景

- 引用：函数参数传递、返回值优化、运算符重载
- 指针：动态内存管理、可空语义、算术操作、C 互操作

## 引用

### 左值引用

```cpp
int x = 42;
int& ref = x;        // ref 是 x 的别名
ref = 100;           // x 变为 100

// 必须初始化，不能重新绑定，不能为 null
// int& bad;          // 编译错误：必须初始化
// int& bad2 = nullptr; // 编译错误

// const 引用：可以绑定临时量
const int& cr = 42;  // OK，临时量生命周期延长
const int& cr2 = x;  // OK，不能通过 cr2 修改 x

// 常见用法：函数参数避免拷贝
void process(const std::string& s);  // 不拷贝，不修改
```

### 右值引用（C++11）

```cpp
int&& rref = 42;          // 绑定到临时量
int&& rref2 = std::move(x);  // 将 x 转为右值引用

// 移动语义的基础
class Buffer {
    std::unique_ptr<char[]> data_;
public:
    // 移动构造：窃取资源，不拷贝
    Buffer(Buffer&& other) noexcept
        : data_(std::move(other.data_)) {}
};
```

### 转发引用（C++11）

```cpp
// 万能引用 / 转发引用：T&& 在模板推导中
template <typename T>
void forwarder(T&& arg) {    // T&& 可以是左值引用或右值引用
    other(std::forward<T>(arg));  // 完美转发
}

// 区分：
// int&&        → 右值引用（确定类型）
// T&&          → 转发引用（模板中，类型待推导）
// auto&&       → 转发引用
```

## 指针

```cpp
int x = 42;
int* p = &x;         // p 存储 x 的地址
*p = 100;            // 解引用修改 x 的值

int* nullp = nullptr;  // 可以为 null
// 使用前必须检查
if (nullp) { *nullp = 1; }

// 指针算术（数组语义）
int arr[5] = {1, 2, 3, 4, 5};
int* p = arr;
p++;        // 指向 arr[1]
p += 2;     // 指向 arr[3]

// void*：通用指针，不能解引用
void* vp = &x;
int* ip = static_cast<int*>(vp);  // 必须转型后使用
```

## 引用 vs 指针对比

| 特性 | 引用 | 指针 |
|------|------|------|
| 必须初始化 | 是 | 否 |
| 可为空 | 否 | 是 |
| 可重新绑定 | 否 | 是 |
| 有算术操作 | 否 | 是 |
| 占用存储 | 编译器可优化为零 | 始终占用一个机器字 |
| 多级间接 | 不支持 | 支持（int**） |

## 关键要点

> 引用是语法糖，本质可能是指针实现，但语义上它是一个已存在的对象的别名，不能为空、不能重新绑定。

> 函数参数优先用 `const T&`（避免拷贝且不修改），需要修改时用 `T&`，需要转移所有权时用 `T&&`。

## 相关模式 / 关联

- [[cpp-移动语义]] — 右值引用的核心应用场景
- [[cpp-智能指针详解]] — 现代 C++ 中指针的替代方案
