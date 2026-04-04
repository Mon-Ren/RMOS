---
title: x87 浮点指令 FPU
tags: [x86, fpu, x87, floating-point]
aliases: [x87 FPU, 协处理器浮点]
created: 2026-04-04
updated: 2026-04-04
---

x87 FPU 是 x86 架构早期的浮点协处理器，使用**栈式寄存器**模型 ST(0)-ST(7)，虽然已被 SSE 取代，但仍在 BIOS/固件和某些遗留代码中使用。

## FPU 寄存器栈

```
ST(0)  ← 栈顶
ST(1)
ST(2)
ST(3)
ST(4)
ST(5)
ST(6)
ST(7)
```

- 8 个 80 位扩展精度寄存器
- 栈式操作：`FLD` 压栈，`FSTP` 弹栈
- 还有状态寄存器（Status Word）和控制寄存器（Control Word）

## 加载浮点数

```nasm
; === FLD — 加载（压栈）===
fld     dword [float_var]    ; 加载 32 位 float 到 ST(0)
fld     qword [double_var]   ; 加载 64 位 double 到 ST(0)
fld     tword [ext_var]      ; 加载 80 位扩展精度

fld     st0                  ; 复制 ST(0)（压入副本）

; 加载常量
fld1                         ; 压入 1.0
fldz                         ; 压入 0.0
fldpi                        ; 压入 π
fldl2e                       ; 压入 log₂(e)
fldl2t                       ; 压入 log₂(10)

section .data
    float_var  dd 3.14
    double_var dq 2.718281828
    ext_var    dt 1.0         ; 10 字节扩展精度
```

## 存储浮点数

```nasm
; === FST — 存储（不弹栈）===
fst     dword [result]       ; ST(0) → 32 位内存（截断）
fst     qword [result]       ; ST(0) → 64 位内存

; === FSTP — 存储并弹栈 ===
fstp    dword [result]       ; 存储后栈顶下移
fstp    qword [result]
fstp    tword [result]       ; 完整 80 位精度

; === FIST / FISTP — 整数存储 ===
fist    word [int_result]    ; ST(0) → 16 位整数
fistp   dword [int_result]   ; ST(0) → 32 位整数（弹栈）
fistp   qword [int_result]   ; ST(0) → 64 位整数
```

## 算术运算

```nasm
; === 双操作数运算（默认与 ST(0) 运算）===

; 加法
fadd    dword [val]          ; ST(0) += [val]
fadd    qword [val]
fadd    st0, st1             ; ST(0) = ST(0) + ST(1)
fadd    st1, st0             ; ST(1) = ST(1) + ST(0)（不改变栈顶）

; 减法
fsub    dword [val]          ; ST(0) -= [val]
fsub    st0, st1             ; ST(0) = ST(0) - ST(1)
fsubr   st0, st1             ; ST(0) = ST(1) - ST(0)（反向减）

; 乘法
fmul    dword [val]          ; ST(0) *= [val]
fmul    st0, st2

; 除法
fdiv    dword [val]          ; ST(0) /= [val]
fdivr   st0, st1             ; 反向除

; === 弹栈版本：运算后弹栈 ===
faddp   st1, st0             ; ST(1) += ST(0), 弹栈
fsubp   st1, st0
fmulp   st1, st0
fdivp   st1, st0
```

## 浮点比较

```nasm
; === FCOM / FCOMP / FCOMPP — 比较 ===
fcom    st1                  ; 比较 ST(0) 和 ST(1)
fcomp   st1                  ; 比较并弹栈
fcompp                       ; 比较 ST(0) 和 ST(1)，弹两次

; 比较内存值
fcom    dword [val]
fcomp   qword [val]

; === FCOMI — 直接设置 EFLAGS（Pentium Pro+）===
fcomi   st0, st1             ; 比较 ST(0) 和 ST(1)
                              ; CF, ZF, PF 直接设置
jae     .st0_gte_st1         ; 之后可用普通条件跳转

; === FTST — 与 0.0 比较 ===
ftst                          ; ST(0) 与 0.0 比较
```

### 比较后检查状态字

```nasm
fcom    st1
fnstsw  ax                    ; 状态字 → AX（不等待异常）
sahf                          ; AH → EFLAGS
jae     .greater_equal        ; ST(0) >= ST(1)
```

## 状态字和控制字

```nasm
; === FNSTSW — 读取状态字 ===
fnstsw  ax                    ; 状态字 → AX（不等待）
fstsw   ax                    ; 状态字 → AX（等待完成）

; 状态字位：
; C0 (bit 8) — 条件码
; C1 (bit 9) — 条件码
; C2 (bit 10) — 条件码
; C3 (bit 14) — 条件码

; === FNSTCW — 读取控制字 ===
fnstcw  [cw]                  ; 保存控制字
and     word [cw], 0xFCFF     ; 清除 RC 位
or      word [cw], 0x0400     ; 设置 RC = 01（截断模式）
fldcw   [cw]                  ; 加载控制字

; 控制字位：
; bits 0-1: 异常屏蔽
; bits 8-9: 精度控制（00=单, 10=双, 11=扩展）
; bits 10-11: 舍入控制（00=就近, 01=向下, 10=向上, 11=截断）
```

## 完整示例：浮点加法函数

```nasm
; float_add(a, b) → a + b
; 参数：a = [esp+4] (float), b = [esp+8] (float)
section .text
global float_add
float_add:
    fld     dword [esp+4]     ; 加载 a → ST(0)
    fadd    dword [esp+8]     ; ST(0) += b
    ; 返回值在 ST(0)（调用约定）
    ret

; double 的版本
global double_add
double_add:
    fld     qword [esp+4]
    fadd    qword [esp+12]
    ret

; 使用 FCOMI 比较
global float_max
float_max:
    fld     dword [esp+8]     ; b → ST(0)
    fld     dword [esp+4]     ; a → ST(0), b → ST(1)
    fcomi   st0, st1          ; 比较 a 和 b
    fstp    st1               ; 弹出较小值（或不用 fstp st1）
    cmovb   eax, edx          ; 如果 a < b，选择 b
    ret
```

## 与 SSE 的对比

| 特性 | x87 | SSE |
|------|-----|-----|
| 寄存器 | 8 个栈式 ST | 8/16 个扁平 XMM |
| 精度 | 80 位扩展 | 32/64 位 |
| SIMD | 不支持 | 支持 |
| 编译器默认 | 早期 GCC | 现代编译器 |
| 内核/BIOS | 常用 | 较少 |

## 关键要点

> **栈式寄存器模型**：`FLD` 压栈，`FSTP` 弹栈。操作在 ST(0)（栈顶）进行。这是与 SSE 最大的区别。

> **80 位扩展精度**：x87 的独特优势，中间计算用 80 位精度减少舍入误差——但这也导致跨平台结果不一致。

> **FCOMI 现代化**：Pentium Pro 引入的 FCOMI 直接设置 EFLAGS，比 FNSTSW+SAHF 组合更高效。

> **已被 SSE 取代**：现代编译器默认用 SSE 做浮点运算。x87 主要在 BIOS、引导加载程序和某些数值敏感场景保留。

## 关联

- [[SSE 指令集]]
- [[浮点数表示与运算]]
- [[x86-寄存器概述]]
