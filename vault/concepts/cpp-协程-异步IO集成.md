---
title: 协程与异步 I/O 集成
tags: [cpp20, coroutine, async-io, epoll, io_uring, awaitable]
aliases: [协程异步IO, co_await 网络读写, 异步文件IO协程]
created: 2026-04-05
updated: 2026-04-05
---

# 协程与异步 I/O 集成

**一句话概述：** 协程最大的价值是让异步 I/O 代码看起来像同步——`co_await async_read(fd)` 挂起协程、注册 epoll 回调，数据到达时 epoll 触发 resume，协程从挂起点继续。不需要回调嵌套、不需要 future 链。

## async_read Awaitable

```cpp
#include <coroutine>
#include <sys/epoll.h>
#include <unistd.h>

// 简化的异步读 Awaitable
class AsyncRead {
    int fd_;
    char* buf_;
    size_t len_;
    ssize_t bytes_read_ = -1;

public:
    AsyncRead(int fd, char* buf, size_t len)
        : fd_(fd), buf_(buf), len_(len) {}

    bool await_ready() {
        // 非阻塞尝试读
        bytes_read_ = ::read(fd_, buf_, len_);
        return bytes_read_ > 0 || (bytes_read_ < 0 && errno != EAGAIN);
    }

    void await_suspend(std::coroutine_handle<> h) {
        // 注册到 epoll，可读时唤醒
        EpollInstance::instance().add(fd_, EPOLLIN, [this, h]() mutable {
            bytes_read_ = ::read(fd_, buf_, len_);
            h.resume();  // 数据到达，恢复协程
        });
    }

    ssize_t await_resume() const {
        return bytes_read_;
    }
};
```

## 异步 TCP 回显服务器

```cpp
Task<void> handle_client(int client_fd) {
    char buf[4096];

    while (true) {
        // co_await 暂停协程，数据到达时恢复
        ssize_t n = co_await AsyncRead(client_fd, buf, sizeof(buf));
        if (n <= 0) break;

        // co_await 异步写
        ssize_t written = 0;
        while (written < n) {
            auto w = co_await AsyncWrite(client_fd, buf + written, n - written);
            if (w <= 0) break;
            written += w;
        }
    }
    close(client_fd);
}

Task<void> server_loop(int listen_fd) {
    while (true) {
        int client = co_await AsyncAccept(listen_fd);
        // 启动协程处理客户端（不等待完成）
        auto task = handle_client(client);
        task.resume();  // 启动协程
    }
}

// 启动
// auto server = server_loop(listen_fd);
// server.resume();
// event_loop.run();  // epoll 循环驱动所有协程
```

## co_await 的事件循环整合

```
事件循环（单线程）：
┌─────────────────────────────┐
│ epoll_wait()                 │ ← 等待事件
│   │                          │
│   ├─ 事件 1: fd=5 可读       │
│   │  └─ resume(handle_5)    │ ← 恢复等待 fd=5 的协程
│   │     协程从 co_await 继续  │
│   │     处理完数据再 co_await │ ← 再次挂起
│   │                          │
│   ├─ 事件 2: fd=8 可写       │
│   │  └─ resume(handle_8)    │
│   │                          │
│   └─ 事件 3: 定时器到期       │
│      └─ resume(handle_t)    │
└─────────────────────────────┘
```

## 关键要点

> 异步 I/O + 协程的核心收益：**单线程处理数千并发连接**。每个连接一个协程（协程帧只有几百字节），比每个连接一个线程（栈 1-8MB）节省几个数量级的内存。

> 协程的挂起/恢复成本极低（~10-50ns，只是一次间接跳转 + 栈指针切换），远低于线程上下文切换（~1-10μs，涉及内核态切换、缓存污染）。

> 生产级实现需要处理：取消（超时取消协程并注销 epoll 监听）、背压（写缓冲区满时暂停读）、异常传播（IO 错误在协程链中正确传播）。

## 相关模式 / 关联

- [[cpp-协程机制深入]] — 协程底层机制
- [[cpp-epoll与高性能服务器模型]] — epoll 原理
- [[cpp-io_uring]] — io_uring 异步 I/O
- [[cpp-异步编程模型对比]] — 各种异步模型对比
- [[cpp-协程-task调度器实现]] — task 调度
