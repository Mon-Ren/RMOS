---
title: CPUID 指令
tags: [x86, cpuid, cpu-features, detection]
aliases: [CPU信息查询, CPU特征检测]
created: 2026-04-04
updated: 2026-04-04
---

CPUID 指令是 x86 处理器的"身份证查询"接口，通过功能号返回 CPU 厂商、型号、支持的指令集和特性位——是运行时 CPU 特征检测的标准方法。

## 基本用法

```nasm
; CPUID 输入：EAX = 功能号（有时 ECX = 子功能号）
; CPUID 输出：EAX, EBX, ECX, EDX 包含结果

mov     eax, 0              ; 功能号 0：获取厂商字符串
cpuid
; 此时：
; EBX:EDX:ECX = 厂商字符串（12 字节 ASCII）
; EAX = 最大支持的功能号

; 读取厂商字符串
mov     [vendor], ebx        ; 前 4 字节
mov     [vendor+4], edx      ; 中 4 字节
mov     [vendor+8], ecx      ; 后 4 字节
; 结果如 "GenuineIntel" 或 "AuthenticAMD"
```

## 常用功能号

### 功能号 0 — 厂商信息

```nasm
mov     eax, 0
cpuid
; EAX = 最大基本功能号
; EBX:EDX:ECX = 厂商字符串
```

### 功能号 1 — 处理器信息和特性位

```nasm
mov     eax, 1
cpuid
; EAX = 处理器签名（Family/Model/Stepping）
; EBX = 逻辑处理器数等
; ECX = 特性位 1
; EDX = 特性位 2
```

**ECX 特性位**（功能号 1）：

| 位 | 特性 | 含义 |
|----|------|------|
| 0 | SSE3 | SSE3 支持 |
| 9 | SSSE3 | SSSE3 支持 |
| 19 | SSE4.1 | SSE4.1 支持 |
| 20 | SSE4.2 | SSE4.2 支持 |
| 23 | POPCNT | POPCNT 指令 |
| 25 | AES-NI | AES 加速指令 |
| 26 | OSXSAVE | XSAVE/XRSTOR 支持 |
| 28 | AVX | AVX 支持 |

**EDX 特性位**（功能号 1）：

| 位 | 特性 | 含义 |
|----|------|------|
| 4 | TSC | 时间戳计数器 |
| 25 | SSE | SSE 支持 |
| 26 | SSE2 | SSE2 支持 |
| 28 | HTT | 超线程 |

### 功能号 7 — 扩展特性

```nasm
mov     eax, 7
mov     ecx, 0              ; 子功能号 0
cpuid
; EBX:
;   bit 3  = BMI1
;   bit 5  = AVX2
;   bit 8  = BMI2
;   bit 16 = AVX512F
;   bit 17 = AVX512DQ
;   bit 28 = AVX512CD
;   bit 30 = AVX512BW
; ECX:
;   bit 14 = AVX512VPOPCNTDQ
; EDX:
;   bit 2  = AVX512_4VNNIW
```

### 功能号 0x80000001 — 扩展特性

```nasm
mov     eax, 0x80000001
cpuid
; ECX: 扩展特性位
; EDX: 扩展特性位（AMD 特有特性）
```

## C 语言封装

