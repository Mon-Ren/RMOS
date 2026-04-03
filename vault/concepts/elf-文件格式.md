---
title: "ELF 文件格式"
tags: [x86, binary, ELF, executable, linker]
aliases: ["ELF", "Executable and Linkable Format", "可执行文件"]
created: 2026-04-03
updated: 2026-04-03
---

# ELF 文件格式

ELF（Executable and Linkable Format）是 Unix 系统的标准可执行文件格式。xv6 内核和用户程序都是 ELF 格式。

## 文件结构

```
┌──────────────────┐
│ ELF Header       │  文件元信息
├──────────────────┤
│ Program Header   │  描述段（加载用）
│ Table            │
├──────────────────┤
│ Segment 1 (text) │  代码段
├──────────────────┤
│ Segment 2 (data) │  数据段
├──────────────────┤
│ Section Header   │  描述节（链接用）
│ Table            │
├──────────────────┤
│ .text            │  机器代码
│ .data            │  已初始化数据
│ .bss             │  未初始化数据（不占文件空间）
│ .rodata          │  只读数据
│ .symtab          │  符号表
│ .strtab          │  字符串表
└──────────────────┘
```

## ELF Header

```c
struct elfhdr {
  uchar  magic[4];     // 0x7f 'E' 'L' 'F'
  uchar  class;        // 1=32bit, 2=64bit
  uchar  data;         // 1=LSB, 2=MSB
  ushort type;         // 2=EXEC, 3=DYN
  ushort machine;      // 3=x86
  uint   entry;        // 入口点地址
  uint   phoff;        // Program Header Table 偏移
  uint   shoff;        // Section Header Table 偏移
  ushort ehsize;       // ELF Header 大小
  ushort phentsize;    // Program Header 条目大小
  ushort phnum;        // Program Header 条目数
  // ...
};
```

## Program Header（段头）

```c
struct proghdr {
  uint type;   // 1=PT_LOAD (可加载段)
  uint off;    // 段在文件中的偏移
  uint vaddr;  // 段加载到的虚拟地址
  uint paddr;  // 物理地址（通常=vaddr）
  uint filesz; // 段在文件中的大小
  uint memsz;  // 段在内存中的大小（≥filesz，多出的是 bss）
  uint flags;  // 1=执行, 2=写, 4=读
  uint align;  // 对齐
};
```

## xv6 bootmain.c 加载内核

```c
void bootmain(void) {
  struct elfhdr *elf = (struct elfhdr*)0x10000;
  // 1. 从磁盘读 ELF header
  readseg((uchar*)elf, 4096, 0);
  // 2. 校验 magic number
  if(elf->magic != ELF_MAGIC) return;
  // 3. 遍历 program headers，加载每个 PT_LOAD 段
  struct proghdr *ph = (struct proghdr*)((uchar*)elf + elf->phoff);
  for(i = 0; i < elf->phnum; i++, ph++) {
    if(ph->type == ELF_PROG_LOAD) {
      readseg(ph->paddr, ph->memsz, ph->off);
    }
  }
  // 4. 跳转到入口点
  ((void(*)(void))elf->entry)();
}
```

## Section vs Segment

| | Section | Segment |
|---|---------|---------|
| 用途 | 链接时 | 运行时 |
| 描述者 | Section Header | Program Header |
| 关注者 | 链接器 (ld) | 加载器 / OS |
| 示例 | .text, .data, .bss | 可加载段、动态链接段 |

一个 Segment 可能包含多个 Section（如 text 段包含 .text + .rodata）。

## 关键要点

> ELF 是连接编译器输出和操作系统加载的桥梁。bootmain 只关心 Program Header Table——按 `vaddr` 加载 `filesz` 字节到内存，然后跳转 `entry`。Section Header 是给链接器和调试器用的，运行时不需要。理解 ELF 格式是理解"程序是怎么变成进程的"的第一步。

## 关联
- [[xv6 启动流程]] — bootmain.c 加载内核 ELF
- [[页表机制]] — 段按 vaddr 加载到页表映射的虚拟地址
- [[汇编与 C 混合编程]] — .text/.data/.bss 在链接时合并
