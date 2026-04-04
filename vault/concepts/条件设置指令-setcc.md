---
title: 条件设置指令 SETcc
tags: [x86, assembly, SETcc, 条件设置]
aliases: [SETcc, SETZ, SETG, 条件设置指令, 条件设置指令 SETcc]
created: 2026-04-04
updated: 2026-04-04
---

SETcc 将条件判断的结果写入字节寄存器，是实现无分支代码的关键工具，避免条件跳转带来的分支预测开销。

## 基本语法

```asm
SETcc r/m8    ; 如果条件成立，则 r/m8 = 1；否则 r/m8 = 0
```

## 完整指令列表

### 无符号比较

| 指令 | 含义 | 条件 |
|------|------|------|
| SETZ / SETE | 等于 / 为零 | ZF = 1 |
| SETNZ / SETNE | 不等于 / 非零 | ZF = 0 |
| SETA / SETNBE | 高于 | CF = 0 ∧ ZF = 0 |
| SETAE / SETNB / SETNC | 高于或等于 | CF = 0 |
| SETB / SETNAE / SETC | 低于 | CF = 1 |
| SETBE / SETNA | 低于或等于 | CF = 1 ∨ ZF = 1 |

### 有符号比较

| 指令 | 含义 | 条件 |
|------|------|------|
| SETG / SETNLE | 大于 | ZF = 0 ∧ SF = OF |
| SETGE / SETNL | 大于或等于 | SF = OF |
| SETL / SETNGE | 小于 | SF ≠ OF |
| SETLE / SETNG | 小于或等于 | ZF = 1 ∨ SF ≠ OF |

### 单标志检查

| 指令 | 条件 |
|------|------|
| SETS | SF = 1（结果为负）|
| SETNS | SF = 0（结果非负）|
| SETO | OF = 1（溢出）|
| SETNO | OF = 0（无溢出）|
| SETP / SETPE | PF = 1（偶校验）|
| SETNP / SETPO | PF = 0（奇校验）|

## 使用示例

### 基本用法

```asm
cmp eax, ebx
setg cl              ; CL = (EAX > EBX) ? 1 : 0（有符号比较）
seta cl              ; CL = (EAX > EBX) ? 1 : 0（无符号比较）

test eax, eax
setz al              ; AL = (EAX == 0) ? 1 : 0
setnz al             ; AL = (EAX != 0) ? 1 : 0
```

### 替代分支：if-else

```c
// C 代码
int max(int a, int b) {
    return (a > b) ? a : b;
}
```

```asm
; 有分支版本（可能分支预测失败）
max:
    cmp edi, esi
    jle .use_esi
    mov eax, edi
    ret
.use_esi:
    mov eax, esi
    ret

; 无分支版本（使用 SETcc + CMOV）
max:
    cmp edi, esi
    setg al              ; AL = (edi > esi) ? 1 : 0
    movzx eax, al
    ; 或者直接用 CMOV（更好）
    cmovg eax, edi
    cmovle eax, esi
    ret
```

### CMP + SET + MOVZX 模式

```c
// 返回布尔值
bool is_positive(int x) {
    return x > 0;
}
```

```asm
is_positive:
    xor eax, eax         ; EAX = 0
    test edi, edi
    setg al              ; AL = (x > 0) ? 1 : 0
    ; EAX 高位已经是 0（因为 XOR EAX,EAX）
    ret

; 如果不用 XOR 清零
is_positive:
    cmp edi, 0
    setg al
    movzx eax, al        ; 零扩展到 32 位
    ret
```

### 多条件组合

```c
// 检查 a < b && b < c
bool in_range(int a, int b, int c) {
    return a < b && b < c;
}
```

```asm
in_range:
    cmp edi, esi
    setl al              ; AL = (a < b)
    cmp esi, edx
    setl cl              ; CL = (b < c)
    and al, cl           ; AL = (a < b) && (b < c)
    movzx eax, al
    ret
```

### 设置标志位

```c
// 返回 flags（类似 CPU 标志）
uint8_t compare_flags(int a, int b) {
    uint8_t flags = 0;
    if (a == b) flags |= 0x40;  // ZF
    if (a < b)  flags |= 0x01;  // CF (模拟)
    return flags;
}
```

```asm
compare_flags:
    xor eax, eax
    cmp edi, esi
    sete al              ; AL = (a == b)
    shl al, 6            ; 移到 ZF 位置
    mov cl, al
    cmp edi, esi
    setb al              ; AL = (a < b unsigned)
    or al, cl            ; 合并
    movzx eax, al
    ret
```

> [!tip] 关键要点
> - SETcc 将条件判断结果写入 8 位寄存器/内存，值为 0 或 1
> - 配合 MOVZX 做零扩展得到完整的 32 位布尔值
> - CMP + SET + MOVZX 模式可替代简单的 if-else 分支
> - 避免了分支预测失败的性能代价
> - 只能操作 8 位目标（AL/BL/CL/DL 等）

## 关联

- [[条件跳转指令]]
- [[条件传送 CMOVcc]]
- [[标志寄存器 EFLAGS]]
- [[比较与测试指令]]
