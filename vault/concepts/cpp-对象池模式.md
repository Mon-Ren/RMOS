---
title: Object Pool 对象池模式
tags: [cpp, pattern, object-pool, performance]
aliases: [Object Pool, 对象池, 内存池, Arena Allocator, Memory Pool]
created: 2026-04-04
updated: 2026-04-04
---

# Object Pool 对象池模式

**一句话概述：** 预分配一块连续内存，通过 free list 管理空闲对象，复用已分配对象以避免频繁的 `new/delete` 开销——高频创建销毁场景的性能利器。

## 意图与场景

对象池解决"频繁分配/释放同类型小对象"的性能问题：

- **减少分配开销**：预分配大块内存，避免每次调用 malloc
- **改善缓存局部性**：对象连续存放，减少 cache miss
- **确定性延迟**：分配操作 O(1)，无系统调用

**适用场景：**
- 游戏引擎（粒子、子弹、敌人）
- 网络服务器（连接、请求对象）
- 数据库连接池
- 编译器（AST 节点）
- 高频交易系统

## C++ 实现代码

### 基本对象池（Free List）

```cpp
#include <vector>
#include <cstddef>
#include <new>
#include <type_traits>
#include <iostream>

template <typename T>
class ObjectPool {
    static_assert(sizeof(T) >= sizeof(void*), 
                  "T must be at least pointer-sized");
    
    struct Block {
        alignas(std::max_align_t) char data[sizeof(T)];
    };
    
    std::vector<Block> storage_;    // 预分配的内存块
    T* free_list_ = nullptr;        // 空闲对象链表
    std::size_t capacity_ = 0;

public:
    explicit ObjectPool(std::size_t initial_capacity = 64) 
        : storage_(initial_capacity), capacity_(initial_capacity) {
        // 初始化 free list
        for (std::size_t i = 0; i < capacity_; ++i) {
            auto* obj = reinterpret_cast<T*>(&storage_[i]);
            *reinterpret_cast<T**>(obj) = free_list_;
            free_list_ = obj;
        }
    }
    
    // 分配对象（构造）
    template <typename... Args>
    T* acquire(Args&&... args) {
        if (!free_list_) grow();  // 池满时扩容
        
        T* obj = free_list_;
        free_list_ = *reinterpret_cast<T**>(obj);
        return ::new (obj) T(std::forward<Args>(args)...);  // placement new
    }
    
    // 归还对象（析构）
    void release(T* obj) noexcept {
        if (!obj) return;
        obj->~T();
        *reinterpret_cast<T**>(obj) = free_list_;
        free_list_ = obj;
    }
    
    ~ObjectPool() {
        // 析构所有已分配对象（简化版：假设全部归还）
    }

private:
    void grow() {
        std::size_t new_cap = storage_.size() * 2;
        storage_.resize(new_cap);
        for (std::size_t i = capacity_; i < new_cap; ++i) {
            auto* obj = reinterpret_cast<T*>(&storage_[i]);
            *reinterpret_cast<T**>(obj) = free_list_;
            free_list_ = obj;
        }
        capacity_ = new_cap;
    }
};
```

### RAII 包装的对象池

```cpp
template <typename T>
class PoolAllocator {
    ObjectPool<T> pool_;

public:
    using value_type = T;
    
    explicit PoolAllocator(std::size_t cap = 128) : pool_(cap) {}
    
    T* allocate(std::size_t) { return pool_.acquire(); }
    void deallocate(T* p, std::size_t) { pool_.release(p); }
};

// RAII 包装：自动归还到池
template <typename T>
class PooledPtr {
    ObjectPool<T>* pool_;
    T* ptr_;
    
public:
    PooledPtr(ObjectPool<T>& pool, T* ptr) : pool_(&pool), ptr_(ptr) {}
    
    ~PooledPtr() { if (ptr_) pool_->release(ptr_); }
    
    PooledPtr(PooledPtr&& o) noexcept : pool_(o.pool_), ptr_(o.ptr_) {
        o.ptr_ = nullptr;
    }
    PooledPtr& operator=(PooledPtr&&) = delete;
    
    T& operator*()  const { return *ptr_; }
    T* operator->() const { return ptr_; }
    T* get()        const { return ptr_; }
    
    PooledPtr(const PooledPtr&) = delete;
    PooledPtr& operator=(const PooledPtr&) = delete;
};

// 使用
void demo() {
    struct GameEntity { int x, y; int hp = 100; };
    
    ObjectPool<GameEntity> pool(1024);
    
    auto entity = PooledPtr(pool, pool.acquire(10, 20));
    std::cout << "Entity HP: " << entity->hp << "\n";
    // 离开作用域自动归还到池
}
```

### Arena 分配器

```cpp
#include <cstddef>
#include <memory>

// Arena：一次性分配，一起释放
class Arena {
    std::unique_ptr<char[]> buffer_;
    std::size_t capacity_;
    std::size_t offset_ = 0;

public:
    explicit Arena(std::size_t cap) 
        : buffer_(std::make_unique<char[]>(cap)), capacity_(cap) {}
    
    void* allocate(std::size_t size, std::size_t align = alignof(std::max_align_t)) {
        // 对齐
        auto aligned = (offset_ + align - 1) & ~(align - 1);
        if (aligned + size > capacity_) throw std::bad_alloc();
        void* ptr = buffer_.get() + aligned;
        offset_ = aligned + size;
        return ptr;
    }
    
    void reset() noexcept { offset_ = 0; }  // 一次性释放所有
    
    std::size_t used() const noexcept { return offset_; }
};
```

## 优缺点

| 优点 | 缺点 |
|------|------|
| 分配/释放 O(1)，无系统调用 | 只能管理同类型对象 |
| 改善缓存局部性 | 池大小需预估，可能浪费内存 |
| 减少内存碎片 | 不支持任意大小分配 |
| 确定性延迟 | 对象析构需显式管理（或 RAII 包装） |

> [!tip] 关键要点
> 对象池本质是**用空间换时间**——预分配的内存替代了 malloc 的开销。实际项目中，优先使用 `std::vector`（连续内存 + 自动管理），只在 profile 证明确实需要时才引入对象池。Arena 分配器适合"批量创建、一次性释放"的场景（如编译器 AST）。

## 相关链接

- [[Flyweight 模式]] — 共享细粒度对象，互补思路
- [[cpp-raii-惯用法]] — 对象池的 RAII 包装
- [[cpp-智能指针详解]] — 自定义删除器实现自动归还
