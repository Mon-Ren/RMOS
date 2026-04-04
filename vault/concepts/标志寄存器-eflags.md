---
title: 标志寄存器 EFLAGS
tags: [x86, assembly, flags, EFLAGS]
aliases: [EFLAGS, FLAGS, 标志寄存器, 标志寄存器 EFLAGS]
created: 2026-04-04
updated: 2026-04-04
---

EFLAGS 是 x86 的 32 位标志寄存器，存放运算结果的状态标志、CPU 控制标志和系统级标志，直接影响条件跳转和程序行为。

## EFLAGS 布局

```
31    ...    22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
┌───────────────┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│   (保留)      │ID│VP│VI│AC│VM│RF│ 0│NT│IOPL│OF│DF│IF│TF│SF│ZF│ 0│AF│ 0│PF│ 1│CF│
└───────────────┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
      系统标志                                          状态标志
```

## 状态标志（运算结果状态）

### CF — 进位标志 (Carry Flag)

无符号运算产生进位或借位时置 1。

```asm
mov al, 0xFF
add al, 0x01     ; AL = 0x00, CF = 1（产生进位）

mov al, 0x00
sub al, 0x01     ; AL = 0xFF, CF = 1（产生借位）

; 检测无符号溢出
jc carry_occurred   ; CF=1 则跳转
```

### ZF — 零标志 (Zero Flag)

运算结果为 0 时置 1。

```asm
mov eax, 5
sub eax, 5       ; EAX = 0, ZF = 1
jz result_is_zero  ; ZF=1 则跳转（JE 和 JZ 等价）
```

### SF — 符号标志 (Sign Flag)

运算结果最高位（符号位）为 1 时置 1。

```asm
mov al, 0x7F
add al, 0x01     ; AL = 0x80, SF = 1（结果为负）
```

### OF — 溢出标志 (Overflow Flag)

有符号运算溢出时置 1。

```asm
mov al, 0x7F     ; +127
add al, 0x01     ; AL = 0x80(-128), OF = 1（有符号溢出）
                 ; CF = 0（无符号 127+1=128，无进位）

jo overflow_occurred  ; OF=1 则跳转
```

### PF — 奇偶标志 (Parity Flag)

结果低 8 位中 1 的个数为偶数时置 1。

```asm
mov al, 0b00001111   ; 4 个 1，偶数
test al, al          ; PF = 1
```

### AF — 辅助进位标志 (Auxiliary Carry Flag)

低 4 位产生进位时置 1，用于 BCD 运算。

```asm
mov al, 0x0F
add al, 0x01     ; AF = 1（低 4 位进位）
```

## 控制标志

### DF — 方向标志 (Direction Flag)

控制字符串操作的方向。

```asm
cld              ; DF = 0，ESI/EDI 递增（正向）
std              ; DF = 1，ESI/EDI 递减（反向）

lea esi, [src]
lea edi, [dst]
mov ecx, 100
cld              ; 确保正向复制
rep movsb
```

### IF — 中断允许标志 (Interrupt Flag)

控制是否响应可屏蔽外部中断。

```asm
sti              ; IF = 1，允许中断
cli              ; IF = 0，禁止中断（内核关键代码常用）
```

### TF — 陷阱标志 (Trap Flag)

置 1 时每执行一条指令就触发单步异常，调试器利用此标志。

```asm
; 调试器设置 TF 后，每条指令执行完触发 INT 1
; 程序自身很少直接操作 TF
```

## 系统标志（特权级使用）

- **IOPL (I/O Privilege Level, 位 12-13)**：I/O 操作所需的最低特权级
- **NT (Nested Task, 位 14)**：任务嵌套标志
- **RF (Resume Flag, 位 16)**：控制调试异常的响应
- **VM (Virtual-8086 Mode, 位 17)**：启用虚拟 8086 模式

## 标志操作指令

```asm
; 通用标志操作
pushfd           ; EFLAGS 压栈
popfd            ; 弹出到 EFLAGS

; 单独操作进位标志
stc              ; CF = 1
clc              ; CF = 0
cmc              ; CF = ~CF

; 读取标志到 AH
lahf             ; AH = EFLAGS 低 8 位（SF,ZF,AF,PF,CF）
```

## 标志与条件跳转的关系

```
运算指令 (ADD/SUB/CMP/TEST/...)
       │
       ▼
  设置 EFLAGS
       │
       ▼
条件跳转指令 (Jcc) 读取 EFLAGS 决定是否跳转
```

```asm
cmp eax, ebx     ; EAX - EBX，结果丢弃，只设标志
jg  eax_greater   ; 有符号比较：eax > ebx → 跳转
ja  eax_above     ; 无符号比较：eax > ebx → 跳转
```

> [!tip] 关键要点
> - CF 用于**无符号**比较，OF/SF 用于**有符号**比较
> - ZF 通用：结果为零时置 1，不管有符号无符号
> - CMP = SUB 不保存结果，TEST = AND 不保存结果
> - DF 控制字符串操作方向：0=递增，1=递减
> - IF 控制中断：CLI 禁中断用于内核临界区

## 关联

- [[条件跳转指令]]
- [[比较与测试指令]]
- [[x86-寄存器概述]]
- [[通用寄存器详解]]
