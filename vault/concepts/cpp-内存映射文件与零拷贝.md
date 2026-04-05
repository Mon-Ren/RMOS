---
title: 内存映射文件与零拷贝
tags: [cpp, mmap, memory-mapped, zero-copy, file-io]
aliases: [mmap 文件映射, 零拷贝 IO, 内存映射读写]
created: 2026-04-05
updated: 2026-04-05
---

# 内存映射文件与零拷贝

**一句话概述：** mmap 把文件映射到虚拟地址空间——读文件变成读内存，由操作系统按需加载页（page fault 触发）。比 read/write 少一次用户态-内核态数据拷贝，大文件处理的性能利器。

```cpp
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

void read_file_mmap(const char* path) {
    int fd = open(path, O_RDONLY);
    struct stat sb;
    fstat(fd, &sb);
    size_t size = sb.st_size;

    // 映射文件到内存
    void* addr = mmap(nullptr, size, PROT_READ, MAP_PRIVATE, fd, 0);
    // addr 现在可以像普通内存一样访问文件内容
    const char* data = static_cast<const char*>(addr);

    // 零拷贝读取
    for (size_t i = 0; i < size; ++i) {
        process(data[i]);  // 不需要 read() 系统调用
    }

    munmap(addr, size);
    close(fd);
}
```

## 关键要点

> mmap 的优势在大文件和随机访问。小文件或顺序访问，read() 可能更快（因为 read 用 page cache，mmap 有 page fault 开销）。数据库引擎通常混合使用两者。

## 相关模式 / 关联

- [[cpp-流与IO基础]] — 流式 IO
- [[cpp-性能优化速查]] — IO 优化
- [[cpp-RAII惯用法]] — RAII 封装 fd/mmap
