---
title: 小对象优化
tags: [cpp, SSO, small-buffer-optimization, SBO, in-place, stack-storage]
aliases: [小对象优化, SSO, SBO, small buffer optimization, 栈上存储, 就地存储]
created: 2026-04-04
updated: 2026-04-04
---

# 小对象优化（SSO/SBO）

小对象优化把小数据直接存在对象内部而非堆上——`std::string` 的 SSO 和 `std::function` 的 SBO 都是这个模式。

## std::string 的 SSO

```
长字符串（> 15 字节）：        短字符串（≤ 15 字节）：
┌────────────────────┐         ┌────────────────────┐
│ ptr ──→ 堆分配     │         │ buffer[16]          │
│ size               │         │ size (低 bit 标记)   │
│ capacity           │         │ capacity            │
└────────────────────┘         └────────────────────┘
sizeof(string) = 32            sizeof(string) = 32

短字符串不触发堆分配——直接在对象的 buffer 中存储。
```

## std::function 的 SBO

```cpp
// function 对象通常有 24-32 字节的内部缓冲区
std::function<int(int)> f;

// 小 lambda：存储在缓冲区中（无堆分配）
int capture = 42;
f = [capture](int x) { return x + capture; };  // sizeof(lambda) 小 → 栈存储

// 大 lambda：堆分配
std::array<int, 1000> big;
f = [big](int x) { return big[x]; };  // sizeof(lambda) 大 → 堆分配
```

## 自己实现 SBO

```cpp
template <typename T, size_t BufferSize = 64>
class SmallOptimized {
    alignas(std::max_align_t) char buffer_[BufferSize];
    T* ptr_;

public:
    template <typename... Args>
    SmallOptimized(Args&&... args) {
        if (sizeof(T) <= BufferSize) {
            ptr_ = ::new (buffer_) T(std::forward<Args>(args)...);  // 栈存储
        } else {
            ptr_ = new T(std::forward<Args>(args)...);  // 堆分配
        }
    }

    ~SmallOptimized() {
        if (is_small()) {
            ptr_->~T();
        } else {
            delete ptr_;
        }
    }

    bool is_small() const {
        return reinterpret_cast<const char*>(ptr_) == buffer_;
    }
};
```

## 关键要点

> SSO/SBO 的核心思想：小对象在栈上存储避免堆分配，大对象回退到堆。性能提升来自避免堆分配（比栈分配慢 100 倍）。

> `sizeof(std::string)` 通常是 32 字节——这就是 SSO 缓冲区的大小限制。

## 相关模式 / 关联

- [[cpp-string深入]] — string 的 SSO
- [[cpp-function实现原理]] — function 的 SBO
