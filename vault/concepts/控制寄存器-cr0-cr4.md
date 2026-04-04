---
title: 控制寄存器 CR0-CR4
tags: [x86, control-registers, paging, protection]
aliases: [CR0, CR2, CR3, CR4, 控制寄存器]
created: 2026-04-04
updated: 2026-04-04
---

控制寄存器 CR0-CR4 控制 x86 处理器的核心操作模式：保护模式、分页、SIMD 使能等，是操作系统内核最常操作的硬件接口之一。

## 寄存器总览

```
CR0 — 操作模式控制（保护模式、分页、写保护）
CR1 — 保留（不可访问，访问触发 #UD）
CR2 — 缺页地址（Page Fault 发生时的线性地址）
CR3 — 页表基址（页目录物理地址）
CR4 — 扩展特性使能（大页、SSE、PAE 等）
```

## CR0 — 操作模式控制

```
┌────┬─────────────────────────────────────────┐
│ 位 │ 符号    │ 含义                          │
├────┼─────────┼───────────────────────────────┤
│ 0  │ PE      │ Protection Enable 保护模式    │
│ 1  │ MP      │ Monitor Coprocessor           │
│ 2  │ EM      │ Emulation（软件模拟 FPU）     │
│ 3  │ TS      │ Task Switched                 │
│ 4  │ ET      │ Extension Type                │
│ 5  │ NE      │ Numeric Error（x87 异常模式） │
│16  │ WP      │ Write Protect（内核写保护）   │
│18  │ AM      │ Alignment Mask                │
│29  │ NW      │ Not Write-through             │
│30  │ CD      │ Cache Disable                 │
│31  │ PG      │ Paging Enable                 │
└────┴─────────┴───────────────────────────────┘
```

```nasm
; 开启保护模式
mov     eax, cr0
or      eax, 1              ; 设置 PE 位
mov     cr0, eax

; 开启分页（PE 必须已设置）
mov     eax, cr0
or      eax, 0x80000000     ; 设置 PG 位
mov     cr0, eax

; 设置写保护（内核也不能写用户页）
mov     eax, cr0
or      eax, 0x10000        ; WP 位
mov     cr0, eax
```

### CR0 关键位详解

| 位 | 名称 | 作用 | 什么时候设 |
|----|------|------|-----------|
| PE (bit 0) | Protection Enable | 进入保护模式 | 引导早期 |
| PG (bit 31) | Paging | 开启分页 | 设置好页表后 |
| WP (bit 16) | Write Protect | 内核也遵循页表写保护 | fork 实现 COW |
| EM (bit 2) | Emulation | 无 FPU 时触发 #NM 异常 | 无 FPU 系统 |
| NE (bit 5) | Numeric Error | x87 异常报告方式 | 使用 x87 时 |

## CR2 — 缺页地址

```nasm
; CR2 在 Page Fault (#PF) 发生时自动设置
; 存储导致缺页的线性地址（虚拟地址）

; Page Fault 处理程序
page_fault_handler:
    mov     eax, cr2           ; 获取导致缺页的地址
    ; 检查是否是合法缺页（COW、按需分配等）
    ; 如果不合法，终止进程
    iret
```

```c
// xv6 中的使用
void trap(struct trapframe *tf) {
    if (tf->trapno == T_PGFLT) {
        uint32_t fault_addr;
        __asm__ __volatile__ ("mov %%cr2, %0" : "=r"(fault_addr));
        
        if (fault_addr >= KERNBASE) {
            panic("kernel page fault");
        }
        // 处理用户态缺页...
    }
}
```

## CR3 — 页表基址

```nasm
; CR3 = 页目录（Page Directory）的物理地址
; 也叫 PDBR（Page Directory Base Register）

; 设置页表
mov     eax, page_directory_phys
mov     cr3, eax              ; 加载新的页表

; 读取当前页表
mov     eax, cr3

; 刷新 TLB — 写 CR3 自动刷新所有 TLB 条目
mov     eax, cr3
mov     cr3, eax              ; 重新写入同一值 = TLB flush

; 部分刷新 — 只刷新单个页
invlpg [addr]                 ; 无效化包含 addr 的 TLB 条目
```

