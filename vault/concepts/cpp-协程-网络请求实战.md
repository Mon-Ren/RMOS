---
title: 协程网络请求实战
tags: [cpp20, coroutine, http, network, async, practical]
aliases: [协程 HTTP 请求, 异步网络编程实战]
created: 2026-04-05
updated: 2026-04-05
---

# 协程网络请求实战

**一句话概述：** 用协程写 HTTP 客户端：DNS 解析、TCP 连接、发送请求、接收响应，每步都是 co_await，整体看起来像同步代码。错误处理用 try-catch，超时用 WithTimeout 包装。

## 实战示例

```cpp
Task<HttpResponse> http_get(std::string host, int port, std::string path) {
    // DNS 解析（异步）
    auto addr = co_await async_resolve(host, port);

    // TCP 连接（异步）
    auto sock = co_await async_connect(addr);

    // 构造请求
    std::string req = "GET " + path + " HTTP/1.1\r\n"
                      "Host: " + host + "\r\n"
                      "Connection: close\r\n\r\n";

    // 发送（异步）
    co_await async_write(sock, req.data(), req.size());

    // 接收响应（异步，带超时）
    std::string response;
    char buf[4096];
    while (true) {
        auto n = co_await WithTimeout{
            async_read(sock, buf, sizeof(buf)),
            std::chrono::seconds(10)
        };
        if (n <= 0) break;
        response.append(buf, n);
    }

    close(sock.fd());
    co_return parse_http_response(response);
}

// 并发请求
Task<void> fetch_multiple() {
    // 同时发起 3 个请求
    auto task1 = http_get("api.example.com", 80, "/data1");
    auto task2 = http_get("api.example.com", 80, "/data2");
    auto task3 = http_get("api.example.com", 80, "/data3");

    // 等待全部完成
    auto [r1, r2, r3] = co_await when_all(task1, task2, task3);
    // 3 个请求在单线程事件循环中并行执行
}
```

## 关键要点

> 协程网络代码的调试方法：在每个 co_await 前后加日志，协程挂起/恢复的顺序就是执行顺序。用 valgrind/ASan 检测协程帧泄漏（忘记 destroy 的协程）。

> 生产代码需要处理：连接池复用、请求重试、断线重连、TLS/SSL、gzip 解压。这些都可以封装成 Awaitable，让业务代码保持简洁。

## 相关模式 / 关联

- [[cpp-协程-异步IO集成]] — 异步 IO Awaitable
- [[cpp-协程-task调度器实现]] — task 调度
- [[cpp-socket编程]] — TCP/UDP 基础
- [[cpp-epoll与高性能服务器模型]] — 事件循环
