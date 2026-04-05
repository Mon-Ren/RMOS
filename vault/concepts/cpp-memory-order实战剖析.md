---
title: memory_order 实战剖析
tags: [cpp, concurrency, memory-order, atomic, acquire-release]
aliases: [内存序实战, memory_order 选择, acquire-release 实例]
created: 2026-04-05
updated: 2026-04-05
---

# memory_order 实战剖析

**一句话概述：** 六种 memory_order 不是让你都背下来——理解 `relaxed`（只保证原子性）、`acquire-release`（建立同步关系）、`seq_cst`（全局顺序）这三个层次，在实际场景中按需选择。

## 意图与场景

- 写无锁代码时选择正确的 memory_order
- 理解为什么默认的 `seq_cst` 往往够用但有时太贵
- 通过真实案例理解 acquire-release 同步的本质

## 六种内存序速查

| 内存序 | 语义 | 典型用途 | x86 开销 |
|--------|------|----------|----------|
| `relaxed` | 只保证原子性，无顺序约束 | 计数器、统计 | 几乎零 |
| `consume` | 数据依赖（实践中用 acquire 替代） | 几乎不用 | 零 |
| `acquire` | 本线程后续读写不能重排到此加载之前 | 读锁、读标志位 | 零（x86 天然保证） |
| `release` | 本线程先前读写不能重排到此存储之后 | 写锁、发布数据 | 零（x86 天然保证） |
| `acq_rel` | acquire + release | read-modify-write | 零（x86） |
| `seq_cst` | 全序，所有线程看到一致的操作顺序 | 默认选择 | `lock` 前缀 |

**x86 的 TSO 模型天然提供了 acquire-release 语义**，所以 `relaxed` 之外的内存序在 x86 上几乎不额外开销。但在 ARM/PowerPC 上差异显著。

## 实战案例

### 案例 1：统计计数器 —— `relaxed` 就够了

```cpp
#include <atomic>
#include <thread>
#include <vector>

std::atomic<uint64_t> counter{0};

// 场景：多线程递增计数，最终只读一次总值
// 只需要保证原子性，不要求线程间观察顺序
void worker() {
    for (int i = 0; i < 100000; ++i) {
        counter.fetch_add(1, std::memory_order_relaxed);
    }
}

// 10 个线程并行递增，主线程 join 后读取
// join() 建立了 happens-before 关系，所以 relaxed 完全够用
```

**为什么 relaxed 够用？**
- 每个 `fetch_add` 本身是原子的（不会丢失更新）
- `join()` 建立了线程间同步，主线程能看到所有更新
- 这里没有"先做 A 再做 B"的顺序约束

### 案例 2：发布-消费模式 —— acquire-release 的经典用法

```cpp
#include <atomic>
#include <thread>
#include <iostream>
#include <string>

struct Data {
    int value;
    std::string name;
};

Data* data = nullptr;
std::atomic<bool> ready{false};

// 生产者：构造数据，然后标记就绪
void producer() {
    data = new Data{42, "answer"};       // ① 普通写入
    ready.store(true, std::memory_order_release);  // ② release 存储
    // release 保证：① 的写入不会被重排到 ② 之后
    // 换句话说：看到 ready==true 的线程，一定能看到 data 的正确值
}

// 消费者：等待就绪，然后读取数据
void consumer() {
    while (!ready.load(std::memory_order_acquire)) {  // ③ acquire 加载
        // 自旋等待
    }
    // acquire 保证：③ 之后的读取不会被重排到 ③ 之前
    // 换句话说：看到 ready==true 后，一定能看到 data 的正确值
    std::cout << data->value << " " << data->name << "\n";  // ④ 普通读取
}
```

**同步关系图：**
```
producer:  ① 写 data ──release──→ ② 写 ready
                                ↓ (synchronizes-with)
consumer:  ③ 读 ready ←──acquire── ④ 读 data
```

`release` 存储和 `acquire` 加载建立了 **synchronizes-with** 关系，进而建立了 **happens-before** 关系：① happens-before ④。

### 案例 3：双重检查锁 —— `seq_cst` 不可少