### CR3 格式

```
┌─────────────────────────┬─────┬─────┬─────┐
│  页目录物理地址 [31:12]  │ PWT │ PCD │  0  │
└─────────────────────────┴─────┴─────┴─────┘
  PWT (bit 3) — Page-level Write-Through
  PCD (bit 4) — Page-level Cache Disable
  低 12 位通常为 0（页目录 4KB 对齐）
```

## CR4 — 扩展特性使能

```
┌────┬──────┬────────────────────────────────┐
│ 位 │ 符号 │ 含义                           │
├────┼──────┼────────────────────────────────┤
│ 0  │ VME  │ Virtual-8086 Mode Extensions   │
│ 1  │ PVI  │ Protected-Mode VM Interrupts   │
│ 2  │ TSD  │ Time Stamp Disable             │
│ 3  │ DE   │ Debugging Extensions           │
│ 4  │ PSE  │ Page Size Extension (4MB 页)   │
│ 5  │ PAE  │ Physical Address Extension     │
│ 6  │ MCE  │ Machine-Check Enable           │
│ 7  │ PGE  │ Page Global Enable             │
│ 8  │ PCE  │ Performance-Monitoring Counter │
│ 9  │ OSFXSR│ FXSAVE/FXRSTOR 支持          │
│10  │ OSXMMEXCPT│ SIMD 浮点异常支持        │
│18  │ OSXSAVE│ XSAVE 指令支持               │
│20  │ SMEP │ Supervisor Mode Execute Prev  │
│21  │ SMAP │ Supervisor Mode Access Prev   │
└────┴──────┴────────────────────────────────┘
```

```nasm
; 开启 PAE（Physical Address Extension — 64 位页表格式）
mov     eax, cr4
or      eax, 0x20            ; PAE 位
mov     cr4, eax

; 开启 4MB 大页
mov     eax, cr4
or      eax, 0x10            ; PSE 位
mov     cr4, eax

; 开启全局页（TLB 不刷新全局页）
mov     eax, cr4
or      eax, 0x80            ; PGE 位
mov     cr4, eax

; 开启 SSE 支持（用户态可用 SSE）
mov     eax, cr4
or      eax, 0x200           ; OSFXSR 位
or      eax, 0x400           ; OSXMMEXCPT 位
mov     cr4, eax

; 启用 SMEP（阻止内核执行用户页）
mov     eax, cr4
or      eax, 0x100000        ; SMEP 位
mov     cr4, eax
```

## xv6 中控制寄存器的使用

```c
// xv6 — 开启分页
void kvmalloc(void) {
    lcr3(V2P(kpgdir));     // 加载页表
    lcr0(rcr0() | CR0_WP); // 开启写保护
}

// 常见的内联汇编封装
static inline void lcr3(uint val) {
    __asm__ __volatile__ ("movl %0, %%cr3" : : "r"(val));
}

static inline uint rcr2(void) {
    uint val;
    __asm__ __volatile__ ("movl %%cr2, %0" : "=r"(val));
    return val;
}

static inline void lcr0(uint val) {
    __asm__ __volatile__ ("movl %0, %%cr0" : : "r"(val));
}
```

## 关键要点

> **CR0.PE + CR0.PG** 是进入现代 x86 操作模式的两步：先开保护模式（PE），再加分页（PG）。

> **CR3 = 页表根**：切换进程 = 换 CR3。写 CR3 自动刷新 TLB。

> **CR2 = 缺页地址**：Page Fault 处理程序必读，用于判断缺页原因和位置。

> **CR4 控制扩展功能**：PAE、大页、全局页、SSE 使能、SMEP/SMAP 安全特性都在这里。

## 关联

- [[页表机制]]
- [[x86 实模式与保护模式]]
- [[虚拟内存]]
- [[保护模式基础]]
