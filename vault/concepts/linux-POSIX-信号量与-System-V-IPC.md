---
title: "Linux POSIX 信号量与 System V IPC"
tags: [linux, semaphore, ipc, shm, msgqueue]
aliases: [POSIX信号量, System V IPC, 共享内存, 消息队列, semget, shmget]
created: 2026-04-05
updated: 2026-04-05
---

# Linux POSIX 信号量与 System V IPC

Linux 提供两种 IPC 机制：POSIX（现代推荐）和 System V（传统）。

## 信号量

### POSIX 信号量（推荐）

```c
// 命名信号量（跨进程）
sem_t *sem = sem_open("/mysem", O_CREAT, 0644, 1);
sem_wait(sem);      // P 操作（-1）
// 临界区
sem_post(sem);      // V 操作（+1）
sem_close(sem);
sem_unlink("/mysem");

// 匿名信号量（线程间）
sem_t sem;
sem_init(&sem, 0, 1);  // 进程内共享，初始值 1
```

### System V 信号量

```c
int semid = semget(IPC_PRIVATE, 1, 0666);  // 1 个信号量
struct sembuf op = {0, -1, 0};  // sem_num=0, sem_op=-1
semop(semid, &op, 1);           // P 操作
semctl(semid, 0, IPC_RMID);    // 删除
```

## 共享内存

```bash
# POSIX（推荐）
int fd = shm_open("/myshm", O_CREAT|O_RDWR, 0666);
ftruncate(fd, size);
void *addr = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
shm_unlink("/myshm");

# System V
int shmid = shmget(IPC_PRIVATE, size, 0666);
void *addr = shmat(shmid, NULL, 0);
shmdt(addr);
shmctl(shmid, IPC_RMID, NULL);
```

## System V IPC 管理

```bash
# 查看 IPC 对象
ipcs                            # 列出所有
ipcs -m                         # 共享内存
ipcs -s                         # 信号量
ipcs -q                         # 消息队列

# 清理
ipcrm -m <shmid>                # 删除共享内存
ipcrm -s <semid>                # 删除信号量
ipcrm -a                        # 删除所有
```

## 关联
- [[linux-文件描述符与-IO-模型]] — IO 与 IPC
- [[linux-namespace-隔离机制]] — IPC namespace 隔离

## 关键结论

> POSIX IPC 比 System V 更现代：用文件路径标识（/mysem），支持有名/匿名两种方式。System V 用 key_t 标识，管理不便（需要 ipcs/ipcrm）。新项目推荐 POSIX。
