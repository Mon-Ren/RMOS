---
title: "xv6 ELF 与进程加载"
tags: [xv6, elf, exec, loader, binary-format]
aliases: ["ELF loading", "ELF格式", "进程加载"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 ELF 与进程加载

`exec()` 系统调用将 ELF 二进制文件加载到进程地址空间，替换当前进程的代码和数据。这是 Unix 进程执行用户程序的核心机制。

## ELF 文件格式

```
┌─────────────────────┐
│ ELF Header          │  魔数、架构、入口地址
├─────────────────────┤
│ Program Header Table │  描述"如何加载"的段信息
├─────────────────────┤
│ Segment 1 (.text)   │  代码段 — 可执行
├─────────────────────┤
│ Segment 2 (.rodata) │  只读数据
├─────────────────────┤
│ Segment 3 (.data)   │  已初始化数据 — 可读写
├─────────────────────┤
│ Section Header Table │  链接器用的信息（加载时忽略）
└─────────────────────┘
```

### ELF Header

```c
struct elfhdr {
  uint magic;        // 0x7F + "ELF"
  uchar elf[12];
  ushort type;       // ET_EXEC=2 (可执行)
  ushort machine;    // EM_386=3 (x86)
  uint entry;        // 程序入口地址 (_start)
  uint phoff;        // Program Header Table 偏移
  uint shoff;        // Section Header Table 偏移
  uint flags;
  ushort ehsize;     // ELF Header 大小
  ushort phentsize;  // Program Header 条目大小
  ushort phnum;      // Program Header 条目数
};
```

### Program Header (段描述符)

```c
struct proghdr {
  uint type;   // PT_LOAD=1 (需要加载)
  uint off;    // 段在文件中的偏移
  uint vaddr;  // 加载到的虚拟地址
  uint memsz;  // 内存中大小（可能 > filesz，差值填零）
  uint filesz; // 文件中大小
  uint flags;  // PF_R, PF_W, PF_X
};
```

## xv6 exec() 实现

```c
int exec(char *path, char **argv) {
  // 1. 读取 ELF header
  ip = namei(path);
  readi(ip, (char*)&elf, 0, sizeof(elf));
  
  if(elf.magic != ELF_MAGIC)
    goto bad;  // 不是 ELF 文件

  // 2. 分配新页表
  pgdir = setupkvm();

  // 3. 遍历 Program Headers，加载每个 PT_LOAD 段
  for(i=0, off=elf.phoff; i<elf.phnum; i++, off+=sizeof(ph)){
    readi(ip, (char*)&ph, off, sizeof(ph));
    if(ph.type != ELF_PROG_LOAD)
      continue;
    
    sz = allocuvm(pgdir, sz, ph.vaddr + ph.memsz);
    loaduvm(pgdir, (char*)ph.vaddr, ip, ph.off, ph.filesz);
  }
  // ph.memsz > filesz 的部分自动为零（kalloc 清零）

  // 4. 分配两页用户栈
  sz = allocuvm(pgdir, sz, sz + 2*PGSIZE);

  // 5. 将参数和环境变量压栈
  sp = copyout(pgdir, sp, argv, argc);

  // 6. 切换到新镜像
  oldpgdir = proc->pgdir;
  proc->pgdir = pgdir;
  proc->sz = sz;
  proc->tf->eip = elf.entry;   // 入口点
  proc->tf->esp = sp;
  switchuvm(proc);
  freevm(oldpgdir);             // 释放旧页表

  return 0;
}
```

## 加载过程图解

```
ELF 文件                      进程地址空间
──────────                    ──────────────
.text   (off=0x1000)  ──→    0x08048000  代码段 (RX)
.rodata                ──→    0x08049000  只读数据 (R)
.data                  ──→    0x0804A000  数据段 (RW)
                               ↕
                             用户栈 (RW) ← sp 指向这里
                               ↕
                             0x80000000  (内核空间，不可访问)
```

## 关键细节

### 为什么 BSS 可以不从文件读取？

`memsz > filesz` 的部分（BSS 段）由 `allocuvm` 分配的页自动为零（`kalloc` 返回的页被清零），不需要从文件读取。

### 为什么需要 setupkvm？

新页表必须包含内核映射。用户程序执行系统调用时进入内核态，内核代码和数据必须在页表中可见。

### exec 失败怎么办？

如果 exec 失败（格式错误、内存不够），恢复旧页表，返回 -1。这保证了 exec 的原子性——要么完全成功，要么完全不变。

## 关键要点

> exec 的本质是"在当前进程内运行另一个程序"。它不创建新进程（那是 fork 的事），而是替换进程的地址空间内容。fork + exec 的组合是 Unix 程序执行的基础模式。

## 关联
- [[xv6 exec 详解]] — exec 的完整流程（这篇偏重 ELF 格式）
- [[xv6 进程管理]] — exec 与 fork/exit 组成进程生命周期
- [[xv6 系统调用]] — exec 的系统调用入口
- [[页表机制]] — pgdir 的创建和切换
- [[xv6 内存分配]] — allocuvm 使用 kalloc 分配物理页
- [[elf-文件格式]] — ELF 格式的完整规范
