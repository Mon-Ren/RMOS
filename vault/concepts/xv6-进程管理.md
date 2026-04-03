---
title: "xv6 进程管理"
tags: [xv6, process, scheduling, fork]
aliases: ["xv6 process", "xv6进程"]
created: 2026-04-03
updated: 2026-04-03
---

# xv6 进程管理

xv6 的进程模型遵循 Unix 传统：`fork` + `exec` + `exit/wait`。

## 进程结构体 `struct proc`

```c
struct proc {
  uint sz;                     // 进程内存大小
  pde_t* pgdir;                // 页表
  char *kstack;                // 内核栈底
  enum procstate state;        // 进程状态
  int pid;                     // 进程 ID
  struct proc *parent;         // 父进程
  struct trapframe *tf;        // 系统调用时的陷阱帧
  struct context *context;     // swtch() 切换上下文
  void *chan;                  // sleep/wakeup 的等待通道
  int killed;                  // 被杀死标记
  struct file *ofile[NOFILE];  // 打开的文件
  struct inode *cwd;           // 当前工作目录
  char name[16];               // 进程名
};
```

## 进程状态机

```
UNUSED → EMBRYO → RUNNABLE ⇄ RUNNING → ZOMBIE
                           ↘ SLEEPING ↗
```

- **UNUSED**：空闲槽位
- **EMBRYO**：正在初始化（分配内核栈、设置上下文）
- **RUNNABLE**：就绪，等待调度
- **RUNNING**：正在执行
- **SLEEPING**：等待某个事件（`chan`）
- **ZOMBIE**：已退出，等待父进程 `wait()` 回收

## 进程创建

### allocproc() — 分配进程槽

1. 遍历 `ptable.proc[NPROC]` 找 `UNUSED` 槽位
2. 分配内核栈（`kalloc`）
3. 在栈底布置 trapframe 和 context
4. context 的 eip 指向 `forkret`

### userinit() — 创建第一个用户进程

- 加载 `initcode.S` 到用户空间
- 设置 `trapframe`：cs/ds 为用户段，eflags 开启中断，eip=0
- 工作目录设为根目录 `/`
- 状态设为 `RUNNABLE`

### fork() — 复制进程

1. `allocproc()` 分配新进程
2. `copyuvm()` 复制整个用户页表（深拷贝）
3. 复制 trapframe，**将子进程 eax 设为 0**（fork 返回值区分父子）
4. `filedup()` 复制文件描述符引用
5. `idup()` 复制 cwd inode 引用

## 调度器

xv6 使用**简单的轮转调度**（Round-Robin）：

```c
void scheduler(void) {
  for(;;) {
    sti();  // 开中断
    acquire(&ptable.lock);
    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++) {
      if(p->state != RUNNABLE) continue;
      switchuvm(p);
      p->state = RUNNING;
      swtch(&(c->scheduler), p->context);  // 上下文切换
      switchkvm();
    }
    release(&ptable.lock);
  }
}
```

- 每个 CPU 有一个独立的 scheduler 循环
- `swtch()` 是汇编实现的上下文切换，只保存 callee-saved 寄存器（edi, esi, ebx, ebp, eip）
- 不保存 eax, ecx, edx（调用者保存）

## 退出与回收

- **`exit()`**：关闭文件、释放 cwd、状态设为 ZOMBIE、唤醒父进程
- **`wait()`**：扫描 ptable 找 ZOMBIE 子进程，释放其资源；若无子进程退出则 sleep

## 关键要点

> xv6 进程管理的核心是 **ptable 全局数组 + 自旋锁**。所有状态转换都在持有 ptable.lock 下进行。调度器是纯轮转、无优先级、无时间片——这是教学 OS 的简化设计，但完整展示了进程生命周期的本质。

## 关联
- [[信号机制]] — kill() 设置 killed 标志，信号触发 exit
- [[xv6 启动流程]] — userinit 是启动的最后一步
- [[页表机制]] — pgdir 和 copyuvm 的内存隔离
- [[xv6 中断与陷阱]] — trapframe 的布局和作用
- [[xv6 系统调用]] — fork/exit/wait 都通过 syscall 接口暴露
- [[上下文切换]] — swtch.S 的实现细节
