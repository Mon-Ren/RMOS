---
title: 循环指令 LOOP
tags: [x86, assembly, LOOP, 循环]
aliases: [LOOP, LOOPNE, LOOPE, 循环指令, 循环指令 LOOP]
created: 2026-04-04
updated: 2026-04-04
---

LOOP 指令集提供基于 ECX 计数器的紧凑循环控制，但在现代 CPU 上 DEC+JNZ 通常更快。

## LOOP — 计数循环

```
LOOP label 的等价操作：
    ECX--
    if (ECX != 0) goto label
```

```asm
; 使用 LOOP 求 1+2+...+100
xor eax, eax         ; 累加器清零
mov ecx, 100         ; 计数 = 100
sum_loop:
    add eax, ecx     ; EAX += ECX
    loop sum_loop    ; ECX--, ECX≠0 则继续
; EAX = 5050
```

### LOOP 的隐式操作

```asm
; 以下两段代码等价：
loop label

; 等价于：
dec ecx
jnz label
```

## LOOPE / LOOPZ — 相等时循环

```
LOOPE label 的等价操作：
    ECX--
    if (ECX != 0 && ZF == 1) goto label
```

```asm
; 比较两个字符串，找第一个不匹配的位置
lea esi, [str1]
lea edi, [str2]
mov ecx, 100         ; 最多比较 100 字节
compare_loop:
    cmpsb            ; 比较 [ESI] 和 [EDI]
    loope compare_loop  ; ECX--, 如果相等且 ECX≠0 则继续
    ; 如果 ZF=0 → 找到不匹配
    ; 如果 ECX=0 → 全部匹配
```

## LOOPNE / LOOPNZ — 不等时循环

```
LOOPNE label 的等价操作：
    ECX--
    if (ECX != 0 && ZF == 0) goto label
```

```asm
; 在数组中搜索值 42
lea edi, [array]
mov ecx, 100         ; 数组长度
search_loop:
    cmp DWORD PTR [edi], 42
    loopne search_loop  ; ECX--, 如果不等且 ECX≠0 则继续
    ; ZF=1 → 找到了（EDI 指向匹配元素）
    ; ECX=0 且 ZF=0 → 未找到
jnz not_found
    ; 找到了，ECX 是剩余计数
```

## JECXZ — ECX 为零则跳转

在循环前检查 ECX 是否为 0，避免执行 0 次的循环。

```asm
jecxz skip_loop      ; 如果 ECX=0，直接跳过循环
my_loop:
    ; ... 循环体 ...
    loop my_loop
skip_loop:

; 常见模式：安全的循环
mov ecx, [count]
jecxz done           ; 防止 ECX=0 时循环 2^32 次
process:
    ; ... 处理 ...
    loop process
done:
```

## 现代优化：LOOP 实际上比 DEC+JNZ 慢

### 原因

现代 CPU 对 `DEC + JNZ` 有特别优化：

1. **微操作融合**：CPU 可以将 DEC 和 JNZ 融合成一个微操作
2. **LOOP 是冷门指令**：编译器很少生成 LOOP，CPU 厂商优化投入少
3. **LOOP 的复杂度**：LOOP 内部需要同时修改 ECX 和检查条件

### 性能对比

```asm
; 慢（LOOP）:
    mov ecx, 1000000
.loop:
    ; ... 操作 ...
    loop .loop

; 快（DEC+JNZ）:
    mov ecx, 1000000
.loop:
    ; ... 操作 ...
    dec ecx
    jnz .loop

; 更快（INC+CMP+JNE — 避免影响 CF）:
    xor ecx, ecx
.loop:
    ; ... 操作 ...
    inc ecx
    cmp ecx, 1000000
    jne .loop
```

> [!warning] 性能建议
> - 现代代码中**避免使用 LOOP**，用 DEC+JNZ 替代
> - 很多汇编教程还教 LOOP，但这更多是历史原因
> - 编译器（GCC/Clang/MSVC）从不生成 LOOP 指令

## LOOP vs 字符串指令

LOOP 和字符串指令（REP 前缀）都使用 ECX，但用途不同：

```asm
; LOOP 用于自定义循环体
mov ecx, 100
my_loop:
    ; 复杂的循环体...
    loop my_loop

; REP 用于特定的内存操作
mov ecx, 100
rep movsb            ; 固定操作：复制字节
```

> [!tip] 关键要点
> - LOOP: ECX--, ECX≠0 则跳转
> - LOOPE: ECX--, ECX≠0 且 ZF=1 则跳转
> - LOOPNE: ECX--, ECX≠0 且 ZF=0 则跳转
> - JECXZ: ECX=0 则跳转（循环前安全检查）
> - **现代代码用 DEC+JNZ 替代 LOOP**（性能更好）

## 关联

- [[条件跳转指令]]
- [[字符串操作指令]]
- [[比较与测试指令]]
