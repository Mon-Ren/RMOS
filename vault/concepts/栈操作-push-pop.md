---
title: 栈操作 PUSH POP
tags: [x86, assembly, stack, PUSH, POP]
aliases: [PUSH, POP, 栈操作, 栈操作 PUSH POP]
created: 2026-04-04
updated: 2026-04-04
---

PUSH 和 POP 是管理栈的基本指令，栈是函数调用、参数传递和局部变量存储的核心机制。

## PUSH — 压栈

```
PUSH 操作数 的等价操作：
    ESP -= 操作数字节数
    [ESP] = 操作数
```

```asm
push eax           ; ESP -= 4, [ESP] = EAX
push ebx           ; ESP -= 4, [ESP] = EBX
push 42            ; ESP -= 4, [ESP] = 42（立即数压栈）

; x86-64 中默认压 8 字节
push rax           ; RSP -= 8, [RSP] = RAX
```

### 栈的状态变化

```
执行前:                    push eax 后:
  ESP ──→ [    ...    ]      ESP ──→ [ EAX 的值 ]  ← 新栈顶
           [    ...    ]              [   ...    ]
           [    ...    ]              [   ...    ]
```

## POP — 出栈

```
POP 操作数 的等价操作：
    操作数 = [ESP]
    ESP += 操作数字节数
```

```asm
pop eax            ; EAX = [ESP], ESP += 4
pop ebx            ; EBX = [ESP], ESP += 4

; x86-64
pop rax            ; RAX = [RSP], RSP += 8
```

## PUSHAD / POPAD — 批量压栈/出栈（32 位）

一次性保存或恢复所有通用寄存器。

```asm
; PUSHAD 压栈顺序（ESP 的值是压栈前的值）:
;   EAX → ECX → EDX → EBX → ESP(旧) → EBP → ESI → EDI
pushad              ; 保存全部通用寄存器

; ... 执行可能破坏寄存器的代码 ...

popad               ; 恢复全部通用寄存器
```

> [!warning] PUSHAD/POPAD 在 x86-64 中已移除
> 64 位模式不支持 PUSHA/PUSHAD/POPA/POPAD，需要手动压栈保存。

## PUSHFD / POPFD — 标志寄存器压栈/出栈

```asm
pushfd              ; ESP -= 4, [ESP] = EFLAGS
popfd               ; EFLAGS = [ESP], ESP += 4

; x86-64
pushfq              ; RSP -= 8, [RSP] = RFLAGS
popfq               ; RFLAGS = [RSP], RSP += 8

; 常见用法：修改某个标志位而不影响其他标志
pushfd
pop eax             ; EAX = EFLAGS
or eax, 0x200       ; 设置 IF 位（允许中断）
push eax
popfd               ; EFLAGS = 修改后的值
```

## 栈的增长方向

x86 栈向**低地址**增长：

```
高地址
┌──────────────┐
│  参数 3      │  [EBP+16]
│  参数 2      │  [EBP+12]
│  参数 1      │  [EBP+8]
│  返回地址    │  [EBP+4]
│  旧 EBP      │  [EBP]      ← EBP 指向这里
│  局部变量 1  │  [EBP-4]
│  局部变量 2  │  [EBP-8]    ← ESP 通常在这里或更低
└──────────────┘
低地址
```

```asm
; 演示栈增长方向
mov eax, esp       ; 保存当前 ESP
push ebx           ; 压栈
cmp eax, esp       ; EAX > ESP（栈向低地址增长）
ja  stack_grows_down
```

## 栈溢出

```asm
; 栈溢出场景：无限递归或超大局部变量
; 每次 CALL 都会压入返回地址
; 每次函数分配局部变量都会减小 ESP
; 当 ESP 越过栈的保护页时，触发 #PF（Page Fault）

; 防止栈溢出的方法：
; 1. 设置栈大小限制（ulimit -s）
; 2. 编译器插入栈探测（stack probe）代码
; 3. 使用 Guard Page 检测溢出
```

## 常见 PUSH/POP 使用模式

```asm
; 1. 保存/恢复寄存器
push eax
push ecx
    ; ... 使用 EAX, ECX ...
pop ecx
pop eax

; 2. 参数传递（cdecl 调用约定）
push arg3
push arg2
push arg1
call my_function
add esp, 12        ; 调用者清理参数

; 3. 临时保存值
push [some_variable]     ; 保存变量值
mov DWORD PTR [some_variable], 0   ; 清零
    ; ... 操作 ...
pop [some_variable]      ; 恢复原值
```

> [!tip] 关键要点
> - 栈向**低地址**增长：PUSH 减小 ESP，POP 增大 ESP
> - PUSHAD/POPAD 在 x86-64 中不存在，需手动保存
> - PUSHFD/POPFD 用于保存/恢复标志寄存器
> - PUSH 立即数是合法操作
> - 注意 PUSH/POP 配对，不平衡的栈是 bug 的常见来源

## 关联

- [[栈帧结构]]
- [[通用寄存器详解]]
- [[x86-调用约定-cdecl]]
- [[无条件跳转与调用-jmp-call]]
