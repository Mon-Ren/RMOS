---
title: "Linux GDB 高级调试"
tags: [linux, gdb, debug, core, 追踪]
aliases: [GDB, gdb调试, 断点, 内存查看, 多线程调试]
created: 2026-04-05
updated: 2026-04-05
---

# Linux GDB 高级调试

GDB 是 Linux 最强大的调试器，支持断点、内存查看、多线程调试和远程调试。

## 启动方式

```bash
gdb ./app                       # 加载程序
gdb ./app core.1234             # 分析 core dump
gdb -p <pid>                    # 附加到运行进程
gdb --args ./app arg1 arg2      # 带参数启动
```

## 断点

```bash
(gdb) break main               # 函数断点
(gdb) break file.c:42          # 行断点
(gdb) break *0x400500          # 地址断点
(gdb) break func if x > 10    # 条件断点
(gdb) tbreak func              # 临时断点（命中一次删除）
(gdb) rbreak regex             # 正则断点
(gdb) watch var                # 数据断点（值变化时中断）
(gdb) rwatch var               # 读断点
(gdb) awatch var               # 读写断点
```

## 执行控制

```bash
(gdb) run                      # 运行
(gdb) continue                 # 继续
(gdb) step                     # 单步进入（s）
(gdb) next                     # 单步跳过（n）
(gdb) finish                   # 执行到函数返回
(gdb) until 100                # 执行到第 100 行
(gdb) return                   # 立即返回
```

## 内存与变量

```bash
(gdb) print variable           # 打印变量
(gdb) print *array@10          # 打印数组 10 个元素
(gdb) print/x variable         # 十六进制
(gdb) display variable         # 每步自动显示
(gdb) x/16xb 0x7fff1234        # 查看 16 字节十六进制
(gdb) x/10i $rip               # 查看 10 条指令
(gdb) info registers           # 寄存器
(gdb) info locals              # 局部变量
(gdb) set var x = 42           # 修改变量
```

## 多线程调试

```bash
(gdb) info threads             # 列出线程
(gdb) thread 2                 # 切换到线程 2
(gdb) thread apply all bt      # 所有线程回溯
(gdb) set scheduler-locking on # 只运行当前线程
```

## 关联
- [[linux-coredump-配置与分析]] — core dump 分析
- [[linux-strace-与调试工具]] — strace 系统调用追踪

## 关键结论

> GDB 的 watchpoint（数据断点）是最强大的功能之一：当变量值变化时自动中断。多线程调试用 `thread apply all bt` 一次看所有线程的状态，是排查死锁的利器。
