---
title: AT&T 与 Intel 语法对比
tags: [assembly, syntax, att, intel, x86]
aliases: [汇编语法对比, AT&T语法, Intel语法]
created: 2026-04-04
updated: 2026-04-04
---

x86 汇编有两种主流语法：**AT&T 语法**（GAS 默认）和 **Intel 语法**（NASM/MASM），它们在操作数顺序、寻址写法、后缀等方面存在系统性差异。

## 操作数顺序（最核心的区别）

```nasm
; Intel 语法：目标在左，源在右（赋值思维）
mov     eax, ebx          ; eax = ebx
add     eax, 10           ; eax += 10
lea     edi, [esi+16]     ; edi = esi + 16
```

```gas
# AT&T 语法：源在左，目标在右（数据流向）
movl    %ebx, %eax        # eax = ebx
addl    $10, %eax         # eax += 10
leal    16(%esi), %edi    # edi = esi + 16
```

## 寄存器和立即数前缀

```nasm
; Intel — 无前缀
mov     eax, 42           ; 寄存器直接写名，立即数直接写值
mov     ebx, eax
```

```gas
# AT&T — 寄存器加 %，立即数加 $
movl    $42, %eax
movl    %eax, %ebx
```

## 操作数大小指示

```nasm
; Intel — 使用 PTR 关键字
mov     BYTE PTR [edi], 0     ; 写入 1 字节
mov     WORD PTR [ebx], ax    ; 写入 2 字节
mov     DWORD PTR [ecx], eax  ; 写入 4 字节
push    QWORD PTR [rsp]       ; 64 位 push

; 有时靠上下文推断大小
mov     eax, [addr]           ; 默认 32 位（eax 隐含大小）
```

```gas
# AT&T — 指令后缀
movb    $0, (%edi)            # b=byte
movw    %ax, (%ebx)           # w=word
movl    %eax, (%ecx)          # l=long(4字节)
pushq   (%rsp)                # q=quad(8字节)
```

### AT&T 大小后缀速查

| 后缀 | 大小 | 示例 |
|------|------|------|
| `b` | 1 字节 (byte) | `movb` |
| `w` | 2 字节 (word) | `movw` |
| `l` | 4 字节 (long) | `movl` |
| `q` | 8 字节 (quad) | `movq` |
| `s` | 单精度浮点 | `movs` |
| `t` | 扩展精度浮点 | `movt` |

## 内存寻址语法

这是两种语法差异最大的地方：

```nasm
; Intel 寻址语法
mov     eax, [ebx]                ; 直接基址
mov     eax, [ebx + 8]            ; 基址 + 偏移
mov     eax, [ebx + ecx*4]        ; 基址 + 索引*比例
mov     eax, [ebx + ecx*4 + 16]   ; 基址 + 索引*比例 + 偏移
lea     eax, [label]              ; 取符号地址
```

```gas
# AT&T 寻址语法：disp(base, index, scale)
movl    (%ebx), %eax
movl    8(%ebx), %eax
movl    (%ebx,%ecx,4), %eax
movl    16(%ebx,%ecx,4), %eax
leal    label, %eax               # AT&T 的 LEA 取地址
```

### 寻址公式对照

```
Intel:  [base + index*scale + displacement]
AT&T:   displacement(base, index, scale)
```

两者计算同一地址：`base + index*scale + displacement`

## 段寄存器和远跳转

```nasm
; Intel
mov     es, ax                    ; 段寄存器赋值
jmp     far [0x1000]              ; 远跳转
push    cs                        ; 段选择子入栈
```

```gas
# AT&T
movw    %ax, %es                  # 段寄存器赋值
ljmp    *0x1000                   # 远跳转（间接跳转加 *）
pushl   %cs                       # 段选择子入栈
```

## 条件码和分支

```nasm
; Intel
cmp     eax, 10
jge     .greater                  ; jump if greater or equal
cmovge  ebx, ecx                  ; 条件传送
```

```gas
# AT&T
cmpl    $10, %eax
jge     .L_greater
cmovl   %ecx, %ebx                # cmov 顺序也反过来
```

## 哪些工具用哪种语法

| 工具/平台 | 默认语法 | 备注 |
|-----------|----------|------|
| **GCC / GAS** | AT&T | `.intel_syntax noprefix` 可切换 |
| **NASM** | Intel | 需安装，跨平台 |
| **MASM** | Intel | Microsoft 汇编器 |
| **GDB** | AT&T | `set disassembly-flavor intel` 可切换 |
| **objdump** | AT&T | `-M intel` 切换为 Intel |
| **IDA Pro** | Intel | 反汇编器默认 Intel |
| **LLDB** | Intel | macOS 调试器默认 Intel |
| **NASM / YASM** | Intel | Linux 下常用汇编器 |

## GAS 中切换到 Intel 语法

```gas
.intel_syntax noprefix      # 切换到 Intel 语法，不使用寄存器前缀

mov     eax, ebx             # 现在是 Intel 风格
mov     [ecx+8], edx

.att_syntax prefix           # 切回 AT&T（.text 等伪指令不可切换）
```

## 完整对照示例

```nasm
; Intel (NASM) — 计算数组元素之和
section .text
global sum_array
sum_array:
    ; 参数：edi = 数组指针, esi = 元素个数
    xor     eax, eax           ; sum = 0
    test    esi, esi
    jz      .done
.loop:
    add     eax, [edi]         ; sum += *ptr
    add     edi, 4             ; ptr++
    dec     esi
    jnz     .loop
.done:
    ret
```

```gas
# AT&T (GAS) — 同一个函数
    .text
    .global sum_array
sum_array:
    # 参数：edi = 数组指针, esi = 元素个数
    xorl    %eax, %eax         # sum = 0
    testl   %esi, %esi
    jz      .Ldone
.Lloop:
    addl    (%edi), %eax       # sum += *ptr
    addl    $4, %edi           # ptr++
    decl    %esi
    jnz     .Lloop
.Ldone:
    ret
```

## 关键要点

> **操作数顺序是最核心差异**：Intel = `mov dst, src`（像赋值），AT&T = `movl src, dst`（像管道数据流）。搞混了就会产生极其隐蔽的 bug。

> **寄存器/立即数前缀**：AT&T 用 `%` 和 `$` 做标记，Intel 直接写。Intel 更简洁，AT&T 更明确。

> **工具链选择**：GCC/GDB 默认 AT&T，但大部分现代反汇编工具（IDA、Ghidra）用 Intel。Linux 内核源码用 GAS（AT&T），用户态编程常用 NASM（Intel）。

> **可以切换**：GAS 支持 `.intel_syntax noprefix`，GDB 支持 `set disassembly-flavor intel`，不必被默认束缚。

## 关联

- [[GAS 汇编语法]]
- [[NASM 汇编语法]]
- [[内联汇编]]
- [[汇编程序结构]]
