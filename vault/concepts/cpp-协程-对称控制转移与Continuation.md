---
title: 对称控制转移与 Continuation
tags: [cpp20, coroutine, symmetric-transfer, continuation, goto-coroutine]
aliases: [对称控制转移, symmetric transfer, 协程跳转]
created: 2026-04-05
updated: 2026-04-05
---

# 对称控制转移与 Continuation

**一句话概述：** C++20 协程的 `await_suspend` 返回 `coroutine_handle` 就是"对称控制转移"——协程 A 挂起后不返回调用者，而是直接跳转到协程 B。这让协程之间的跳转不经过栈，避免栈溢出，也是实现调度器的关键机制。

## 非对称 vs 对称

```
非对称控制转移（普通函数/协程）：
  A 调用 B → B 返回 → 回到 A
  栈上：A → B → A → B → A（嵌套深度累加）

对称控制转移（C++20 co_await）：
  A co_await B → A 挂起 → 直接跳到 B → B 完成 → 跳到 C
  不经过 A 的调用者，直接在协程间跳转
  栈上始终只有 1-2 帧深度
```

## 实现机制

```cpp
struct Scheduler {
    // await_suspend 返回 coroutine_handle = 对称控制转移
    std::coroutine_handle<> await_suspend(std::coroutine_handle<> caller) {
        queue_.push(caller);          // 存储调用者
        auto next = queue_.front();   // 取下一个任务
        queue_.pop();
        return next;                  // 直接跳转到 next（不是返回 caller 的调用者）
    }
    // 返回 handle 后：
    // 当前协程挂起 → CPU 直接跳到返回的 handle 执行
    // 调用栈深度不变
};

// 链式任务不栈溢出
Task<void> process(int n) {
    if (n <= 0) co_return;
    co_await switch_to(pool_);    // 对称转移：不压栈
    process_data(n);
    co_await process(n - 1);      // 对称转移：递归但不栈溢出
}
```

## Continuation 传递风格

```cpp
// 协程本质上是 CPS（Continuation-Passing Style）的语法糖
// co_await expr 等价于：expr 完成后，执行 continuation（后续代码）

Task<int> example() {
    int a = co_await fetch_a();        // continuation: 计算 b
    int b = co_await fetch_b(a);       // continuation: 计算 c
    int c = a + b;                     // continuation: return c
    co_return c;
    // 编译器把整个函数切成 3 段，每段是一个 continuation
}
```

## 关键要点

> 对称控制转移是 C++20 协程相比 Boost.Coroutine 的关键改进。旧协程用 swapcontext（非对称），递归深度受限于栈大小。C++20 协程通过 heap 分配的协程帧 + 对称转移，递归深度只受限于内存。

> `await_suspend` 的三种返回类型：`void`（挂起，返回调用者）、`bool`（true=挂起，false=立即恢复）、`coroutine_handle`（对称转移）。

> 协程间通信的模式：A co_await B 时，A 把自己的 handle 传给 B 作为 continuation。B 完成后调用 A.resume()，或通过调度器安排 A 恢复。

## 相关模式 / 关联

- [[cpp-协程机制深入]] — 协程帧与状态机
- [[cpp-协程-task调度器实现]] — 调度器实现
- [[cpp-函数式编程模式]] — CPS 变换
- [[cpp-尾置返回类型]] — 尾调用优化
