---
title: 数据传输指令 MOV
tags: [x86, assembly, MOV, 数据传输]
aliases: [MOV Instruction, MOV 指令, 数据传输指令, 数据传输指令 MOV]
created: 2026-04-04
updated: 2026-04-04
---

MOV 是汇编中最常用的指令，用于在寄存器、内存和立即数之间传输数据，注意 MOV 不支持 mem-to-mem 传输。

## MOV 基本形式

### 寄存器 ← 寄存器

```asm
mov eax, ebx       ; EAX = EBX
mov cl, dl         ; CL = DL（8 位）
mov rax, rbx       ; RAX = RBX（64 位）
```

### 寄存器 ← 立即数

```asm
mov eax, 42            ; EAX = 42
mov BYTE PTR [ebx], 0  ; 内存清零（通过立即数写内存）
mov rax, 0x123456789ABCDEF0  ; 64 位立即数（仅 MOV r64, imm64 支持）
```

### 寄存器 ← 内存

```asm
mov eax, [ebx]             ; EAX = *EBX
mov eax, [ebx + 4]         ; EAX = *(EBX + 4)
mov eax, [ebx + ecx*4]     ; EAX = array[ECX]
mov cl, [global_var]       ; CL = global_var
```

### 内存 ← 寄存器

```asm
mov [ebx], eax             ; *EBX = EAX
mov [ebx + 8], cl          ; *(EBX + 8) = CL
mov [array + ecx*4], edx   ; array[ECX] = EDX
```

### 内存 ← 立即数

```asm
mov DWORD PTR [ebx], 100   ; *EBX = 100
mov BYTE PTR [var], 'A'    ; var = 'A'
```

> [!warning] MOV 的限制
> - **不支持** `MOV mem, mem`（内存到内存）
> - **不支持** `MOV seg, seg`（段寄存器到段寄存器）
> - 段寄存器只能从寄存器或内存加载：`MOV ds, ax`

## MOVZX — 零扩展传送 (Move with Zero-Extend)

将小尺寸数据零扩展到大尺寸。

```asm
movzx eax, BYTE PTR [ebx]    ; AL = *EBX, 高 24 位清零
movzx eax, bx                ; AX = BX, 高 16 位清零
movzx ecx, dl                ; ECX = DL（零扩展）

; 用途：无符号字节/字转换为 32 位
; unsigned char c = buffer[i];
; int val = c;  // 编译为 MOVZX
```

## MOVSX — 符号扩展传送 (Move with Sign-Extend)

将小尺寸数据符号扩展到大尺寸。

```asm
movsx eax, BYTE PTR [ebx]    ; AL = *EBX, 高 24 位按符号位填充
movsx eax, bx                ; AX → EAX（符号扩展）
movsx ecx, dl                ; ECX = DL（符号扩展）

; 用途：有符号字节/字转换为 32 位
; signed char c = buffer[i];
; int val = c;  // 编译为 MOVSX
```

### MOVZX vs MOVSX 对比

```asm
mov BYTE PTR [var], 0xFF     ; var = 0xFF (-1 有符号, 255 无符号)

movzx eax, BYTE PTR [var]    ; EAX = 0x000000FF (255)
movsx  eax, BYTE PTR [var]   ; EAX = 0xFFFFFFFF (-1)
```

## LEA — 加载有效地址 (Load Effective Address)

计算地址但**不访问内存**，纯地址运算。

```asm
lea eax, [ebx + ecx*4 + 8]   ; EAX = EBX + ECX*4 + 8（地址计算）

; 常见用法
lea edi, [buffer]             ; EDI = &buffer
lea eax, [ecx + ecx*2]       ; EAX = ECX * 3（乘法技巧）
lea eax, [ecx*4]             ; EAX = ECX * 4

; x86-64: LEA + RIP 相对用于获取全局变量地址
lea rax, [rel my_global]      ; RAX = &my_global
```

> [!info] LEA vs MOV 的区别
> - `MOV eax, [ebx+4]` → 计算地址 EBX+4，然后**读取该地址的内存值**
> - `LEA eax, [ebx+4]` → 计算地址 EBX+4，将**地址本身**存入 EAX
> - LEA 不访问内存，纯粹是算术运算

## XCHG — 交换 (Exchange)

交换两个操作数的值。**访问内存时自动加 LOCK 前缀**。

```asm
xchg eax, ebx         ; 交换 EAX 和 EBX
xchg al, ah            ; 交换 AL 和 AH（交换字节的快捷方式）

; 内存交换（自动 LOCK）
xchg [counter], eax    ; 原子交换，常用于自旋锁

; 经典自旋锁
spin_lock:
    mov eax, 1
    xchg [lock_var], eax   ; 原子交换
    test eax, eax
    jnz spin_lock          ; 如果原值不为 0，继续自旋
```

## 特殊 MOV 指令

```asm
; 立即数到寄存器的短编码
xor eax, eax       ; 清零 EAX（比 MOV eax, 0 短 1 字节）

; 段寄存器操作
mov ds, ax          ; 从通用寄存器加载段寄存器
mov ax, ds          ; 读取段寄存器到通用寄存器

; 控制寄存器（特权指令）
mov eax, cr0        ; 读取 CR0
mov cr3, eax        ; 设置页目录基址

; 调试寄存器
mov dr0, eax        ; 设置断点地址 0
```

> [!tip] 关键要点
> - MOV 是最基础的指令，但不支持 mem-to-mem
> - MOVZX 用于无符号扩展，MOVSX 用于有符号扩展
> - LEA 是纯地址计算，常被编译器用于算术优化
> - XCHG 访问内存时自动 LOCK，是实现原子操作的基础
> - XOR reg, reg 是清零的最优方式（2 字节 vs MOV 的 5 字节）

## 关联

- [[内存寻址模式]]
- [[x86-指令编码格式]]
- [[通用寄存器详解]]
