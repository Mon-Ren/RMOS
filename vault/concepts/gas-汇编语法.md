---
title: GAS 汇编语法
tags: [x86, assembly, GAS, AT&T, GNU]
aliases: [GAS Syntax, AT&T Syntax, GAS 汇编语法, AT&T 语法]
created: 2026-04-04
updated: 2026-04-04
---

GAS（GNU Assembler）使用 AT&T 语法，是 Linux/GCC 工具链的标准汇编格式，与 Intel/NASM 语法有显著差异。

## AT&T vs Intel 语法对比

| 特性 | AT&T (GAS) | Intel (NASM) |
|------|-----------|--------------|
| 操作数顺序 | 源在左，目标在右 | 源在右，目标在左 |
| 寄存器 | `%eax` | `eax` |
| 立即数 | `$42` | `42` |
| 内存寻址 | `(%eax)` | `[eax]` |
| 大小后缀 | `movl` | `mov dword` |
| 偏移 | `8(%eax)` | `[eax+8]` |

```asm
# AT&T 语法（GAS）
movl $42, %eax       # EAX = 42
movl %ebx, %eax      # EAX = EBX
movl (%ecx), %eax    # EAX = *ECX
addl $8, %eax        # EAX += 8

# Intel 语法（NASM）的等价写法
mov eax, 42
mov eax, ebx
mov eax, [ecx]
add eax, 8
```

## 寄存器前缀：%

所有寄存器名必须加 `%` 前缀。

```asm
movl %eax, %ebx      # EBX = EAX
pushl %ebp           # 压入 EBP
popl %ebp            # 弹出到 EBP

# x86-64
movq %rax, %rbx      # RBX = RAX
```

## 立即数前缀：$

```asm
movl $42, %eax       # EAX = 42（立即数）
movl $0x1000, %eax   # EAX = 0x1000

# 获取标签地址（类似 LEA）
movl $my_var, %eax   # EAX = &my_var（地址）
# vs
movl my_var, %eax    # EAX = my_var 的值（内存读取）
```

## 操作数大小后缀

AT&T 语法通过指令后缀指定操作数大小：

| 后缀 | 大小 | 示例 |
|------|------|------|
| `b` | byte (8位) | `movb`, `addb` |
| `w` | word (16位) | `movw`, `addw` |
| `l` | long (32位) | `movl`, `addl` |
| `q` | quad (64位) | `movq`, `addq` |

```asm
movb $0x42, (%eax)     # 写入 1 字节
movw $0x1234, (%eax)   # 写入 2 字节
movl $0x12345678, (%eax) # 写入 4 字节
movq $0x123456789ABCDEF0, (%rax) # 写入 8 字节

addb $1, %al           # AL += 1
addw $1, %ax           # AX += 1
addl $1, %eax          # EAX += 1
addq $1, %rax          # RAX += 1
```

## 内存寻址语法

```asm
# 直接寻址
movl my_var, %eax          # EAX = my_var 的值

# 寄存器间接寻址
movl (%eax), %ebx          # EBX = *EAX

# 基址 + 偏移
movl 8(%eax), %ebx         # EBX = *(EAX + 8)

# 基址 + 索引×比例 + 偏移
# 格式: displacement(base, index, scale)
movl 8(%eax, %ecx, 4), %ebx  # EBX = *(EAX + ECX*4 + 8)

# 完整 SIB 寻址
# offset(%base, %index, scale)
# scale 只能是 1, 2, 4, 8
```

### 段前缀

```asm
movl %fs:0x28, %eax       # EAX = FS:[0x28]（Linux 栈保护 canary）
movl %gs:0x0, %eax        # EAX = GS:[0]（per-CPU 数据）

# AT&T 中段前缀格式是 %seg:offset(%base)
movl %gs:16(%rsp), %rax   # RAX = GS:[RSP + 16]
```

## 伪指令 (Directives)

```asm
.section .data              # 数据段
.section .text              # 代码段
.section .bss               # 未初始化数据段
.section .rodata            # 只读数据段

.globl _start               # 全局符号（类似 NASM 的 global）
.global main                # 同上
.extern printf              # 外部符号

_start:                     # 标签（冒号可选）
main:

# 数据定义
.byte 0x42                  # 1 字节
.value 0x1234               # 2 字节（word）
.short 0x1234               # 2 字节
.long 0x12345678            # 4 字节
.int 0x12345678             # 4 字节
.quad 0x123456789ABCDEF0    # 8 字节
.ascii "Hello"              # ASCII 字符串（不含 \0）
.asciz "Hello"              # ASCII 字符串（含 \0）
.string "Hello"             # 同 .asciz
.string16 "Hello"           # UTF-16 字符串

# 对齐
.align 4                    # 4 字节对齐
.align 16                   # 16 字节对齐

# 等价
.equ BUFFER_SIZE, 1024      # 常量定义
.set BUFFER_SIZE, 2048      # 可重定义

# 填充
.zero 100                   # 100 字节零填充
.space 100, 0x90            # 100 字节 0x90 填充（NOP）
```

## 完整示例：Hello World（GAS 语法）

```asm
# hello.s — GAS/AT&T 语法, x86-64 Linux
.section .data
msg:
    .asciz "Hello, world!\n"
    len = . - msg - 1      # 字符串长度（不含 \0）

.section .text
.globl _start

_start:
    # write(1, msg, len)
    movq $1, %rax          # sys_write
    movq $1, %rdi          # fd = stdout
    leaq msg(%rip), %rsi   # buf = msg (RIP-relative)
    movq $len, %rdx        # count = len
    syscall

    # exit(0)
    movq $60, %rax         # sys_exit
    xorq %rdi, %rdi        # status = 0
    syscall
```

## GAS 与 NASM 的关键区别总结

```asm
# GAS (AT&T)                         # NASM (Intel)
movl $42, %eax                       mov eax, 42
movl %ebx, %eax                      mov eax, ebx
movl (%ecx), %eax                    mov eax, [ecx]
movl 8(%ecx,%edx,4), %eax            mov eax, [ecx+edx*4+8]
leaq msg(%rip), %rsi                 lea rsi, [rel msg]

pushl %ebp                           push ebp
popl %ebp                            pop ebp

.section .data                       section .data
.section .text                       section .text
.globl main                          global main
.long 0x12345678                     dd 0x12345678
.asciz "hello"                       db "hello", 0

cmpl $0, %eax                        cmp eax, 0
je .Lskip                            je skip
```

> [!tip] 关键要点
> - AT&T 语法：`源, 目标`（与 Intel 相反）
> - 寄存器加 `%`，立即数加 `$`
> - 大小后缀：b/w/l/q（不用 PTR）
> - 内存寻址：`disp(%base, %index, `scale)`
> - GAS 在 Linux/GCC 工具链中是默认汇编器
> - 可以在 GAS 中使用 `.intel_syntax noprefix` 切换到 Intel 语法

## 关联

- [[NASM 汇编语法]]
- [[AT&T 与 Intel 语法对比]]
- [[汇编与链接过程]]
