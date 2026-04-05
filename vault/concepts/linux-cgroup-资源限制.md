---
title: Linux cgroup 资源限制
tags: [linux, cgroup, resource, container, 限制]
aliases: [cgroup, cgroups, 资源限制, CPU限制, 内存限制, 容器基础]
created: 2026-04-05
updated: 2026-04-05
---

# Linux cgroup 资源限制

cgroup（Control Group）是 Linux 内核机制，用于限制、记录和隔离进程组的资源使用。

## cgroup v2 结构

```
/sys/fs/cgroup/
├── cgroup.controllers      # 可用控制器
├── cgroup.subtree_control   # 启用的控制器
├── cpu.max                  # CPU 限制
├── memory.max               # 内存限制
├── memory.current           # 当前内存使用
├── pids.max                 # 进程数限制
└── mygroup/                 # 子 cgroup
    ├── cpu.max
    ├── memory.max
    └── cgroup.procs         # 包含的进程 PID
```

## 资源限制示例

```bash
# 创建 cgroup
mkdir /sys/fs/cgroup/myapp

# CPU 限制：使用 1 个核的 50%
echo "50000 100000" > /sys/fs/cgroup/myapp/cpu.max

# 内存限制：最多 512MB
echo "536870912" > /sys/fs/cgroup/myapp/memory.max

# 进程数限制
echo "100" > /sys/fs/cgroup/myapp/pids.max

# 将进程加入 cgroup
echo $$ > /sys/fs/cgroup/myapp/cgroup.procs

# 查看状态
cat /sys/fs/cgroup/myapp/memory.current
cat /sys/fs/cgroup/myapp/cpu.stat
```

## systemd 集成

```ini
# /etc/systemd/system/myapp.service
[Service]
CPUQuota=50%
MemoryMax=512M
MemoryHigh=256M
TasksMax=100
```

```bash
systemctl daemon-reload
systemctl start myapp
systemd-cgtop                  # cgroup 资源监控
```

## Docker / 容器中的 cgroup

```bash
# Docker 自动创建 cgroup
docker run -d --cpus=2 --memory=512m --name app nginx
# 查看
cat /sys/fs/cgroup/docker/<container-id>/memory.max
cat /sys/fs/cgroup/docker/<container-id>/cpu.max
```

## 关键要点

> 容器的本质就是 cgroup（资源限制）+ namespace（隔离）+ rootfs（文件系统）。理解 cgroup 就理解了容器的底层。

> cgroup v2 是统一层级模型，比 v1 的多层级更简洁。现代发行版默认使用 v2。

## 相关笔记

- [[Linux 内存管理基础]] — 内存管理
- [[Linux 进程基础与 ps 命令]] — 进程管理
