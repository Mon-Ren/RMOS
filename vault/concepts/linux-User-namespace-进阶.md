---
title: "Linux Namespaces 进阶：User namespace"
tags: [linux, namespace, user, unshare, rootless]
aliases: [User namespace, rootless容器, 非特权namespace, UID映射]
created: 2026-04-05
updated: 2026-04-05
---

# Linux User Namespace 进阶

User namespace 允许非特权用户在隔离环境中拥有 root 权限，是 rootless 容器的基础。

## UID/GID 映射

```
Host namespace    User namespace
root (0)      →   nobody (65534)    ← 不映射
alice (1000)  →   root (0)          ← 映射
alice+1 (1001)→   user1 (1)         ← 映射
```

```bash
# 创建 user namespace
unshare --user --map-root-user bash
id                              # uid=0(root) 在 namespace 内
whoami                          # root

# 查看映射
cat /proc/$$/uid_map
#         0       1000          1
#    ns_uid  host_uid  count
```

## 配置映射

```bash
# /etc/subuid 和 /etc/subgid
alice:100000:65536    # alice 可用 100000-165535

# 写入映射
echo "0 1000 1" > /proc/$$/uid_map
echo "0 1000 1" > /proc/$$/gid_map
# 或用 newuidmap/newgidmap（需要 setuid）
```

## Rootless 容器

```bash
# Podman rootless
podman run --userns=auto alpine echo hello
# 无需 root，自动分配 subuid/subgid

# Docker rootless
dockerd-rootless-setuptool.sh install
```

## 安全注意事项

```bash
# user namespace 有安全限制
cat /proc/sys/kernel/unprivileged_userns_clone   # 1=允许
echo 0 > /proc/sys/kernel/unprivileged_userns_clone  # 禁止

# 部分 capability 在 user namespace 中无效
# 例如：CAP_SYS_ADMIN 在 user ns 中不能挂载真正的磁盘
```

## 关联
- [[linux-namespace-隔离机制]] — namespace 基础
- [[linux-Docker-基础]] — Docker 支持 rootless

## 关键结论

> User namespace 是"最小特权"的实践：普通用户在 namespace 内拥有 root 能力，但对外部系统无影响。rootless 容器（Podman/Docker）依赖它来完全避免特权进程。
