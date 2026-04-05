---
title: "Linux IO uring 异步 IO"
tags: [linux, io_uring, async, aio, performance]
aliases: [io_uring, IOuring, 异步IO, 新一代AIO]
created: 2026-04-05
updated: 2026-04-05
---

# Linux IO uring 异步 IO

io_uring 是 Linux 5.1+ 引入的高性能异步 IO 框架，通过共享内存环形缓冲区减少系统调用。

## 核心设计

```
用户空间                    内核空间
┌──────────┐               ┌──────────┐
│ SQ (提交) │──提交请求──→│ SQ (消费) │
│ 环形缓冲区 │               │          │
├──────────┤               ├──────────┤
│ CQ (完成) │←──返回结果──│ CQ (发布) │
│ 环形缓冲区 │               │          │
└──────────┘               └──────────┘
```

### 工作流程

1. 用户将 IO 请求写入 SQ（Submission Queue）
2. 内核消费 SQ 中的请求
3. IO 完成后，内核将结果写入 CQ（Completion Queue）
4. 用户从 CQ 读取结果

## 基本使用

```c
#include <liburing.h>

struct io_uring ring;
io_uring_queue_init(32, &ring, 0);   // 队列深度 32

// 提交读请求
struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd, buf, size, offset);
io_uring_submit(&ring);

// 等待完成
struct io_uring_cqe *cqe;
io_uring_wait_cqe(&ring, &cqe);
int result = cqe->res;
io_uring_cqe_seen(&ring, cqe);
```

## 与 epoll/aio 对比

| | select/poll | epoll | aio | io_uring |
|---|------------|-------|-----|----------|
| 系统调用 | O(n) | O(1) 事件 | 多次 | 批量提交 |
| IO 模型 | 同步 | 同步 | 异步 | 异步 |
| 缓冲区 | 用户态 | 用户态 | 内核态 | 共享环 |
| 文件支持 | ✅ | ✅ | ❌ 有限 | ✅ 全部 |

## 支持的操作

io_uring 不仅支持文件 IO，还支持：
- 网络 IO（socket、accept、connect、send/recv）
- 文件操作（open、read、write、stat、rename）
- 异步 poll（替代 epoll）
- 注册固定文件/缓冲区（减少拷贝）

## 关联
- [[linux-文件描述符与-IO-模型]] — IO 模型全景
- [[linux-epoll-深入原理]] — epoll 是 io_uring 的前身

## 关键结论

> io_uring 是 Linux IO 的未来：通过共享内存环形缓冲区实现真正的零拷贝异步 IO。数据库（PostgreSQL/SQLite）、HTTP 服务器、文件拷贝工具都在迁移到 io_uring。内核 5.6+ 支持功能基本完整。
