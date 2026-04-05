---
title: 类型擦除深度剖析
tags: [cpp, type-erasure, std-function, virtual-dispatch, sbo]
aliases: [类型擦除实现, std::function 原理, type erasure 手写]
created: 2026-04-05
updated: 2026-04-05
---

# 类型擦除深度剖析

**一句话概述：** 类型擦除的本质是"运行时多态 + 值语义"——用一个外部类持有数据，内部通过虚函数指针分发操作。`std::function<void()>` 可以装 lambda、函数指针、bind 表达式、任何 callable，因为它们都被擦除了具体类型，只剩一个统一的虚接口。

## 意图与场景

- 理解 `std::function` 为什么能装任何 callable
- 手写一个类型擦除容器，掌握其核心结构
- 理解 SBO（Small Buffer Optimization）在类型擦除中的应用

## 核心原理：两层结构

```
std::function<int(int)>
┌─────────────────────────────┐
│ 外壳（固定大小）              │
│   ├── vptr → 虚表           │
│   ├── SBO 缓冲区（~24字节）  │ ← 小对象存在栈上
│   └── 指向数据的指针          │ ← 大对象存在堆上
└─────────────────────────────┘
         │
         ▼ (vptr 指向的虚表)
┌─────────────────────────────┐
│ 派生模型<Callable>            │
│   ├── invoke(args) override │ ← 调用实际 callable
│   ├── clone_into(buf) override │ ← 拷贝到新位置
│   └── move_into(buf) override  │ ← 移动到新位置
│   └── callable 对象           │ ← 存储的实际数据
└─────────────────────────────┘
```

## 手写实现

```cpp
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <new>
#include <type_traits>
#include <utility>

template <typename Signature>
class Function;  // 未定义

template <typename R, typename... Args>
class Function<R(Args...)> {
    // SBO 缓冲区大小（std::function 通常是 16 或 24 字节指针大小）
    static constexpr size_t BufferSize = 32;
    static constexpr size_t BufferAlign = 8;

    // ─── 内部虚基类 ───
    struct Concept {
        virtual ~Concept() = default;
        virtual R invoke(Args... args) = 0;
        virtual Concept* clone_to(void* buf) = 0;
        virtual Concept* move_to(void* buf) = 0;
        virtual bool fits_inline() const = 0;
    };

    // ─── 派生模型：包装任意 callable ───
    template <typename F>
    struct Model : Concept {
        F func;

        template <typename U>
        explicit Model(U&& u) : func(std::forward<U>(u)) {}

        R invoke(Args... args) override {
            return func(std::forward<Args>(args)...);
        }

        Concept* clone_to(void* buf) override {
            if constexpr (sizeof(Model) <= BufferSize &&
                          alignof(Model) <= BufferAlign) {
                return ::new (buf) Model(func);  // placement new，拷贝构造
            } else {
                return new Model(func);           // 堆上分配
            }
        }

        Concept* move_to(void* buf) override {
            if constexpr (sizeof(Model) <= BufferSize &&
                          alignof(Model) <= BufferAlign) {
                return ::new (buf) Model(std::move(func));
            } else {
                return new Model(std::move(func));
            }
        }

        bool fits_inline() const override {
            return sizeof(Model) <= BufferSize && alignof(Model) <= BufferAlign;
        }
    };

    // ─── 存储 ───
    alignas(BufferAlign) char buffer_[BufferSize];  // SBO 缓冲区
    Concept* concept_;  // 指向实际对象（可能在 buffer_ 里，也可能在堆上）

    bool is_inline() const {
        return concept_ &&
               static_cast<const void*>(concept_) == static_cast<const void*>(buffer_);
    }

public:
    // ─── 构造 ───
    Function() noexcept : concept_(nullptr) {}

    template <typename F,
              typename = std::enable_if_t<
                  !std::is_same_v<std::decay_t<F>, Function>>>
    Function(F&& f) {
        using ModelT = Model<std::decay_t<F>>;
        static_assert(sizeof(ModelT) > 0, "Model must have content");
        if constexpr (sizeof(ModelT) <= BufferSize &&
                      alignof(ModelT) <= BufferAlign) {
            concept_ = ::new (buffer_) ModelT(std::forward<F>(f));
        } else {
            concept_ = new ModelT(std::forward<F>(f));
        }
    }

    // ─── 拷贝 ───
    Function(const Function& other) {
        if (other.concept_) {
            concept_ = other.concept_->clone_to(buffer_);
        } else {
            concept_ = nullptr;
        }
    }

    Function& operator=(const Function& other) {
        if (this != &other) {
            destroy();
            if (other.concept_) {
                concept_ = other.concept_->clone_to(buffer_);
            }
        }
        return *this;
    }

    // ─── 移动 ───
    Function(Function&& other) noexcept {
        if (other.concept_) {
            if (other.is_inline()) {
                concept_ = other.concept_->move_to(buffer_);
                other.destroy();
            } else {
                // 堆上对象：直接转移指针
                concept_ = other.concept_;
                other.concept_ = nullptr;
            }
        } else {
            concept_ = nullptr;
        }
    }

    // ─── 析构 ───
    ~Function() { destroy(); }

    void destroy() {
        if (concept_) {
            if (is_inline()) {
                concept_->~Concept();  // 析构但不释放（在 buffer 里）
            } else {
                delete concept_;        // 析构并释放堆内存
            }
            concept_ = nullptr;
        }
    }

    // ─── 调用 ───
    R operator()(Args... args) {
        if (!concept_) throw std::bad_function_call();
        return concept_->invoke(std::forward<Args>(args)...);
    }

    explicit operator bool() const noexcept { return concept_ != nullptr; }
};
```

