---
title: "xv6 调度器实现"
tags: [xv6, scheduler, round-robin, process]
aliases: ["Scheduler", "调度器", "Round-Robin"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 调度器实现

xv6 使用简单的 Round-Robin（轮转）调度策略，每个 CPU 核心运行一个无限循环，遍历进程表找到 RUNNABLE 进程并切换执行。

## 核心机制

### 调度器主循环

```c
// proc.c:323 — 每个 CPU 独立运行的调度器
void scheduler(void) {
  struct proc *p;
  struct cpu *c = mycpu();
  c->proc = 0;

  for(;;){
    sti();                          // 开启中断
    acquire(&ptable.lock);
    for(p = ptable.proc; p < &ptable.proc[NPROC]; p++){
      if(p->state != RUNNABLE)
        continue;
      c->proc = p;
      switchuvm(p);                 // 切换到进程的页表
      p->state = RUNNING;
      swtch(&(c->scheduler), p->context);  // ← 关键切换
      switchkvm();                  // 切回内核页表
      c->proc = 0;
    }
    release(&ptable.lock);
  }
}
```

### 调度的两次上下文切换

```
scheduler()                      用户进程
    │                               │
    ├─ switchuvm(p)  切换页表       │
    ├─ p->state = RUNNING          │
    ├─ swtch(scheduler, p->context)─┼──→ 进程从上次中断处继续
    │                               │     ...进程执行...
    │  ←────── sched() ─────────────┤     中断/yield/exit/sleep
    ├─ switchkvm()   切回内核页表    │
    ├─ c->proc = 0                 │
    └─ 继续遍历下一个 RUNNABLE 进程  │
```

关键：`swtch` 保存调度器上下文，恢复进程上下文；进程调用 `sched()` 时反向切换回来。

### sched() — 进程主动让出

```c
// proc.c:366 — 进程 → 调度器的切换入口
void sched(void) {
  int intena;
  struct proc *p = myproc();

  // 安全性检查（4 个 panic 条件）
  if(!holding(&ptable.lock))    panic("sched ptable.lock");
  if(mycpu()->ncli != 1)        panic("sched locks");
  if(p->state == RUNNING)       panic("sched running");
  if(readeflags()&FL_IF)        panic("sched interruptible");

  intena = mycpu()->intena;
  swtch(&p->context, mycpu()->scheduler);  // → 回到 scheduler
  mycpu()->intena = intena;
}
```

四个 panic 检查确保切换安全：
1. 必须持有 ptable.lock
2. 只持有一个锁（ncli==1）
3. 进程状态不能是 RUNNING（应设为 SLEEPING/RUNNABLE）
4. 中断必须关闭

### yield() — 时间片用完主动让出

```c
// proc.c:392 — 时钟中断调用
void yield(void) {
  acquire(&ptable.lock);
  myproc()->state = RUNNABLE;
  sched();
  release(&ptable.lock);
}
```

时钟中断（`trap.c`）每 tick 检查，如果当前进程运行超过 100 ticks 就调用 `yield()`。

### 进程状态机

```
         allocproc()
UNUSED ─────────────→ EMBRYO
                         │  设置内核栈/trapframe/context
                         ↓
                      RUNNABLE ←──── SLEEPING
                         │           (sleep → wakeup)
                         │  scheduler 选中
                         ↓
                      RUNNING ───→ SLEEPING (sleep)
                         │
                         │  sched() 但 state 不变
                         ↓
                      RUNNABLE (yield)
                         │
                         ↓
                      ZOMBIE (exit)
                         │
                         ↓
                      UNUSED (wait 回收)
```

### 多核调度

每个 CPU 独立运行自己的 `scheduler()` 实例。`ptable.lock` 是全局锁，保证同一时间只有一个 CPU 能选择进程。`swtch` 在 per-CPU 的调度器栈和进程内核栈之间切换。

```c
// proc.h — CPU 结构中的调度器上下文
struct cpu {
  struct context *scheduler;   // 调度器的上下文（独立栈）
  struct proc *proc;           // 当前运行的进程
  // ...
};
```

## 局限性

- **O(N) 扫描**：每次调度遍历整个进程表，进程多时效率低
- **无优先级**：所有进程平等轮转
- **无实时性**：不支持优先级或 deadline 调度
- **全局锁**：多核竞争 ptable.lock，扩展性差

## 关键要点
> xv6 调度器是 Round-Robin 的无限循环：遍历进程表找 RUNNABLE 进程，通过 swtch 切换执行。调度的入口是 sched()，它做 4 项安全检查后切换回 scheduler。yield()、sleep()、exit() 都通过 sched() 实现让出。

## 关联
- [[上下文切换]] — swtch.S 的汇编实现
- [[xv6 进程管理]] — 进程状态和 ptable
- [[xv6 睡眠与唤醒]] — sleep/wakeup 的等待队列机制
- [[调度算法比较]] — 与其他调度策略的对比
- [[xv6 锁与同步]] — ptable.lock 的角色
- [[xv6 内核栈]] — scheduler 和进程各自使用的栈
