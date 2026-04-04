---
title: AVX 指令集
tags: [x86, avx, simd, 256-bit]
aliases: [AVX, Advanced Vector Extensions]
created: 2026-04-04
updated: 2026-04-04
---

AVX（Advanced Vector Extensions）将 SIMD 寄存器扩展到 256 位（YMM），引入 VEX 前缀和三操作数语法，是 SSE 的重大升级。

## YMM 寄存器

```
YMM0 - YMM7    (x86-64: YMM0-YMM15)

每个 256 位：
├── XMM 部分（低 128 位）— 兼容 SSE
└── 高 128 位 — AVX 扩展

可视为：
├── 8 × 32 位 float
├── 4 × 64 位 double
└── 16 × 16 位 / 8 × 32 位 / 4 × 64 位整数 (AVX2)
```

## VEX 前缀 — AVX 编码革新

AVX 引入 **VEX 前缀**（Vector Extension Prefix），替代了 SSE 指令的 `66`/`F2`/`F3` + `0F`/`0F38`/`0F3A` 前缀序列：

```
传统 SSE 前缀：[66/F2/F3] [0F/0F38/0F3A] [操作码] [ModR/M]
VEX 前缀：     C4/C5 [R X B m-mmmm] [W vvvv L pp] [操作码]
```

VEX 好处：
- 消除传统前缀的冗余编码
- 支持三操作数（消灭隐式的 "目标 = 源1" 依赖）
- 消除 SSE 对目标寄存器的隐式破坏

## 三操作数语法（关键改进）

```nasm
; === SSE：两操作数，目标被覆盖 ===
addps   xmm0, xmm1       ; xmm0 = xmm0 + xmm1（破坏 xmm0）

; === AVX：三操作数，不破坏输入 ===
vaddps  ymm0, ymm1, ymm2  ; ymm0 = ymm1 + ymm2（ymm1 不变）
vaddps  xmm0, xmm1, xmm2  ; AVX 的 128 位模式
```

**优势**：减少 MOV 指令，编译器更容易优化。

## 打包浮点运算

```nasm
section .data
    align 32
    a: dd 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0
    b: dd 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0

section .text
global avx_ops
avx_ops:
    vmovaps ymm0, [a]              ; 加载 8 个 float
    vmovaps ymm1, [b]

    ; 打包加法
    vaddps  ymm2, ymm0, ymm1       ; ymm2 = [9,9,9,9,9,9,9,9]

    ; 打包乘法
    vmulps  ymm2, ymm0, ymm1       ; 逐元素乘

    ; 打包减法
    vsubps  ymm2, ymm0, ymm1

    ; 打包除法
    vdivps  ymm2, ymm0, ymm1

    ; 平方根
    vsqrtps ymm2, ymm0

    ; 最大/最小
    vmaxps  ymm2, ymm0, ymm1
    vminps  ymm2, ymm0, ymm1

    ; 融合乘加（FMA）—— 无中间舍入
    ; vfmadd213ps ymm0, ymm1, ymm2  ; ymm0 = ymm1 * ymm2 + ymm0

    ret
```

## 标量运算

```nasm
; AVX 标量浮点
vmovss  xmm0, [val]               ; 加载 1 个 float
vaddss  xmm0, xmm1, xmm2          ; xmm0[0] = xmm1[0] + xmm2[0]
vmulss  xmm0, xmm1, xmm2
vdivss  xmm0, xmm1, xmm2
vsqrtss xmm0, xmm1                ; xmm0[0] = sqrt(xmm1[0])
```

## 比较与混合

```nasm
; 打包比较
vcmpps  ymm0, ymm1, ymm2, 0x01    ; LT 比较
vcmpeqps ymm0, ymm1, ymm2         ; 相等

; 重排
vshufps ymm0, ymm1, ymm2, 0x1B    ; 每 128 位 lane 内重排
vperm2f128 ymm0, ymm1, ymm2, 0x20 ; 跨 lane 交换 128 位块

; 掩码移动
vmaskmovps ymm0, ymm1, [src]      ; 根据 ymm1 掩码加载
vmaskmovps [dst], ymm1, ymm0      ; 根据 ymm1 掩码存储
```

