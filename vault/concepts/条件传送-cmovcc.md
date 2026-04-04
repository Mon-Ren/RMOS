---
title: 条件传送 CMOVcc
tags: [x86, assembly, CMOVcc, 条件传送, 优化]
aliases: [CMOVcc, CMOV, CMOVZ, CMOVG, 条件传送, 条件传送 CMOVcc]
created: 2026-04-04
updated: 2026-04-04
---

CMOVcc 在条件成立时才执行 MOV 操作，是消除分支预测失败代价的核心优化手段，由 Pentium Pro（i686）引入。

## 基本语法

```asm
CMOVcc r16/32/64, r/m16/32/64   ; 条件成立时 dest = src
```

## 指令列表

### 无符号比较

| 指令 | 含义 | 条件 |
|------|------|------|
| CMOVZ / CMOVE | 等于则传送 | ZF = 1 |
| CMOVNZ / CMOVNE | 不等于则传送 | ZF = 0 |
| CMOVA / CMOVNBE | 高于则传送 | CF = 0 ∧ ZF = 0 |
| CMOVAE / CMOVNB | 高于等于则传送 | CF = 0 |
| CMOVB / CMOVNAE | 低于则传送 | CF = 1 |
| CMOVBE / CMOVNA | 低于等于则传送 | CF = 1 ∨ ZF = 1 |

### 有符号比较

| 指令 | 含义 | 条件 |
|------|------|------|
| CMOVG / CMOVNLE | 大于则传送 | ZF = 0 ∧ SF = OF |
| CMOVGE / CMOVNL | 大于等于则传送 | SF = OF |
| CMOVL / CMOVNGE | 小于则传送 | SF ≠ OF |
| CMOVLE / CMOVNG | 小于等于则传送 | ZF = 1 ∨ SF ≠ OF |

### 单标志

| 指令 | 条件 |
|------|------|
| CMOVS / CMOVNS | SF = 1 / SF = 0 |
| CMOVO / CMOVNO | OF = 1 / OF = 0 |
| CMOVP / CMOVNP | PF = 1 / PF = 0 |

## 使用示例

### 经典用法：条件赋值

```c
// C 代码
int abs_val(int x) {
    if (x < 0) x = -x;
    return x;
}
```

```asm
; 有分支版本
abs_val:
    test edi, edi
    jge .positive
    neg edi
.positive:
    mov eax, edi
    ret

; CMOV 版本（无分支）
abs_val:
    mov eax, edi
    neg eax             ; EAX = -x（无条件计算）
    cmovl eax, edi      ; 如果 x < 0, EAX = x(应为 -x)... 
    ; 正确写法：
    mov eax, edi
    mov ecx, edi
    neg ecx             ; ECX = -x
    test eax, eax
    cmovl eax, ecx      ; x < 0 时 EAX = -x
    ret
```

### max / min 函数

```c
int max(int a, int b) {
    return (a > b) ? a : b;
}
```

```asm
max:
    mov eax, edi        ; EAX = a
    cmp edi, esi
    cmovl eax, esi      ; 如果 a < b, EAX = b
    ret

min:
    mov eax, edi        ; EAX = a
    cmp edi, esi
    cmovg eax, esi      ; 如果 a > b, EAX = b
    ret
```

### 数组条件处理

```c
// 将数组中所有负数替换为 0
void clamp_negative(int *arr, int n) {
    for (int i = 0; i < n; i++) {
        if (arr[i] < 0) arr[i] = 0;
    }
}
```

```asm
clamp_negative:
    ; rdi = arr, rsi = n
    xor ecx, ecx
.loop:
    cmp ecx, esi
    jge .done
    mov eax, [rdi + rcx*4]
    xor edx, edx           ; EDX = 0
    test eax, eax
    cmovs eax, edx         ; 如果 EAX < 0, EAX = 0
    mov [rdi + rcx*4], eax
    inc ecx
    jmp .loop
.done:
    ret
```

## CMOV vs 分支跳转：性能对比

```
分支版本（可能分支预测失败）:
    cmp eax, ebx
    jle .else       ← 预测失败时流水线清空（~15-20 周期惩罚）
    mov ecx, edx
    jmp .end
.else:
    mov ecx, esi
.end:

CMOV 版本（无分支，始终执行）:
    cmp eax, ebx
    mov ecx, edx    ← 始终执行（两个路径都准备好）
    cmovle ecx, esi  ← 条件成立时覆盖（无分支预测）
```

> [!info] 何时使用 CMOV
> - ✅ 条件赋值（简单的 if-else，两边都是简单表达式）
> - ✅ 分支预测困难（数据随机，如排序中的比较）
> - ✅ max/min/clamp 等操作
> - ❌ 两边计算代价大（CMOV 会执行两个路径）
> - ❌ 条件赋值涉及内存访问（CMOV 的源必须可读）
> - ❌ 简单循环的退出条件（分支预测器通常能正确预测）

## 硬件要求

```
CMOVcc 需要：
  - Intel: Pentium Pro 及以后 (i686+)
  - AMD: K6-2 及以后
  - GCC 选项: -march=i686 或更高
  
  不可用：
  - i386, i486, Pentium (P5)
  - 嵌入式/老硬件
```

```bash
# 编译时检查
gcc -march=i686 -O2 test.c     # 启用 CMOV
gcc -march=i386 -O2 test.c     # 不使用 CMOV
```

> [!tip] 关键要点
> - CMOV 消除分支预测失败的代价（每次失败约 15-20 周期）
> - 条件成立时执行 MOV，不成立时什么都不做
> - 需要 i686+（Pentium Pro, 1995）
> - 适合：简单条件赋值、分支不可预测的场景
> - 不适合：两边计算代价大、涉及复杂内存访问的情况
> - 编译器在 -O2/-O3 下会自动选择 CMOV 或分支版本

## 关联

- [[条件跳转指令]]
- [[条件设置指令 SETcc]]
- [[比较与测试指令]]
- [[汇编优化技巧]]
