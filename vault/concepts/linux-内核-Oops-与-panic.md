---
title: "Linux 内核 Oops 与 panic"
tags: [linux, kernel, oops, panic, crash, debug]
aliases: [Oops, kernel panic, 内核崩溃, kdump, crash dump]
created: 2026-04-05
updated: 2026-04-05
---

# Linux 内核 Oops 与 panic

内核 Oops 是内核发现错误时的"异常报告"，panic 是不可恢复的严重错误。

## Oops vs panic

| | Oops | panic |
|---|------|-------|
| 严重程度 | 中（杀掉出错进程） | 高（系统停止） |
| 系统状态 | 可能继续运行 | 必须重启 |
| 触发原因 | 空指针、非法内存 | 不可恢复错误 |
| 行为 | 杀进程 + 记录日志 | 停机 + 可能转储 |

## 分析 Oops

```
Unable to handle kernel NULL pointer dereference at virtual address 0000000000000000
Oops: 0002 [#1] PREEMPT SMP
CPU: 3 PID: 1234 Comm: myapp Tainted: P
RIP: 0010:my_function+0x42/0x100 [my_module]
```

关键信息：
- RIP/RSP：出错的指令地址和栈指针
- Call Trace：调用栈
- CR2：出错的内存地址

```bash
# 查看 Oops 日志
dmesg | grep -i "oops\|BUG\|RIP"
journalctl -k | grep -i oops

# 用 addr2line 解析地址
addr2line -e vmlinux 0xffffffffc0123456
```

## kdump 配置

```bash
# 安装
apt install linux-crashdump kexec-tools    # Debian
yum install kexec-tools                    # RHEL

# 配置
vim /etc/default/kdump-tools
# USE_KDUMP=1
# KDUMP_COREDIR="/var/crash"

# 预留内存（grub）
# /etc/default/grub
GRUB_CMDLINE_LINUX="crashkernel=256M"

update-grub
systemctl enable kdump-tools
```

## 分析 crash dump

```bash
# 用 crash 工具分析
crash /usr/lib/debug/boot/vmlinux-$(uname -r) /var/crash/<timestamp>/dump

crash> bt                 # 回溯
crash> ps                 # 进程列表
crash> mod                # 模块
crash> log                # 内核日志
```

## 关联
- [[linux-内核编译与配置]] — 编译带调试符号的内核
- [[linux-strace-与调试工具]] — 用户空间调试

## 关键结论

> Oops 后系统可能还能运行但状态不可信，应尽快保存数据并重启。生产服务器应配置 kdump：崩溃时自动保存内存转储，事后用 crash 工具分析根因。
