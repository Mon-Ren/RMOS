---
title: "Linux Page Cache 与回写"
tags: [linux, page cache, writeback, buffer, cache]
aliases: [Page Cache, 页面缓存, 回写, writeback, 缓存机制]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Page Cache 与回写

Page Cache 是 Linux 文件 IO 性能的核心：读操作命中缓存避免磁盘访问，写操作先写缓存再异步回写。

## 工作流程

```
读: read() → Page Cache 命中? → 返回（无磁盘IO）
                  ↓ 未命中
              磁盘读取 → 填充 Page Cache → 返回

写: write() → 写入 Page Cache → 标记 dirty → 立即返回
                      ↓ 异步
              writeback 线程 → 写回磁盘 → 清除 dirty
```

## 查看缓存状态

```bash
free -h                         # buff/cache 列
vmstat 1                        # si/so（swap in/out）bi/bo（block in/out）
cat /proc/meminfo | grep -i cache

# dirty 页统计
cat /proc/vmstat | grep dirty
cat /proc/sys/vm/dirty_ratio           # 触发同步回写的 dirty 比例
cat /proc/sys/vm/dirty_background_ratio # 触发后台回写的 dirty 比例
```

## 调优参数

```bash
# 后台回写阈值（默认 10%）
sysctl -w vm.dirty_background_ratio=5

# 同步回写阈值（默认 20%）
sysctl -w vm.dirty_ratio=10

# dirty 页最大存活时间（默认 30s）
sysctl -w vm.dirty_expire_centisecs=1500

# 回写间隔（默认 5s）
sysctl -w vm.dirty_writeback_centisecs=500
```

## IO 模式

```c
// 默认：带缓冲（使用 Page Cache）
int fd = open("file", O_RDWR);
read(fd, buf, size);

// 直接 IO：绕过 Page Cache
int fd = open("file", O_RDWR | O_DIRECT);
read(fd, buf, size);  // buf 必须对齐

// 同步 IO：每次写立即回写
int fd = open("file", O_RDWR | O_SYNC);

// msync/msync：mmap 后手动回写
msync(addr, length, MS_SYNC);
```

## 关联
- [[linux-虚拟内存与-mmap]] — mmap 直接映射 Page Cache
- [[linux-文件描述符与-IO-模型]] — 缓冲 IO vs 直接 IO
- [[linux-内存管理基础]] — buff/cache 内存

## 关键结论

> Linux 的 Page Cache 会用尽空闲内存做缓存（`free` 中的 buff/cache），这很正常。内存压力大时内核自动回收缓存。调小 dirty_ratio 可以减少大量写操作造成的延迟尖峰。
