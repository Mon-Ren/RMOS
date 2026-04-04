---
title: 无条件跳转与调用
tags: [x86, assembly, JMP, CALL, RET, 函数调用]
aliases: [JMP, CALL, RET, 无条件跳转, 无条件跳转与调用, 无条件跳转与调用-jmp-call]
created: 2026-04-04
updated: 2026-04-04
---

JMP、CALL 和 RET 是控制流的基本指令：JMP 实现无条件跳转，CALL/RET 实现函数调用与返回。

## JMP — 无条件跳转

JMP 修改 EIP/RIP，无条件跳转到目标地址。

### 直接跳转

```asm
jmp label            ; 跳转到标签（相对偏移）
jmp 0x08048000       ; 跳转到绝对地址（near jump）
jmp 0x08:0x00010000  ; 远跳转（far jump），同时修改 CS:EIP
```

### 间接跳转

```asm
jmp eax              ; 跳转到 EAX 中的地址
jmp [eax]            ; 跳转到 EAX 指向的内存中存放的地址
jmp [jmp_table + ecx*4]  ; 跳转表（switch-case 实现）

; 虚函数调用（C++ 多态）
mov eax, [obj]           ; eax = vtable 指针
call [eax + offset]      ; 调用虚函数
```

### 跳转表实现 switch

```asm
; switch (eax) { case 0: ... case 1: ... case 2: ... }
cmp eax, 3
jae default_case
jmp [jump_table + eax*4]

section .rodata
jump_table:
    dd case_0, case_1, case_2

case_0:
    ; ...
    jmp switch_end
case_1:
    ; ...
    jmp switch_end
case_2:
    ; ...
switch_end:
```

## CALL — 函数调用

CALL = PUSH 返回地址 + JMP 目标地址。

```asm
call function       ; 等价于：
                    ;   push (下一条指令的地址)
                    ;   jmp function

; 间接调用
call eax            ; 跳转到 EAX 中的地址
call [eax]          ; 跳转到 [EAX] 指向的函数指针
call [vtable + 8]   ; 虚函数调用
```

### CALL 执行前后栈的状态

```
执行 CALL func 前:          执行 CALL func 后:
ESP ──→ [ ... ]             ESP ──→ [ 返回地址 ]  ← 新栈顶
         [ ... ]                     [ ... ]
         [ ... ]                     [ ... ]
```

## RET — 函数返回

RET = POP 返回地址 + JMP 返回地址。

```asm
ret                 ; 等价于：
                    ;   pop eip
                    ;   jmp eip
```

### RET N — 返回并清理参数

```asm
ret 8               ; 等价于：
                    ;   pop eip
                    ;   add esp, 8   （清理 2 个参数）
                    ;   jmp eip

; 用于 stdcall 调用约定（被调用者清理参数）
; Windows API 常用此约定
```

## 完整函数调用示例

```c
// C 代码
int add(int a, int b) {
    return a + b;
}
int result = add(3, 5);
```

```asm
; 调用方
push 5               ; 第二个参数
push 3               ; 第一个参数
call add
add esp, 8           ; 调用者清理参数（cdecl 约定）

; add 函数
add:
    push ebp             ; 保存旧帧指针
    mov ebp, esp         ; 建立新栈帧
    
    mov eax, [ebp+8]     ; 第一个参数 (a)
    add eax, [ebp+12]    ; 第二个参数 (b)
    
    pop ebp              ; 恢复旧帧指针
    ret                  ; 返回（EAX 中是返回值）
```

## CALL/RET 与栈帧的配合

```
高地址
┌──────────────┐
│  arg2 (5)    │  [EBP+12]
│  arg1 (3)    │  [EBP+8]
│  返回地址    │  [EBP+4]    ← CALL 压入
│  旧 EBP      │  [EBP]      ← PUSH EBP / MOV EBP, ESP
│  局部变量    │  [EBP-4]    ← SUB ESP, N 分配
│              │  ← ESP
低地址
```

```asm
; 标准函数序言 (Prologue)
func:
    push ebp
    mov ebp, esp
    sub esp, 16          ; 分配局部空间

; 标准函数尾声 (Epilogue)
    mov esp, ebp         ; 释放局部空间（等价于 add esp, 16）
    pop ebp
    ret
; 或使用 leave 指令：
    leave                ; = MOV ESP, EBP; POP EBP
    ret
```

> [!tip] 关键要点
> - JMP 只修改 EIP，不操作栈
> - CALL 压入返回地址再跳转，RET 弹出返回地址跳回
> - RET N 清理 N 字节的参数（stdcall 约定）
> - CALL/RET 是函数调用的底层实现
> - 间接跳转用于虚函数、回调、跳转表等动态分派场景

## 关联

- [[条件跳转指令]]
- [[x86-调用约定-cdecl]]
- [[栈帧结构]]
- [[栈操作 PUSH POP]]
