---
title: 数据竞争检测与线程安全
tags: [cpp, concurrency, thread-safety, data-race, sanitizer, TSan]
aliases: [线程安全, thread safety, 数据竞争检测, TSan, ThreadSanitizer]
created: 2026-04-04
updated: 2026-04-04
---

# 数据竞争检测与线程安全

数据竞争是并发 bug 的主要来源——ThreadSanitizer 是发现它们的最强工具。

## ThreadSanitizer（TSan）

```bash
# 编译并启用 TSan
g++ -fsanitize=thread -g -O1 main.cpp -o main

# 运行
./main

# 输出示例：
# WARNING: ThreadSanitizer: data race
#   Write of size 4 at 0x7b04... by thread T2:
#     #0 worker() main.cpp:15
#   Previous read of size 4 at 0x7b04... by thread T1:
#     #0 reader() main.cpp:10
```

## 线程安全级别

```
线程安全级别          含义                          标注方式
不可变 (Immutable)   构造后不修改，天然线程安全     const
线程隔离 (Isolated)  每线程独立实例，无共享         thread_local
受保护 (Guarded)     所有访问需持有特定 mutex       GUARDED_BY(mtx)
线程安全 (Thread-safe) 任何调用组合都安全            可以用多个 mutex
条件线程安全         特定调用组合需外部同步          文档说明
非线程安全           不保证并发安全                 文档说明
```

## 常见线程安全模式

```cpp
// 1. 互斥锁保护
class ThreadSafeQueue {
    std::mutex mtx_;
    std::queue<int> q_;
public:
    void push(int val) {
        std::lock_guard<std::mutex> lock(mtx_);
        q_.push(val);
    }
    bool try_pop(int& val) {
        std::lock_guard<std::mutex> lock(mtx_);
        if (q_.empty()) return false;
        val = q_.front(); q_.pop();
        return true;
    }
};

// 2. 不可变对象（天然线程安全）
class Config {
    const std::string name_;
    const int timeout_;
public:
    Config(std::string n, int t) : name_(std::move(n)), timeout_(t) {}
    // 所有成员 const → 多线程只读 → 安全
};

// 3. 线程局部存储
thread_local std::mt19937 rng(std::random_device{}());
```

## 关键要点

> TSan 有运行时开销（约 2-15 倍变慢），但能捕获几乎所有数据竞争。开发阶段应始终开启。

> 线程安全文档应该写在类的头文件注释里——使用者需要知道哪些操作是安全的。

## 相关模式 / 关联

- [[cpp-内存模型与数据竞争]] — 数据竞争的定义
- [[cpp-atomic与内存序]] — 无锁同步
