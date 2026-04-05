---
title: "Linux proc 文件系统详解"
tags: [linux, proc, kernel, filesystem, 虚拟文件系统]
aliases: [procfs, /proc, proc文件系统, 内核接口]
created: 2026-04-05
updated: 2026-04-05
---

# Linux proc 文件系统详解

/proc 是一个虚拟文件系统，提供内核和进程运行时信息的接口，不占用磁盘空间。

## 核心机制

/proc 由内核动态生成，每次读取都是内核实时计算的结果。主要分为两类：

### 全局系统信息

```bash
cat /proc/cpuinfo              # CPU 型号、核心数、缓存
cat /proc/meminfo              # 内存总量、可用量、缓存
cat /proc/loadavg              # 1/5/15 分钟平均负载
cat /proc/uptime               # 系统运行时间和空闲时间
cat /proc/version              # 内核版本
cat /proc/stat                 # CPU 统计（user/system/idle）
cat /proc/interrupts           # 中断计数
cat /proc/diskstats            # 磁盘 IO 统计
cat /proc/net/tcp              # TCP 连接表
cat /proc/filesystems          # 支持的文件系统
```

### 进程信息（/proc/PID/）

```bash
cat /proc/$$/cmdline           # 启动命令行（\0 分隔）
cat /proc/$$/status            # 进程状态汇总
cat /proc/$$/stat              # 紧凑格式状态
cat /proc/$$/maps              # 内存映射
cat /proc/$$/fd/               # 打开的文件描述符
cat /proc/$$/environ           # 环境变量
cat /proc/$$/cwd               # 符号链接 → 当前工作目录
cat /proc/$$/exe               # 符号链接 → 可执行文件
cat /proc/$$/task/             # 线程信息
```

### 可调参数（sysctl 接口）

```bash
cat /proc/sys/net/ipv4/ip_forward           # IP 转发开关
cat /proc/sys/vm/swappiness                # swap 倾向
cat /proc/sys/kernel/pid_max               # 最大 PID

# 动态修改（立即生效，重启丢失）
echo 1 > /proc/sys/net/ipv4/ip_forward
echo 10 > /proc/sys/vm/swappiness

# 持久化
sysctl -w net.ipv4.ip_forward=1
# 或写入 /etc/sysctl.conf
```

## 与 sysfs 的对比

| | /proc | /sys |
|---|-------|------|
| 用途 | 进程信息 + 系统参数 | 设备和驱动 |
| 模型 | 平坦结构 | 层次化结构 |
| 典型内容 | cpuinfo, meminfo, PID/ | block/, net/, class/ |

## 关联
- [[linux-进程基础与-ps-命令]] — ps 依赖 /proc 读取进程信息
- [[linux-虚拟内存与-mmap]] — /proc/PID/maps 显示进程内存布局
- [[linux-内核模块管理]] — /proc/modules 等同 lsmod

## 关键结论

> /proc 是用户空间与内核之间的运行时接口：读取系统状态用 /proc，调优参数用 sysctl（映射到 /proc/sys/）。
