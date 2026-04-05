---
title: io_uring 异步 I/O
tags: [system, io_uring, async-io, linux, kernel]
aliases: [io_uring 入门, 异步系统调用, Linux io_uring]
created: 2026-04-05
updated: 2026-04-05
---

# io_uring 异步 I/O

**一句话概述：** io_uring 是 Linux 5.1+ 的新一代异步 I/O 接口——通过两个环形缓冲区（SQ 提交队列、CQ 完成队列）实现用户态和内核态的零拷贝通信。比 epoll + 非阻塞 IO 更高效，比 aio 更通用（支持文件、网络、accept 甚至自定义操作）。

## 核心架构

```
用户态                          内核态
┌──────────┐                  ┌──────────┐
│ SQ ring  │─── 提交请求 ───→│ 内核处理  │
│ (提交队列)│                  │          │
│ [read]   │                  │ 完成后    │
│ [write]  │                  │          │
│ [accept] │                  │          │
└──────────┘                  └──────────┘
      ↑                              │
      │          CQ ring             │
      └──────── 完成通知 ←───────────┘

关键优势：
- 用户态直接写 SQ ring（无需系统调用）
- 内核直接写 CQ ring（无需唤醒用户态）
- 支持批量提交/完成（减少系统调用次数）
- 支持 fixed buffers（零拷贝）
```

## 基本用法

```cpp
#include <liburing.h>

void io_uring_example() {
    struct io_uring ring;
    io_uring_queue_init(32, &ring, 0);  // 队列深度 32

    // 提交读请求
    struct io_uring_sqe* sqe = io_uring_get_sqe(&ring);
    io_uring_prep_read(sqe, fd, buf, sizeof(buf), offset);
    io_uring_sqe_set_data(sqe, (void*)1);  // 用户数据

    // 提交到内核
    io_uring_submit(&ring);

    // 等待完成
    struct io_uring_cqe* cqe;
    io_uring_wait_cqe(&ring, &cqe);
    if (cqe->res >= 0) {
        // 读取成功，cqe->res 是读取的字节数
    }
    io_uring_cqe_seen(&ring, cqe);  // 标记已消费

    io_uring_queue_exit(&ring);
}
```

## 关键要点

> io_uring 的性能优势来自批量操作：一次 io_uring_submit 提交多个请求，一次 io_uring_peek_cqe 批量获取结果。减少系统调用次数是关键。

> io_uring 在高并发场景（>10K 连接）比 epoll 快 10-30%，因为减少了用户态/内核态切换。但学习曲线较陡，且需要 Linux 5.1+。

## 相关模式 / 关联

- [[cpp-epoll与高性能服务器模型]] — epoll 对比
- [[cpp-协程-异步IO集成]] — 协程 + io_uring
- [[cpp-非阻塞IO]] — 非阻塞操作
