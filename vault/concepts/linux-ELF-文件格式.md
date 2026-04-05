---
title: Linux ELF 文件格式
tags: [linux, elf, binary, linker, executable]
aliases: [ELF, 可执行文件, 目标文件, 链接, 段]
created: 2026-04-05
updated: 2026-04-05
---

# Linux ELF 文件格式

ELF（Executable and Linkable Format）是 Linux 的标准二进制格式，包含可执行文件、目标文件和共享库。

## ELF 文件类型

| 类型 | 说明 | 扩展名 |
|------|------|--------|
| ET_REL | 可重定位文件（目标文件） | .o |
| ET_EXEC | 可执行文件 | 无 |
| ET_DYN | 共享库 / PIE 可执行 | .so |
| ET_CORE | 核心转储 | core |

## ELF 结构

```
┌──────────────────┐
│ ELF Header       │ → 魔数、类型、入口地址
├──────────────────┤
│ Program Headers  │ → 加载信息（Segment 视图）
├──────────────────┤
│ .text            │ → 代码段（只读可执行）
│ .rodata          │ → 只读数据
│ .data            │ → 已初始化数据
│ .bss             │ → 未初始化数据（零填充）
│ .symtab          │ → 符号表
│ .strtab          │ → 字符串表
│ .dynamic         │ → 动态链接信息
│ .got             │ → 全局偏移表
│ .plt             │ → 过程链接表
├──────────────────┤
│ Section Headers  │ → 段表（Section 视图）
└──────────────────┘
```

## 查看 ELF

```bash
file app                       # 文件类型
readelf -h app                 # ELF 头
readelf -l app                 # Program Headers（Segment）
readelf -S app                 # Section Headers
readelf -s app                 # 符号表
readelf -d app                 # 动态段
objdump -d app                 # 反汇编
objdump -t app                 # 符号表
nm app                         # 符号列表
strings app                    # 提取字符串
```

## 链接过程

```
source.c → (gcc -c) → source.o → (ld) → app
                      ET_REL          ET_EXEC/ET_DYN
```

```bash
# 编译
gcc -c main.c -o main.o        # 编译不链接
gcc main.o utils.o -o app      # 链接

# 查看未解析符号
nm -u main.o                   # U 表示 undefined
```

## 关键要点

> `.text` 是代码，`.data` 是初始化全局变量，`.bss` 是未初始化全局变量（不占文件空间，加载时填充零）。

> GOT/PLT 是动态链接的核心：GOT 存放函数地址，PLT 是跳板。首次调用时通过动态链接器解析地址。

## 相关笔记

- [[Linux 共享库与 ldconfig]] — 动态链接
- [[重定位与符号解析]] — 链接过程
