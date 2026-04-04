---
title: NASM 汇编语法
tags: [assembly, nasm, syntax, x86]
aliases: [NASM语法, Netwide Assembler]
created: 2026-04-04
updated: 2026-04-04
---

NASM（Netwide Assembler）是 x86/x64 平台最流行的汇编器之一，采用 **Intel 语法**，目标操作数在左，源操作数在右。

## Intel 语法特点

NASM 使用 Intel 风格语法，与 AT&T 语法有显著区别：

| 特性 | Intel (NASM) | AT&T (GAS) |
|------|-------------|------------|
| 操作数顺序 | `mov dst, src` | `movl src, dst` |
| 寄存器 | `eax` | `%eax` |
| 立即数 | `42` | `$42` |
| 内存寻址 | `[eax+4]` | `4(%eax)` |

## 段定义与符号

```nasm
section .text           ; 代码段
global _start           ; 导出符号
extern printf           ; 外部符号引用

_start:
    mov eax, 4          ; 系统调用号 (write)
    mov ebx, 1          ; stdout
    mov ecx, msg        ; 缓冲区地址
    mov edx, 13         ; 长度
    int 0x80            ; 系统调用

section .data           ; 已初始化数据段
    msg db "Hello, World!", 10   ; 定义字节串
    num dw 42           ; 16 位字
    big dd 100000       ; 32 位双字
    huge dq 0x123456789ABCDEF0  ; 64 位四字

section .bss            ; 未初始化数据段
    buffer resb 256     ; 预留 256 字节
    array  resd 100     ; 预留 100 个双字
```

## 数据定义指令

```nasm
; DB — Define Byte (1 字节)
char    db  'A'            ; 单个字符
str     db  "Hello", 0     ; 以 null 结尾的字符串
bytes   db  0x55, 0xAA     ; 多个字节
times 16 db 0              ; 填充 16 个零字节

; DW — Define Word (2 字节)
wval    dw  1000

; DD — Define Double Word (4 字节)
dval    dd  3.14           ; 也可定义浮点数
addr    dd  _start         ; 地址

; DQ — Define Quad Word (8 字节)
qval    dq  12345678901234
```

## 宏定义

```nasm
; 简单宏（无参数）
%define SYSCALL_EXIT  1
%define SYSCALL_WRITE 4

; 带参数的宏
%macro syscall3 4       ; 4 个参数
    mov eax, %1
    mov ebx, %2
    mov ecx, %3
    mov edx, %4
    int 0x80
%endmacro

; 使用宏
syscall3 SYSCALL_WRITE, 1, msg, 13

; 带可变参数的宏
%macro push_all 0-8     ; 0 到 8 个参数
    %rep %0             ; %0 = 实际参数个数
        push %1
        %rotate 1       ; 旋转参数列表
    %endrep
%endmacro

%macro pop_all 0-8
    %rep %0
        %rotate -1
        pop %1
    %endrep
%endmacro
```

## 条件汇编

```nasm
%define BITS 32

%if BITS == 32
    ; 32 位特定代码
    mov eax, [esp+4]
%elif BITS == 64
    ; 64 位特定代码
    mov rax, [rsp+8]
%endif

; %ifdef / %ifndef
%ifdef DEBUG
    ; 调试版本代码
    call debug_print
%endif
```

## 与 GAS 语法的关键差异

```nasm
; === NASM (Intel 语法) ===
mov     eax, [ebx+ecx*4+8]   ; eax = *(ebx + ecx*4 + 8)
lea     edi, [esi+16]         ; 取地址
push    dword 42              ; push immediate
cmp     eax, 10
jge     .greater              ; 局部标号
```

```gas
# === GAS (AT&T 语法) ===
movl    8(%ebx,%ecx,4), %eax  # eax = *(ebx + ecx*4 + 8)
leal    16(%esi), %edi         # 取地址
pushl   $42                    # push immediate
cmpl    $10, %eax
jge     .L_greater
```

## 常用 NASM 伪指令

```nasm
; ALIGN — 对齐
align 16                ; 16 字节对齐
nop                     ; 填充用的 nop

; TIMES — 重复
times 510 db 0          ; 常用于 MBR 引导扇区
dw 0xAA55               ; 引导签名

; EQU — 常量定义
BUFFER_SIZE equ 256
SYS_READ    equ 3
SYS_WRITE   equ 4

; INCBIN — 包含二进制文件
; inccbinary "data.bin"    ; 注释掉避免实际包含
```

## 关键要点

> **NASM = Intel 语法 + 跨平台汇编器**，是 Linux/Windows x86 汇编的首选工具之一。

> **核心差异**：Intel 语法 `mov dst, src`（人在左），AT&T 语法 `movl src, dst`（源在左）。记忆：Intel 风格更直观。

> **宏功能强大**：`%macro` 支持参数、可变参数、条件汇编，是代码复用的核心机制。

> **段声明**：`.text`(代码), `.data`(已初始化数据), `.bss`(未初始化数据) 是最基础的三个 section。

## 关联

- [[GAS 汇编语法]]
- [[AT&T 与 Intel 语法对比]]
- [[汇编程序结构]]
- [[汇编与链接过程]]
