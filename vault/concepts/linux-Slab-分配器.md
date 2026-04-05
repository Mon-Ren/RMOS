---
title: "Linux Slab 分配器"
tags: [linux, kernel, slab, memory, allocator]
aliases: [Slab, Slub, Slob, 内核内存分配器, kmem_cache]
created: 2026-04-05
updated: 2026-04-05
---

# Linux Slab 分配器

Slab 是 Linux 内核的对象缓存分配器，为频繁创建销毁的内核对象（inode、dentry 等）提供高效内存管理。

## 三种实现

| 分配器 | 特点 | 适用场景 |
|--------|------|----------|
| Slab | 原始实现，有队列管理 | Solaris 风格 |
| Slub | 现代默认，简化设计 | 大多数系统 |
| Slob | 极简，适合嵌入式 | 小内存系统 |

## Slub 工作原理

```
Page Frame → Slub Cache → Object
              kmem_cache
              ├── slab (page 1) → [obj][obj][obj]...
              ├── slab (page 2) → [obj][obj][obj]...
              └── slab (page 3) → ...
```

### 三层结构

1. **kmem_cache**：特定对象类型的缓存
2. **slab**：一个或多个连续页，存放同类对象
3. **per-CPU slab**：每个 CPU 独立缓存，无锁分配

## 查看 Slab 信息

```bash
cat /proc/slabinfo              # 所有 slab 缓存
slabtop                         # 实时排序
cat /proc/meminfo | grep Slab   # slab 总量
```

## 内核 API

```c
// 创建缓存
struct kmem_cache *cache = kmem_cache_create(
    "my_object",                // 名称
    sizeof(struct my_obj),      // 对象大小
    0,                          // 对齐
    SLAB_HWCACHE_ALIGN,         // 标志
    NULL                        // 构造函数
);

// 分配/释放
void *obj = kmem_cache_alloc(cache, GFP_KERNEL);
kmem_cache_free(cache, obj);

// 销毁缓存
kmem_cache_destroy(cache);
```

## 关联
- [[linux-内存管理基础]] — 页级内存管理
- [[linux-虚拟内存与-mmap]] — 用户空间内存分配

## 关键结论

> Slub 是现代 Linux 默认分配器：比 Slab 更简洁（减少 50% 元数据开销），per-CPU 缓存避免锁竞争。`slabtop` 可以看到 dentry 和 inode 缓存通常占最大比例。
