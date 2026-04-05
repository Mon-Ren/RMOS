---
title: 协程调试技巧与常见陷阱
tags: [cpp20, coroutine, debugging, pitfalls, lifetime, dangling]
aliases: [协程调试, 协程陷阱, 协程生命周期问题]
created: 2026-04-05
updated: 2026-04-05
---

# 协程调试技巧与常见陷阱

**一句话概述：** 协程最常见的 bug 是生命周期问题——悬垂引用、协程帧泄漏、在错误的线程恢复。调试协程需要理解协程帧的分配/释放时机，以及 continuation 的传递路径。

## 陷阱 1：悬垂引用

```cpp
// ❌ 危险：临时变量的引用被协程帧保存
Task<int> broken() {
    std::string s = "hello";
    co_await async_operation();  // 挂起
    // s 的引用被保存在协程帧中
    // 如果 s 是栈上变量且调用者已经返回 → 悬垂引用
    co_return s.size();
}

// ✅ 安全：值捕获或确保生命周期
Task<int> safe() {
    auto s = std::make_shared<std::string>("hello");
    co_await async_operation();
    co_return s->size();  // shared_ptr 保证生命周期
}
```

## 陷阱 2：协程帧泄漏

```cpp
// ❌ 忘记 destroy
auto task = my_coroutine();
task.resume();
// task 析构时如果没调用 handle_.destroy() → 协程帧泄漏

// ✅ RAII 管理
Task::~Task() {
    if (handle_) handle_.destroy();
}
```

## 陷阱 3：线程安全

```cpp
// co_await 可能导致恢复在不同线程
Task<void> dangerous() {
    std::cout << "Thread: " << std::this_thread::get_id() << "\n";
    co_await async_io();  // 可能在 IO 线程恢复
    std::cout << "Thread: " << std::this_thread::get_id() << "\n";
    // 两次打印可能不同线程！
}
```

## 调试技巧

```cpp
// GDB：打印协程帧
(gdb) p __coro_frame
(gdb) x/20gx <coroutine_frame_address>

// 编译器标志
-fcoroutines   # 启用协程支持
-g             # 调试信息（包含协程帧信息）

// 内存检测
ASan 能检测协程帧泄漏（协程帧是堆分配的）
```

## 关键要点

> 协程调试最大的困难：调用栈不直观。协程 A 调用 co_await B，B 完成后恢复 A，但调用栈上看不到"从 B 返回到 A"的痕迹。解决：加日志追踪协程 ID 和挂起/恢复事件。

> 永远记住：协程帧可能比调用者的栈帧活得更久。任何以引用方式传入协程的局部变量都可能悬垂。安全做法：值传递或用 shared_ptr 管理。

## 相关模式 / 关联

- [[cpp-协程机制深入]] — 协程帧生命周期
- [[cpp-悬垂指针与use-after-free]] — 悬垂引用
- [[cpp-内存泄漏检测]] — ASan/valgrind
- [[cpp-调试技术与断言]] — 调试方法
