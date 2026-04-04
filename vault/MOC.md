---
title: Map of Content
updated: 2026-04-04
---

# 🗺️ Map of Content

*最后更新: 2026-04-04*

## 基础概念

- [[虚拟内存]] — 地址空间抽象、隔离与保护
- [[页表机制]] — 虚拟地址到物理地址的翻译
- [[多级页表]] — 页表的层次化结构，减少内存开销
- [[分页与分段对比]] — 两种内存管理方式的区别
- [[x86 内存模型与 TLB]] — 硬件层面的内存管理
- [[x86 实模式与保护模式]] — x86 模式切换
- [[gdt-与段描述符]] — 全局描述符表
- [[x86 特权级]] — Ring 0-3 的保护机制
- [[x86 调用约定 cdecl]] — 函数调用 ABI
- [[栈帧结构]] — 函数调用时的栈布局

## 汇编 — 寄存器与标志

- [[x86-寄存器概述]] — 寄存器分类总览
- [[x86-通用寄存器详解]] — EAX/EBX/ECX/EDX/ESI/EDI/EBP/ESP
- [[段寄存器]] — CS/DS/SS/ES/FS/GS
- [[标志寄存器-eflags]] — CF/ZF/SF/OF/PF 等标志位
- [[控制寄存器-cr0-cr4]] — 分页、保护模式控制
- [[调试寄存器]] — DR0-DR7 硬件断点

## 汇编 — 指令集

- [[x86-指令编码格式]] — Prefix→Opcode→ModR/M→SIB→Disp→Imm
- [[内存寻址模式]] — 立即/寄存器/直接/间接/SIB 寻址
- [[数据传输指令-mov]] — MOV/MOVZX/MOVSX/LEA/XCHG
- [[栈操作-push-pop]] — PUSH/POP/PUSHAD/PUSHFD
- [[算术运算指令]] — ADD/SUB/MUL/DIV/INC/DEC
- [[逻辑运算指令]] — AND/OR/XOR/NOT/TEST
- [[移位与循环指令]] — SHL/SHR/SAR/ROL/ROR
- [[比较与测试指令]] — CMP/TEST 标志位变化
- [[条件跳转指令]] — JE/JNE/JG/JL/JA/JB
- [[无条件跳转与调用-jmp-call]] — JMP/CALL/RET
- [[字符串操作指令]] — MOVSB/CMPSB/SCASB + REP
- [[循环指令-loop]] — LOOP/LOOPE/LOOPNE/JECXZ
- [[条件设置指令-setcc]] — SETZ/SETG/SETL 系列
- [[条件传送-cmovcc]] — CMOVcc 消除分支
- [[中断与异常指令]] — INT/INT3/IRET/BOUND
- [[系统调用指令-syscall]] — INT 0x80/SYSENTER/SYSCALL
- [[原子操作指令]] — XCHG/LOCK/CMPXCHG/XADD
- [[内存屏障指令]] — SFENCE/LFENCE/MFENCE
- [[CPUID 指令]] — CPU 特性检测

## 汇编 — SIMD 与浮点

- [[SIMD 概念]] — 单指令多数据并行
- [[SSE 指令集]] — XMM 128 位 SIMD
- [[AVX 指令集]] — YMM 256 位 SIMD、AVX-512
- [[x87-浮点指令-fpu]] — ST 寄存器栈、浮点运算
- [[浮点数表示与运算]] — IEEE 754 格式

## 汇编 — 工具链与语法

- [[gas-汇编语法]] — AT&T 语法详解
- [[nasm-汇编语法]] — Intel 语法详解
- [[at-t-与-intel-语法对比]] — 两种语法的差异
- [[内联汇编]] — GCC 扩展内联、约束符号
- [[汇编程序结构]] — .text/.data/.bss 段
- [[汇编与链接过程]] — 汇编器/链接器流程
- [[重定位与符号解析]] — ELF 重定位、PLT/GOT

## 汇编 — 高级主题

- [[保护模式基础]] — GDT、段描述符、门描述符
- [[长模式-x86-64]] — 64 位扩展、RIP 相对寻址
- [[缓存与缓存行]] — 缓存层次、伪共享
- [[汇编优化技巧]] — CMOV、循环展开、SIMD、寄存器分配

## xv6 内核

- [[xv6 启动流程]] — 从 bootloader 到第一个进程
- [[xv6 进程管理]] — 进程状态机与调度
- [[xv6 exec 详解]] — 系统调用 exec 的实现
- [[xv6 ELF 与进程加载]] — ELF 格式和进程加载流程
- [[xv6 内存分配]] — kalloc/kfree 物理页管理
- [[xv6 内核栈]] — 每个进程的内核栈
- [[xv6 系统调用]] — syscall 接口
- [[xv6 中断与陷阱]] — trap 处理机制
- [[xv6 调度器实现]] — Round-Robin 调度
- [[xv6 锁与同步]] — 自旋锁与睡眠锁
- [[xv6 睡眠与唤醒]] — sleep/wakeup 机制
- [[xv6 文件系统]] — 文件系统层次结构
- [[xv6 文件描述符]] — fd 三层结构与 I/O 抽象
- [[xv6 缓冲区缓存]] — 磁盘块缓存
- [[xv6 日志系统]] — crash recovery
- [[xv6 磁盘驱动]] — IDE 磁盘 I/O
- [[xv6 管道]] — 管道通信
- [[xv6 shell 工作原理]] — shell 的管道和重定向
- [[cow-写时复制]] — fork 优化

## 同步与并发

- [[信号量]] — P/V 操作与经典同步问题
- [[死锁]] — 四个必要条件与处理策略
- [[原子指令与内存屏障]] — CAS、LL/SC、内存序
- [[无锁数据结构]] — CAS-based 并发数据结构
- [[调度算法比较]] — RR、优先级、MLFQ、CFS
- [[上下文切换]] — swtch.S 的实现
- [[信号机制]] — Unix 信号处理
- [[xv6 睡眠与唤醒]] — 等待队列机制

## 硬件与中断

- [[idt-与中断机制]] — 中断描述符表
- [[中断向量与-apic]] — 中断路由
- [[lapic-与-ioapic]] — 本地和 I/O APIC
- [[内存映射 I/O]] — MMIO 访问设备寄存器
- [[DMA 与总线架构]] — 直接内存访问
- [[设备驱动模型]] — 设备抽象
- [[多处理器启动]] — AP 启动流程
- [[汇编与 C 混合编程]] — inline asm

## 其他

- [[elf-文件格式]] — ELF 规范
- [[x86 系统调用演进]] — int 80h → syscall
- [[系统调用实现]] — 系统调用的通用框架
