---
title: 系统调用指令
tags: [x86, assembly, syscall, 系统调用, SYSENTER]
aliases: [SYSCALL, SYSENTER, INT 0x80, 系统调用, 系统调用指令, 系统调用指令-syscall]
created: 2026-04-04
updated: 2026-04-04
---

系统调用是用户程序请求内核服务的接口，x86 提供了三种系统调用机制，从传统的 INT 0x80 到现代的 SYSCALL/SYSENTER。

## INT 0x80 — 传统 Linux 系统调用

最简单的系统调用方式，通过软件中断实现。

```asm
; 32 位 Linux 系统调用
; EAX = 系统调用号
; EBX, ECX, EDX, ESI, EDI, EBP = 参数 1-6

; write(1, msg, len)
mov eax, 4           ; sys_write
mov ebx, 1           ; fd = stdout
mov ecx, msg         ; buf = msg
mov edx, 13          ; count = 13
int 0x80             ; 调用内核

; exit(0)
mov eax, 1           ; sys_exit
xor ebx, ebx         ; status = 0
int 0x80

section .data
msg: db "Hello, world!", 10
```

### 常用 32 位 Linux 系统调用号

| 号码 | 名称 | 原型 |
|------|------|------|
| 1 | sys_exit | exit(int status) |
| 2 | sys_fork | fork() |
| 3 | sys_read | read(fd, buf, count) |
| 4 | sys_write | write(fd, buf, count) |
| 5 | sys_open | open(path, flags, mode) |
| 6 | sys_close | close(fd) |
| 9 | sys_mmap | mmap(addr, len, prot, flags, fd, off) |
| 11 | sys_execve | execve(path, argv, envp) |

## SYSENTER / SYSEXIT — Intel 快速系统调用

Intel Pentium II 引入，比 INT 0x80 快很多。

```asm
; SYSENTER 进入内核：
; 1. CS = IA32_SYSENTER_CS
; 2. EIP = IA32_SYSENTER_EIP
; 3. SS = IA32_SYSENTER_CS + 8
; 4. ESP = IA32_SYSENTER_ESP
; 5. EFLAGS 中的 IF 被清零

; 使用方式（32 位，glibc 封装）：
mov eax, syscall_number
mov edx, esp         ; 用户栈指针（内核用）
mov ecx, return_eip  ; SYSEXIT 返回地址
sysenter

; SYSEXIT 返回用户态
sysexit              ; CS = IA32_SYSENTER_CS+16, EIP=ECX, SS=CS+8, ESP=EDX
```

## SYSCALL / SYSRET — AMD 快速系统调用

AMD 引入，x86-64 Linux 的标准系统调用方式。

```asm
; 64 位 Linux 系统调用（SYSCALL）
; RAX = 系统调用号
; RDI, RSI, RDX, R10, R8, R9 = 参数 1-6

; write(1, msg, 13)
mov rax, 1           ; sys_write
mov rdi, 1           ; fd = stdout
lea rsi, [rel msg]   ; buf = msg
mov rdx, 13          ; count = 13
syscall              ; 调用内核，返回值在 RAX

; exit(0)
mov rax, 60          ; sys_exit
xor rdi, rdi         ; status = 0
syscall

section .data
msg: db "Hello, world!", 10
```

### SYSCALL 执行过程

```
1. RCX ← RIP（保存返回地址到 RCX）
2. R11 ← RFLAGS（保存标志到 R11）
3. RIP ← IA32_LSTAR（内核入口点，即 syscall_64）
4. CS ← IA32_STAR[47:32]
5. SS ← IA32_STAR[47:32] + 8
6. RFLAGS &= ~IA32_FMASK
```

### SYSRET 返回用户态

```asm
; SYSRET（内核使用）
; RIP = RCX（恢复用户态返回地址）
; RFLAGS = R11（恢复用户态标志）
; CS = IA32_STAR[63:48]+16
; SS = IA32_STAR[63:48]+8
sysretq              ; 64 位返回
```

## 三种系统调用方式对比

| 特性 | INT 0x80 | SYSENTER | SYSCALL |
|------|----------|----------|---------|
| 引入 | 8086 | Pentium II | AMD K6-2 |
| 位模式 | 32/64 | 32 | 64 |
| 速度 | 慢（~200+ 周期） | 快（~100 周期） | 快（~100 周期） |
| 保存返回地址 | 栈上（通过 INT） | 需手动设置 ECX | 自动存入 RCX |
| 保存标志 | 栈上（通过 INT） | 需手动设置 | 自动存入 R11 |
| 参数寄存器 | EBX,ECX,EDX,ESI,EDI,EBP | 需从用户栈读取 | RDI,RSI,RDX,R10,R8,R9 |

## 参数传递约定

### 32 位 (INT 0x80)

```asm
; EAX = 调用号
; 参数 1-6: EBX, ECX, EDX, ESI, EDI, EBP
; 返回值: EAX（负数表示错误，-errno）
; 超过 6 个参数：不支持（需要其他机制）

mov eax, sys_write
mov ebx, fd
mov ecx, buf
mov edx, len
int 0x80
test eax, eax        ; 检查返回值
js   error_handler   ; 负数 → 错误
```

### 64 位 (SYSCALL)

```asm
; RAX = 调用号
; 参数 1-6: RDI, RSI, RDX, R10, R8, R9
; 返回值: RAX（负数表示错误，-errno）

mov rax, sys_write
mov rdi, fd
mov rsi, buf
mov rdx, len
syscall
test rax, rax
js   error_handler
```

> [!info] 注意寄存器差异
> - 32 位用 EBX/ECX/EDX/ESI/EDI/EBP
> - 64 位用 RDI/RSI/RDX/R10/R8/R9（注意第 4 个参数是 R10 不是 RCX，因为 SYSCALL 会破坏 RCX）

## 完整示例：64 位 Hello World

```asm
; hello.asm — 64 位 Linux NASM
section .data
    msg db "Hello, world!", 10
    len equ $ - msg

section .text
    global _start

_start:
    ; write(1, msg, len)
    mov rax, 1
    mov rdi, 1
    lea rsi, [rel msg]
    mov rdx, len
    syscall

    ; exit(0)
    mov rax, 60
    xor rdi, rdi
    syscall
```

> [!tip] 关键要点
> - INT 0x80 是最传统的系统调用方式（32 位 Linux）
> - SYSCALL 是 x86-64 Linux 的标准方式
> - 64 位的参数寄存器不同于 32 位：RDI/RSI/RDX/R10/R8/R9
> - SYSCALL 破坏 RCX 和 R11，所以第 4 个参数用 R10
> - 返回值为负数时表示错误，绝对值是 errno

## 关联

- [[中断与异常指令]]
- [[x86-系统调用演进]]
- [[xv6 系统调用]]
- [[x86-调用约定-cdecl]]
