---
title: C++ 对象池模式
tags: [cpp, object-pool, memory-pool, arena, allocation, reuse]
aliases: [对象池, 内存池, memory pool, arena allocator, 复用]
created: 2026-04-04
updated: 2026-04-04
---

# 对象池模式

对象池预先分配一大块内存，从中快速分配和回收对象——避免频繁的堆分配。

## 简单对象池

```cpp
template <typename T, size_t PoolSize = 1024>
class ObjectPool {
    alignas(T) char buffer_[PoolSize * sizeof(T)];
    std::vector<T*> free_list_;
public:
    ObjectPool() {
        for (size_t i = 0; i < PoolSize; ++i) {
            free_list_.push_back(
                reinterpret_cast<T*>(buffer_ + i * sizeof(T)));
        }
    }

    template <typename... Args>
    T* acquire(Args&&... args) {
        if (free_list_.empty()) return nullptr;
        T* ptr = free_list_.back();
        free_list_.pop_back();
        return ::new (ptr) T(std::forward<Args>(args)...);  // placement new
    }

    void release(T* ptr) {
        ptr->~T();                    // 手动析构
        free_list_.push_back(ptr);    // 归还池
    }
};
```

## 使用场景

```cpp
// 场景：频繁创建销毁小对象
class Particle {
    float x, y, vx, vy;
public:
    Particle(float x, float y) : x(x), y(y), vx(0), vy(0) {}
};

ObjectPool<Particle, 10000> pool;
auto* p = pool.acquire(10.0f, 20.0f);
// ... 使用 ...
pool.release(p);  // 归还池中，不是 delete
```

## 与 PMR 的对比

```cpp
// C++17 PMR：标准库的对象池方案
#include <memory_resource>

char buffer[1024 * 64];
std::pmr::monotonic_buffer_resource pool{buffer, sizeof(buffer)};
std::pmr::vector<Particle> particles{&pool};
// 自动从 buffer 分配，不需要手动 release
```

## 关键要点

> 对象池的核心收益是避免堆分配——`new`/`delete` 比 placement new + 手动析构慢得多。

> PMR 的 `monotonic_buffer_resource` 是标准库中更通用的对象池方案——不需要手动 release，一次性释放。

## 相关模式 / 关联

- [[cpp-new与delete深入]] — placement new
- [[cpp-allocator与PMR]] — PMR 内存池
