---
title: "汇编与 C 混合编程"
tags: [x86, assembly, C, inline-asm, ABI]
aliases: ["inline assembly", "内联汇编", "汇编混合"]
created: 2026-04-03
updated: 2026-04-03
---

# 汇编与 C 混合编程

xv6 中大量使用汇编与 C 混合——性能关键路径和硬件操作用汇编，逻辑控制用 C。

## 三种混合方式

### 1. 纯汇编文件（.S）

```asm
# swtch.S
.globl swtch
swtch:
  movl 4(%esp), %eax
  pushl %ebp
  # ...
  ret
```

用 `as` 编译，通过 `.globl` 导出符号供 C 调用。

### 2. 内联汇编

```c
// 读 CR2 寄存器（缺页地址）
static inline uint rcr2(void) {
  uint val;
  asm volatile("movl %%cr2, %0" : "=r" (val));
  return val;
}
```

### 3. 扩展内联汇编（GCC 风格）

```c
// xchg 原子交换
static inline uint xchg(uint *addr, uint newval) {
  uint result;
  asm volatile("lock; xchgl %0, %1"   // 汇编模板
    : "+m" (*addr), "=a" (result)      // 输出操作数
    : "1" (newval)                     // 输入操作数
    : "cc");                           // 修改的寄存器
  return result;
}
```

## GCC 扩展内联汇编语法

```c
asm (模板 : 输出 : 输入 : 修改);
```

### 约束符

| 符号 | 含义 |
|------|------|
| `=r` | 只写寄存器 |
| `+r` | 读写寄存器 |
| `r` | 只读寄存器 |
| `=m` | 只写内存 |
| `+m` | 读写内存 |
| `a` | EAX |
| `b` | EBX |
| `c` | ECX |
| `d` | EDX |
| `S` | ESI |
| `D` | EDI |
| `i` | 立即数 |
| `cc` | 修改了条件码 |

### 操作数编号

```c
asm("addl %1, %0" : "+r"(a) : "r"(b));
// %0 = a (第 0 个操作数)
// %1 = b (第 1 个操作数)
// %%  = 字面 % 寄存器
```

## xv6 中的典型用法

### 读写控制寄存器

```c
static inline void lcr3(uint val) {
  asm volatile("movl %0, %%cr3" : : "r" (val));
}
```

### 读写端口

```c
static inline void outb(ushort port, uchar data) {
  asm volatile("outb %0, %1" : : "a" (data), "d" (port));
}
static inline uchar inb(ushort port) {
  uchar data;
  asm volatile("inb %1, %0" : "=a" (data) : "d" (port));
  return data;
}
```

### 内存屏障

```c
static inline void mfence(void) {
  asm volatile("mfence" ::: "memory");
}
```

## 关键要点

> 内联汇编是 C 与硬件的桥梁——需要操作控制寄存器、端口、原子指令时必须用汇编。GCC 扩展语法的关键是**约束符**：告诉编译器哪些操作数用哪些寄存器/内存，哪些被修改。`volatile` 防止编译器优化掉看似无副作用的汇编。xv6 中约 50 个内联汇编函数，覆盖了所有硬件交互。

## 关联
- [[x86 调用约定 cdecl]] — 汇编函数遵循的调用规则
- [[栈帧结构]] — 汇编中的栈操作
- [[原子指令与内存屏障]] — xchg 等必须用汇编
- [[ELF 文件格式]] — .S 文件编译成 .o 后链接
