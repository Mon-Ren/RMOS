---
title: 系统调用与用户态切换开销
tags: [system, syscall, context-switch, kernel, performance]
aliases: [系统调用开销, 用户态内核态切换, syscall 成本]
created: 2026-04-05
updated: 2026-04-05
---

# 系统调用与用户态切换开销

**一句话概述：** 一次系统调用的开销约 ~100-500ns（不含实际 I/O）——保存寄存器、切换到内核栈、执行内核代码、切换回用户态。SYSCALL/SYSENTER 指令比 INT 0x80 快（不查 IDT），但仍需 TLB 刷新（除非用 PCID）。

```
系统调用开销分解（x86-64, 现代 CPU）：
SYSCALL 指令:      ~20 ns（切换到内核模式）
内核入口开销:       ~30 ns（保存寄存器、切换栈）
内核逻辑:          ~20-100 ns（查表、参数校验）
SYSRET 指令:       ~20 ns（切换回用户模式）
TLB 刷新:          ~0-100 ns（取决于 PCID）

总计（无 I/O）:     ~100-300 ns
```

## 关键要点

> 减少系统调用的策略：批量操作（writev、sendmmsg）、用户态缓存（setvbuf）、用户态协议处理（io_uring 批量提交）、mmap 替代 read。

## 相关模式 / 关联

- [[cpp-系统调用封装]] — 系统调用包装
- [[cpp-epoll与高性能服务器模型]] — I/O 多路复用
- [[cpp-io_uring异步IO]] — 异步系统调用
- [[x86 系统调用演进]] — int 80h → syscall
