---
title: 共享内存 IPC 深入
tags: [system, shared-memory, ipc, shm, mmap, semaphore]
aliases: [共享内存通信, 进程间共享内存, POSIX 共享内存]
created: 2026-04-05
updated: 2026-04-05
---

# 共享内存 IPC 深入

**一句话概述：** 共享内存是最快的 IPC——两个进程映射同一块物理内存，数据直接读写，无需内核拷贝。但需要自己做同步（信号量、互斥锁存在共享内存中）。

```cpp
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <semaphore.h>

// 创建共享内存
int shm_fd = shm_open("/myshm", O_CREAT | O_RDWR, 0666);
ftruncate(shm_fd, 4096);
void* ptr = mmap(nullptr, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);

// 共享内存中放互斥锁 + 数据
struct SharedData {
    pthread_mutex_t mtx;
    int counter;
};
auto* data = static_cast<SharedData*>(ptr);

// 进程 A
pthread_mutex_lock(&data->mtx);
data->counter++;
pthread_mutex_unlock(&data->mtx);
```

## 关键要点

> 共享内存中的互斥锁必须用 `PTHREAD_PROCESS_SHARED` 属性初始化。默认的 mutex 只能在同一进程内使用。

## 相关模式 / 关联

- [[cpp-内存映射文件与零拷贝]] — mmap
- [[cpp-信号量]] — 同步机制
