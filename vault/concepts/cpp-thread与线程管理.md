---
title: std::thread 与线程管理
tags: [cpp, concurrency, thread, jthread, join, detach]
aliases: [thread, 线程, jthread, join, detach, 线程管理]
created: 2026-04-04
updated: 2026-04-04
---

# std::thread 与线程管理

`std::thread` 是 C++ 对操作系统线程的薄封装——创建即启动，必须明确生命周期管理（join 或 detach）。

## 意图与场景

- 并行执行独立任务
- CPU 密集型计算的并行化
- I/O 操作与计算的重叠

## 基本用法

```cpp
#include <thread>
#include <iostream>

void worker(int id) {
    std::cout << "Thread " << id << " running\n";
}

int main() {
    std::thread t1(worker, 1);     // 创建并启动线程
    std::thread t2(worker, 2);

    // ⚠️ 必须 join 或 detach，否则析构时 std::terminate()
    t1.join();     // 等待 t1 完成
    t2.join();     // 等待 t2 完成
}

// 传引用
void increment(int& counter) { counter++; }

int n = 0;
std::thread t(increment, std::ref(n));  // 必须用 std::ref 包装
t.join();
// n == 1
```

## jthread（C++20）

```cpp
#include <thread>

// jthread = thread + 自动 join + 停止令牌
std::jthread t([](std::stop_token st) {
    while (!st.stop_requested()) {   // 检查停止请求
        do_work();
    }
});

// 析构时自动 join（如果未 join 过）
// 不需要显式 join，异常安全更好

// 请求停止
t.request_stop();
```

## 线程管理要点

```cpp
// 获取硬件并发数
unsigned n = std::thread::hardware_concurrency();  // 返回 CPU 核心数（可能为 0）

// 线程 ID
std::thread::id tid = std::this_thread::get_id();

// 让出时间片
std::this_thread::yield();

// 休眠
std::this_thread::sleep_for(std::chrono::milliseconds(100));
std::this_thread::sleep_until(std::chrono::system_clock::now() + 1s);
```

## 常见陷阱

```cpp
// ❌ 忘记 join 或 detach
void bad() {
    std::thread t(work);
    // t 析构 → std::terminate()！
}

// ❌ 线程访问已销毁的局部变量
std::thread bad2() {
    int local = 42;
    return std::thread([&] { use(local); });  // 悬垂引用！
}

// ✅ RAII 包装
class ThreadGuard {
    std::thread& t_;
public:
    explicit ThreadGuard(std::thread& t) : t_(t) {}
    ~ThreadGuard() { if (t_.joinable()) t_.join(); }
    ThreadGuard(const ThreadGuard&) = delete;
};
```

## 关键要点

> `std::thread` 创建即启动。必须在销毁前 `join()`（等待完成）或 `detach()`（分离，后台运行），否则程序终止。

> C++20 的 `jthread` 解决了大部分 `std::thread` 的痛点——自动 join 和内置停止令牌。

## 相关模式 / 关联

- [[cpp-mutex与lock]] — 线程间同步
- [[cpp-future与async]] — 更高层的并发抽象
