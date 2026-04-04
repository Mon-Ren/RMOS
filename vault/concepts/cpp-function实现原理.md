---
title: std::function 实现原理
tags: [cpp, function, type-erasure, implementation, small-buffer-optimization]
aliases: [function实现, 类型擦除实现, small buffer optimization, 闭包存储]
created: 2026-04-04
updated: 2026-04-04
---

# std::function 实现原理

`std::function` 用类型擦除 + 小对象优化实现"存储任意可调用对象"——理解其内部有助于做出性能权衡。

## 内部结构

```cpp
// 简化的 function 内部实现
template <typename Signature>
class function;

template <typename R, typename... Args>
class function<R(Args...)> {
    // 小对象缓冲区（避免小 lambda 的堆分配）
    static constexpr size_t BufferSize = 3 * sizeof(void*);
    alignas(std::max_align_t) char buffer_[BufferSize];

    // 操作函数指针（虚函数表的替代）
    R (*invoke_)(const function&, Args...);
    void (*copy_)(const function&, function&);
    void (*move_)(function&, function&);
    void (*destroy_)(function&);

    // 大对象的堆指针
    void* heap_ptr_ = nullptr;

public:
    R operator()(Args... args) const {
        return invoke_(*this, std::forward<Args>(args)...);
    }
    // ...
};
```

## 小对象优化

```cpp
// 无捕获 lambda：很小，存在 buffer 里
auto l1 = [](int x) { return x * 2; };
std::function<int(int)> f1 = l1;  // 不分配堆内存

// 少量捕获的 lambda：可能仍在 buffer 里
int n = 42;
auto l2 = [n](int x) { return x + n; };
std::function<int(int)> f2 = l2;  // sizeof(lambda) <= BufferSize → 不堆分配

// 大 lambda 或有大量捕获：堆分配
std::array<int, 1000> big_arr;
auto l3 = [big_arr](int x) { return big_arr[x]; };
std::function<int(int)> f3 = l3;  // 堆分配

// ⚠️ std::function 不支持移动语义的优化——即使 lambda 是 move-only，也会拷贝
```

## 性能开销

```
调用开销：
- 函数指针：1次间接跳转
- std::function：2次间接跳转（invoke_ 虚调用 + 可能的 lambda 内部调用）
- auto lambda：零开销（内联展开）

内存开销：
- std::function：~32 字节（buffer + 指针 + 函数指针）
- 函数指针：8 字节
- auto lambda：因捕获而异
```

## 关键要点

> `std::function` 的小对象优化避免了小 lambda 的堆分配——但有大小阈值（通常 24-32 字节）。

> 如果类型已知，用 `auto` 存储 lambda 而非 `std::function`——可以避免虚调用开销和堆分配。

## 相关模式 / 关联

- [[cpp-函数指针与function]] — function 的使用
- [[cpp-类型擦除]] — type erasure 原理
