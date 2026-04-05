---
title: Linux strace 与调试工具
tags: [linux, strace, debug, ltrace, gdb, 调试]
aliases: [strace, ltrace, gdb, 调试工具, 系统调用跟踪]
created: 2026-04-05
updated: 2026-04-05
---

# Linux strace 与调试工具

strace 跟踪进程的系统调用和信号，是排查"程序为什么不工作"的第一工具。

## strace 基础

```bash
# 跟踪程序启动
strace ls
strace -e trace=open,read,write ls   # 只跟踪特定调用
strace -e trace=file ls              # 文件相关调用
strace -e trace=network curl google.com  # 网络相关调用

# 跟踪已运行进程
strace -p <pid>
strace -p <pid> -f                  # 跟踪子进程

# 输出控制
strace -o trace.log ls              # 输出到文件
strace -c ls                        # 统计摘要（各调用次数和时间）
strace -T ls                        # 每个调用显示耗时
strace -e trace=network -t curl google.com  # 带时间戳
```

## 常见使用场景

```bash
# 程序找不到文件
strace -e trace=open,openat ./app 2>&1 | grep ENOENT

# 程序卡住，看它在等什么
strace -p <pid>
# 如果停在 poll/epoll_wait → 等网络
# 如果停在 futex → 等锁

# 程序网络连接失败
strace -e trace=network ./app 2>&1 | grep connect

# 看程序读了哪些配置文件
strace -e trace=openat ./app 2>&1 | grep -v ENOENT
```

## 其他调试工具

```bash
# ltrace — 跟踪库函数调用
ltrace ./app

# gdb — 交互式调试
gdb ./app
(gdb) break main
(gdb) run
(gdb) backtrace
(gdb) print variable

# ldd — 查看共享库依赖
ldd /usr/bin/python3

# objdump — 反汇编
objdump -d ./app | less

# readelf — 查看 ELF 文件
readelf -h ./app                # ELF 头
readelf -S ./app                # Section 列表
```

## 关键要点

> `strace -c` 统计模式可以快速看出程序在哪些系统调用上花了最多时间，适合性能瓶颈分析。

> strace 会显著降低程序速度（可能慢 10-100 倍），不要在生产环境长时间使用。

## 相关笔记

- [[Linux 文件描述符与 IO 模型]] — 系统调用基础
- [[Linux 性能分析工具]] — perf/vmstat
