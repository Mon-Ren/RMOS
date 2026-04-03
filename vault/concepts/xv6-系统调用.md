---
title: "xv6 系统调用"
tags: [xv6, syscall, int80, kernel-interface]
aliases: ["system call", "系统调用"]
created: 2026-04-03
updated: 2026-04-03
---

# xv6 系统调用

系统调用是用户程序进入内核的唯一入口。xv6 通过 `int 0x80` 软中断实现。

## 调用链路

```
用户态: write(fd, buf, n)
  │
  │ usys.S: mov $SYS_write, %eax; int $T_SYSCALL
  ▼
内核态: trap() → syscall()
  │
  │ 从 trapframe 取参数
  │ syscalls[SYS_write]() → sys_write()
  ▼
sys_write() 执行内核功能
  │
  │ 返回值写入 trapframe->eax
  ▼
trap() 返回 → 用户态读 eax
```

## 参数传递

系统调用参数通过**用户栈**传递，而非寄存器：

```c
// 用户态调用 write(fd, buf, n)
// 栈布局：[retaddr][fd][buf][n]
// esp+4 = fd, esp+8 = buf, esp+12 = n

int argint(int n, int *ip) {
  return fetchint((myproc()->tf->esp) + 4 + 4*n, ip);
}
```

## syscall() 分发

```c
static int (*syscalls[])(void) = {
  [SYS_fork]    sys_fork,
  [SYS_exit]    sys_exit,
  [SYS_wait]    sys_wait,
  [SYS_pipe]    sys_pipe,
  [SYS_read]    sys_read,
  [SYS_kill]    sys_kill,
  [SYS_exec]    sys_exec,
  [SYS_fstat]   sys_fstat,
  [SYS_chdir]   sys_chdir,
  [SYS_dup]     sys_dup,
  [SYS_getpid]  sys_getpid,
  [SYS_sbrk]    sys_sbrk,
  [SYS_sleep]   sys_sleep,
  [SYS_uptime]  sys_uptime,
  [SYS_open]    sys_open,
  [SYS_write]   sys_write,
  [SYS_mknod]   sys_mknod,
  [SYS_unlink]  sys_unlink,
  [SYS_link]    sys_link,
  [SYS_mkdir]   sys_mkdir,
  [SYS_close]   sys_close,
};

void syscall(void) {
  int num = myproc()->tf->eax;
  if(num > 0 && num < NELEM(syscalls) && syscalls[num]) {
    myproc()->tf->eax = syscalls[num]();  // 返回值写回 eax
  } else {
    cprintf("unknown sys call %d\n", num);
    myproc()->tf->eax = -1;
  }
}
```

## 全部系统调用（21 个）

| 类别 | 系统调用 |
|------|----------|
| **进程** | fork, exit, wait, exec, kill, getpid, sleep, uptime |
| **文件** | open, close, read, write, fstat, dup, link, unlink, mknod, mkdir, chdir |
| **管道** | pipe |
| **内存** | sbrk |

## 安全检查

- `fetchint/fetchstr/argptr` 检查用户地址是否在进程地址空间内
- `argfd` 检查文件描述符是否有效
- 内核不信任用户传入的指针，所有边界检查都在参数提取阶段完成

## 关键要点

> xv6 系统调用的核心是 **int 0x80 + 函数指针表** 的两级分发。参数从用户栈提取而非寄存器（与 Linux 不同），返回值通过 trapframe->eax 传回。整个设计只有 21 个系统调用，但覆盖了 Unix 基本功能。

## 关联
- [[xv6 中断与陷阱]] — trap() 检测 T_SYSCALL 后调用 syscall()
- [[xv6 进程管理]] — fork/exit/wait/exec 的内核实现
- [[xv6 文件系统]] — open/read/write 的底层实现
- [[xv6 内存分配]] — sbrk 调用 growproc 扩展进程空间
- [[页表机制]] — 参数地址的合法性检查依赖页表