```cpp
#include <atomic>
#include <mutex>
#include <memory>

class Singleton {
    static std::atomic<Singleton*> instance;
    static std::mutex mtx;

public:
    static Singleton* get() {
        Singleton* tmp = instance.load(std::memory_order_acquire);  // 第一次检查
        if (!tmp) {
            std::lock_guard<std::mutex> lock(mtx);
            tmp = instance.load(std::memory_order_relaxed);         // 第二次检查
            if (!tmp) {
                tmp = new Singleton();
                instance.store(tmp, std::memory_order_release);     // 发布
            }
        }
        return tmp;
    }
};
```

这个实现是正确的，但**微妙之处**在于：`acquire`/`release` 配对保证了 Singleton 的构造完成对其他线程可见。

但如果用更激进的写法（比如在某些场景用 `relaxed` 做第一次检查），就需要非常小心——在 ARM 上可能出现看到非空指针但对象未完全构造的情况。

### 案例 4：seq_cst 的代价 —— Dekker 算法的教训

```cpp
std::atomic<bool> flag1{false}, flag2{false};

// 线程 1
flag1.store(true, std::memory_order_seq_cst);   // A
bool r1 = flag2.load(std::memory_order_seq_cst); // B

// 线程 2
flag2.store(true, std::memory_order_seq_cst);   // C
bool r2 = flag1.load(std::memory_order_seq_cst); // D

// seq_cst 保证：不可能出现 r1==false && r2==false
// 如果把上面全换成 acquire-release，这个保证就不成立了！
```

**为什么需要 seq_cst？**

Dekker 算法的核心是"两个线程互相声明自己要进入、然后检查对方"。如果用 acquire-release，CPU 可以让两个 store 都"延迟"对另一个线程不可见（store buffer），导致两个线程都看到对方的旧值。

seq_cst 在 store 后加了一个全内存屏障（x86 上是 `lock` 前缀或 `mfence`），保证全局可见顺序一致。

### 案例 5：自旋锁 —— acquire-release 配对

```cpp
class SpinLock {
    std::atomic<bool> locked_{false};
public:
    void lock() {
        // CAS 失败时用 acquire（防止自旋中的读写被重排到 CAS 前）
        while (locked_.exchange(true, std::memory_order_acquire)) {
            // 自旋等待：x86 上加 pause 指令减少 CPU 空转
            __builtin_ia32_pause();
        }
        // 到这里，我们拿到了锁
        // acquire 保证：锁内的读写不会被重排到 lock() 之前
    }

    void unlock() {
        // release 保证：锁内的读写不会被重排到 unlock() 之后
        locked_.store(false, std::memory_order_release);
    }
};
```

## 决策流程

```
需要多线程访问同一个原子变量吗？
├── 否 → 不需要 atomic
└── 是 →
    只做计数器/统计（最终读一次）？
    ├── 是 → relaxed
    └── 否 →
        需要发布数据给其他线程？
        ├── 是 → store 用 release，load 用 acquire
        └── 否 →
            需要全局一致顺序（如 Dekker、SeqLock）？
            ├── 是 → seq_cst
            └── 否 → 先用 seq_cst，性能不够再降级
```

**实践建议：不确定就用 `seq_cst`。** 正确的 `relaxed` 比错误的 `relaxed` 快一万倍——因为后者是 bug。

## 关键要点

> x86 是强内存模型（TSO），`acquire`/`release` 在硬件层面几乎零开销——真正有性能差异的是 ARM 和 PowerPC。所以 x86 上优化内存序的收益有限，但在跨平台代码中至关重要。

> `memory_order_consume` 在 C++17 被"建议弃用"、C++20 中仍未移除——实践中直接用 `acquire` 替代。原因是编译器很难正确实现数据依赖追踪，几乎所有实现都把 `consume` 提升为 `acquire`。

> 选择内存序的核心是问自己："我需要在这两个操作之间建立什么顺序约束？" 如果没有约束需求，`relaxed`；如果需要"看到数据前先看到标志"，`acquire-release`；如果需要所有线程对多个原子变量的操作顺序一致，`seq_cst`。

## 相关模式 / 关联

- [[cpp-atomic与内存序]] — 六种内存序的正式定义
- [[cpp-内存屏障与CPU重排]] — 硬件层面的内存屏障
- [[cpp-内存模型与数据竞争]] — C++ 内存模型基础
- [[cpp-并发安全的数据结构设计]] — 锁和无锁设计
- [[原子指令与内存屏障]] — 硬件原子操作
- [[无锁数据结构]] — CAS-based 无锁数据结构
