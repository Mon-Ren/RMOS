---
title: "Linux systemd-nspawn 容器"
tags: [linux, systemd, nspawn, container, 轻量容器]
aliases: [nspawn, systemd-nspawn, 轻量容器, chroot增强]
created: 2026-04-05
updated: 2026-04-05
---

# Linux systemd-nspawn 容器

systemd-nspawn 是 systemd 内置的轻量级容器工具，比 Docker 更接近传统 chroot 但支持完整 namespace 隔离。

## 基本使用

```bash
# 创建容器（debootstrap）
debootstrap --arch=amd64 stable /var/lib/machines/debian
# 或从镜像
machinectl pull-arch --arch=amd64 debian

# 启动容器
systemd-nspawn -D /var/lib/machines/debian
systemd-nspawn -b -D /var/lib/machines/debian    # 启动 systemd

# 管理
machinectl list
machinectl start debian
machinectl login debian
machinectl shell root@debian
machinectl stop debian
```

## 与 Docker 对比

| | Docker | nspawn |
|---|--------|--------|
| 镜像格式 | OCI | 目录/镜像文件 |
| 网络 | 桥接/veth | 简单/桥接 |
| 存储 | 分层 overlay | 目录 |
| 编排 | Compose/K8s | systemd unit |
| 复杂度 | 高 | 低 |

## systemd unit 集成

```ini
# /etc/systemd/system/mycontainer.service
[Unit]
Description=My Container

[Service]
ExecStart=systemd-nspawn -b -D /var/lib/machines/myapp
KillMode=mixed
Type=notify

[Install]
WantedBy=multi-user.target
```

## 网络配置

```bash
# 桥接网络
systemd-nspawn -b -D /var/lib/machines/debian \
  --network-bridge=br0 \
  --network-veth-extra=host0

# 端口转发
systemd-nspawn -b -D /var/lib/machines/debian \
  --port=tcp:8080:80
```

## 关联
- [[linux-Docker-基础]] — Docker 容器
- [[linux-namespace-隔离机制]] — 底层隔离机制

## 关键结论

> nspawn 适合不需要 Docker 生态的轻量容器场景：开发环境隔离、测试不同发行版、systemd 服务容器化。它比 Docker 简单得多，直接用目录作为 rootfs，无需构建镜像。
