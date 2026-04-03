---
title: "xv6 缓冲区缓存"
tags: [xv6, buffer-cache, disk, fs]
aliases: ["Buffer Cache", "BCACHE", "磁盘缓存"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 缓冲区缓存

缓冲区缓存是内存中的磁盘块缓存层，减少磁盘 I/O 并提供磁盘块的同步访问点。

## 核心机制

### 设计目标

1. **缓存**：避免重复读取相同磁盘块
2. **同步**：同一时间只有一个进程访问特定磁盘块
3. **共享**：多个进程可以读取同一块（但互斥修改）

### 接口

| 函数 | 说明 |
|------|------|
| `bread(dev, blockno)` | 读取磁盘块，返回锁住的 buffer |
| `bwrite(b)` | 将 buffer 写回磁盘 |
| `brelse(b)` | 释放 buffer（释放锁 + 放回缓存链表） |

```
调用者: bread() → 获取 buffer → 读/写数据 → bwrite()（可选）→ brelse()
```

### 数据结构

```c
// bio.c:28 — 缓冲区缓存
struct {
  struct spinlock lock;
  struct buf buf[NBUF];     // 固定大小的 buffer 池
  struct buf head;          // 双向循环链表头（LRU 顺序）
} bcache;

// buf.h — 单个 buffer
struct buf {
  int flags;                // B_VALID | B_DIRTY
  uint dev;
  uint blockno;
  struct sleeplock lock;    // 每 buffer 独立的睡眠锁
  uint refcnt;              // 引用计数
  struct buf *prev;         // LRU 链表
  struct buf *next;
  uchar data[BSIZE];        // 512 字节数据
};
```

### 查找与分配 (bget)

```c
// bio.c:55
static struct buf* bget(uint dev, uint blockno) {
  acquire(&bcache.lock);

  // 1. 在缓存中查找
  for(b = bcache.head.next; b != &bcache.head; b = b->next){
    if(b->dev == dev && b->blockno == blockno){
      b->refcnt++;
      release(&bcache.lock);
      acquiresleep(&b->lock);   // 获取 buffer 级别的锁
      return b;
    }
  }

  // 2. 未命中，从 LRU 尾部回收
  for(b = bcache.head.prev; b != &bcache.head; b = b->prev){
    if(b->refcnt == 0 && (b->flags & B_DIRTY) == 0) {
      b->dev = dev;
      b->blockno = blockno;
      b->flags = 0;
      b->refcnt = 1;
      release(&bcache.lock);
      acquiresleep(&b->lock);
      return b;
    }
  }
  panic("bget: no buffers");
}
```

### LRU 策略

使用双向循环链表维护 LRU 顺序：
- `head.next` = 最近使用（MRU 端）
- `head.prev` = 最久未使用（LRU 端）
- `brelse()` 将释放的 buffer 移到 MRU 端
- 分配时从 LRU 端扫描 `refcnt==0 && !B_DIRTY` 的 buffer

```
head ↔ [MRU] ↔ [...] ↔ [...] ↔ [LRU] ↔ head
            ↑ brelse 移到这里    ↑ bget 从这里回收
```

### 双重锁机制

xv6 的 buffer cache 使用两级锁：
1. **`bcache.lock`（spinlock）**：保护缓存的查找和分配
2. **`b->lock`（sleeplock）**：保护单个 buffer 的数据操作

```
bread():
  acquire(bcache.lock)     ← 短暂持有，找到 buffer 后释放
  找到/分配 buffer
  release(bcache.lock)
  acquiresleep(b->lock)    ← 可能长时间持有（IO 等待）
  如果需要，读磁盘
  return b（锁住的）

brelse():
  releasesleep(b->lock)    ← 释放数据锁
  acquire(bcache.lock)     ← 更新 LRU 链表
  b->refcnt--; 移到 MRU
  release(bcache.lock)
```

### B_DIRTY 的特殊含义

`B_DIRTY` 不仅表示数据已修改，还被日志系统使用：
- `log_write()` 设置 `B_DIRTY` 但不立即写盘
- `bget()` 回收时跳过 `B_DIRTY` 的 buffer（日志尚未提交）
- 只有 `commit()` → `install_trans()` 才清除 `B_DIRTY`

## 关键要点
> xv6 缓冲区缓存是固定大小（NBUF）的 LRU 缓存，使用双向循环链表管理。双重锁设计：spinlock 保护缓存结构，sleeplock 保护单个 buffer。B_DIRTY 标志同时服务于数据修改和日志系统的原子性保证。

## 关联
- [[xv6 日志系统]] — 日志通过 log_write/bwrite 与 buffer cache 交互
- [[xv6 文件系统]] — fs.c 上层通过 bread/bwrite 访问磁盘
- [[xv6 锁与同步]] — spinlock + sleeplock 的组合使用
- [[设备驱动模型]] — ide.c 实际的磁盘读写
- [[xv6 内存分配]] — buffer 数据区也是 kalloc 分配的页
