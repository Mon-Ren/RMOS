---
title: "Linux systemd-resolved DNS 服务"
tags: [linux, systemd, dns, resolved, 名称解析]
aliases: [resolved, resolvectl, systemd-resolved, DNS缓存]
created: 2026-04-05
updated: 2026-04-05
---

# Linux systemd-resolved DNS 服务

systemd-resolved 是 systemd 的 DNS 解析服务，提供本地 DNS 缓存、DNSSEC 验证和 DNS-over-TLS。

## 架构

```
应用 → nsswitch → libnss_resolve.so → /run/systemd/resolve/stub-resolv.conf
                                            ↓
                                    systemd-resolved
                                       ↓       ↓
                                    DNS 缓存   上游 DNS
```

## 核心功能

```bash
# 状态查看
resolvectl status
resolvectl statistics         # 缓存命中率
resolvectl query example.com  # 测试解析

# DNS 配置
resolvectl dns eth0 8.8.8.8 1.1.1.1
resolvectl domain eth0 example.com
resolvectl default-route eth0 true    # 是否用作默认路由

# 缓存管理
resolvectl flush-caches
systemd-resolve --statistics

# DNSSEC
resolvectl dnssec eth0 allow-downgrade  # 或 yes/no
```

## 与 /etc/resolv.conf 的关系

```bash
# systemd-resolved 管理的 resolv.conf 三种模式
# 1. stub（推荐）
ls -la /etc/resolv.conf
# → /run/systemd/resolve/stub-resolv.conf（指向 127.0.0.53）

# 2. static
# → /run/systemd/resolve/resolv.conf（上游 DNS）

# 3. 由 NetworkManager 管理
```

## 故障排查

```bash
# DNS 解析失败排查流程
resolvectl status                    # 检查配置
resolvectl query example.com         # 测试解析
resolvectl flush-caches              # 清缓存
journalctl -u systemd-resolved       # 查看日志
systemd-resolve --statistics         # 缓存统计

# 手动测试
dig @127.0.0.53 example.com          # 测试本地 DNS
dig @8.8.8.8 example.com             # 测试上游 DNS
```

## 关联
- [[linux-DNS-解析与配置]] — DNS 基础和工具
- [[linux-systemd-networkd-网络配置]] — 配合 networkd

## 关键结论

> 127.0.0.53 是 systemd-resolved 的 stub DNS 地址。所有 DNS 查询先经过本地缓存，缓存未命中才转发上游。`resolvectl flush-caches` 排 DNS 问题时应首先执行。
