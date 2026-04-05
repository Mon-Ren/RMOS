---
title: Linux 进程基础与 ps 命令
tags: [linux, process, ps, top, proc]
aliases: [进程, ps, top, 进程管理, PID]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 进程基础与 ps 命令

进程是 Linux 资源分配的基本单位，理解进程模型是系统管理的基础。

## 进程核心概念

- **PID**：进程 ID，唯一标识
- **PPID**：父进程 ID
- **UID/GID**：进程的用户和组身份
- **进程状态**：R（运行）、S（可中断睡眠）、D（不可中断睡眠）、Z（僵尸）、T（停止）
- **进程组/会话**：终端控制的基础

## ps 命令

```bash
# 常用组合
ps aux                         # BSD 风格，所有进程详细信息
ps -ef                         # System V 风格，含 PPID
ps -eo pid,ppid,%cpu,%mem,cmd  # 自定义列
ps aux --sort=-%mem | head     # 按内存排序

# 查看特定进程
ps -p 1234                     # 查看指定 PID
ps -u alice                    # 查看用户进程
ps -C nginx                    # 按命令名
ps aux | grep nginx            # 管道过滤
```

## top / htop

```bash
top                            # 实时进程监控
# 交互键: P 按CPU排序, M 按内存, k 杀进程, q 退出
htop                           # 增强版（需安装）
```

## /proc 文件系统

```bash
cat /proc/1/cmdline            # 进程 1 的启动命令
cat /proc/1/status             # 进程状态
cat /proc/1/maps               # 内存映射
cat /proc/cpuinfo              # CPU 信息
cat /proc/meminfo              # 内存信息
cat /proc/loadavg              # 系统负载
```

## 关键要点

> PID 1 是 init/systemd，是所有用户进程的祖先。杀死 PID 1 等于关机。

> 僵尸进程（Z 状态）已终止但父进程未 wait() 回收，需要找到并处理父进程。

## 相关笔记

- [[Linux 信号与 kill 命令]] — 进程间通信信号
- [[Linux 后台任务与 nohup]] — 后台运行进程
