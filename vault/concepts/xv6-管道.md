---
title: "xv6 管道"
tags: [xv6, pipe, IPC, inter-process]
aliases: ["pipe", "管道通信"]
created: 2026-04-03
updated: 2026-04-03
---

# xv6 管道

管道是 Unix 进程间通信（IPC）的基本机制：单向字节流，一端写、一端读。

## 数据结构

```c
#define PIPESIZE 512

struct pipe {
  struct spinlock lock;
  char data[PIPESIZE];   // 环形缓冲区
  uint nread;            // 已读字节数
  uint nwrite;           // 已写字节数
  int readopen;          // 读端是否打开
  int writeopen;         // 写端是否打开
};
```

## pipealloc — 创建管道

```c
int pipealloc(struct file **f0, struct file **f1) {
  // 分配两个 file 结构
  *f0 = filealloc();  // 读端
  *f1 = filealloc();  // 写端
  // 分配管道缓冲区
  p = (struct pipe*)kalloc();
  // f0 设为只读，f1 设为只写
  (*f0)->type = FD_PIPE;
  (*f0)->readable = 1;
  (*f0)->pipe = p;
  (*f1)->type = FD_PIPE;
  (*f1)->writable = 1;
  (*f1)->pipe = p;
}
```

## piperead — 读管道

```c
int piperead(struct pipe *p, char *addr, int n) {
  acquire(&p->lock);
  while(p->nread == p->nwrite && p->writeopen)  // 缓冲区空且写端未关闭
    sleep(&p->nread, &p->lock);                  // 睡眠等待数据
  // 从环形缓冲区读取
  for(i = 0; i < n; i++) {
    if(p->nread == p->nwrite) break;
    addr[i] = p->data[p->nread++ % PIPESIZE];
  }
  wakeup(&p->nwrite);  // 唤醒可能在等待空间的写者
  release(&p->lock);
  return i;
}
```

## pipewrite — 写管道

```c
int pipewrite(struct pipe *p, char *addr, int n) {
  acquire(&p->lock);
  for(i = 0; i < n; i++) {
    while(p->nwrite == p->nread + PIPESIZE) {  // 缓冲区满
      if(!p->readopen || myproc()->killed) {    // 读端已关闭
        release(&p->lock);
        return -1;
      }
      wakeup(&p->nread);         // 唤醒读者
      sleep(&p->nwrite, &p->lock); // 睡眠等空间
    }
    p->data[p->nwrite++ % PIPESIZE] = addr[i];
  }
  wakeup(&p->nread);  // 通知有新数据
  release(&p->lock);
  return n;
}
```

## 环形缓冲区

```
data[0..511] 循环使用
nwrite % PIPESIZE = 写位置
nread % PIPESIZE = 读位置
可用空间 = PIPESIZE - (nwrite - nread)
```

- `nwrite - nread = 0` → 缓冲区空 → 读者睡眠
- `nwrite - nread = PIPESIZE` → 缓冲区满 → 写者睡眠

## 典型用法

```c
// shell 中的管道: ls | grep txt
int p[2];
pipe(p);
if(fork() == 0) {
  close(1);        // 关闭 stdout
  dup(p[1]);       // 复制管道写端到 fd 1
  close(p[0]);     // 关闭不需要的读端
  close(p[1]);
  exec("ls", ...);
} else {
  close(0);        // 关闭 stdin
  dup(p[0]);       // 复制管道读端到 fd 0
  close(p[0]);
  close(p[1]);
  exec("grep", "txt", ...);
}
```

## 关键要点

> 管道的核心是 **512 字节环形缓冲区 + sleep/wakeup 同步**。写满则写者睡眠，读空则读者睡眠，用不同的 chan（&nread / &nwrite）区分。关闭端的处理很重要：写端关闭时读者读完数据返回 0（EOF）；读端关闭时写者收到 SIGPIPE（xv6 中直接返回 -1）。

## 关联
- [[xv6 系统调用]] — pipe() 是系统调用入口
- [[xv6 文件系统]] — 管道复用 file 结构和 fd 表
- [[xv6 锁与同步]] — spinlock 保护环形缓冲区
- [[xv6 进程管理]] — fork 后父子进程共享管道
