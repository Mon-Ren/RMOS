---
title: "xv6 启动流程"
tags: [xv6, boot, kernel, assembly]
aliases: ["xv6 boot", "xv6引导"]
created: 2026-04-03
updated: 2026-04-03
---

# xv6 启动流程

xv6 从加电到运行用户进程，经历三个阶段。

## 阶段一：BIOS → bootasm.S（实模式 → 保护模式）

1. BIOS 加载引导扇区到 `0x7c00`，CPU 运行在 16 位实模式
2. 关闭中断（`cli`），清零段寄存器
3. 开启 A20 地址线（突破 1MB 限制）
4. 加载 GDT，设置 `CR0_PE` 进入 32 位保护模式
5. 长跳转到 `start32`，设置数据段寄存器

关键代码（`bootasm.S`）：
```asm
lgdt    gdtdesc
movl    %cr0, %eax
orl     $CR0_PE, %eax
movl    %eax, %cr0
ljmp    $(SEG_KCODE<<3), $start32
```

## 阶段二：bootmain.c（加载内核 ELF）

1. 初始化 IDE 磁盘驱动
2. 从磁盘读取 ELF 格式的内核镜像
3. 将内核段（text、data、bss）复制到对应物理地址
4. 跳转到 ELF 入口点 `_start`（即 `entry.S`）

## 阶段三：entry.S → main.c（内核初始化）

`entry.S` 设置临时页表 `entrypgdir`，映射 `[0, 4MB)` 和 `[KERNBASE, KERNBASE+4MB)` 到同一物理地址，开启分页后跳转到 `main()`。

`main()` 的初始化顺序：

```c
kinit1(end, P2V(4*1024*1024));  // 物理页分配器（初步）
kvmalloc();                      // 内核页表
mpinit();                        // 检测多处理器
lapicinit();                     // 本地 APIC 中断控制器
seginit();                       // 段描述符
picinit();                       // 禁用 8259A PIC
ioapicinit();                    // IO APIC
consoleinit();                   // 控制台
uartinit();                      // 串口
pinit();                         // 进程表
tvinit();                        // 陷阱向量
binit();                         // 缓冲区缓存
fileinit();                      // 文件表
ideinit();                       // 磁盘驱动
startothers();                   // 启动其他 CPU
kinit2(...);                     // 物理页分配器（完整）
userinit();                      // 创建第一个用户进程
mpmain();                        // 进入调度器
```

## 核心要点

> xv6 启动的关键是**分阶段建立执行环境**：先实模式加载内核，再用临时页表过渡到保护模式，最后在 C 代码中完成全部子系统初始化。`entrypgdir` 的双重映射（物理地址 = 虚拟地址的低 4MB + 高地址偏移）是切换分页的关键技巧。

## 关联
- [[页表机制]] — entrypgdir 的映射原理
- [[xv6 进程管理]] — userinit 创建第一个进程
- [[xv6 中断与陷阱]] — tvinit 初始化陷阱向量
- [[多处理器启动]] — startothers 启动 AP 的流程
