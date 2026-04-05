---
title: epoll 与高性能服务器模型
tags: [system, epoll, io-multiplexing, event-driven, reactor]
aliases: [epoll 深入, I/O 多路复用, Reactor 模型, 高并发服务器]
created: 2026-04-05
updated: 2026-04-05
---

# epoll 与高性能服务器模型

**一句话概述：** epoll 是 Linux 上 I/O 多路复用的终极方案——`epoll_create` 创建 epoll 实例，`epoll_ctl` 注册关注的 fd，`epoll_wait` 等待事件到来。相比 select/poll 的 O(n) 轮询，epoll 是 O(1) 的事件通知（内核维护就绪链表）。

## select/poll → epoll 的演进

```
select 的问题：
1. fd_set 有上限（默认 1024，改 FD_SETSIZE 需重编译）
2. 每次调用需要从用户态拷贝整个 fd_set 到内核
3. 内核需要遍历所有 fd 检查就绪状态 → O(n)
4. 返回后用户态也需要遍历所有 fd 找就绪的 → O(n)

poll 的改进：
1. 去掉了 1024 限制（动态数组）
2. 但还是 O(n) 轮询 + 完整拷贝

epoll 的改进：
1. 内核维护红黑树（管理关注的 fd）+ 就绪链表（rdllist）
2. epoll_ctl 注册一次，不用每次等待都传全部 fd
3. epoll_wait 只返回就绪的 fd → O(就绪数) 而非 O(总数)
4. 内核通过回调机制在事件发生时加入就绪列表
```

## epoll 三个系统调用

```cpp
#include <sys/epoll.h>
#include <unistd.h>
#include <fcntl.h>

// 1. 创建 epoll 实例
int epfd = epoll_create1(0);  // 返回 epoll 文件描述符

// 2. 注册/修改/删除关注的 fd
struct epoll_event ev;
ev.events = EPOLLIN | EPOLLET;  // 关注读事件 + 边缘触发
ev.data.fd = listen_fd;

epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);   // 添加
epoll_ctl(epfd, EPOLL_CTL_MOD, listen_fd, &ev);   // 修改
epoll_ctl(epfd, EPOLL_CTL_DEL, listen_fd, nullptr); // 删除

// 3. 等待事件
struct epoll_event events[64];
int n = epoll_wait(epfd, events, 64, -1);  // -1 = 无限等待
for (int i = 0; i < n; ++i) {
    if (events[i].events & EPOLLIN) {
        // 有数据可读
        handle_read(events[i].data.fd);
    }
}
```

## 水平触发 vs 边缘触发

```
水平触发（LT, Level-Triggered，默认）：
  只要缓冲区有数据可读，每次 epoll_wait 都会返回这个 fd
  → 编程简单，可以一次读不完下次再读
  → select/poll 就是水平触发

边缘触发（ET, Edge-Triggered）：
  只在状态从"没数据"变为"有数据"时通知一次
  → 必须一次读完（循环 read 直到 EAGAIN）
  → 减少 epoll_wait 调用次数，但编程复杂
  → 高性能服务器通常用 ET

为什么 ET 更快？
  LT：1000 字节到达 → epoll_wait 返回 → 读 100 字节 → epoll_wait 又返回（还有 900 字节）
  ET：1000 字节到达 → epoll_wait 返回 → 必须读到 EAGAIN → 只通知一次
```

## 完整的 Reactor 服务器框架

```cpp
#include <sys/epoll.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>
#include <cerrno>
#include <cstring>
#include <vector>
#include <functional>
#include <unordered_map>

void set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

class EpollServer {
    int listen_fd_;
    int epfd_;
    static constexpr int MAX_EVENTS = 1024;
    bool running_ = true;

    // 每个 fd 的回调
    using Handler = std::function<void(int fd, uint32_t events)>;
    std::unordered_map<int, Handler> handlers_;

public:
    EpollServer() {
        epfd_ = epoll_create1(0);
        if (epfd_ < 0) throw std::runtime_error("epoll_create1 failed");
    }

    ~EpollServer() { close(epfd_); }

    void add_fd(int fd, uint32_t events, Handler handler) {
        set_nonblocking(fd);
        handlers_[fd] = std::move(handler);

        struct epoll_event ev{};
        ev.events = events;
        ev.data.fd = fd;
        epoll_ctl(epfd_, EPOLL_CTL_ADD, fd, &ev);
    }

    void remove_fd(int fd) {
        epoll_ctl(epfd_, EPOLL_CTL_DEL, fd, nullptr);
        handlers_.erase(fd);
    }

    void listen(uint16_t port) {
        listen_fd_ = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, 0);
        int opt = 1;
        setsockopt(listen_fd_, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

        sockaddr_in addr{};
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);
        bind(listen_fd_, (sockaddr*)&addr, sizeof(addr));
        ::listen(listen_fd_, 128);

        add_fd(listen_fd_, EPOLLIN, [this](int fd, uint32_t) {
            while (true) {
                sockaddr_in client_addr{};
                socklen_t len = sizeof(client_addr);
                int client_fd = accept4(fd, (sockaddr*)&client_addr, &len,
                                        SOCK_NONBLOCK);
                if (client_fd < 0) break;

                add_fd(client_fd, EPOLLIN | EPOLLET, [this](int cfd, uint32_t ev) {
                    if (ev & EPOLLIN) {
                        char buf[4096];
                        while (true) {  // ET 模式必须读到 EAGAIN
                            ssize_t n = read(cfd, buf, sizeof(buf));
                            if (n > 0) {
                                write(cfd, buf, n);  // echo
                            } else if (n == 0) {
                                remove_fd(cfd);
                                close(cfd);
                                break;
                            } else {
                                if (errno == EAGAIN) break;
                                remove_fd(cfd);
                                close(cfd);
                                break;
                            }
                        }
                    }
                });
            }
        });
    }

    void run() {
        struct epoll_event events[MAX_EVENTS];
        while (running_) {
            int n = epoll_wait(epfd_, events, MAX_EVENTS, -1);
            for (int i = 0; i < n; ++i) {
                int fd = events[i].data.fd;
                auto it = handlers_.find(fd);
                if (it != handlers_.end()) {
                    it->second(fd, events[i].events);
                }
            }
        }
    }
};
```

## 关键要点

> epoll 的 `EPOLLET`（边缘触发）+ 非阻塞 fd 是高性能服务器的标准搭配。但必须用循环读到 `EAGAIN`/`EWOULDBLOCK`，否则会丢失数据。

> `EPOLLEXCLUSIVE`（Linux 4.5+）解决惊群问题——多个线程 `epoll_wait` 同一个 epfd 时，事件只唤醒一个线程。比 `EPOLLSHARE`（旧方案，所有线程唤醒）高效。

> epoll 不支持普通文件（磁盘文件总是"就绪"的），也不支持管道/终端的边缘触发。这些限制在使用时需要注意。

> 现代高性能服务器通常用 epoll + 线程池（one-loop-per-thread），或直接用 `io_uring`（Linux 5.1+ 的新异步 I/O 接口）。

## 相关模式 / 关联

- [[cpp-socket编程]] — TCP/UDP 基础
- [[cpp-非阻塞IO]] — 非阻塞操作
- [[cpp-线程池设计]] — epoll + 线程池模型
- [[cpp-io_uring]] — 下一代异步 I/O
- [[cpp-异步编程模型对比]] — Reactor vs Proactor
