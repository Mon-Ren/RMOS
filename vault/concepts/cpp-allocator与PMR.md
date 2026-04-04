---
title: Allocator 与 PMR
tags: [cpp, allocator, PMR, polymorphic-allocator, memory-resource, custom-allocator]
aliases: [allocator, PMR, polymorphic_allocator, memory_resource, 自定义分配器, 内存资源]
created: 2026-04-04
updated: 2026-04-04
---

# Allocator 与 PMR

Allocator 控制容器的内存分配策略——替换默认的 `new/delete` 为内存池、栈分配、共享内存等。

## std::allocator（默认）

```cpp
// std::allocator<T> 就是包装了 new/delete
std::vector<int> v;  // 使用 std::allocator<int>

// allocator 的接口（简化）
template <typename T>
struct allocator {
    T* allocate(size_t n);           // 分配 n * sizeof(T) 字节
    void deallocate(T* p, size_t n); // 释放
    template <typename U, typename... Args>
    void construct(U* p, Args&&...); // 在 p 上构造
    void destroy(T* p);              // 析构
};
```

## 自定义 Allocator

```cpp
// 栈分配器：从固定大小的栈缓冲区分配
template <typename T, size_t N>
class StackAllocator {
    alignas(T) char buffer_[N * sizeof(T)];
    size_t offset_ = 0;
public:
    using value_type = T;

    T* allocate(size_t n) {
        if (offset_ + n > N) throw std::bad_alloc();
        T* p = reinterpret_cast<T*>(buffer_ + offset_ * sizeof(T));
        offset_ += n;
        return p;
    }

    void deallocate(T*, size_t) { /* 栈分配不释放 */ }

    // 必须提供 rebind
    template <typename U>
    struct rebind { using other = StackAllocator<U, N>; };
};
```

## PMR（C++17）

```cpp
#include <memory_resource>

// PMR：多态分配器——通过虚函数调度，无需模板参数
// 使用方式：pmr::vector 代替 vector
std::pmr::vector<int> v;  // 使用默认资源（new/delete）

// 使用单调缓冲区（快速，不单独释放）
char buffer[1024];
std::pmr::monotonic_buffer_resource pool{buffer, sizeof(buffer)};
std::pmr::vector<int> fast_vec{&pool};  // 从 pool 分配
// 插入元素时从 buffer 分配，极快

// 使用同步池
std::pmr::synchronized_pool_resource sync_pool;
std::pmr::vector<std::string> strings{&sync_pool};

// PMR 容器可以互相赋值（因为分配器类型相同，只是资源不同）
std::pmr::vector<int> v1{&pool};
std::pmr::vector<int> v2{&sync_pool};
v2 = v1;  // OK：pmr::vector<int> 是同一类型
```

## 关键要点

> `std::allocator<T>` 是默认分配器——直接用 new/delete。自定义 allocator 可以用于内存池、共享内存、固定缓冲区等场景。

> PMR（C++17）通过多态虚函数替代模板参数——不同 allocator 的容器是同一类型，可以互相赋值和传递。

## 相关模式 / 关联

- [[cpp-new与delete深入]] — 底层内存操作
- [[cpp-对象池模式]] — 自定义分配器的典型应用
