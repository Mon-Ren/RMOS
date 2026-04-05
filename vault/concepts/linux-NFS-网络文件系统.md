---
title: "Linux NFS 网络文件系统"
tags: [linux, nfs, network, filesystem, 共享]
aliases: [NFS, 网络文件系统, nfsd, mount nfs, 共享存储]
created: 2026-04-05
updated: 2026-04-05
---

# Linux NFS 网络文件系统

NFS（Network File System）允许在网络上共享目录，客户端像访问本地文件一样访问远程文件。

## 服务端配置

```bash
# 安装
apt install nfs-kernel-server    # Debian
yum install nfs-utils            # RHEL

# 配置共享目录 (/etc/exports)
/shared      192.168.1.0/24(rw,sync,no_subtree_check)
/readonly    *(ro,sync,no_root_squash)
/project     *.example.com(rw,sync,root_squash)

# 生效
exportfs -ra                     # 重新导出所有
systemctl enable --now nfs-server

# 查看导出
exportfs -v
showmount -e localhost
```

## 客户端挂载

```bash
# 临时挂载
mount -t nfs server:/shared /mnt/shared
mount -t nfs4 server:/shared /mnt/shared   # NFSv4

# /etc/fstab 持久挂载
server:/shared  /mnt/shared  nfs  defaults,_netdev  0  0

# 自动挂载（autofs）
# /etc/auto.master
/-  /etc/auto.direct  --timeout=60
# /etc/auto.direct
/mnt/shared  -rw  server:/shared
```

## 性能调优

```bash
# 挂载选项
mount -t nfs -o rsize=131072,wsize=131072,hard,intr server:/shared /mnt

# 常用选项
# rsize/wsize: 读写块大小（默认 1MB）
# hard: 硬挂载（失败重试）/ soft: 软挂载（超时返回错误）
# noatime: 不更新访问时间
```

## 关联
- [[linux-网络基础命令]] — 网络诊断和配置
- [[linux-文件权限与 chmod]] — NFS 权限映射（root_squash）

## 关键结论

> NFS 适合局域网内多台机器共享存储（如 K8s 持久卷、CI/CD 共享目录），不适合跨公网或高并发场景。
