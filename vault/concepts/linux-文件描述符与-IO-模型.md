---
title: Linux 文件描述符与 IO 模型
tags: [linux, fd, io, select, epoll, 阻塞]
aliases: [文件描述符, IO模型, select, poll, epoll, 阻塞IO, 非阻塞IO]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 文件描述符与 IO 模型

文件描述符（fd）是 Linux 一切皆文件抽象的核心，IO 模型决定了程序如何等待数据。

## 文件描述符

每个进程有自己的 fd 表，0/1/2 是标准输入/输出/错误。

```bash
# 查看进程 fd
ls -la /proc/<pid>/fd/
lsof -p <pid>                  # 查看进程打开的文件
ulimit -n                      # 查看 fd 上限
ulimit -n 65535                # 修改上限

# fd 类型
# 0-stdin, 1-stdout, 2-stderr
# 3+ 文件、socket、pipe、device
```

## 五种 IO 模型

### 1. 阻塞 IO（Blocking）

```
应用调用 read() → 内核等待数据 → 数据到达 → 拷贝到用户空间 → 返回
应用一直阻塞等待
```

### 2. 非阻塞 IO（Non-blocking）

```
应用轮询 read() → 没数据立即返回 EAGAIN → 再次轮询
CPU 浪费在轮询上
```

### 3. IO 多路复用（Multiplexing）

```c
// select（最多 1024 个 fd）
fd_set readfds;
select(maxfd+1, &readfds, NULL, NULL, NULL);

// poll（无 fd 数量限制）
struct pollfd fds[1000];
poll(fds, nfds, -1);

// epoll（Linux 最优方案）
int epfd = epoll_create1(0);
struct epoll_event ev;
ev.events = EPOLLIN;
ev.data.fd = listenfd;
epoll_ctl(epfd, EPOLL_CTL_ADD, listenfd, &ev);
int n = epoll_wait(epfd, events, MAXEVENTS, -1);
```

### 4. 信号驱动 IO（SIGIO）

内核数据准备好后发信号通知应用。

### 5. 异步 IO（AIO）

内核完成数据拷贝后通知应用，应用全程不阻塞。

## 关键要点

> epoll 是 Linux 高性能网络的基础：nginx、Redis、Node.js 都用 epoll。相比 select/poll，epoll 在大量连接（10K+）时性能优势明显。

> select 有 FD_SETSIZE（通常 1024）限制，poll 无限制但 O(n) 扫描，epoll 是 O(1) 事件通知。

## 相关笔记

- [[Linux 虚拟内存与 mmap]] — 内存映射 IO
- [[Linux TCP 连接状态与排查]] — 网络连接
