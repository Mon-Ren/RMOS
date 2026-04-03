---
title: "xv6 日志系统"
tags: [xv6, logging, crash-recovery, fs]
aliases: ["Logging System", "WAL", "Write-Ahead Log"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 日志系统

xv6 使用简单的物理 redo 日志（Write-Ahead Logging）保证文件系统在崩溃后的原子性和一致性。

## 核心机制

### 设计动机

文件系统操作通常涉及多个磁盘块的修改（如创建文件需要修改 inode、目录块、位图）。如果在写入过程中系统崩溃，文件系统会处于不一致状态。日志系统确保：**要么所有修改都提交，要么都不提交**。

### 日志结构

磁盘上的日志布局：
```
┌──────────────────┐
│  superblock       │ ← 记录日志起始块号和大小
├──────────────────┤
│  log header       │ ← 包含已提交的块号列表
│  (block #s: A,B,C)│
├──────────────────┤
│  log block A      │ ← 数据块的副本
│  log block B      │
│  log block C      │
├──────────────────┤
│  data blocks      │ ← 文件系统数据区
└──────────────────┘
```

### 核心数据结构

```c
// log.c:26 — 日志头（内存 + 磁盘）
struct logheader {
  int n;                // 日志中的块数
  int block[LOGSIZE];   // 各块对应的目标块号
};

// log.c:31 — 内存中的日志状态
struct log {
  struct spinlock lock;
  int start;            // 日志区起始块号
  int size;             // 日志区最大容量
  int outstanding;      // 正在执行的 FS 系统调用数
  int committing;       // 是否正在提交
  int dev;
  struct logheader lh;
};
```

### 操作接口

**begin_op()** — 开始一个文件系统操作：
```c
// log.c:70
void begin_op(void) {
  acquire(&log.lock);
  while(1){
    if(log.committing){             // 正在提交，等待
      sleep(&log, &log.lock);
    } else if(log.lh.n + (log.outstanding+1)*MAXOPBLOCKS > log.size){
      // 日志空间不够，等待提交释放
      sleep(&log, &log.lock);
    } else {
      log.outstanding += 1;
      release(&log.lock);
      break;
    }
  }
}
```

**log_write()** — 记录一个脏块（类似 bwrite 但不立即写磁盘）：
```c
void log_write(struct buf *b) {
  // 检查日志空间
  if(log.lh.n >= LOGSIZE || log.lh.n >= log.size - 1)
    panic("too big a transaction");
  // 记录块号
  log.lh.block[log.lh.n] = b->blockno;
  log.lh.n++;
  b->flags |= B_DIRTY;  // 标记为脏
}
```

**end_op()** — 结束操作，可能触发提交：
```c
void end_op(void) {
  int do_commit = 0;
  acquire(&log.lock);
  log.outstanding -= 1;
  if(log.committing)
    panic("log.committing");
  if(log.outstanding == 0){        // 没有活跃操作了
    do_commit = 1;
    log.committing = 1;
  } else {
    wakeup(&log);                   // 唤醒等待者
  }
  release(&log.lock);
  if(do_commit)
    commit();                       // 提交
}
```

### 提交流程（commit）

```
commit()
  → write_log()     将所有脏块写入日志区
  → write_head()    写日志头（标记为已提交）
  → install_trans() 将日志块复制到目标位置
  → log.lh.n = 0    清空日志
  → write_head()    写空日志头（标记完成）
```

### 崩溃恢复

```c
// log.c:105
static void recover_from_log(void) {
  read_head();          // 读取日志头
  install_trans();      // 如果有已提交的事务，回放到文件系统
  log.lh.n = 0;
  write_head();         // 清空日志
}
```

启动时读取日志头，如果有未清理的已提交事务，说明上次系统崩溃在 `install_trans()` 之前但 `write_head()` 之后，直接重放即可恢复一致性。

## 关键要点
> xv6 的日志系统是简化的 WAL：多个 FS 操作共享一个事务，只在所有操作完成后才提交。崩溃恢复通过重放已提交的日志实现原子性。关键约束：begin_op 要么等待提交完成，要么等待日志空间释放。

## 关联
- [[xv6 文件系统]] — 日志保护的上层文件系统操作
- [[xv6 缓冲区缓存]] — 日志写入通过 buffer cache 的 bread/bwrite
- [[xv6 锁与同步]] — 日志使用 spinlock 和 sleep 机制
- [[xv6 系统调用]] — 文件系统系统调用包裹在 begin_op/end_op 中
