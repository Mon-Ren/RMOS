---
title: SSE 指令集
tags: [x86, sse, simd, floating-point]
aliases: [SSE, Streaming SIMD Extensions]
created: 2026-04-04
updated: 2026-04-04
---

SSE（Streaming SIMD Extensions）引入 128 位 XMM 寄存器和 SIMD 指令，让一条指令同时处理 4 个 float 或 2 个 double，是现代高性能计算的基础。

## XMM 寄存器

```
XMM0 - XMM7    (x86-32)
XMM0 - XMM15   (x86-64)

每个 128 位，可视为：
├── 4 × 32 位 float（单精度）
├── 2 × 64 位 double（双精度，SSE2）
└── 16 × 8 位 / 8 × 16 位 / 4 × 32 位 / 2 × 64 位整数（SSE2）
```

## 数据移动

```nasm
; === 对齐加载（要求 16 字节对齐，更快）===
movaps  xmm0, [aligned_data]     ; 加载 4 个 packed single
movapd  xmm0, [aligned_data]     ; 加载 2 个 packed double (SSE2)
movdqa  xmm0, [aligned_data]     ; 加载 packed 整数 (SSE2)

; === 非对齐加载（不要求对齐，稍慢）===
movups  xmm0, [unaligned_data]   ; 非对齐加载
movupd  xmm0, [unaligned_data]

; === 存储 ===
movaps  [dst], xmm0              ; 对齐存储
movups  [dst], xmm0              ; 非对齐存储

; === 标量加载（只加载低位一个元素）===
movss   xmm0, [float_val]        ; 加载 1 个 float 到低位，高位清零
movsd   xmm0, [double_val]       ; 加载 1 个 double

; === 整数移动（SSE2）===
movd    xmm0, eax                ; 32 位整数 → XMM 低位
movq    xmm0, rax                ; 64 位整数 → XMM 低位（x86-64）
movd    eax, xmm0                ; XMM 低位 → 32 位整数
```

## 打包浮点运算

```nasm
section .data
    align 16
    a: dd 1.0, 2.0, 3.0, 4.0       ; 4 个 float
    b: dd 5.0, 6.0, 7.0, 8.0
    result: dd 0.0, 0.0, 0.0, 0.0

section .text
global sse_add
sse_add:
    movaps  xmm0, [a]              ; xmm0 = [1.0, 2.0, 3.0, 4.0]
    movaps  xmm1, [b]              ; xmm1 = [5.0, 6.0, 7.0, 8.0]

    ; 打包加法：4 个 float 同时相加
    addps   xmm0, xmm1             ; xmm0 = [6.0, 8.0, 10.0, 12.0]

    ; 打包乘法
    mulps   xmm0, xmm1             ; 逐元素相乘

    ; 打包减法
    subps   xmm0, xmm1

    ; 打包除法
    divps   xmm0, xmm1

    movaps  [result], xmm0
    ret
```

## 标量浮点运算

```nasm
; 标量 = 只操作最低位元素
movss   xmm0, [pi]                ; xmm0 = [3.14, 0, 0, 0]
movss   xmm1, [e]                 ; xmm1 = [2.718, 0, 0, 0]

addss   xmm0, xmm1                ; xmm0[0] = 3.14 + 2.718
subss   xmm0, xmm1                ; xmm0[0] -= xmm1[0]
mulss   xmm0, xmm1                ; xmm0[0] *= xmm1[0]
divss   xmm0, xmm1                ; xmm0[0] /= xmm1[0]
sqrtss  xmm0, xmm0                ; xmm0[0] = sqrt(xmm0[0])

section .data
    pi: dd 3.1415926535
    e:  dd 2.7182818284
```

## 特殊数学函数

