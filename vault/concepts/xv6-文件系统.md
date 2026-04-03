---
title: "xv6 文件系统"
tags: [xv6, filesystem, inode, log]
aliases: ["xv6 fs", "xv6文件系统"]
created: 2026-04-03
updated: 2026-04-03
---

# xv6 文件系统

xv6 的文件系统是经典的 Unix 分层设计，共五层。

## 五层架构

```
┌─────────────────────┐
│   名称层 (Names)     │  路径解析 /usr/rtm/xv6/fs.c
├─────────────────────┤
│   目录层 (Directory) │  目录是特殊的 inode，内容是 dirent 序列
├─────────────────────┤
│   文件层 (Inode)     │  inode 读写、元数据、数据块管理
├─────────────────────┤
│   日志层 (Log)       │  崩溃恢复：多步写入的原子性
├─────────────────────┤
│   块层 (Blocks)      │  磁盘块的分配与释放（bitmap）
└─────────────────────┘
```

## 磁盘布局

```
[ boot | super | log | inode blocks | free bitmap | data blocks ]
```

### superblock 超级块

```c
struct superblock {
  uint size;       // 文件系统总块数
  uint nblocks;    // 数据块数
  uint ninodes;    // inode 数
  uint nlog;       // 日志块数
  uint logstart;   // 日志起始块号
  uint inodestart; // inode 起始块号
  uint bmapstart;  // 位图起始块号
};
```

### dinode 磁盘 inode

```c
struct dinode {
  short type;          // 文件类型 (0=free, 1=dir, 2=file, 3=device)
  short major;         // 设备号（仅 T_DEV）
  short minor;         // 设备号（仅 T_DEV）
  short nlink;         // 硬链接数
  uint size;           // 文件大小（字节）
  uint addrs[NDIRECT+1]; // 数据块地址
};
```

### 数据块寻址

```
addrs[0..11]   → 12 个直接块（12 × 512B = 6KB）
addrs[12]      → 1 个一级间接块（128 × 512B = 64KB）
最大文件 = 6KB + 64KB = 70KB
```

## 日志系统

保证多块写入的**原子性**。写操作流程：

```
begin_op()
  │ log_write(bp)  ← 不立即写磁盘，记录到内存日志
  │ log_write(bp)
  │ ...
end_op()
  │ 写入日志头（包含块号列表）
  │ 将日志块写到对应磁盘位置
  │ 清除日志头（提交完成）
```

崩溃恢复：启动时检查日志头，若有未完成的日志 → 重放写入。

## inode 缓存

内核维护一个 inode 缓存（`icache`），iget() 获取引用，iput() 释放。nlink==0 且无引用时释放磁盘块。

## 目录结构

目录是类型为 `T_DIR` 的 inode，内容是一系列 `dirent`：

```c
struct dirent {
  ushort inum;    // inode 号
  char name[14];  // 文件名
};
```

路径解析：从根 inode 开始，逐级查找 dirent → iget 对应 inode → 继续。

## 关键要点

> xv6 文件系统的精妙之处在**日志层**：用简单的 WAL（Write-Ahead Logging）保证了多块更新的原子性。数据块寻址用 12 直接 + 1 间接，教学上够用，但最大 70KB 严重限制了文件大小。inode 缓存和 buffer cache 两层缓存减少了磁盘 IO。

## 关联
- [[xv6 锁与同步]] — sleeplock 保护 inode 和 buffer
- [[xv6 系统调用]] — sysfile.c 实现 open/read/write
- [[xv6 内存分配]] — kalloc 为 buffer cache 分配页
- [[xv6 管道]] — 管道作为特殊文件的实现
