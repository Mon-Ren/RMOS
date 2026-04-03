---
title: "xv6 exec 详解"
tags: [xv6, exec, elf, process, memory]
aliases: ["exec系统调用", "程序加载"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 exec 详解

`exec` 是将当前进程的地址空间替换为新程序的系统调用。它是 xv6 中最复杂的系统调用之一，涉及 ELF 解析、页表重建和栈初始化。

## 核心机制

### 完整流程

```c
// exec.c — 全流程
int exec(char *path, char **argv) {
  // 1. 打开文件
  ip = namei(path);
  ilock(ip);

  // 2. 校验 ELF 头
  readi(ip, &elf, 0, sizeof(elf));
  if(elf.magic != ELF_MAGIC) goto bad;

  // 3. 创建新页表（仅内核映射）
  pgdir = setupkvm();

  // 4. 加载所有 LOAD 段
  for(i=0; i<elf.phnum; i++){
    if(ph.type != ELF_PROG_LOAD) continue;
    sz = allocuvm(pgdir, sz, ph.vaddr + ph.memsz);  // 分配页
    loaduvm(pgdir, ph.vaddr, ip, ph.off, ph.filesz); // 从文件拷贝
  }

  // 5. 分配用户栈（2 页：1 页 guard + 1 页栈）
  sz = allocuvm(pgdir, sz, sz + 2*PGSIZE);
  clearpteu(pgdir, sz - 2*PGSIZE);  // guard 页设为不可访问

  // 6. 构造 argc/argv 栈内容
  for(argc = 0; argv[argc]; argc++){
    sp -= strlen(argv[argc]) + 1;
    copyout(pgdir, sp, argv[argc], ...);  // 拷贝字符串到用户栈
    ustack[3+argc] = sp;                  // 记录指针
  }
  // ustack: [fake_ret_pc, argc, argv_ptr, arg0, arg1, ..., 0]

  // 7. 原子替换：切换页表 + 释放旧页表
  oldpgdir = curproc->pgdir;
  curproc->pgdir = pgdir;
  curproc->sz = sz;
  curproc->tf->eip = elf.entry;   // 入口点 → main()
  curproc->tf->esp = sp;          // 栈顶
  switchuvm(curproc);
  freevm(oldpgdir);               // 释放旧地址空间

  return 0;
}
```

### ELF 文件解析

xv6 只支持简单的 ELF 格式：

```
ELF 文件布局:
┌─────────────────┐
│ ELF Header      │ ← elf.magic, elf.phoff, elf.phnum
├─────────────────┤
│ Program Headers │ ← ph.type, ph.vaddr, ph.filesz, ph.memsz
│ (phnum 个)      │
├─────────────────┤
│ Segment 数据    │ ← 实际的代码/数据
└─────────────────┘
```

```c
// elf.h — ELF 魔数
#define ELF_MAGIC 0x464C457FU  // "\x7fELF" 反转

struct elfhdr {
  uint magic;
  uchar elf[12];
  ushort type;
  ushort machine;
  uint version;
  uint entry;      // 程序入口点地址
  uint phoff;      // 程序头表偏移
  uint shoff;
  uint flags;
  ushort ehsize;
  ushort phentsize;
  ushort phnum;    // 程序头数量
  // ...
};
```

### 段加载 (Load Segment)

每个 `PT_LOAD` 类型的段需要：
1. `allocuvm()` 在新页表中分配虚拟内存
2. `loaduvm()` 从文件拷贝数据到新页表映射的物理页

```
文件偏移 ph.off     虚拟地址 ph.vaddr
     │                   │
     ▼                   ▼
┌──────────┐      ┌──────────────┐
│ 文件数据  │ ──→  │ 代码/数据段   │  ph.filesz (从文件读取)
│ ph.filesz│      │              │
└──────────┘      │ BSS 段       │  ph.memsz - ph.filesz (清零)
                  │ (全零)       │
                  └──────────────┘
```

### 用户栈初始化

exec 在栈底分配 2 页，高页作栈，低页作 guard（不可访问，触发 page fault 时就知道栈溢出了）：

```
高地址 (sz)
┌─────────────────┐
│ 用户栈           │ ← sp 初始指向这里
│ (1 页, PGSIZE)   │
├─────────────────┤ ← sz - PGSIZE
│ Guard 页         │ ← PTE_U 清除，访问触发 trap
│ (不可访问)       │
├─────────────────┤ ← sz - 2*PGSIZE
│ 其他段           │
└─────────────────┘
低地址 (0)
```

栈内容布局（从高到低）：
```
sp → ┌──────────────┐
     │ argv[argc]=0 │ ← 终止标记
     │ argv[n-1]    │ ← 指向栈中的字符串
     │ ...          │
     │ argv[0]      │
     │ argv_ptr     │ ← argv 的地址
     │ argc         │ ← 参数个数
     │ 0xFFFFFFFF   │ ← 假返回地址（main 不会返回）
     └──────────────┘
```

### 原子性保证

exec 的替换是原子的：只在所有资源（新页表、文件读取、栈分配）都成功后才替换 `curproc->pgdir`。失败时 `goto bad` 释放已分配的资源，原进程不受影响。

```c
bad:
  if(pgdir) freevm(pgdir);    // 释放新建的页表
  if(ip){ iunlockput(ip); end_op(); }
  return -1;                   // 进程保持原状
```

## 关键要点
> exec 核心是「建新页表 → 加载 ELF 段 → 初始化用户栈 → 原子替换」。所有分配都完成后才替换 pgdir，失败则完全回滚。栈底有 guard 页检测溢出，栈上布局模拟 C 函数调用约定（fake ret PC + argc + argv）。

## 关联
- [[ELF 文件格式]] — ELF 头和程序头的详细结构
- [[页表机制]] — setupkvm/allocuvm/loaduvm 的页表操作
- [[xv6 进程管理]] — exec 在进程生命周期中的角色
- [[xv6 系统调用]] — exec 作为系统调用的入口
- [[xv6 内存分配]] — kalloc/uvmalloc 提供物理页
- [[COW 写时复制]] — 现代 OS 中 exec 的优化方向
- [[xv6 shell 工作原理]] — shell 调用 exec 执行命令
