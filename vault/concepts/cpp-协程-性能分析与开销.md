---
title: 协程性能分析与开销
tags: [cpp20, coroutine, performance, overhead, allocation, benchmark]
aliases: [协程开销, 协程性能, coroutine 性能对比]
created: 2026-04-05
updated: 2026-04-05
---

# 协程性能分析与开销

**一句话概述：** 协程的挂起/恢复本身极快（~20-50ns，一次间接跳转），真正的开销来自协程帧的堆分配（~100-200ns）和 cache miss。用自定义 allocator 或编译器优化（HALO）可以消除堆分配。

## 开销分解

```
操作                          典型耗时
─────────────────────────────────────
协程帧分配（operator new）    100-200 ns
协程帧释放（operator delete） 50-100 ns
co_await 挂起                5-10 ns（跳转）
co_await 恢复                5-10 ns（跳转）
co_yield 产生值              10-20 ns
─────────────────────────────────────
对比：
线程上下文切换               1-10 μs（1000x 慢）
std::function 调用           3-5 ns
虚函数调用                   2-3 ns
```

## HALO 优化（Heap Allocation eLision Optimization）

```cpp
// 编译器可能优化掉堆分配
Task<int> simple() {
    co_return 42;
}

void caller() {
    auto t = simple();  // 编译器可能直接在栈上分配协程帧
    // 如果协程的生命周期完全在 caller 内且不逃逸
    // GCC/Clang 可以 elide 掉 operator new
}
// HALO 不保证，但 -O2 下简单协程通常能触发
```

## 自定义分配器

```cpp
struct Task {
    struct promise_type {
        // 自定义 operator new：从池中分配
        static void* operator new(size_t size) {
            return CoroutinePool::allocate(size);
        }
        static void operator delete(void* ptr, size_t size) {
            CoroutinePool::deallocate(ptr, size);
        }
        // ...
    };
};
// 10 万次协程分配：池分配 2ms vs malloc 20ms
```

## 关键要点

> 协程 vs 线程的真正优势不在单次调用速度，而在**规模**：10 万个协程（每个几百字节帧）vs 10 万个线程（每个 1-8MB 栈）。协程让你轻松处理百万并发。

> 协程帧大小 = 参数 + 局部变量（跨挂点存活的）+ promise_type + 管理开销。编译器会做 liveness analysis 去掉不需要保存的局部变量。

## 相关模式 / 关联

- [[cpp-协程机制深入]] — 协程帧布局
- [[cpp-性能分析与基准测试]] — 基准测试方法
- [[cpp-内存池分配器]] — 自定义分配
- [[cpp-异步编程模型对比]] — 性能对比
