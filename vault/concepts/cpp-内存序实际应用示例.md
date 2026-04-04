---
title: C++ 内存序实际应用示例
tags: [cpp, memory-order, acquire-release, practical, example]
aliases: [内存序示例, acquire-release示例, 无锁队列, 自旋锁实现]
created: 2026-04-04
updated: 2026-04-04
---

# 内存序实际应用示例

理解内存序最好的方式是看实际例子——自旋锁、单次初始化、无锁队列。

## 自旋锁（acquire-release）

```cpp
class SpinLock {
    std::atomic_flag flag_ = ATOMIC_FLAG_INIT;
public:
    void lock() {
        while (flag_.test_and_set(std::memory_order_acquire)) {
            // 自旋等待
        }
    }
    void unlock() {
        flag_.clear(std::memory_order_release);
    }
};
// acquire 保证：获取锁之后的操作不会被重排到获取锁之前
// release 保证：释放锁之前的操作对获取锁的线程可见
```

## 单次初始化（双重检查锁）

```cpp
class Singleton {
    static std::atomic<Singleton*> instance_;
    static std::mutex mtx_;
public:
    static Singleton* get() {
        auto* p = instance_.load(std::memory_order_acquire);  // 第一次检查
        if (!p) {
            std::lock_guard<std::mutex> lock(mtx_);
            p = instance_.load(std::memory_order_relaxed);     // 第二次检查
            if (!p) {
                p = new Singleton();
                instance_.store(p, std::memory_order_release); // 发布
            }
        }
        return p;
    }
};
```

## 生产者-消费者标志

```cpp
std::atomic<bool> ready{false};
int data = 0;

// 生产者
void produce() {
    data = 42;                                          // (1) 写数据
    ready.store(true, std::memory_order_release);       // (2) 发布
}

// 消费者
void consume() {
    while (!ready.load(std::memory_order_acquire)) {}   // (3) 等待发布
    assert(data == 42);                                  // (4) 保证看到 (1)
}
// release-acquire 配对：(1) happens-before (4)
```

## 关键要点

> acquire-release 是最常用的内存序组合——它建立线程间的 happens-before 关系，保证数据可见性。

> 只有需要全局顺序一致性时才用 `seq_cst`——大部分同步用 acquire-release 就够了。

## 相关模式 / 关联

- [[cpp-atomic与内存序]] — 内存序理论
- [[cpp-内存模型与数据竞争]] — happens-before 关系
