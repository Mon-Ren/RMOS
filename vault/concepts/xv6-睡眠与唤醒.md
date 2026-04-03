---
title: "xv6 睡眠与唤醒"
tags: [xv6, sleep, wakeup, synchronization, wait-queue]
aliases: ["Sleep/Wakeup", "等待队列", "条件同步"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 睡眠与唤醒

xv6 的 sleep/wakeup 是比 spinlock 更高级的同步原语，允许进程在等待条件时**释放 CPU**（进入 SLEEPING 状态），而不是忙等。

## 核心机制

### sleep() — 原子释放锁并休眠

```c
// proc.c:418
void sleep(void *chan, struct spinlock *lk) {
  struct proc *p = myproc();

  // 关键：先拿 ptable.lock，再释放 lk
  if(lk != &ptable.lock){
    acquire(&ptable.lock);   // ① 获取进程表锁
    release(lk);             // ② 释放调用者的锁
  }

  p->chan = chan;            // ③ 设置睡眠通道（等待条件的标识）
  p->state = SLEEPING;      // ④ 标记为睡眠
  sched();                  // ⑤ 切换到调度器

  // 被 wakeup 唤醒后继续执行
  p->chan = 0;
  if(lk != &ptable.lock){
    release(&ptable.lock);
    acquire(lk);             // ⑥ 重新获取调用者的锁
  }
}
```

### wakeup() — 唤醒所有等待同一通道的进程

```c
// proc.c:469
void wakeup(void *chan) {
  acquire(&ptable.lock);
  wakeup1(chan);
  release(&ptable.lock);
}

// proc.c:458 — 内部实现
static void wakeup1(void *chan) {
  struct proc *p;
  for(p = ptable.proc; p < &ptable.proc[NPROC]; p++)
    if(p->state == SLEEPING && p->chan == chan)
      p->state = RUNNABLE;   // 改状态，不直接运行
}
```

### Channel（通道）模型

sleep/wakeup 使用 `void *chan` 作为匹配标识，而非显式的等待队列：

```
进程 A: sleep(&disk_buf[3], &lock)    ← chan = &disk_buf[3]
进程 B: sleep(&disk_buf[3], &lock)    ← chan = &disk_buf[3]
...
进程 C: wakeup(&disk_buf[3])          ← 唤醒所有 chan 匹配的进程
```

channel 可以是任意指针（通常是锁保护的共享变量地址），只要 sleep 和 wakeup 使用相同的值即可匹配。

### 防止竞态的关键设计

sleep 的**原子性**在于 `acquire(ptable.lock)` 和 `release(lk)` 的顺序：

```
调用者:                     唤醒者:
  acquire(mylock)             acquire(ptable.lock)
  if(条件不满足)               // 检查条件，设置 channel
    sleep(chan, mylock)  ←──→ wakeup1(chan)
  // 条件满足                  release(ptable.lock)
  release(mylock)
```

如果先释放 mylock 再获取 ptable.lock，中间可能有 wakeup 发生导致丢失：
```
❌ 错误顺序：
  release(mylock)          ← 唤醒者此时获得 mylock
  wakeup(chan)             ← 此时进程还没 sleep，wakeup 白费
  acquire(ptable.lock)     ← 进程现在才 sleep，但 wakeup 已经过了
  sleep()                  ← 永久睡眠！
```

正确的顺序（先拿 ptable.lock）保证 wakeup 必定在 sleep 设置 state 之后才能执行。

### 使用模式

```c
// 典型用法：等待条件
acquire(&mylock);
while(条件不满足){
  sleep(&条件变量, &mylock);  // 释放 mylock，等待
}
// 条件满足，持有 mylock
操作共享数据...
release(&mylock);

// 唤醒端
acquire(&mylock);
修改条件...
wakeup(&条件变量);          // 唤醒所有等待者
release(&mylock);
```

### 实际应用示例

**管道读取**（pipe.c）：
```c
// 读端
while(pipe->nread == pipe->nwrite)
  sleep(&pipe->nread, &pipe->lock);  // 管道空，等待写入
```

**进程等待子进程**（proc.c）：
```c
// wait()
sleep(curproc, &ptable.lock);  // 等待子进程 exit 调用 wakeup1
```

**日志提交**（log.c）：
```c
// begin_op
while(log.committing)
  sleep(&log, &log.lock);  // 等待提交完成
```

### 唤醒所有 vs 唤醒一个

xv6 只有 `wakeup()`（唤醒所有），没有 `signal()`（唤醒一个）。这叫做「惊群」(thundering herd)：多个进程被唤醒后只有一个能获得资源，其余的回到 sleep。xv6 接受这个开销因为实现简单。

## 关键要点
> sleep(chan, lock) 原子地释放 lock 并进入 SLEEPING 状态；wakeup(chan) 将所有匹配 channel 的进程设为 RUNNABLE。关键是先获取 ptable.lock 再释放调用者的锁，防止 wakeup 丢失。xv6 只有 broadcast（唤醒所有），没有 signal（唤醒一个）。

## 关联
- [[xv6 锁与同步]] — spinlock 保护短临界区，sleep/wakeup 保护长等待
- [[xv6 调度器实现]] — sched() 实现上下文切换
- [[xv6 管道]] — 管道的读写阻塞使用 sleep/wakeup
- [[xv6 缓冲区缓存]] — sleeplock 在 sleep/wakeup 之上构建
- [[xv6 进程管理]] — wait() 和 exit() 的父子进程同步
- [[xv6 日志系统]] — begin_op/end_op 中的等待逻辑