```nasm
; === 平方根 ===
sqrtps  xmm0, xmm1                ; 4 个 float 同时开方
sqrtpd  xmm0, xmm1                ; 2 个 double 开方 (SSE2)

; === 最大/最小值 ===
maxps   xmm0, xmm1                ; 逐元素取最大
minps   xmm0, xmm1                ; 逐元素取最小
maxss   xmm0, xmm1                ; 标量最大
minss   xmm0, xmm1                ; 标量最小

; === 取绝对值（需要技巧）===
andps   xmm0, [abs_mask]          ; 清除符号位

section .data
    align 16
    abs_mask: dd 0x7FFFFFFF, 0x7FFFFFFF, 0x7FFFFFFF, 0x7FFFFFFF

; === 比较 ===
cmpps   xmm0, xmm1, 0            ; 打包比较，EQ → 全 1 / 全 0
; 比较谓词：0=EQ, 1=LT, 2=LE, 4=NEQ, 5=NLT, 6=NLE
cmpeqps xmm0, xmm1               ; 等于（宏形式）
cmpltps xmm0, xmm1               ; 小于

; === 混合和重组 ===
shufps  xmm0, xmm1, 0x1B          ; 任意重排 4 个元素
unpcklps xmm0, xmm1               ; 低 2 元素交错
unpckhps xmm0, xmm1               ; 高 2 元素交错
movlhps  xmm0, xmm1               ; xmm1 低 64 位 → xmm0 高 64 位
movhlps  xmm0, xmm1               ; xmm1 高 64 位 → xmm0 低 64 位
```

## SSE2 整数运算

```nasm
; === 128 位整数操作 ===
movdqa  xmm0, [int_array]         ; 加载 4 个 32 位整数

paddd   xmm0, xmm1                ; 4 个 32 位整数同时加
psubd   xmm0, xmm1                ; 减
pmulld  xmm0, xmm1                ; 乘 (SSE4.1)

; 16 位整数
paddw   xmm0, xmm1                ; 8 个 16 位整数加
psubw   xmm0, xmm1

; 8 位整数
paddb   xmm0, xmm1                ; 16 个 8 位整数加

; 比较
pcmpeqd xmm0, xmm1                ; 32 位相等比较
pcmpgtd xmm0, xmm1                ; 32 位大于比较
```

## 完整示例：向量点积

```nasm
; float dot_product(float *a, float *b, int n)
; 计算 a 和 b 的 n 元素点积
section .text
global dot_product
dot_product:
    push    ebp
    mov     ebp, esp
    push    esi
    push    edi

    mov     esi, [ebp+8]          ; a
    mov     edi, [ebp+12]         ; b
    mov     ecx, [ebp+16]         ; n
    shr     ecx, 2                ; n / 4（每次处理 4 个）

    xorps   xmm0, xmm0            ; 累加器清零
.loop:
    movups  xmm1, [esi]           ; 加载 a[0..3]
    movups  xmm2, [edi]           ; 加载 b[0..3]
    mulps   xmm1, xmm2            ; 逐元素乘
    addps   xmm0, xmm1            ; 累加

    add     esi, 16
    add     edi, 16
    dec     ecx
    jnz     .loop

    ; 水平求和：将 xmm0 中 4 个 float 相加
    haddps  xmm0, xmm0            ; xmm0 = [a+b, c+d, a+b, c+d]
    haddps  xmm0, xmm0            ; xmm0 = [a+b+c+d, ...]

    pop     edi
    pop     esi
    pop     ebp
    ret
```

## 关键要点

> **打包运算 = SIMD 核心**：`ADDPS` 一条指令完成 4 个 float 的加法，理论 4 倍加速。

> **对齐很重要**：`MOVAPS`（对齐）比 `MOVUPS`（非对齐）快，数据应 16 字节对齐。

> **SSE2 = 整数 SIMD**：在 SSE 基础上增加整数打包运算（PADDD 等），成为 x86-64 的基线指令集。

> **标量 vs 打包**：`ADDSS` 只处理一个 float，`ADDPS` 处理 4 个。选择取决于你的数据是否可以并行。

## 关联

- [[SIMD 概念]]
- [[AVX 指令集]]
- [[x87 浮点指令 FPU]]
- [[浮点数表示与运算]]
- [[汇编优化技巧]]
