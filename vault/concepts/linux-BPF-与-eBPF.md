---
title: "Linux BPF 与 eBPF"
tags: [linux, bpf, ebpf, observability, security, 网络]
aliases: [BPF, eBPF, 伯克利包过滤器, 内核可编程]
created: 2026-04-05
updated: 2026-04-05
---

# Linux BPF 与 eBPF

eBPF（extended Berkeley Packet Filter）允许在内核中安全运行沙箱程序，无需修改内核源码或加载内核模块。

## 核心概念

```
用户空间                内核空间
┌─────────┐           ┌──────────┐
│ 用户程序 │──load──→│ eBPF 验证器│
└─────────┘           │    ↓      │
                      │ eBPF 程序 │←──挂载点（hook）
┌─────────┐           │    ↓      │
│ BPF Map │←────────→│ BPF Map   │（数据共享）
└─────────┘           └──────────┘
```

### 验证器（Verifier）

- 验证程序不会崩溃内核
- 检查数组越界、无限循环、无效内存访问
- 保证程序安全才能加载

### 挂载点（Hook Points）

| 类型 | 挂载点 |
|------|--------|
| 网络 | XDP（网卡驱动）、TC、socket |
| 跟踪 | kprobe、uprobe、tracepoint |
| 安全 | LSM（Linux Security Module） |
| 调度 | sched_ext（调度器扩展） |

## 工具生态

```bash
# BCC 工具集
apt install bpfcc-tools
execsnoop                    # 监控进程执行
opensnoop                    # 监控文件打开
tcplife                      # 监控 TCP 连接生命周期
biosnoop                     # 监控块设备 IO
runqlat                      # 运行队列延迟

# bpftrace（一行式追踪）
bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args.filename)); }'

# bpftool（内核管理）
bpftool prog list            # 列出已加载程序
bpftool map list             # 列出 BPF Map
```

## 应用场景

- **网络**：XDP 高性能包过滤（替代 iptables 的 Cilium）
- **可观测性**：零开销追踪（替代 strace/perf）
- **安全**：容器运行时策略（Falco、KubeArmor）
- **调度**：sched_ext 自定义 CPU 调度器

## 关联
- [[linux-文件描述符与-IO-模型]] — eBPF 挂载在网络 IO 路径
- [[linux-namespace-隔离机制]] — eBPF 配合容器安全
- [[linux-性能分析工具]] — BCC/bpftrace 是性能分析利器

## 关键结论

> eBPF 是 Linux 内核的"可编程接口"：安全地在内核中运行用户定义的程序。它是可观测性（BCC/bpftrace）和高性能网络（Cilium/XDP）的基础技术。
