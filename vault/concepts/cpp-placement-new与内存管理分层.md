---
title: placement new 与内存管理分层
tags: [cpp, placement-new, operator-new, memory-management, allocator]
aliases: [placement new, operator new 分层, 内存管理架构]
created: 2026-04-05
updated: 2026-04-05
---

# placement new 与内存管理分层

**一句话概述：** C++ 的 `new` 实际上分两步：先调 `operator new` 分配原始内存（类似 malloc），再调构造函数初始化对象。`placement new` 让你跳过分配步骤，直接在指定内存地址上构造对象——这是自定义内存管理（内存池、arena、对象池）的基础。

## 三个层次

```
用户代码                    new Widget(args)
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
第二层：构造函数调用              第一层：内存分配
Widget::Widget(args)           operator new(size_t)
(编译器自动插入)                (可自定义)
                    │                       │
                    └───────────┬───────────┘
                                ▼
第三层：底层分配
malloc(size) / mmap / VirtualAlloc
(通常你不需要管这一层)
```

## 四种 new 表达式

```cpp
#include <new>       // placement new 需要
#include <cstdlib>

// ─── 1. 普通 new ───
Widget* p = new Widget(args);
// 编译器展开为：
// void* mem = operator new(sizeof(Widget));  // 分配内存
// Widget* p = new(mem) Widget(args);          // 构造对象
// (注意：这里 new(mem) 是 placement new 语法)

// ─── 2. placement new ───
alignas(Widget) char buffer[sizeof(Widget)];  // 栈上缓冲区
Widget* p = new (buffer) Widget(args);
// 只调用构造函数，不分配内存
// 对象"活"在 buffer 里

// ─── 3. nothrow new ───
Widget* p = new (std::nothrow) Widget(args);
// 分配失败时返回 nullptr（不抛异常）

// ─── 4. 对齐指定的 new（C++17） ───
Widget* p = new (std::align_val_t{64}) Widget(args);
// 按 64 字节对齐分配（SIMD、缓存行对齐用）
```

## 自定义 operator new

```cpp
// 全局替换（影响所有 new 调用）
void* operator new(std::size_t size) {
    std::cout << "分配 " << size << " 字节\n";
    void* p = std::malloc(size);
    if (!p) throw std::bad_alloc();
    return p;
}

void operator delete(void* p) noexcept {
    std::free(p);
}

// 类特定的 operator new（只影响该类的 new）
class Widget {
public:
    static void* operator new(std::size_t size) {
        // 从自定义内存池分配
        return MemoryPool::allocate(size);
    }

    static void operator delete(void* p) {
        MemoryPool::deallocate(p);
    }

    // placement new 不需要自定义（编译器默认就行）
    // 但可以禁止非标准的 placement new
    static void* operator new(std::size_t, void* p) = delete;  // 禁止
};
```

## 实战：Arena 分配器

```cpp
#include <cstddef>
#include <memory>
#include <vector>

class Arena {
    std::byte* buffer_;
    std::byte* current_;
    size_t capacity_;

public:
    explicit Arena(size_t cap)
        : buffer_(static_cast<std::byte*>(std::malloc(cap)))
        , current_(buffer_)
        , capacity_(cap)
    {}

    ~Arena() { std::free(buffer_); }

    Arena(const Arena&) = delete;
    Arena& operator=(const Arena&) = delete;

    void* allocate(size_t size, size_t align = alignof(std::max_align_t)) {
        // 对齐当前指针
        std::uintptr_t addr = reinterpret_cast<std::uintptr_t>(current_);
        std::uintptr_t aligned = (addr + align - 1) & ~(align - 1);
        size_t padding = aligned - addr;

        if (padding + size > static_cast<size_t>(buffer_ + capacity_ - current_)) {
            throw std::bad_alloc();
        }

        void* result = reinterpret_cast<void*>(aligned);
        current_ = reinterpret_cast<std::byte*>(aligned) + size;
        return result;
    }

    // 重置：不释放内存，从头开始
    void reset() { current_ = buffer_; }

    size_t used() const { return current_ - buffer_; }
};

// 使用
void process_batch() {
    Arena arena(1024 * 1024);  // 1MB arena

    // 批量创建对象，零 malloc 开销
    std::vector<Widget*> widgets;
    for (int i = 0; i < 10000; ++i) {
        void* mem = arena.allocate(sizeof(Widget));
        widgets.push_back(new (mem) Widget(i));  // placement new
    }

    // 使用完毕，批量销毁
    for (auto* w : widgets) {
        w->~Widget();  // 手动调用析构函数
    }

    arena.reset();  // 一次性回收全部内存
    // 10000 次对象创建只用了 1 次 malloc
}
```

## placement new 的注意事项

```cpp
// 1. 内存必须对齐
alignas(Widget) char buffer1[sizeof(Widget)];  // ✅ 对齐了
char buffer2[sizeof(Widget)];                   // ❌ 可能未对齐！

// 2. 析构必须手动调用
Widget* p = new (buffer1) Widget();
// ... 使用 p ...
p->~Widget();        // ✅ 必须手动析构
// delete p;          // ❌ 不能 delete！buffer1 不是 malloc 分配的

// 3. placement new 后对象的生命周期
{
    alignas(Widget) char buf[sizeof(Widget)];
    Widget* w = new (buf) Widget();
    // w 的生命周期绑定到 buf 的作用域
    w->~Widget();
    // 离开作用域后 buf 销毁 → w 的内存没了
}

// 4. 可以用 std::launder（C++17）处理指针重用
// 当同一块内存被 placement new 重用后，旧指针变成"指针失效"
// 需要用 std::launder 获取有效指针
```

## 关键要点

> `new` 表达式和 `operator new` 函数是两个不同的东西。`new Widget()` 是语言关键字/表达式；`operator new(size_t)` 是可替换的库函数。`delete` 同理。

> placement new 的主要用途不是直接使用，而是实现自定义内存管理——对象池、arena、共享内存、内存映射文件上的对象构造等。

> `std::allocator` 的 `construct()` 在 C++17 前用 placement new，在 C++20 中被废弃（改用 `std::construct_at`，处理更完善的对齐和生命周期规则）。

## 相关模式 / 关关联

- [[cpp-new与delete深入]] — operator new/delete 完整指南
- [[cpp-对象池模式]] — 对象池中的 placement new
- [[cpp-allocator与PMR]] — 标准库分配器
- [[cpp-智能指针详解]] — 自动管理 vs 手动管理
- [[cpp-小对象优化]] — SBO 中的 placement new