```c
#include <stdint.h>
#include <string.h>

// 获取厂商字符串
void get_vendor(char *vendor) {
    uint32_t ebx, ecx, edx;
    __asm__ __volatile__ (
        "cpuid"
        : "=b"(ebx), "=c"(ecx), "=d"(edx)
        : "a"(0)
    );
    memcpy(vendor, &ebx, 4);
    memcpy(vendor+4, &edx, 4);
    memcpy(vendor+8, &ecx, 4);
    vendor[12] = '\0';
}

// 检测 SSE 支持
int has_sse(void) {
    uint32_t edx;
    __asm__ __volatile__ (
        "cpuid"
        : "=d"(edx)
        : "a"(1)
    );
    return (edx >> 25) & 1;
}

// 检测 AVX 支持
int has_avx(void) {
    uint32_t ecx, edx;
    __asm__ __volatile__ (
        "cpuid"
        : "=c"(ecx), "=d"(edx)
        : "a"(1)
    );
    // AVX 需要 CPUID + OSXSAVE + XGETBV 都支持
    if (!((ecx >> 28) & 1)) return 0;   // CPUID 说不支持
    if (!((ecx >> 27) & 1)) return 0;   // 没有 OSXSAVE
    
    // 检查 XCR0 是否启用了 AVX 状态保存
    uint32_t xcr0_lo, xcr0_hi;
    __asm__ __volatile__ (
        "xgetbv"
        : "=a"(xcr0_lo), "=d"(xcr0_hi)
        : "c"(0)
    );
    return (xcr0_lo & 6) == 6;          // bit 1 (SSE) + bit 2 (AVX)
}

// 检测 AVX2
int has_avx2(void) {
    uint32_t ebx;
    __asm__ __volatile__ (
        "cpuid"
        : "=b"(ebx)
        : "a"(7), "c"(0)
    );
    return (ebx >> 5) & 1;
}
```

## 检测 SSE/AVX 支持的完整流程

```
检测 SSE:
  CPUID.1:EDX.SSE = 1?
  → SSE 可用

检测 AVX:
  CPUID.1:ECX.AVX = 1?          (CPU 支持)
  AND CPUID.1:ECX.OSXSAVE = 1?  (OS 支持 XSAVE)
  AND (XGETBV(0) & 6) == 6?     (OS 启用了 AVX 状态保存)
  → AVX 可用

检测 AVX-512:
  AVX 检测通过 AND
  CPUID.7:EBX.AVX512F = 1?
  AND (XGETBV(0) & 0xE6) == 0xE6? (OS 启用了 AVX-512 状态保存)
  → AVX-512 可用
```

## xv6 中的使用

```c
// xv6 — 检测 APIC ID 和多处理器
void detect_cpu(void) {
    uint32_t eax, ebx, ecx, edx;
    
    // 获取厂商
    __asm__ __volatile__ ("cpuid"
        : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx)
        : "a"(0));
    
    // 获取 APIC ID（EBX 的高字节）
    __asm__ __volatile__ ("cpuid"
        : "=b"(ebx)
        : "a"(1));
    uint8_t apic_id = (ebx >> 24) & 0xFF;
    
    // 获取逻辑处理器数
    uint8_t logical_cores = (ebx >> 16) & 0xFF;
}
```

## 其他常用功能号

```nasm
; 功能号 2 — 缓存描述符（旧方法）
mov     eax, 2
cpuid

; 功能号 4 — 确定性缓存参数
mov     eax, 4
mov     ecx, 0              ; 缓存级别
cpuid
; EAX[7:5] = 缓存类型（1=数据, 2=指令, 3=统一）
; EAX[31:26]+1 = 关联方式
; EBX[21:12]+1 = 缓存行大小

; 功能号 0x80000002-4 — 处理器品牌字符串
mov     eax, 0x80000002
cpuid
; EAX:EBX:ECX:EDX = 品牌字符串前 16 字节
mov     eax, 0x80000003
cpuid
; 中 16 字节
mov     eax, 0x80000004
cpuid
; 后 16 字节（共 48 字节，如 "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz"）
```

## 关键要点

> **CPUID 是运行时 CPU 特征检测的标准方法**：在程序启动时调用，确定可用的指令集，然后选择优化路径。

> **功能号 1 是最重要的**：返回 SSE/SSE2/SSE3/AVX 等基础特性位。

> **AVX 检测需要三步**：CPUID + OSXSAVE + XGETBV，缺一不可。OS 必须主动启用 AVX 状态保存。

> **xv6 用它检测多处理器**：CPUID 功能号 1 的 EBX 高 8 位是 APIC ID。

## 关联

- [[x86-寄存器概述]]
- [[多处理器启动]]
- [[SSE 指令集]]
- [[AVX 指令集]]
