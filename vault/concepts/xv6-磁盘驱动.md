---
title: "xv6 磁盘驱动"
tags: [xv6, ide, disk, driver, pio]
aliases: ["IDE Driver", "磁盘I/O", "PIO模式"]
created: 2026-04-04
updated: 2026-04-04
---

# xv6 磁盘驱动

xv6 使用 PIO（Programmed I/O）模式的 IDE 磁盘驱动，通过 CPU 直接读写 I/O 端口与磁盘控制器通信，不使用 DMA。

## 核心机制

### IDE 硬件接口

IDE 磁盘控制器通过 I/O 端口（0x1F0-0x1F7）访问：

| 端口 | 读/写 | 用途 |
|------|-------|------|
| 0x1F0 | R/W | 数据端口（16 位） |
| 0x1F2 | W | 扇区数 |
| 0x1F3 | W | LBA 地址低 8 位 |
| 0x1F4 | W | LBA 地址中 8 位 |
| 0x1F5 | W | LBA 地址高 8 位 |
| 0x1F6 | W | 驱动器/磁头/LBA 模式 |
| 0x1F7 | R/W | 状态/命令 |

### 初始化

```c
// ide.c:35
void ideinit(void) {
  initlock(&idelock, "ide");
  ioapicenable(IRQ_IDE, ncpu - 1);  // 将 IDE 中断路由到最后一个 CPU
  idewait(0);

  // 探测磁盘 1 是否存在
  outb(0x1f6, 0xe0 | (1<<4));
  for(i=0; i<1000; i++){
    if(inb(0x1f7) != 0){
      havedisk1 = 1;
      break;
    }
  }
  outb(0x1f6, 0xe0 | (0<<4));  // 切回磁盘 0
}
```

### 发起磁盘请求

```c
// ide.c:60 — idestart 发起 I/O 命令
static void idestart(struct buf *b) {
  int sector = b->blockno * sector_per_block;

  idewait(0);                       // 等待磁盘就绪
  outb(0x3f6, 0);                   // 允许中断
  outb(0x1f2, sector_per_block);    // 扇区数
  outb(0x1f3, sector & 0xff);       // LBA 地址
  outb(0x1f4, (sector >> 8) & 0xff);
  outb(0x1f5, (sector >> 16) & 0xff);
  outb(0x1f6, 0xe0 | ((b->dev&1)<<4) | ((sector>>24)&0x0f));

  if(b->flags & B_DIRTY){
    outb(0x1f7, write_cmd);
    outsl(0x1f0, b->data, BSIZE/4);  // PIO: CPU 直接写数据到端口
  } else {
    outb(0x1f7, read_cmd);           // 读命令，数据由中断返回
  }
}
```

### 请求队列与中断驱动

xv6 的 IDE 驱动使用**单链表队列**和**中断驱动**模式：

```
                    idelock
                       │
  请求1 → 请求2 → 请求3 → idequeue (当前处理中)
                              │
                         idestart() 发起
                              │
                         ...磁盘操作...
                              │
                         中断触发 (IRQ_IDE)
                              │
                         ideintr() 完成当前
                              │
                         唤醒等待进程
                              │
                         启动下一个请求
```

```c
// ide.c — ideintr 中断处理
void ideintr(void) {
  struct buf *b;

  // 取出已完成的请求
  b = idequeue;
  idequeue = b->qnext;

  // 读模式：从端口读取数据到 buffer
  if(!(b->flags & B_DIRTY)){
    insl(0x1f0, b->data, BSIZE/4);  // PIO 读取
  }

  b->flags |= B_VALID;
  b->flags &= ~B_DIRTY;
  wakeup(b);  // 唤醒在 bread() 中等待的进程

  // 启动队列中的下一个请求
  if(idequeue != 0)
    idestart(idequeue);
}
```

### PIO vs DMA

xv6 使用 PIO（编程 I/O），数据传输全程由 CPU 参与：

```
PIO 写:  CPU → 端口 0x1F0 → 磁盘控制器 → 磁盘
PIO 读:  磁盘 → 磁盘控制器 → 端口 0x1F0 → CPU

DMA:     CPU → 命令 → 磁盘控制器 ↔ 内存 (CPU 可做其他事)
                      (DMA 引擎直接访问内存)
```

- **PIO**：简单但浪费 CPU（`outsl` 循环期间 CPU 不能做别的事）
- **DMA**：高效但需要 DMA 控制器和内存映射
- xv6 选择 PIO 是为了简化教学实现

### 与 buffer cache 的关系

```
bread(dev, blockno)
  → bget() 检查缓存
  → 未命中：acquiresleep(b->lock)
  → iderw(b)
      → acquire(idelock)
      → 加入 idequeue
      → 如果队列空，idestart(b) 立即发起
      → release(idelock)
      → sleep(b, &idelock)    ← 等待中断唤醒
      → 中断: ideintr() → wakeup(b)
  → 返回锁住的 buffer
```

### 多磁盘支持

xv6 支持最多 2 个 IDE 磁盘（havedisk1 标志），通过 `b->dev` 的最低位选择驱动器号。

## 关键要点
> xv6 IDE 驱动是 PIO 模式，CPU 通过 in/out 指令直接读写 0x1F0-0x1F7 端口。单链表请求队列 + 中断驱动：idestart 发起命令，ideintr 处理完成并唤醒等待者。bread() 调用者通过 sleep(&idelock) 等待 I/O 完成。

## 关联
- [[xv6 缓冲区缓存]] — bread/bwrite 调用 iderw
- [[xv6 睡眠与唤醒]] — iderw 使用 sleep 等待中断
- [[设备驱动模型]] — 设备驱动的通用模式
- [[xv6 锁与同步]] — idelock 保护请求队列
- [[IDT 与中断机制]] — IRQ_IDE 如何路由到中断处理
- [[DMA 与总线架构]] — PIO 的对比方案
