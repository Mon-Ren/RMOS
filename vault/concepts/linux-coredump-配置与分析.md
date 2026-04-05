---
title: "Linux coredump 配置与分析"
tags: [linux, coredump, gdb, debug, crash]
aliases: [coredump, core dump, 核心转储, gdb调试, core文件]
created: 2026-04-05
updated: 2026-04-05
---

# Linux coredump 配置与分析

coredump 是进程崩溃时的内存快照，用于事后分析段错误、空指针等问题。

## 配置

```bash
# 查看/设置 core 文件大小限制
ulimit -c                        # 查看（0=禁用）
ulimit -c unlimited              # 当前 shell 不限

# 持久化 (/etc/security/limits.conf)
*  soft  core  unlimited
*  hard  core  unlimited

# core 文件路径和命名
cat /proc/sys/kernel/core_pattern
# /var/crash/core.%e.%p.%t     → core.nginx.1234.1700000000

# systemd-coredump（现代方式）
coredumpctl list                 # 列出 coredump
coredumpctl info <pid>           # 查看详情
coredumpctl gdb <pid>            # 用 gdb 分析
```

## GDB 分析

```bash
# 加载 core 文件
gdb ./myapp core.1234
# 或
gdb ./myapp -c core.1234

# 常用命令
(gdb) bt                         # 回溯调用栈
(gdb) bt full                    # 完整回溯含局部变量
(gdb) frame 2                    # 切换到第 2 帧
(gdb) info locals                # 查看局部变量
(gdb) print variable             # 查看变量值
(gdb) info registers             # 寄存器
(gdb) x/16x $rsp                 # 查看栈内存
```

## 常见段错误原因

```c
// 1. 空指针解引用
int *p = NULL;
*p = 42;                         // SIGSEGV

// 2. 释放后使用
free(p);
*p = 42;                         // SIGSEGV

// 3. 栈溢出
void recurse() { recurse(); }    // SIGSEGV

// 4. 越界访问
int arr[10];
arr[10000] = 1;                  // 可能 SIGSEGV
```

## 编译调试版本

```bash
gcc -g -O0 -fsanitize=address app.c -o app   # 带调试信息
gcc -g -O0 app.c -o app                       # 标准调试
```

## 关联
- [[linux-strace-与调试工具]] — strace 动态追踪
- [[linux-ELF-文件格式]] — ELF 调试信息

## 关键结论

> `coredumpctl` 是现代 Linux（systemd）分析崩溃的首选方式，比手动找 core 文件方便得多。编译时加 `-g` 保留符号信息，否则 core 文件中看不到函数名和变量名。
