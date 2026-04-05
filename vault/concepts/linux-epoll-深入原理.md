---
title: "Linux epoll 深入原理"
tags: [linux, epoll, io, network, 多路复用]
aliases: [epoll, epoll_create, epoll_wait, epoll_ctl, LT, ET]
created: 2026-04-05
updated: 2026-04-05
---

# Linux epoll 深入原理

epoll 是 Linux 高性能网络的核心，相比 select/poll 在大规模并发连接下有数量级的性能提升。

## 核心 API

```c
int epfd = epoll_create1(0);              // 创建 epoll 实例

struct epoll_event ev;
ev.events = EPOLLIN;                       // 监听可读
ev.data.fd = listenfd;
epoll_ctl(epfd, EPOLL_CTL_ADD, listenfd, &ev);  // 添加 fd

struct epoll_event events[MAXEVENTS];
int n = epoll_wait(epfd, events, MAXEVENTS, -1); // 等待事件
for (int i = 0; i < n; i++) {
    if (events[i].events & EPOLLIN) {
        // 处理可读
    }
}
```

## 内部原理

```
用户调用 epoll_ctl(ADD) 
  → 内核建立 fd → epoll 实例的回调关系
  → fd 就绪时，回调将 fd 加入就绪链表

用户调用 epoll_wait
  → 检查就绪链表
  → 非空则立即返回（O(1)）
  → 为空则挂起等待
```

## LT vs ET

| 模式 | 全称 | 行为 |
|------|------|------|
| LT（默认） | Level Trigger | 只要有数据就一直通知 |
| ET | Edge Trigger | 状态变化时通知一次 |

```c
// ET 模式（必须非阻塞 + 读到 EAGAIN）
ev.events = EPOLLIN | EPOLLET;
fcntl(fd, F_SETFL, O_NONBLOCK);
```

```c
// ET 模式读取循环
while (1) {
    n = read(fd, buf, sizeof(buf));
    if (n < 0 && errno == EAGAIN) break;  // 读完了
    if (n <= 0) break;
    // 处理 buf
}
```

## 性能对比

| | select | poll | epoll |
|---|--------|------|-------|
| fd 上限 | 1024 | 无 | 无 |
| 检查方式 | O(n) 轮询 | O(n) 轮询 | O(1) 就绪通知 |
| fd 拷贝 | 每次全量 | 每次全量 | 只增删 |
| 10K 连接 | 慢 | 慢 | 快 |

## 关联
- [[linux-文件描述符与-IO-模型]] — IO 多路复用全景
- [[linux-TCP-连接状态与排查]] — TCP 连接管理

## 关键结论

> epoll 的 O(1) 事件通知机制是 Nginx/Redis/Node.js 高并发的基础。ET 模式减少了系统调用次数但编程更复杂（必须非阻塞 + 循环读到 EAGAIN）。