## AVX2 — 整数 256 位 SIMD

```nasm
; AVX2 将整数操作扩展到 256 位
vmovdqa ymm0, [int_data]          ; 加载 8 个 32 位整数

vpaddd  ymm0, ymm1, ymm2          ; 8 × 32 位加法
vpsubd  ymm0, ymm1, ymm2
vpmulld ymm0, ymm1, ymm2          ; 8 × 32 位乘法

; 128 位通道内操作
vphaddd ymm0, ymm1, ymm2          ; 水平加

; 跨通道重排
vpermd  ymm0, ymm1, ymm2          ; 用 ymm1 索引重排 ymm2 的 32 位元素
vpermps ymm0, ymm1, ymm2          ; float 版本
```

## AVX-512 — 512 位 SIMD

```nasm
; ZMM0-ZMM31（512 位）
vmovaps zmm0, [data]              ; 加载 16 个 float
vaddps  zmm0, zmm1, zmm2          ; 16 个 float 同时加

; 掩码寄存器 k0-k7（64 位布尔）
vaddps  zmm0 {k1}, zmm1, zmm2    ; 用 k1 掩码选择性加

; 融合操作
vfmadd132ps zmm0, zmm1, zmm2     ; zmm0 = zmm0 * zmm2 + zmm1

; 新指令
vreduceps zmm0, zmm1, 0x08       ; 取模
vrangeps  zmm0, zmm1, zmm2, 0x00  ; 取 min/max
```

### AVX-512 新特性

- **操作掩码（k 寄存器）**：条件执行，消除分支
- **更多寄存器**：32 个 ZMM（vs AVX 的 16 个 YMM）
- **新的操作码**：REDUCE, RANGE, GETMANT, GETEXP 等
- **EVEX 前缀**：替代 VEX，支持更多功能

## 完整示例：AVX 向量加法

```nasm
; void avx_vector_add(float *dst, float *a, float *b, int n)
; n 必须是 8 的倍数
section .text
global avx_vector_add
avx_vector_add:
    push    rbp
    mov     rbp, rsp
    push    rbx

    mov     rdi, [rbp+16]         ; dst
    mov     rsi, [rbp+24]         ; a
    mov     rdx, [rbp+32]         ; b
    mov     rcx, [rbp+40]         ; n
    shr     rcx, 3                ; n / 8

.loop:
    vmovaps ymm0, [rsi]           ; 加载 a[0..7]
    vmovaps ymm1, [rdx]           ; 加载 b[0..7]
    vaddps  ymm2, ymm0, ymm1      ; 8 个 float 相加
    vmovaps [rdi], ymm2           ; 存回 dst

    add     rsi, 32               ; 前进 8*4 = 32 字节
    add     rdx, 32
    add     rdi, 32
    dec     rcx
    jnz     .loop

    vzeroupper                    ; 清除高位，避免 SSE/AVX 切换惩罚！

    pop     rbx
    pop     rbp
    ret
```

> **注意**：`vzeroupper` 在混合使用 SSE 和 AVX 时至关重要，否则会有严重的性能惩罚。

## 关键要点

> **三操作数语法是最大改进**：`VADDPS dst, src1, src2` 不再隐式破坏 src1，减少 MOV 指令。

> **VEX 前缀**替代 SSE 的冗余前缀序列，编码更高效。

> **AVX2 扩展整数到 256 位**：AVX 只有浮点 256 位，AVX2 才有 `VPADDD ymm`。

> **AVX-512 引入掩码寄存器**：条件 SIMD 运算不需要分支预测——用 k 寄存器做选择。

> **务必 vzeroupper**：混合 SSE/AVX 代码不调 VZEROUPPER 会导致 50+ 周期的惩罚。

## 关联

- [[SSE 指令集]]
- [[SIMD 概念]]
- [[汇编优化技巧]]
