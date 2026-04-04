---
title: "xv6 文件描述符"
tags: [xv6, file-descriptor, unix, vfs]
aliases: ["file descriptor", "文件描述符", "fd"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 文件描述符

文件描述符是 Unix "一切皆文件"抽象的核心。它将进程的 I/O 操作与底层实现（磁盘文件、管道、设备）解耦。

## 三层结构

```
进程                    内核全局表              磁盘/设备
─────────────────────────────────────────────────────
proc.ofile[fd]  →    file table[]      →    inode / pipe
(每个进程私有)        (全局共享)           (实际资源)
```

### 1. 进程文件表 `proc.ofile[NOFILE]`

```c
struct proc {
  struct file *ofile[NOFILE];  // 打开的文件指针数组
};
```

- 每个进程最多 `NOFILE`（16）个打开文件
- `ofile[fd]` 为 NULL 表示该 fd 未使用
- fd 0/1/2 分别是 stdin/stdout/stderr

### 2. 全局文件表 `ftable.file[NFILE]`

```c
struct file {
  enum { FD_NONE, FD_PIPE, FD_INODE, FD_DEVICE } type;
  int ref;           // 引用计数
  char readable;
  char writable;
  struct pipe *pipe;  // type=FD_PIPE
  struct inode *ip;   // type=FD_INODE or FD_DEVICE
  uint off;           // 读写偏移（仅 FD_INODE）
};
```

- `ref`：多个 fd 可以指向同一个 file（fork 后父子共享）
- `type` 决定 read/write 走哪条路径

### 3. Inode / Pipe / Device

- **inode**：磁盘文件，通过 `icache` 管理
- **pipe**：管道，有独立的 buffer 和读写端
- **device**：设备（console、磁盘），通过 `devsw[]` 分发

## 关键系统调用

### open()

```c
int open(char *path, int omode) {
  // 1. namei(path) 查找 inode
  // 2. 分配 file 结构体
  // 3. 找到 proc.ofile[] 的空槽位
  // 4. 关联 file → inode
  // 5. 返回 fd
}
```

### read() / write()

```c
int read(int fd, char *buf, int n) {
  f = proc->ofile[fd];
  switch(f->type) {
    case FD_PIPE:  return piperead(f->pipe, buf, n);
    case FD_INODE: return readi(f->ip, buf, f->off, n);
    case FD_DEVICE: return devsw[f->major].read(buf, n);
  }
}
```

### dup()

```c
int dup(int fd) {
  // 找新槽位，指向同一个 file，ref++
}
```

父子进程 fork 后共享 file 表——`dup` 的效果。关闭一个 fd 只是 `ref--`，ref=0 才真正关闭。

### close()

```c
int close(int fd) {
  proc->ofile[fd] = NULL;
  fileclose(f);  // ref--, ref=0 则释放
}
```

## fork 与文件共享

```
fork 前:                          fork 后:
procA.ofile[3] → fileX            procA.ofile[3] → fileX (ref=2)
                                   procB.ofile[3] → fileX ↑
```

- 子进程复制了 fd 数组，但指向**同一个 file 结构体**
- 共享偏移量——父子进程写同一文件会交替追加
- 这是 `ls | wc` 这种管道操作的基础

## pipe 的特殊性

管道在文件系统中没有 inode。它是纯内存结构：

```c
struct pipe {
  struct spinlock lock;
  char data[PIPESIZE];
  uint nread;     // 读取字节数
  uint nwrite;    // 写入字节数
  int readopen;   // 读端是否打开
  int writeopen;  // 写端是否打开
};
```

`pipe()` 系统调用返回两个 fd，一个指向 pipe 的读端，一个指向写端。

## 关键要点

> 文件描述符是 Unix 哲学的精髓：通过统一的 fd 接口，进程无需关心底层是磁盘、管道还是设备。fork + dup + pipe 组合出 shell 管道、重定向等强大功能。

## 关联
- [[xv6 进程管理]] — proc.ofile 是进程结构体的一部分
- [[xv6 管道]] — pipe 的实现细节
- [[xv6 文件系统]] — inode 和磁盘文件的管理
- [[xv6 系统调用]] — open/read/write/close 的入口
- [[xv6 shell 工作原理]] — shell 如何用 fd 实现重定向和管道
