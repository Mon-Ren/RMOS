---
title: Linux namespace 隔离机制
tags: [linux, namespace, container, isolation, 容器]
aliases: [namespace, 命名空间, 容器隔离, pid ns, net ns, mount ns]
created: 2026-04-05
updated: 2026-04-05
---

# Linux namespace 隔离机制

namespace 是 Linux 内核提供的资源隔离机制，让进程拥有独立的系统资源视图。

## namespace 类型

| 类型 | 隔离内容 | 系统调用标志 |
|------|----------|-------------|
| PID | 进程 ID | CLONE_NEWPID |
| NET | 网络（IP、端口、路由） | CLONE_NEWNET |
| MOUNT | 文件系统挂载点 | CLONE_NEWNS |
| UTS | 主机名和域名 | CLONE_NEWUTS |
| IPC | 信号量、消息队列、共享内存 | CLONE_NEWIPC |
| USER | 用户和组 ID | CLONE_NEWUSER |
| CGROUP | cgroup 根目录 | CLONE_NEWCGROUP |
| TIME | 系统时钟 | CLONE_NEWTIME |

## 查看 namespace

```bash
ls -la /proc/<pid>/ns/         # 进程的 namespace
nsenter -t <pid> -m -p bash    # 进入进程的 mount/pid namespace
readlink /proc/self/ns/net     # 查看当前 net namespace
unshare --mount bash           # 创建新的 mount namespace
```

## unshare 示例

```bash
# 创建新的 UTS namespace（独立主机名）
unshare --uts bash
hostname my-container
hostname                       # 独立的主机名

# 创建新的 mount namespace
unshare --mount bash
mount -t tmpfs none /tmp       # 独立的挂载

# 创建新的 PID namespace
unshare --pid --fork --mount-proc bash
ps aux                         # 只看到自己和子进程
```

## 容器 = cgroup + namespace

```bash
# 查看 Docker 容器的 namespace
docker inspect <container> | grep Pid
ls -la /proc/<pid>/ns/

# 查看容器的 cgroup
cat /proc/<pid>/cgroup
```

## 关键要点

> 容器不是虚拟机，只是通过 namespace 隔离视图 + cgroup 限制资源。所有容器共享同一个内核。

> PID namespace 嵌套存在：容器内的 PID 1 在宿主机上是普通进程。容器内的 `kill -9 1` 不会杀死宿主机的 init。

## 相关笔记

- [[Linux cgroup 资源限制]] — 资源限制
- [[Linux 虚拟内存与 mmap]] — 内存隔离
