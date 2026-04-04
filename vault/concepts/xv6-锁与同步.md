---
title: "xv6 锁与同步"
tags: [xv6, lock, spinlock, sleeplock, concurrency]
aliases: ["spinlock", "sleeplock", "自旋锁", "睡眠锁", "同步"]
created: 2026-04-03
updated: 2026-04-03
---

# xv6 锁与同步

xv6 提供两种锁：**自旋锁**（spinlock）和**睡眠锁**（sleeplock），用于多核环境下的互斥。

## 自旋锁 spinlock

```c
struct spinlock {
  uint locked;       // 0=未锁, 1=已锁
  char *name;        // 锁名（调试用）
  struct cpu *cpu;   // 持有锁的 CPU
  uint pcs[10];      // 持有锁时的调用栈
};
```

### acquire — 获取锁

```c
void acquire(struct spinlock *lk) {
  pushcli();                    // 关中断（防止死锁）
  if(holding(lk)) panic("acquire");
  while(xchg(&lk->locked, 1) != 0)  // 原子交换，忙等
    ;
  __sync_synchronize();         // 内存屏障
  lk->cpu = mycpu();
}
```

- `xchg` 是 x86 原子指令，保证读-改-写的原子性
- **持有锁时必须关中断**，否则中断处理程序可能请求同一把锁 → 死锁
- `pushcli/popcli` 支持嵌套：两次 pushcli 需要两次 popcli

### release — 释放锁

```c
void release(struct spinlock *lk) {
  lk->cpu = 0;
  __sync_synchronize();         // 确保临界区的写对其他核可见
  asm volatile("movl $0, %0" : "+m" (lk->locked));
  popcli();                     // 恢复中断
}
```

## 睡眠锁 sleeplock

```c
struct sleeplock {
  uint locked;        // 0=未锁, 1=已锁
  struct spinlock lk; // 保护 locked 的内部自旋锁
  char *name;
  int pid;            // 持有锁的进程
};
```

### 与自旋锁的区别

| | 自旋锁 | 睡眠锁 |
|---|---|---|
| 等待方式 | 忙等（循环） | sleep() 让出 CPU |
| 持有期间 | 关中断 | 可以睡眠 |
| 适用场景 | 短临界区（几条指令） | 长操作（磁盘 IO） |
| 使用者 | 内核数据结构 | inode, buffer |
| 性能 | 低延迟但浪费 CPU | 不浪费 CPU 但有调度开销 |

### acquiresleep

```c
void acquiresleep(struct sleeplock *lk) {
  acquire(&lk->lk);           // 内部自旋锁
  while(lk->locked)
    sleep(lk, &lk->lk);      // 在 chan=lk 上睡眠，释放内部锁
  lk->locked = 1;
  release(&lk->lk);
}
```

## xv6 中的锁使用

| 锁 | 保护对象 |
|----|----------|
| ptable.lock | 进程表 |
| kmem.lock | 物理内存空闲链表 |
| bcache.lock | buffer cache |
| idelock | IDE 磁盘驱动 |
| uartlock | 串口输出 |
| inode 内部 sleeplock | 单个 inode 的读写 |

## 关键要点

> 自旋锁的核心是 **xchg 原子指令 + 关中断**，保证临界区在单核和多核环境下都是互斥的。睡眠锁在自旋锁之上加了 sleep/wakeup 机制，适合持锁时间长的场景。xv6 的锁设计遵循最小化临界区原则——自旋锁只保护最短路径，长操作用睡眠锁。

## 关联
- [[死锁]] — 锁序约定防止循环等待
- [[信号量]] — sleep/wakeup 是 xv6 版的信号量机制
- [[xv6 进程管理]] — ptable.lock 保护进程表
- [[xv6 中断与陷阱]] — pushcli 关中断防止自旋锁死锁
- [[xv6 文件系统]] — sleeplock 保护 inode 和 buffer
- [[xv6 内存分配]] — kmem.lock 保护空闲页链表
- [[xv6 管道]] — 管道用 spinlock 保护环形缓冲区
