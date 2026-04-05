---
title: "Linux huge pages 大页内存"
tags: [linux, memory, hugepage, thp, transparent]
aliases: [大页, huge pages, THP, transparent huge pages, 2MB页]
created: 2026-04-05
updated: 2026-04-05
---

# Linux huge pages 大页内存

大页（Huge Pages）减少 TLB 未命中，提升内存密集型应用性能。

## 页大小

| 页大小 | TLB 覆盖 | 适用场景 |
|--------|----------|----------|
| 4KB | 4MB（512 项） | 通用 |
| 2MB（大页） | 1GB | 数据库、虚拟化 |
| 1GB（巨大页） | 512GB | 大内存应用 |

## 透明大页（THP）

```bash
# 查看 THP 状态
cat /sys/kernel/mm/transparent_hugepage/enabled
# [always] madvise never

# 查看使用情况
cat /proc/meminfo | grep -i huge
AnonHugePages:    204800 kB

# 控制
echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

## 静态大页（手动管理）

```bash
# 预留大页
echo 1024 > /proc/sys/vm/nr_hugepages     # 1024 个 2MB 大页 = 2GB

# 挂载 hugetlbfs
mount -t hugetlbfs hugetlbfs /mnt/huge

# 查看
cat /proc/meminfo | grep HugePages
HugePages_Total:    1024
HugePages_Free:     1024
Hugepagesize:       2048 kB
```

## 应用使用大页

```c
// mmap 大页
void *addr = mmap(NULL, size, PROT_READ|PROT_WRITE,
                  MAP_PRIVATE|MAP_ANONYMOUS|MAP_HUGETLB, -1, 0);

// 或使用 hugetlbfs
int fd = open("/mnt/huge/mydata", O_CREAT|O_RDWR, 0755);
void *addr = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
```

## 数据库场景

```bash
# PostgreSQL 使用大页
echo "huge_pages = on" >> postgresql.conf
echo 2048 > /proc/sys/vm/nr_hugepages

# Oracle 使用大页
echo "vm.nr_hugepages = $(cat /proc/meminfo | grep MemTotal)" >> /etc/sysctl.conf
```

## 关联
- [[linux-虚拟内存与-mmap]] — mmap 映射
- [[linux-内存管理基础]] — 内存管理基础

## 关键结论

> THP 是"透明"的（自动合并为 2MB 页），对大多数应用无需修改代码。但数据库等延迟敏感场景可能因 THP 的 compaction 造成延迟抖动，建议关闭 THP 而手动管理静态大页。