## SBO 为什么重要

```
// 小 lambda（无捕获或少量捕获）→ 存在栈上的 buffer_ 里
Function<int(int)> f = [](int x) { return x * 2; };
// sizeof(lambda) = 1 → inline → 零堆分配

// 大 lambda（大量捕获）→ 堆上分配
std::array<int, 1000> big_data;
Function<int(int)> g = [big_data](int x) { return big_data[x]; };
// sizeof(lambda) = 4000 → heap allocated

// 性能差异：
// inline 调用：~1ns（一次间接跳转）
// heap 调用：~3ns（一次间接跳转 + 可能的 cache miss）
```

## 与虚函数的关系

类型擦除 = **外置虚表** + **值语义**。

传统继承多态：
```
Animal* a = new Dog();  // 指针语义，需要堆分配
a->speak();             // 通过 vptr 调用
delete a;               // 调用者管理生命周期
```

类型擦除：
```
std::function<void()> f = Dog{};  // 值语义
f();                              // 通过内部 vptr 调用
// f 离开作用域自动清理
```

区别：类型擦除的"虚表"不是由继承关系决定的，而是在构造时根据传入的类型**即时生成**的。这就是为什么它能装任意类型——不需要这些类型有共同的基类。

## 关键要点

> `std::function` 的 SBO 阈值在 GCC/Clang 上通常是 16 字节指针大小，在 MSVC 上是 6 + 1 个指针。无捕获 lambda 通常 1 字节，一定能 inline；捕获几个变量的 lambda 通常也能 inline。

> 类型擦除的代价：(1) 一次间接函数调用（虚调用），(2) 可能的堆分配，(3) 无法内联（编译器通常无法穿透虚调用做内联）。如果性能敏感且类型已知，优先用模板而非类型擦除。

> 手写类型擦除（而不是用 `std::function`）的好处是可以定制接口、控制内存分配、避免 `std::function` 的 type-erasure overhead。标准库的 `std::any`、`std::shared_ptr`（删除器）、`std::unique_ptr`（删除器）都是类型擦除的例子。

## 相关模式 / 关联

- [[cpp-function实现原理]] — std::function 的更多细节
- [[cpp-继承与多态]] — 传统虚函数 vs 类型擦除
- [[cpp-策略设计]] — 编译时多态 vs 运行时多态
- [[cpp-pimpl-惯用法]] — Pimpl 也是类型擦除的一种
- [[cpp-function与lambda性能对比]] — 调用开销比较
