---
title: 信号处理最佳实践
tags: [system, signal, sigaction, async-signal-safe, posix]
aliases: [信号处理安全, async-signal-safe, 信号 handler]
created: 2026-04-05
updated: 2026-04-05
---

# 信号处理最佳实践

**一句话概述：** 信号处理函数中只能调用 async-signal-safe 的函数（约 120 个 POSIX 函数）。printf、malloc、new、mutex lock 都不安全。安全的做法：handler 里只设一个 atomic flag，主循环检查 flag 处理。

```cpp
#include <signal.h>
#include <atomic>

std::atomic<bool> g_shutdown{false};

void signal_handler(int) {
    g_shutdown.store(true, std::memory_order_release);
    // 这里只做这一件事：设 flag
    // 不调用 printf、不分配内存、不加锁
}

int main() {
    struct sigaction sa{};
    sa.sa_handler = signal_handler;
    sigaction(SIGINT, &sa, nullptr);

    while (!g_shutdown.load(std::memory_order_acquire)) {
        // 正常工作循环
    }
    // 收到 SIGINT 后安全退出
}
```

## 关键要点

> 永远用 sigaction 而非 signal()——signal() 的语义在不同系统上不一致（是否自动重置、是否阻塞其他信号）。

## 相关模式 / 关联

- [[信号机制]] — Unix 信号基础
- [[cpp-多进程编程]] — fork/exec
