---
title: "Linux SystemTap 动态追踪"
tags: [linux, systemtap, tracing, debug, probe]
aliases: [SystemTap, stap, 动态追踪, 探针, 内核追踪]
created: 2026-04-05
updated: 2026-04-05
---

# Linux SystemTap 动态追踪

SystemTap 是 Linux 的动态追踪框架，通过脚本语言在内核和用户空间插入探针（probe）收集运行时信息。

## 核心概念

```
探针（Probe）→ 事件触发 → 执行处理程序（Handler）→ 收集数据
```

### 探针类型

| 类型 | 说明 |
|------|------|
| kernel.function("func") | 内核函数入口 |
| kernel.function("func").return | 内核函数返回 |
| syscall.* | 系统调用 |
| process("app").function("func") | 用户函数 |
| timer.s(5) | 定时器 |

## 基本脚本

```stap
# 追踪系统调用
probe begin { printf("开始追踪\n") }
probe syscall.open { printf("%s 打开 %s\n", execname, user_string($filename)) }
probe end { printf("结束\n") }

# 统计函数调用
global counts
probe kernel.function("*@fs/*.c") { counts[ppfunc()] <<< 1 }
probe end {
    foreach (func in counts-)
        printf("%s: %d\n", func, @count(counts[func]))
}
```

## 使用

```bash
# 安装
apt install systemtap

# 运行脚本
stap -v script.stp
stap -e 'probe syscall.read { printf("%s\n", execname) }'

# 列出探针
stap -l 'syscall.*'
stap -l 'kernel.function("*tcp*")'

# 性能分析
stap -e 'global t; probe syscall.read { t[execname] <<< 1 } probe end { foreach(e in t-) printf("%s: %d\n", e, @count(t[e])) }'
```

## 与其他追踪工具对比

| | SystemTap | bpftrace | perf |
|---|-----------|----------|------|
| 脚本语言 | 类 awk | 类 awk | 命令行 |
| 安全性 | 编译内核模块 | eBPF 验证器 | 采样 |
| 性能影响 | 中等 | 低 | 低 |
| 用户追踪 | ✅ | ✅ | 有限 |

## 关联
- [[linux-BPF-与-eBPF]] — eBPF/bpftrace 是现代替代
- [[linux-strace-与调试工具]] — strace 是简单场景的首选

## 关键结论

> SystemTap 功能强大但需要 debuginfo 包且有一定风险（编译内核模块）。现代场景优先使用 bpftrace/bcc（基于 eBPF，更安全）。
